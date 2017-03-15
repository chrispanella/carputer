# carputer
This is a project for a raspberry pi car computer. It will be a gui application with OBD communication via bluetooth.

Currently it is under development. As of now it will run and scan for bluetooth devices in the area. 


Guide:
(This works assuming you did a fresh compile of Raspbian or the Ubuntu Mate image)

1) Compile bluez/setup bluetooth from this lovely tutorial... https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation

2) Install dependencies/libraries using "apt-get install -y libraries"
  a) pkg-config
  b) libboost-python-dev
  c) libboost-thread-dev
  d) libbluetooth-dev
  e) python-dev

3) Install pybluez "pip3 install pybluez"

Reboot and run the module using idle3.
