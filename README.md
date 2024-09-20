# Livetrack-Hub
A Python-based project using a Raspberry Pi to display the real-time location of friends or family based on shared GPS data, with updates shown on a dedicated display.

*1.1*
Flash the Raspberry Pi OS onto SD card
- no HDMI output; fixed by adding 'hdmi_force_hotplug=1' and 'hdmi_group=1' to the OS config

*1.2*
Pi setup
- 'sudo apt update', 'sudo apt upgrade', 'sudo apt install python3-pip'.
- 'pip3 install requests' - throws an error: "externally-managed-environment"
- create and activate a virtual environement with 'python3 -m venv myenv' & 'source myenv/bin/activate'
- install packages: 'pip install requests geopy numpy'

notes: we use a virtual environment to avoid potential issues with system-managed Python packages because the Raspberry Pi is a Debian-based system.

*1.3*
Enable SSH (Secure Shell) to access the Pi remotely/headlessly.
- enter the pi configuration with 'sudo raspi-config'
- navigate to interface options and enable SSH
- find the raspberry's IP with 'hostname -I'
*1.3.1*
On local machine
- to access pi remotely, we must input 'ssh user@ip'
- password



