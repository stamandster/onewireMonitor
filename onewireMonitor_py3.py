#!/usr/bin/python3

print("---------------------------------------------------------------------------------------")
print(" OnewireMonitor v1.1")
print("")
print(" Written by Christopher St.Amand for the Raspberry Pi - v1.1 06/15/2024")
print(" https://github.com/SkullKill/onewireMonitor")
print(" Initially written by Simon Kong for the Raspberry Pi - V1.0 03/09/2019")
print(" https://github.com/SkullKill/onewireMonitor")
print("")
print(" Monitor Onewire devices folder(s) & hard reset DS18B20 power not present")
print("---------------------------------------------------------------------------------------")

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
def w1_devices(base_dir, pattern):
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
  print("{} - ... Running".format(datetime.datetime.now()))
  GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
  GPIO.setup(controlpin, GPIO.OUT)

  loop = 0

  while loop == 0:
    result = w1_devices(w1_path, w1_pattern)

    if result == False:
        print("{} - ERROR: OneWire Offline, resetting".format(datetime.datetime.now()))
        #Power Control Pin, can be connected to a relay that is NC
        print("{} - SETTING GPIO LOW".format(datetime.datetime.now()))
        GPIO.output(controlpin, GPIO.LOW)
        time.sleep(3)
        print("{} - SETTING GPIO HIGH".format(datetime.datetime.now()))
        GPIO.output(controlpin, GPIO.HIGH)
	time.sleep(3)
	result2 = w1_devices(w1_path, w1_pattern)
        if result2 == True:
            print("{} - Onewire Resolved".format(datetime.datetime.now()))

        print("...")
	
    else:
        # un/comment the next line, to log when the next cycle is starting
        # print("{} - ... Detect Cycle".format(datetime.datetime.now()))
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
  #GPIO.cleanup()
  print("{} - Exiting Onewire Monitor".format(datetime.datetime.now()))
