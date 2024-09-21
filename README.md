# LiveTrack Hub
A Python-based project using a Raspberry Pi to display the real-time location of friends or family based on shared GPS data, with updates shown on a dedicated display.

# Documentation

## 1.0 | Setting up Raspberry Pi
### 1.1 Flash the Raspberry Pi OS onto SD card
- ~~no HDMI output~~ ; fixed by adding `hdmi_force_hotplug=1` and `hdmi_group=1` to the *raspOS config*.

### 1.2 Pi setup
- in terminal, ran `sudo apt update`, `sudo apt upgrade`, `sudo apt install python3-pip`.
- `pip3 install requests` - throws an error: "externally-managed-environment"
- had to create and activate a **virtual environment** with `python3 -m venv myenv` & `source myenv/bin/activate`
- installed packages: `pip install requests geopy numpy`
> used a virtual environment to avoid potential issues with system-managed Python packages because the Raspberry Pi is a Debian-based system.

### 1.3 Enable SSH (Secure Shell) to access the Pi remotely/headlessly.
- entered the pi configuration with `sudo raspi-config`
- navigated to interface options and enabled SSH
- found the raspberry's IP with `hostname -I`

**1.3.1
On local machine** 
- to access pi remotely, must input `ssh user@ip`
- enter requested password

## 2.0 | Enabling Google Maps API
### 2.1 API Access from Google Cloud
- Created a project on Google Cloud (using free trial)
- Enabled Geocoding & Distance Matrix APIs
- Created API keys to make calls in future python scripts

## 3.0 | API Key Management
### 3.1 Using Environment Variables
> To prevent API exposure, it is good practice to use environment variables to store API key(s).
- exported key as env. variable `echo 'export GOOGLE_API="[apikey]"' >> ~/.bashrc`
### 3.2 Future implementation
- `import os` package 
- `key = os.getenv('GOOGLE_API')` to get environmental variable

## 4.0 | Testing Functions & API Calls
> after securely configuring the api key, we are able to use it to make API calls. Here, I just tested it by writing some functions that will be similarly used for our project.
### 4.1 Test: Fetch (get_coords & get_addr)
- Used *Geocoding API* to convert any given address into a tuple of coordinates 
- Must use making HTTP request using package `requests` in script
- Pass address along with API key and handled the response that contains coordinates 'results' .json
### 4.2 Test: Calculating Distance



