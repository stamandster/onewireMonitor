#!/usr/bin/python3

#########################################################################################
#
# oneWireMonitor
#
# Written by Christopher St.Amand for the Raspberry Pi - v1.1 06/15/2024
# Initially written by Simon Kong for the Raspberry Pi - V1.0 03/09/2019 - https://github.com/SkullKill/onewireMonitor
#
# Monitor Onewire devices folder and hard reset power to the DS18B20 if folder(s) are not 
# present.
#########################################################################################

import signal
import RPi.GPIO as GPIO
import time
import os
import fnmatch
import datetime


# Variables
w1_path='/sys/bus/w1/devices'  # Path to Onewire devices folder, shouldn't need to be changed
w1_pattern='28-*'              # Onewire folder(s) pattern, shouldn't need to be changed
controlpin=25                  # *** WARNING: Do not use the same GPIO pin as another script****
detectcycle=60                 # Adjust Detect Cycle time


# handle kill signal0
def handle_exit(sig, frame):
  raise(SystemExit)

# Handle kill signal1
def setup_OSsignal():
  signal.signal(signal.SIGTERM, handle_exit)


# Starting Onewire Monitor
print("\n\n{} - Starting OneWire monitor".format(datetime.datetime.now()))
setup_OSsignal()


# Search Function
def search_folders(base_dir, pattern):
    matching_folders = []
    
    # Loop through all entries in the base directory
    for entry in os.listdir(base_dir):
        # Form the full path
        full_path = os.path.join(base_dir, entry)
        
        # Check if the entry is a directory and matches the pattern
        if os.path.isdir(full_path) and fnmatch.fnmatch(entry, pattern):
            matching_folders.append(full_path)
    
    # Return True matching folders if found, otherwise return False
    if matching_folders:
	# un/comment next line to log to console found onewire sensors
        #print(matching_folders)
        return True
    else:
        return False


try:
  print("{} - Initializing ...".format(datetime.datetime.now()))
  GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
  GPIO.setup(controlpin, GPIO.OUT)
 
  while True:
    result = search_folders(w1_path, w1_pattern)

    if result == False:
        print("{} - OneWire Offline, resetting".format(datetime.datetime.now()))
        #Power Control Pin, can be connected to a relay that is NC
        print("{} - GPIO LOW".format(datetime.datetime.now()))
        GPIO.output(controlpin, GPIO.LOW)
        time.sleep(3)
        print("{} - GPIO HIGH".format(datetime.datetime.now()))
        GPIO.output(controlpin, GPIO.HIGH)
    else:
        # un/comment the next line, to log when the next cycle is starting
        print("{} - ... Detect Cycle".format(datetime.datetime.now()))
        #sleep
        time.sleep(detectcycle)


except KeyboardInterrupt:
  print("")


except SystemExit:
  print("")


except:
  print("")


finally:
  #print("{} - cleaning up GPIO pins".format(datetime.datetime.now()))
  # Comment the following command if you are ALSO using another script utilizing 
  # RPi.GPIO as it will cause the other scripts to stop functioning, ex. CraftbeerPi
  GPIO.cleanup()
  print("{} - Exiting Onewire Monitor".format(datetime.datetime.now()))
