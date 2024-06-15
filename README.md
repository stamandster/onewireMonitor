# onewireMonitor for Raspberry Pi v1.1 06/11/2024 
This will **Monitor onewire temp directory and hard reset power to the DS18B20 if folder is not present.** 
It has a script to monitor that the main program is running, and restarts it if for whatever reason it crashes.

**NOTE: It would be better to find the cause the issue (wiring/connector/capacitance) than to use this.**


## Onewire (1-wire) Raspberry Pi Setup

### Software
```
    raspi-config
        Interfacing Options >> 1-Wire >> enable yes,
        reboot
```

### Hardware Changes

Instead of default Raspberry Pi 3v3 or 5v pin, the default script VDD pin is GPIO#17 [physical pin 11] (you can change to another GPIO pin in the script) - https://pinout.xyz/

## Installation

Configure New LGPIO via - https://rpi-lgpio.readthedocs.io/en/release-0.4/install.html

Download the script files
```
git clone https://github.com/stamandster/onewireMonitor
```

Copy both onewireMonitor.sh and onewireMonitor_py3.py to /usr/local/sbin and set permission
```
cd onewireMonitor
sudo cp onewireMonitor* /usr/local/sbin/
```

Set Permissions on Folder
```
sudo chmod +x /usr/local/sbin/onewireMonitor*
```

Adjust variables in script to match your needs, found in the beginning sections of the script
```
sudo nano /usr/local/sbin/onewireMonitor_py3.py
```
```
# Variables
w1_path='/sys/bus/w1/devices'  # Path to Onewire devices folder, shouldn't need to be changed
w1_pattern='28-*'              # Onewire folder(s) pattern, shouldn't need to be changed
controlpin=25                  # *** WARNING: Do not use the same GPIO pin as another script****
detectcycle=60                 # Adjust cycle time as you see fit
```

Configure /etc/crontab and add the following line at the end of the file
```
sudo crontab -e
```

```
# monitor and start onewireMonitor is process is not running
*/1 * * * * root /usr/local/sbin/onewireMonitor.sh > /dev/null 2>&1
```

Alternatively, you can run the script directly from any folder after adjusting your variables

## Notes

A Raspberry Pi has a limit of 16mA per GPIO pin, with a total of 51mA for all GPIO's. A DS18B20 sink a max of 4mA, 1 GPIO can technically power a maximum of 4, and safely 3.


