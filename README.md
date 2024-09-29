# LiveTrack Hub
A Python-based project using a Raspberry Pi to display the real-time location of friends or family based on shared GPS data, with updates shown on a dedicated display.

# Documentation

## 1.0 | Setting up Raspberry Pi
#### 1.1 Flash the Raspberry Pi OS onto SD card
- ~~no HDMI output~~ ; fixed by adding `hdmi_force_hotplug=1` and `hdmi_group=1` to the *raspOS config*.

#### 1.2 Pi setup
- in terminal, ran `sudo apt update`, `sudo apt upgrade`, `sudo apt install python3-pip`.
- `pip3 install requests` - throws an error: "externally-managed-environment"
- had to create and activate a **virtual environment** with `python3 -m venv myenv` & `source myenv/bin/activate`
- installed packages: `pip install requests geopy numpy`
> used a virtual environment to avoid potential issues with system-managed Python packages because the Raspberry Pi is a Debian-based system. This also creates a better control over dependencies in the future.

#### 1.3 Enable SSH (Secure Shell) to access the Pi remotely/headlessly.
- entered the pi configuration with `sudo raspi-config`
- navigated to interface options and enabled SSH
- found the raspberry's IP with `hostname -I`

**1.3.1
On local machine** 
- accessed pi remotely by running `ssh user@ip`
- enter requested password

## 2.0 | Enabling Google Maps API
#### 2.1 API Access from Google Cloud
- Created a project on Google Cloud (using free trial)
- Enabled Geocoding & Distance Matrix APIs
- Created API keys to make calls in future python scripts

## 3.0 | API Key Management
#### 3.1 Using Environment Variables
> To prevent API exposure, it is good practice to use environment variables to store API key(s).
- exported key as env. variable `echo 'export GOOGLE_API="[apikey]"' >> ~/.bashrc`
#### 3.2 Future implementation
- `import os` package 
- `key = os.getenv('GOOGLE_API')` to get environmental variable
#### 3.3 Cleaning up for better readability**
- We defined `GEOCODE` and `DISTANCEMATRIX` as constants. This ensures that the endpoints are easily accessible and can be reused throughout the program without risking any typographical errors. It promotes maintainability - if the url needs to be changed, we only need to change it in one place.

## 4.0 | Testing Functions & API Calls
> after securely configuring the api key, we are able to use it to make API calls. Here, I just tested it by writing some functions that will be similarly used for our project.
#### 4.1 Test: Fetch (get_coords & get_addr)
- Used *Geocoding API* to convert any given address into a string of coordinates 
- Must use making HTTP request using package `requests` in script
- Pass address along with API key and handled the response that contains coordinates 'results' .json
**4.1.1
Refactored get_coords & get_addr**
- modified the `get_addr` function to accept individual latitude and longitude values.
- learned that tuples can be easily unpacked by adding a * when passing to a function.
- note: I wanted to use tuples rather string because it allows for better continuity and flexibility when working with coordinates.
#### 4.2 Test: Calculating Distance
- Integrated google distance matrix API for calculating distance & duration between two coordinates. Added two new functions `get_distance` and `get_duration`.
- geopy can also calculate distance but it's calculations are more used to calculate direct distances between two points in a straight line. this will be useful for geofencing in the future
#### 4.3 Test: Geofencing
- This is *important* for real-time location tracking. 
- Looked into geopy for geofencing (straight-line distancing) to determine if someone is within a certain proximity / radius of 'home'. 
- We have a boolean function that returns as `False` (not home). If that device is within that bubble, it returns `True`. 
#### 4.4 Modular Programming
- Decided to separate so far the livetrack.py script into 4 separate scripts I have currently.
- This is to make things more readable and have a cleaner workspace for future reference.
- So far, we have: livetrack.py, gui.py, Coordinates.py, and Addresses.py

## 5.0 | GUI Setup
#### 5.1 Download Tkinter as Framework
> Using [tkdocs]https://tkdocs.com/tutorial/onepage.html, installed tkinter and created a basic GUI just to test feasibility. Using static coordinates and campus coordinates as a temporary geofence.
- Tkinter is already installed in the python std library. However, still verified by running script:
 ```python
 import tkinter
 tkinter._test()
 ```
#### 5.2 Create GUI
- In gui.py, created a function that calls the tkinter library and it's tools.
- Most things performed in this step are trial-and-error, nothing is set and stone for our future GUI. 
#### 5.3 Importlib
- Couldn't figure out why the update_status functions wasn't working - was not changing statuses regardless of the coordinates / distance.
- Figured out that we can use the `importlib.reload()` function from the `importlib` library to ensure our coordinates are being refreshed.
- This is especially good for later since we will be using dynamic real-time data and not static manual data.
#### 5.4 Scaling the GUI for x Users
#### 5.5 Optimizing Data Handling







