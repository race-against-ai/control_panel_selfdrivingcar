import json
import paramiko
from control_panel_backend.control_panel import ControlPanel

def load_config(filename):
    try:
        with open(filename, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {
            "start": False,
            "stream": False,
            "motor": False,
            "process": False,
            "debug": False,
            "curvespeed": 0.0,
            "straightlinespeed": 0.0
        }
    except json.JSONDecodeError:
        config = {
            "start": False,
            "stream": False,
            "motor": False,
            "process": False,
            "debug": False,
            "curvespeed": 0.0,
            "straightlinespeed": 0.0
        }   
    return config

def send_config_via_ssh(local_path, ssh_host, ssh_port, ssh_username, ssh_password, remote_path):
    # Establish SSH connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

    # Transfer local file to remote path via SSH
    sftp = ssh.open_sftp()
    sftp.put(local_path, remote_path)

    # Close SSH connection
    sftp.close()
    ssh.close()
    print("Erfolgreich gesendet!")

if __name__ == "__main__":
    config = load_config('config_selfdriving_car.json')
    print("Geladene Konfiguration:", config)
    
    ssh_host = '192.168.30.123'
    ssh_port = 22  # Standard-SSH-Port
    ssh_username = 'itlab'
    ssh_password = '1234'
    remote_path = '/home/itlab/cam/inside-out-server/data.json'
    local_path = 'control_panel_backend/config_selfdriving_car.json'
    with open(local_path, 'w') as file:
        json.dump(config, file)
        
    send_config_via_ssh(local_path, ssh_host, ssh_port, ssh_username, ssh_password, remote_path)
    
    vehicle_control = ControlPanel()
    vehicle_control.start()
