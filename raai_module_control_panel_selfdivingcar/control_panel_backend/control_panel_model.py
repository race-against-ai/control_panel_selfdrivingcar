# Copyright (C) 2023, NG:ITL
from PySide6.QtCore import QObject, Signal, Property

class ControlPanelModel(QObject):
    # --------------- signals ---------------
    # ---------- standard ----------
    throttle_changed = Signal()
    brake_changed = Signal()
    clutch_changed = Signal()
    steering_changed = Signal()
    sls_changed = Signal()
    cs_changed = Signal()

    # ---------- actual values ----------
    actual_throttle_changed = Signal()
    actual_brake_changed = Signal()
    actual_clutch_changed = Signal()
    actual_steering_changed = Signal()
    steering_offset_changed = Signal()
    actual_straightlinespeed_changed = Signal()
    actual_curvespeed_changed = Signal()

    # ---------- max values -----------
    max_throttle_changed = Signal()
    max_brake_changed = Signal()
    max_clutch_changed = Signal()
    max_steering_changed = Signal()
    all_speed_max_changed = Signal()
    straightlinespeed_changed = Signal()
    curvespeed_changed = Signal()

    # ---------- button status ----------
    button_status_changed = Signal()
    platform_status_changed = Signal()
    pedal_status_changed = Signal()
    head_tracking_status_changed = Signal()
    start_status_changed = Signal()
    stream_status_changed = Signal()
    motor_status_changed = Signal()
    debug_status_changed = Signal()
    process_status_changed = Signal()

    # ---------- head tracking -----------
    head_tracking_yaw_angle_changed = Signal()

    def __init__(self) -> None:
        QObject.__init__(self)
        # standard, used for sending
        self._throttle = 0.0
        self._brake = 0.0
        self._clutch = 0.0
        self._steering = 0.0
        self._sls = 0.0
        self._cs = 0.0

        # actual, used for processing
        self._actual_throttle = 0.0
        self._actual_brake = 0.0
        self._actual_clutch = 0.0
        self._actual_steering = 0.0
        self._actual_straightlinespeed = 0.0
        self._actual_curvespeed = 0.0

        # max, limits of each value
        self._max_throttle = 100.0
        self._max_brake = 100.0
        self._max_clutch = 100.0
        self._max_steering = 100.0
        self._all_speed_max = 100.0
        self._straightlinespeed = 100.0
        self._curvespeed = 100.0

        # Head tracking
        self._head_tracking_yaw_angle = 0.0

        self._steering_offset = 0.0

        # button activation status, whether the buttons are active
        self._buttons_activated = True
        self._platform_activated = True
        self._pedals_activated = True
        self._head_tracking_activated = True
        self._start_activated = False
        self._stream_activated = False
        self._motor_activated = False
        self._debug_activated = False
        self._process_activated = False

    @Property(float)
    def straightlinespeed(self):
        return self._straightlinespeed

    
    def straightlinespeed(self, value):
        
        self._straightlinespeed = value
        self.straightlinespeed_changed.emit()
        print(f"straightlinespeed set to {value}")

    @Property(float)
    def curvespeed(self):
        return self._curvespeed

    
    def curvespeed(self, value):
        
        self._curvespeed = value
        self.curvespeed_changed.emit()
        print(f"curvespeed set to {value}")

    # -------------------- set all --------------------
    def set_all(self, throttle: float, brake: float, clutch: float, steering: float, cs: float, sls: float) -> None:
        self.set_throttle(throttle)
        self.set_brake(brake)
        self.set_clutch(clutch)
        self.set_steering(steering)
        self.set_cs(cs)
        self.set_sls(sls)

    def set_actual_all(self, throttle: float, brake: float, clutch: float, steering: float, cs: float, sls: float) -> None:
        self.set_actual_throttle(throttle)
        self.set_actual_brake(brake)
        self.set_actual_clutch(clutch)
        self.set_actual_steering(steering)
        self.set_actual_straightlinespeed(sls)
        self.set_actual_curvespeed(cs)

    def set_head_tracking_values(self, yaw_angle: float):
        self.set_head_tracking_yaw_angle(yaw_angle)

    # -------------------- adding values --------------------
    def add_speed_max(self, value: float) -> None:
        if value:
            self.set_all_speed_max(self.get_all_speed_max() + value)

    def add_max_throttle(self, amount: float) -> None:
        self.set_max_throttle(self.get_max_throttle() + amount)

    def add_max_brake(self, amount: float) -> None:
        self.set_max_brake(self._max_brake + amount)

    def add_max_clutch(self, amount: float) -> None:
        self.set_max_clutch(self._max_clutch + amount)

    def add_max_steering(self, amount: float) -> None:
        self.set_max_steering(self._max_steering + amount)

    def add_curvespeed(self, amount: float) -> None:
        self.set_curvespeed(self._curvespeed + amount)

    def add_straightlinespeed(self, amount: float) -> None:
        self.set_straightlinespeed(self._straightlinespeed + amount)

    def add_steering_offset(self, amount: float) -> None:
        self.set_steering_offset(self.get_steering_offset() + amount)

    # ---------- change ----------
    def change_button_status(self) -> None:
        self.set_button_status(self.get_button_status())

    def change_platform_status(self) -> None:
        self.set_platform_status(self.get_platform_status())

    def change_pedal_status(self) -> None:
        self.set_pedal_status(self.get_pedal_status())

    def change_head_tracking_status(self) -> None:
        self.set_head_tracking_status(self.get_head_tracking_status())

    def change_start_status(self) -> None:
        self.set_start_status(self.get_start_status())

    def change_stream_status(self) -> None:
        self.set_stream_status(self.get_stream_status())

    def change_motor_status(self) -> None:
        self.set_motor_status(self.get_motor_status())

    def change_debug_status(self) -> None:
        self.set_debug_status(self.get_debug_status())

    def change_process_status(self) -> None:
        self.set_process_status(self.get_process_status())

    # -------------------- getters --------------------
    # ---------- standard ----------
    def get_throttle(self) -> float:
        return self._throttle

    def get_brake(self) -> float:
        return self._brake

    def get_clutch(self) -> float:
        return self._clutch

    def get_steering(self) -> float:
        return self._steering
    
    def get_sls(self) -> float:
        return self._sls
    
    def get_cs(self) -> float:
        return self._cs

    def get_steering_offset(self) -> float:
        return self._steering_offset

    # ---------- actual values ----------
    def get_actual_throttle(self) -> float:
        return self._actual_throttle

    def get_actual_brake(self) -> float:
        return self._actual_brake

    def get_actual_clutch(self) -> float:
        return self._actual_clutch

    def get_actual_steering(self) -> float:
        return self._actual_steering
    
    def get_actual_straightlinespeed(self) -> float:
        return self._actual_straightlinespeed
    
    def get_actual_curvespeed(self) -> float:
        return self._actual_curvespeed

    # ---------- max values ----------
    def get_max_throttle(self) -> float:
        return self._max_throttle

    def get_max_brake(self) -> float:
        return self._max_brake

    def get_max_clutch(self) -> float:
        return self._max_clutch

    def get_max_steering(self) -> float:
        return self._max_steering
    
    def get_curvespeed(self) -> float:
        return self._curvespeed
    
    def get_straightlinespeed(self) -> float:
        return self._straightlinespeed

    def get_all_speed_max(self) -> float:
        return self._all_speed_max

    # ---------- button status ----------
    def get_button_status(self) -> bool:
        return self._buttons_activated

    def get_platform_status(self) -> bool:
        return self._platform_activated

    def get_pedal_status(self) -> bool:
        return self._pedals_activated

    def get_head_tracking_status(self) -> bool:
        return self._head_tracking_activated

    def get_start_status(self) -> bool:
        return self._start_activated

    def get_stream_status(self) -> bool:
        return self._stream_activated

    def get_motor_status(self) -> bool:
        return self._motor_activated

    def get_debug_status(self) -> bool:
        return self._debug_activated

    def get_process_status(self) -> bool:
        return self._process_activated

    # ---------- head tracking -----------
    def get_head_tracking_yaw_angle(self) -> float:
        return self._head_tracking_yaw_angle

    # -------------------- setters --------------------
    # ---------- standard ----------
    def set_throttle(self, value: float) -> None:
        if self._throttle != value:
            self._throttle = value
            self.throttle_changed.emit()

    def set_brake(self, value: float) -> None:
        if self._brake != value:
            self._brake = value
            self.brake_changed.emit()

    def set_clutch(self, value: float) -> None:
        if self._clutch != value:
            self._clutch = value
            self.clutch_changed.emit()

    def set_steering(self, value: float) -> None:
        if self._steering != value:
            self._steering = value
            self.steering_changed.emit()

    def set_sls(self, value: float) -> None:
        if self._sls != value:
            self._sls = value
            self.sls_changed.emit()

    def set_cs(self, value: float) -> None:
        if self._cs != value:
            self._cs = value
            self.cs_changed.emit()

    def set_steering_offset(self, value: float) -> None:
        if self._steering_offset != value:
            self._steering_offset = value
            self.steering_offset_changed.emit()

    # ---------- actual values ----------
    def set_actual_throttle(self, value: float) -> None:
        if self._actual_throttle != value:
            self._actual_throttle = value
            self.actual_throttle_changed.emit()

    def set_actual_brake(self, value: float) -> None:
        if self._actual_brake != value:
            self._actual_brake = value
            self.actual_brake_changed.emit()

    def set_actual_clutch(self, value: float) -> None:
        if self._actual_clutch != value:
            self._actual_clutch = value
            self.actual_clutch_changed.emit()

    def set_actual_steering(self, value: float) -> None:
        if self._actual_steering != value:
            self._actual_steering = value
            self.actual_steering_changed.emit()

    def set_actual_straightlinespeed(self, value: float) -> None:
        if self._actual_straightlinespeed != value:
            self._actual_straightlinespeed = value
            self.actual_straightlinespeed_changed.emit()

    def set_actual_curvespeed(self, value: float) -> None:
        if self._actual_curvespeed != value:
            self._actual_curvespeed = value
            self.actual_curvespeed_changed.emit()

    # ---------- max values ----------
    def set_max_throttle(self, value: float) -> None:
        if self._max_throttle != value:
            self._max_throttle = value
            self.max_throttle_changed.emit()

    def set_max_brake(self, value: float) -> None:
        if self._max_brake != value:
            self._max_brake = value
            self.max_brake_changed.emit()

    def set_max_clutch(self, value: float) -> None:
        if self._max_clutch != value:
            self._max_clutch = value
            self.max_clutch_changed.emit()

    def set_max_steering(self, value: float) -> None:
        if self._max_steering != value:
            self._max_steering = value
            self.max_steering_changed.emit()

    def set_curvespeed(self, value: float) -> None:
        if self._curvespeed != value:
            self._curvespeed = value
            self.curvespeed_changed.emit()

    def set_straightlinespeed(self, value: float) -> None:
        if self._straightlinespeed != value:
            self._straightlinespeed = value
            self.straightlinespeed_changed.emit()

    def set_all_speed_max(self, value: float) -> None:
        if self._all_speed_max != value:
            self._all_speed_max = value
            self.all_speed_max_changed.emit()

    # ---------- button status ----------
    def set_button_status(self, status: bool) -> None:
        if self._buttons_activated != status:
            self._buttons_activated = status
            self.button_status_changed.emit()

    def set_platform_status(self, status: bool) -> None:
        if self._platform_activated != status:
            self._platform_activated = status
            self.platform_status_changed.emit()

    def set_pedal_status(self, status: bool) -> None:
        if self._pedals_activated != status:
            self._pedals_activated = status
            self.pedal_status_changed.emit()

    def set_head_tracking_status(self, status: bool) -> None:
        if self._head_tracking_activated != status:
            self._head_tracking_activated = status
            self.head_tracking_status_changed.emit()

    def set_start_status(self, status: bool) -> None:
        if self._start_activated != status:
            self._start_activated = status
            self.start_status_changed.emit()

    def set_stream_status(self, status: bool) -> None:
        if self._stream_activated != status:
            self._stream_activated = status
            self.stream_status_changed.emit()

    def set_motor_status(self, status: bool) -> None:
        if self._motor_activated != status:
            self._motor_activated = status
            self.motor_status_changed.emit()

    def set_debug_status(self, status: bool) -> None:
        if self._debug_activated != status:
            self._debug_activated = status
            self.debug_status_changed.emit()

    def set_process_status(self, status: bool) -> None:
        if self._process_activated != status:
            self._process_activated = status
            self.process_status_changed.emit()

    # ---------- head tracking -----------
    def set_head_tracking_yaw_angle(self, value: float) -> None:
        if self._head_tracking_yaw_angle != value:
            self._head_tracking_yaw_angle = value
            self.head_tracking_yaw_angle_changed.emit()

    # -------------------- properties --------------------
    # ---------- standard ----------
    throttle = Property(float, get_throttle, set_throttle, notify=throttle_changed)  # type: ignore
    brake = Property(float, get_brake, set_brake, notify=brake_changed)  # type: ignore
    clutch = Property(float, get_clutch, set_clutch, notify=clutch_changed)  # type: ignore
    steering = Property(float, get_steering, set_steering, notify=steering_changed)  # type: ignore
    sls = Property(float, get_sls, set_sls, notify=sls_changed)  # type: ignore
    cs = Property(float, get_cs, set_cs, notify=cs_changed)  # type: ignore

    steering_offset = Property(float, get_steering_offset, set_steering_offset, notify=steering_offset_changed)  # type: ignore

    # ---------- actual values ----------
    actual_throttle = Property(float, get_actual_throttle, set_actual_throttle, notify=actual_throttle_changed)  # type: ignore
    actual_brake = Property(float, get_actual_brake, set_actual_brake, notify=actual_brake_changed)  # type: ignore
    actual_clutch = Property(float, get_actual_clutch, set_actual_clutch, notify=actual_clutch_changed)  # type: ignore
    actual_steering = Property(float, get_actual_steering, set_actual_steering, notify=actual_steering_changed)  # type: ignore
    actual_straightlinespeed = Property(float, get_actual_straightlinespeed, set_actual_straightlinespeed, notify=actual_straightlinespeed_changed)  # type: ignore
    actual_curvespeed = Property(float, get_actual_curvespeed, set_actual_curvespeed, notify=actual_curvespeed_changed)  # type: ignore
    actual_steering = Property(float, get_actual_steering, set_actual_steering, notify=actual_steering_changed)  # type: ignore

    # ---------- max values ----------
    max_throttle = Property(float, get_max_throttle, set_max_throttle, notify=max_throttle_changed)  # type: ignore
    max_brake = Property(float, get_max_brake, set_max_brake, notify=max_brake_changed)  # type: ignore
    max_clutch = Property(float, get_max_clutch, set_max_clutch, notify=max_clutch_changed)  # type: ignore
    max_steering = Property(float, get_max_steering, set_max_steering, notify=max_steering_changed)  # type: ignore
    straightlinespeed = Property(float, get_straightlinespeed, set_straightlinespeed, notify=straightlinespeed_changed)  # type: ignore
    curvespeed = Property(float, get_curvespeed, set_curvespeed, notify=curvespeed_changed)  # type: ignore
    all_speed_max = Property(float, get_all_speed_max, set_all_speed_max, notify=all_speed_max_changed)  # type: ignore

    # ---------- button status ----------
    button_status = Property(bool, get_button_status, set_button_status, notify=button_status_changed)  # type: ignore
    platform_status = Property(bool, get_platform_status, set_platform_status, notify=platform_status_changed)  # type: ignore
    pedal_status = Property(bool, get_pedal_status, set_pedal_status, notify=pedal_status_changed)  # type: ignore
    head_tracking_status = Property(bool, get_head_tracking_status, set_head_tracking_status, notify=head_tracking_status_changed)  # type: ignore
    start_status = Property(bool, get_start_status, set_start_status, notify=start_status_changed)  # type: ignore
    stream_status = Property(bool, get_stream_status, set_stream_status, notify=stream_status_changed)  # type: ignore
    motor_status = Property(bool, get_motor_status, set_motor_status, notify=motor_status_changed)  # type: ignore
    debug_status = Property(bool, get_debug_status, set_debug_status, notify=debug_status_changed)  # type: ignore
    process_status = Property(bool, get_process_status, set_process_status, notify=process_status_changed)  # type: ignore
    

    # ---------- head tracking ----------
    head_tracking_yaw_angle = Property(
        float, get_head_tracking_yaw_angle, set_head_tracking_yaw_angle, notify=head_tracking_yaw_angle_changed  # type: ignore
    )