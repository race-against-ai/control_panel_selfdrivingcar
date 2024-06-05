# Copyright (C) 2023, NG:ITL
import os
import sys
import json
import pynng
import time
import paramiko
import subprocess

from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QTimer
from PySide6.QtCore import QSocketNotifier

from control_panel_backend import control_panel_model
from control_panel_backend.control_panel_model import ControlPanelModel
from control_panel_backend.timer_model import Timer
from control_panel_backend.database_interface_model import DriverDataPublisher
from enum import IntEnum



CONTROL_PANEL_PYNNG_ADDRESS = "ipc:///tmp/RAAI/control_panel.ipc"
CONTROL_COMPONENT_PYNNG_ADDRESS = "ipc:///tmp/RAAI/vehicle_output_writer.ipc"
PLATFORM_CONTROLLER_PYNNG_ADDRESS = "ipc:///tmp/RAAI/driver_input_reader.ipc"


def send_data(pub: pynng.Pub0, payload: dict, topic: str = " ", p_print: bool = True) -> None:
    """
    publishes data via pynng

    :param pub: publisher
    :param payload: data that should be sent in form of a dictionary
    :param topic: the topic under which the data should be published  (e.g. "lap_time:")
    :param p_print: if true, the message that is sent will be printed out. Standard is set to true
    """
    json_data = json.dumps(payload)
    topic = topic + " "
    msg = topic + json_data
    if p_print is True:
        print(f"data send: {msg}")
    pub.send(msg.encode())


def receive_data(sub: pynng.Sub0):
    """
    receives data via pynng and returns a variable that stores the content

    :param sub: subscriber
    :param timer: timeout timer for max waiting time for new signal
    """
    msg = sub.recv()
    data = remove_pynng_topic(msg)
    data = json.loads(data)
    return data


def remove_pynng_topic(data, sign: str = " ") -> str:
    """
    removes the topic from data that got received via pynng and returns a variable that stores the content

    :param data: date received from subscriber
    :param sign: last digit from the topic
    """
    decoded_data: str = data.decode()
    i = decoded_data.find(sign)
    decoded_data = decoded_data[i + 1 :]
    return decoded_data


def read_config(config_file_path: str) -> dict:
    if os.path.isfile(config_file_path):
        with open(config_file_path, "r") as file:
            return json.load(file)
    else:
        return create_config(config_file_path)


def create_config(config_file_path: str) -> dict:
    """wrote this to ensure that a config file always exists, ports have to be adjusted if necessary"""
    print("No Config File found, creating new one from Template")
    print("---!Using default argments for a Config file")
    template = {
        "max_throttle": 15,
        "max_brake": 50,
        "max_clutch": 50,
        "max_steering": 100,
        "button_status": False,
        "platform_status": True,
        "pedal_status": True,
        "head_tracking_status": False,
        "start_status": False,
        "stream_status": False,
        "motor_status": False,
        "debug_status": False,
        "process_status": False,
        "steering_offset": -8.0,
        "straightlinespeed": 0,
        "curvespeed": 0,
    }

    file = json.dumps(template, indent=4)
    with open(config_file_path, "w") as f:
        f.write(file)

    return template


def resource_path() -> Path:
    base_path = getattr(sys, "_MEIPASS", os.getcwd())
    return Path(base_path)



class TimerStates(IntEnum):
    RESET = 0
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3


