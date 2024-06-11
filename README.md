# onewireMonitor
onewireMonitor for Raspberry Pi. 
This will **Monitor onewire temp directory and hard reset power to the DS18B20 if folder is not present.** 
It has a script to monitor that the main program is running, and restarts it if for whatever reason it crashes.

**NOTE: It would be better to find the cause the issue (wiring/connector/capacitance) than to use this.**

The script [onewireMonitor](https://github.com/SkullKill/onewireMonitor) is design specificly for the Raspberry Pi.

## V 1.1 06/11/2024

## One wire setup

### Software
    rasppi-config
        Interfacing Options >> 1-Wire >> enable yes,
        reboot

### Hardware

- Data pin to rpi gpio (BCM) #4 [physical pin 7]
- Ground to rip ground [physical pin 9] using this because it is next to #4
- Power pin to rpi gpio #17 [physical pin 11] using this because it is next to the ground pin
- You can use any other pin, but #17 is what the code is written for, just change the code if using another pin.


## Installation

- Download the files
-     git clone https://github.com/stamandster/onewireMonitor
- Copy both onewireMonitor.sh and onewireMonitor_py3.py to /usr/local/sbin and set permission
-     cd onewireMonitor
-     cp onewireMonitor* /usr/local/sbin/
- Set Permissions on Folder
-     chmod +x /usr/local/sbin/onewireMonitor*
- Find out the folder / DS18B20 serial to monitor
- Change "/sys/bus/w1/devices/28-XXXXXXXXXXXX" to the correct value in onewireMonitor_py3.py
-     ls /sys/bus/w1/devices/
-     nano /usr/local/sbin/onewireMonitor_py3.py
- Configure /etc/crontab and add the following line at the end of the file
-     nano /etc/crontab

```
# monitor and start onewireMonitor is process is not running
*/1 * * * * root /usr/local/sbin/onewireMonitor.sh > /dev/null 2>&1
```


## Notes

A Raspberry Pi has a limit of 16mA per GPIO pin, with a total of 51mA for all GPIO's. A DS18B20 sink a max of 4mA, 1 GPIO can technically power a maximum of 4, and safely 3.


