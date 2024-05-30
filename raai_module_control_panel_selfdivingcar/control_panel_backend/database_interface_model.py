from PySide6.QtCore import QObject, Signal, Slot, Property
import pynng
from time import sleep
import json


class DriverDataPublisher(QObject):
    driversChanged = Signal()
    statusChanged = Signal()

    def __init__(self, pub_address, req_address):
        super().__init__()
        self.__drivers = [
            {
                "id": "4823662a-29c5-47d7-bdba-68baa2825990",
                "name": "Dummy",
                "email": "example@email.test",
                "created": "2023-11-02-08-58-03",
            }
        ]

        self.__status = ""

        self.PUB_ADDRESS = pub_address
        self.pub_socket = pynng.Pub0()
        self.pub_socket.listen(self.PUB_ADDRESS)
        sleep(1)

        self.req_socket = pynng.Req0()
        self.req_socket.dial(req_address, block=False)

    def sort_drivers(self, drivers):
        """
        Sorts a list of drivers based on their 'created' attribute.

        Args:
        drivers (list): The list of drivers to sort.

        Returns:
        list: The sorted list of drivers.
        """
        drivers.sort(key=lambda x: x["created"], reverse=True)
        return drivers

    @Slot(str)
    def send_data(self, driver_name):
        """
        Sends the current driver name to the publish socket.

        Args:
        driver_name (str): The name of the driver to send.
        """
        data = "current_driver: " + driver_name
        self.pub_socket.send(data.encode("utf-8"))
        self.set_status(f"Sent data: {driver_name}")

    @Slot()
    def refresh_driver(self):
        """Sends a request to refresh the driver data and handles the response."""
        data = "get_drivers"
        self.req_socket.send(data.encode("utf-8"))
        response = self.req_socket.recv().decode("utf-8")

        if response == "No Driver found":
            self.set_status("No driver found")
        elif response == "Error":
            self.set_status("Error while refreshing drivers")
        else:
            response = json.loads(response)
            response = self.sort_drivers(response)

            self.set_drivers(response)
            self.set_status("Refreshed drivers")
        print(self.drivers)

    @Slot(str)
    def search_driver(self, name: str):
        """
        Searches for a driver by name.

        Args:
        name (str): The name of the driver to search for.
        """
        result = [driver for driver in self.__drivers if driver["name"] == name]
        if result:
            self.set_drivers(result)
            self.set_status("Found driver " + name)
        else:
            self.set_status("No driver found")

    @Slot(str)
    def create_driver(self, name: str):
        """
        Creates a new driver with the given name.

        Args:
        name (str): The name of the driver to create.
        """
        data = f"post_driver: {name}"
        try:
            self.req_socket.send(data.encode("utf-8"))
            response = self.req_socket.recv().decode("utf-8")
            if response:
                try:
                    self.__drivers.append(json.loads(response))
                    self.__drivers = self.sort_drivers(self.__drivers)
                    self.driversChanged.emit()
                    self.set_status("Created driver: " + name)
                except Exception as e:
                    print(e)
                    self.set_status("Driver creation failed")
            else:
                self.set_status("Driver creation failed")
        except:
            self.set_status("Driver creation failed")

    @Property(list, notify=driversChanged)  # type: ignore
    def drivers(self):
        return self.__drivers

    @Property(str, notify=statusChanged)  # type: ignore
    def status(self):
        return self.__status

    def set_drivers(self, drivers):
        if self.__drivers != drivers:
            self.__drivers = drivers
            self.driversChanged.emit()

    def set_status(self, status):
        if self.__status != status:
            self.__status = status
            self.statusChanged.emit()
