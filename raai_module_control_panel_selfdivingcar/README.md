# RAAI Module Control Panel

The Overlay component of the overall Control Component. It Visualizes the Driver Inputs and also gives Throttle Data
over to the Vehicle Output Writer

## Structure
The visualized Driver Data is **received** from the driver_input_reader module over the pynng address <br>
``ipc:///tmp/RAAI/driver_input_reader.ipc``

The Throttle Data controlled by the Control Panel then gets **sent** over the address <br>
``ipc:///tmp/RAAI/control_panel.ipc``