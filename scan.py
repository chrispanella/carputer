import bluetooth
import sys
import subprocess
from time import *
from tkinter import *
from gattlib import *

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

print("Beginning the scan... \n")
duration = 8
nearby_devices = bluetooth.discover_devices(lookup_names=True, duration=duration)

addr_list = []
name_list = []
device_list = [addr_list, name_list]
choice = 1

if len(nearby_devices) != 0:
    print("Available Devices: \n")
    for (addr, name) in nearby_devices:
        addr_list.append(addr)
        name_list.append(name)
        print("{}) {}".format(choice, name,))
        choice += 1
    print("")
    selected_device = eval(input("Select device by it's number: "))
else:
    print ("There are no nearby devices available. \n Please verify that bluetooth is enabled \n on both devices and try again")
    sleep(3)
    sys.exit()

if is_number(selected_device):
    print("You selected: {} \n".format(selected_device))
    sleep(3)
    print("Attempting to connect with the device... \n")
elif selected_device == None:
    print("You didn't choose anything, restart and try again")
    sys.exit()
elif is_number(selected_device) == False:
    print("You made an invalid selection. Please restart and pick a number that is listed")
    sys.exit()

selected_addr = addr_list[selected_device - 1]
selected_name = name_list[selected_device - 1]

service_matches = bluetooth.find_service(address=selected_addr)

if len(service_matches) == 0:
    print("Couldn't find service for {}".format(selected_name))
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]
protocol = first_match["protocol"]

print("Name: {} \n Host: {} \n Port: {} \n Protocol: {} \n".format(name, host, port, protocol))

sleep(2)

pin = input("Please enter the PIN for the device:  ")

# Kill any "bluetooth-agent" process that is already running
subprocess.call("kill -9 'pidof bluetooth-agent'", shell=True)

# Start a new "bluetooth-agent process with the entered PIN
status = subprocess.call("bluetooth-agent " + pin + " &", shell=True)

sleep(1)
print("Connecting to '{}' on '{}' \n".format(name, host))

if protocol == "RFCOMM":
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        sock.connect((host, port))
    except bluetooth.btcommon.BluetoothError as err:
        print("Error: {}".format(err))
        pass
elif protocol == "L2CAP":
    try:
        sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
        sock.connect((host, port))
    except bluetooth.btcommon.BluetoothError as err:
        print("Error: {}".format(err))
        pass
else:
    print("There is an error with the connection. Please try again")
    sys.exit()

while True:
    cmd = input("Send command (q to quit):  ")
    if cmd == "q":
        print("Closing...")
        sys.exit()
    print("command,,, {}".format(cmd))
    cmd = cmd.encode('UTF-8') # shows as 'text_in_here'.encode('UTF-8')
    print("encoded,,, {}".format(cmd))
    sock.sendall(cmd)
    print("Command sent; awaiting response,,,")
    reply = sock.recv(1024) # Buffer size
    print("Response received,")
    print("Raw response,,, {}".format(reply))
    reply.decode('UTF-8') # Shows as b'reply_goes_here'.decode('UTF-8')
    print("Response decoded:\n {}".format(reply))
    sleep(0.1)
