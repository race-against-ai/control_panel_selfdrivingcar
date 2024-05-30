from PySide6.QtCore import QObject, Signal, Property


def pad_left(string: str, length: int, padchar: str = "0") -> str:
    string = padchar * (length - len(string)) + string[0:length]
    return string


class Timer(QObject):
    millis_changed = Signal(name="millisChanged")
    seconds_changed = Signal(name="secondsChanged")
    minutes_changed = Signal(name="minutesChanged")

    def __init__(self, millis: int, seconds: int, minutes: int) -> None:
        QObject.__init__(self)
        self._millis = millis
        self._seconds = seconds
        self._minutes = minutes

    def set_timestamp(self, timestamp_ns: int) -> None:
        timestamp_ms = timestamp_ns // (1000 * 1000)

        millis = timestamp_ms % 1000
        seconds = (timestamp_ms // 1000) % 60
        minutes = (timestamp_ms // (1000 * 60)) % 60

        self.set_millis(millis)
        self.set_seconds(seconds)
        self.set_minutes(minutes)

    def get_millis(self) -> int:
        return self._millis

    def get_seconds(self) -> int:
        return self._seconds

    def get_minutes(self) -> int:
        return self._minutes

    def set_millis(self, millis: int) -> None:
        self._millis = millis
        self.millis_changed.emit()

    def set_seconds(self, seconds: int) -> None:
        self._seconds = seconds
        self.seconds_changed.emit()

    def set_minutes(self, minutes: int) -> None:
        self._minutes = minutes
        self.minutes_changed.emit()

    millis = Property(int, get_millis, set_millis, notify=millis_changed)  # type: ignore
    seconds = Property(int, get_seconds, set_seconds, notify=seconds_changed)  # type: ignore
    minutes = Property(int, get_minutes, set_minutes, notify=minutes_changed)  # type: ignore