class ControlPanel:
    
    def __init__(self, config_file_path="./control_panel_config.json") -> None:
        self.config = read_config(config_file_path)

        self.start_timestamp_ns = time.time_ns()
        self.diff = 0
        self.t_model = Timer(0, 0, 0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_callback)  # type: ignore

        self.database_model = DriverDataPublisher(
            self.config["pynng"]["publishers"]["name_publisher"]["address"],
            self.config["pynng"]["requesters"]["database_request"]["address"],
        )

        self.timer_state = 0

        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.control_panel_model = ControlPanelModel()
        
        # and load the QML panel
        self.engine.load(resource_path() / "frontend/qml/main.qml")

        self.engine.rootContext().setContextProperty("t_model", self.t_model)
        self.engine.rootContext().setContextProperty("database_model", self.database_model)
        self.engine.rootContext().setContextProperty("sendValueAndUpdate", ControlPanel.sendValueAndUpdate)
        self.engine.rootContext().setContextProperty("control_panel_model", self.control_panel_model)


        # connect to the signals from the QML file
        self.engine.rootObjects()[0].sliderMaxThrottleChanged.connect(self.control_panel_model.set_max_throttle)  # type: ignore
        self.engine.rootObjects()[0].sliderMaxBrakeChanged.connect(self.control_panel_model.set_max_brake)  # type: ignore
        self.engine.rootObjects()[0].sliderMaxClutchChanged.connect(self.control_panel_model.set_max_clutch)  # type: ignore
        self.engine.rootObjects()[0].sliderMaxSteeringChanged.connect(self.control_panel_model.set_max_steering)  # type: ignore
        self.engine.rootObjects()[0].sliderAllMaxSpeedChanged.connect(self.control_panel_model.set_all_speed_max)  # type: ignore
        self.engine.rootObjects()[0].sliderCurveSpeedChanged.connect(lambda: self.handle_speed_update("curvespeed"))  # type: ignore
        self.engine.rootObjects()[0].sliderStraightLineSpeedChanged.connect(lambda: self.handle_speed_update("straightlinespeed"))  # type: ignore


        self.engine.rootObjects()[0].sliderSteeringOffsetChanged.connect(self.control_panel_model.set_steering_offset)  # type: ignore

        self.engine.rootObjects()[0].buttonResetHeadTracking.connect(self.handle_head_tracker_reset_request)  # type: ignore

        self.engine.rootObjects()[0].buttonButtonStatusChanged.connect(self.control_panel_model.change_button_status)  # type: ignore
        self.engine.rootObjects()[0].buttonPlatformStatusChanged.connect(self.change_platform_status)  # type: ignore
        self.engine.rootObjects()[0].buttonPedalStatusChanged.connect(self.control_panel_model.change_pedal_status)  # type: ignore
        self.engine.rootObjects()[0].buttonHeadTrackingChanged.connect(self.control_panel_model.change_head_tracking_status) #type: ignore
        self.engine.rootObjects()[0].buttonStartStatusChanged.connect(self.change_start_status)  # type: ignore
        self.engine.rootObjects()[0].buttonStreamStatusChanged.connect(self.change_stream_status)  # type: ignore
        self.engine.rootObjects()[0].buttonMotorStatusChanged.connect(self.change_motor_status)  # type: ignore
        self.engine.rootObjects()[0].buttonDebugStatusChanged.connect(self.change_debug_status)  # type: ignore
        self.engine.rootObjects()[0].buttonProcessStatusChanged.connect(self.change_process_status)  # type: ignore

        self.engine.rootObjects()[0].timerStart.connect(self.timer_start)  # type: ignore
        self.engine.rootObjects()[0].timerPause.connect(self.timer_pause)  # type: ignore
        self.engine.rootObjects()[0].timerStop.connect(self.timer_stop)  # type: ignore
        self.engine.rootObjects()[0].timerReset.connect(self.timer_reset)  # type: ignore
        self.engine.rootObjects()[0].timerResetFull.connect(self.timer_reset_full)  # type: ignore
        self.engine.rootObjects()[0].timerIgnore.connect(self.timer_ignore)  # type: ignore

        self.driver_input_timer = QTimer()
        self.driver_input_timer.timeout.connect(self.send_driver_throttle_data)  # type: ignore
        self.driver_input_timer.start(1)

        self.control_panel_model.set_steering_offset(self.config["steering_offset"])

        self.control_panel_model.set_max_throttle(self.config["max_throttle"])
        self.control_panel_model.set_max_brake(self.config["max_brake"])
        self.control_panel_model.set_straightlinespeed(self.config["straightlinespeed"])
        self.control_panel_model.set_curvespeed(self.config["curvespeed"])
        self.control_panel_model.set_max_clutch(self.config["max_clutch"])
        self.control_panel_model.set_max_steering(self.config["max_steering"])


        self.control_panel_model.set_button_status(self.config["button_status"])
        self.control_panel_model.set_platform_status(self.config["platform_status"])
        self.control_panel_model.set_pedal_status(self.config["pedal_status"])
        self.control_panel_model.set_head_tracking_status(self.config["head_tracking_status"])
        self.control_panel_model.set_start_status(self.config["start_status"])
        self.control_panel_model.set_stream_status(self.config["stream_status"])
        self.control_panel_model.set_motor_status(self.config["motor_status"])
        self.control_panel_model.set_debug_status(self.config["debug_status"])
        self.control_panel_model.set_process_status(self.config["process_status"])
        

        self.sent_center_request = False

        self.max_throttle = self.control_panel_model.get_max_throttle()
        self.max_brake = self.control_panel_model.get_max_brake()
        self.max_clutch = self.control_panel_model.get_max_clutch()
        self.straightlinespeed = self.control_panel_model.get_straightlinespeed()
        self.curvespeed = self.control_panel_model.get_curvespeed()
  

        self.max_steering = self.control_panel_model.get_max_steering()
        self.steering_offset = self.control_panel_model.get_steering_offset()

        self.__pynng_data_publisher = pynng.Pub0()
        self.__pynng_data_publisher.listen(CONTROL_PANEL_PYNNG_ADDRESS)

        self.__driver_input_receiver = pynng.Sub0()
        self.__driver_input_receiver.subscribe("driver_input")
        self.__driver_input_receiver.dial(PLATFORM_CONTROLLER_PYNNG_ADDRESS, block=False)
        self._notifier = QSocketNotifier(self.__driver_input_receiver.recv_fd, QSocketNotifier.Read)
        self._notifier.activated.connect(self.handle_driver_input)  # type: ignore

    def timer_callback(self) -> None:
        current_timestamp_ns = time.time_ns()
        self.diff = current_timestamp_ns - self.start_timestamp_ns
        self.t_model.set_timestamp(self.diff)

    def handle_head_tracker_reset_request(self) -> None:
        pass

    def send_driver_throttle_data(self) -> None:
        self.max_throttle = self.control_panel_model.get_max_throttle()
        self.max_brake = self.control_panel_model.get_max_brake()
        self.max_clutch = self.control_panel_model.get_max_clutch()
        self.straightlinespeed = self.control_panel_model.get_straightlinespeed()
        self.curvespeed = self.control_panel_model.get_curvespeed()

        self.max_steering = self.control_panel_model.get_max_steering()
        self.steering_offset = self.control_panel_model.get_steering_offset()

        throttle_payload = {
            "throttle": 0,
            "brake": 0,
            "clutch": 0,
            "steering": self.max_steering,
            "steering_offset": self.steering_offset,
        }

        if self.control_panel_model.get_pedal_status():
            throttle_payload = {
                "max_throttle": self.max_throttle,
                "max_brake": self.max_brake,
                "max_clutch": self.max_clutch,
                "max_steering": self.max_steering,
                "steering_offset": self.steering_offset,
            }

        send_data(self.__pynng_data_publisher, throttle_payload, "config", p_print=False)
        ControlPanel.send_speed_data(self)

    def send_speed_data(self) -> None:
        self.straightlinespeed = self.control_panel_model.get_straightlinespeed()
        self.curvespeed = self.control_panel_model.get_curvespeed()

    def handle_driver_input(self) -> None:
        driver_payload = receive_data(self.__driver_input_receiver)

        throttle = driver_payload["throttle"]
        brake = driver_payload["brake"]
        clutch = driver_payload["clutch"]
        steering = driver_payload["steering"]
        tilt_x = driver_payload["tilt_x"]
        tilt_y = driver_payload["tilt_y"]
        vibration = driver_payload["vibration"]

        self.control_panel_model.set_actual_all(throttle, brake, clutch, steering)

        self.max_throttle = self.control_panel_model.get_max_throttle()
        self.max_brake = self.control_panel_model.get_max_brake()
        self.max_clutch = self.control_panel_model.get_max_clutch()
        self.max_steering = self.control_panel_model.get_max_steering()

        throttle_scaled = throttle * (self.max_throttle / 100)
        brake_scaled = brake * (self.max_brake / 100)
        clutch_scaled = clutch * (self.max_clutch / 100)
        steering_scaled = steering * (self.max_steering / 100)

        self.control_panel_model.set_all(throttle_scaled, brake_scaled, clutch_scaled, steering_scaled)

    def start(self):
        self.app.exec()

        print("exiting control panel")

    # timer is listening to specified port
    # used for links in buttons
    def send_to_timer(self, string: str, topic: str) -> None:
        """
        Sends a message to the timer.

        Args:
        string (str): The message to send.
        topic (str): The topic to send the message on.
        """

        payload = {"signal": string}
        send_data(self.__pynng_data_publisher, payload, topic)

    def timer_start(self) -> None:
        if self.timer_state == TimerStates.STOPPED:
            self.diff = 0
            self.t_model.set_timestamp(0)

        self.start_timestamp_ns = time.time_ns() - self.diff
        self.timer.start()
        self.timer_state = TimerStates.RUNNING

    def timer_pause(self) -> None:
        if self.timer_state == TimerStates.PAUSED:
            self.start()
        else:
            self.timer.stop()
            self.timer_state = TimerStates.PAUSED

    def timer_stop(self) -> None:
        if self.timer_state == TimerStates.PAUSED:
            self.start()
        else:
            self.timer.stop()
            self.timer_state = TimerStates.PAUSED

    def timer_reset(self) -> None:
        self.timer.stop()
        self.diff = 0
        self.t_model.set_timestamp(0)
        self.timer_state = TimerStates.RESET

    def timer_reset_full(self) -> None:
        self.send_to_timer("reset full", "timer_signal")

    def timer_ignore(self) -> None:
        self.send_to_timer("ignore", "timer_signal")

    def change_platform_status(self) -> None:
        self.control_panel_model.set_platform_status(not self.control_panel_model.get_platform_status())
        self.send_platform_signal()

    def send_platform_signal(self) -> None:
        payload = {"platform_status": self.control_panel_model.get_platform_status()}
        send_data(self.__pynng_data_publisher, payload, "platform")

    def change_start_status(self) -> None:
        start_status = not self.control_panel_model.get_start_status()
        self.control_panel_model.set_start_status(start_status)
        
        if start_status:
            print("on button pressed")
            self.run_start_script()
        elif start_status == False:
            print("off button pressed")
            self.stop_tmux_session()

    def change_stream_status(self) -> None:
        self.control_panel_model.set_stream_status(not self.control_panel_model.get_stream_status())
        self.sendValueAndUpdate("stream")

    def change_motor_status(self) -> None:
        self.control_panel_model.set_motor_status(not self.control_panel_model.get_motor_status())
        self.sendValueAndUpdate("motor")

    def change_debug_status(self) -> None:
        self.control_panel_model.set_debug_status(not self.control_panel_model.get_debug_status())
        self.sendValueAndUpdate("debug")

    def change_process_status(self) -> None:
        self.control_panel_model.set_process_status(not self.control_panel_model.get_process_status())
        self.sendValueAndUpdate("process")

    @staticmethod
    def updateJsonFile(json_file_path, key):
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if key in data:
            data[key] = not data[key]
            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=2)
        else:
            print(f"Key {key} nicht in der JSON gefunden.")

    @staticmethod
    def updateJsonFileFloat(json_file_path, key, new_value):
        with open(json_file_path, 'r') as file:
            data = json.load(file)

        if key in data:
            data[key] = new_value
            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=2)
        else:
            print(f"Schlüssel '{key}' nicht in der JSON gefunden.")


    @staticmethod
    def send_json_file_via_ssh(local_path, ssh_host, ssh_port, ssh_username, ssh_password, remote_path):
        # Read JSON file
        with open(local_path, 'r') as file:
            json_data = json.load(file)

        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

        # Transfer JSON data via SSH
        sftp = ssh.open_sftp()
        with sftp.file(remote_path, 'w') as remote_file:
            remote_file.write(json.dumps(json_data))

        # Close SSH connection
        sftp.close()
        ssh.close()
        print("Erfolgreich gesendet!")

    @staticmethod
    def sendValueAndUpdate(key):
        print('update ' + key)
        local_path = 'control_panel_backend/config_selfdriving_car.json'

        control_panel_model = ControlPanelModel()

        if key == "straightlinespeed":
            new_value = control_panel_model.straightlinespeed
            print(new_value)
            ControlPanel.updateJsonFileFloat(local_path, key, new_value)
        elif key == "curvespeed":
            new_value = control_panel_model.curvespeed
            print(new_value)
            ControlPanel.updateJsonFileFloat(local_path, key, new_value)
        else:
            ControlPanel.updateJsonFile(local_path, key)
        
        ssh_host = '192.168.30.123'
        ssh_port = 22  # Standard-SSH-Port
        ssh_username = 'itlab'
        ssh_password = '1234'
        remote_path = '/home/itlab/cam/inside-out-server/data.json'
        ControlPanel.send_json_file_via_ssh(local_path, ssh_host, ssh_port, ssh_username, ssh_password, remote_path)

    def handle_speed_update(self, key):
        print(f'Updating {key}')
        local_path = 'control_panel_backend/config_selfdriving_car.json'

        if key == "straightlinespeed":
            new_value = self.control_panel_model.get_straightlinespeed()
            new_value2 = round(new_value, 1)
            print(f'Straight line speed new value: {new_value2}')
            self.updateJsonFileFloat(local_path, key, new_value2)
        elif key == "curvespeed":
            new_value = self.control_panel_model.get_curvespeed()
            new_value2 = round(new_value, 1)
            print(f'Curve speed new value: {new_value2}')
            self.updateJsonFileFloat(local_path, key, new_value2)
        
        ssh_host = '192.168.30.123'
        ssh_port = 22
        ssh_username = 'itlab'
        ssh_password = '1234'
        remote_path = '/home/itlab/cam/inside-out-server/data.json'
        self.send_json_file_via_ssh(local_path, ssh_host, ssh_port, ssh_username, ssh_password, remote_path)

    def run_start_script(self) -> None:
        #SSH connection information for the Raspberry Pi
        ssh_host = '192.168.30.123'
        ssh_port = 22 
        ssh_username = 'itlab'
        ssh_password = '1234'
        script_path = '/home/itlab/start.sh'

        try:
            #SSH connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
            print("SSH connected")
            
            #start tmux session and run sh
            command = f'tmux new-session -d -s my_session "bash {script_path}"'
            stdin, stdout, stderr = ssh.exec_command(command)
            print("Script executed within tmux session")

            ssh.close()
            print("SSH connection closed")

            print("Shell script successfully started within a tmux session.")
        except Exception as e:
            print(f"Error executing the shell script over SSH: {e}")


    def stop_tmux_session(self) -> None:
        #SSH connection information for the Raspberry Pi
        ssh_host = '192.168.30.123'
        ssh_port = 22 
        ssh_username = 'itlab'
        ssh_password = '1234'
        tmux_session_name = 'my_session'  #tmux session name

        try:
            #SSH connection
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)
            print("SSH connected")
            
            #termination signal to sh script
            stdin, stdout, stderr = ssh.exec_command(f'tmux send-keys -t {tmux_session_name} C-c')
            print("Script terminated")

            #close tmux session
            stdin, stdout, stderr = ssh.exec_command(f'tmux kill-session -t {tmux_session_name}')
            print("Tmux session closed")

            ssh.close()
            print("SSH connection closed")

            print(f"Tmux session '{tmux_session_name}' successfully stopped.")
        except Exception as e:
            print(f"Error stopping the tmux session over SSH: {e}")