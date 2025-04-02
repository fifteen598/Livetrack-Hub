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

---

## 2.0 | Enabling Google Maps API
#### 2.1 API Access from Google Cloud
- Created a project on Google Cloud (using free trial)
- Enabled Geocoding & Distance Matrix APIs
- Created API keys to make calls in future python scripts

---

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

---

## 5.0 | GUI Setup
#### 5.1 Download Tkinter as Framework
> Using https://tkdocs.com/tutorial/onepage.html, installed tkinter and created a basic GUI just to test feasibility. Using static coordinates and campus coordinates as a temporary geofence.
- Tkinter is already installed in the python std library. However, still verified by running script:
 ```python
 import tkinter
 tkinter._test()
 ```
#### 5.2 Create GUI
- In gui.py, created a function that calls the tkinter library and it's tools.
- Most things performed in this step are trial-and-error, nothing is set and stone for our future GUI. 
#### 5.3 Importlib
- Couldn't figure out why the `update_status` functions wasn't working - was not changing statuses regardless of the coordinates / distance.
- Figured out that we can use the `importlib.reload()` function from the `importlib` library to ensure our coordinates are being refreshed.
- This is especially good for later since we will be using dynamic real-time data and not static manual data.
#### 5.4 Transition to Figma + Tkinter Designer
- Scrapped the old GUI due to aesthetic limitations and decided to design the new GUI using *Figma* for the design and *Tkinter Designer* to convert design into functional Tkinter assets.
> Resource: https://www.figma.com/ - A beautifully designed website that allows developers to bring design and developing togther with no boundaries on creativity. 
> Resource: https://github.com/ParthJadhav/Tkinter-Designer - Uses Figma API to analyze a design file to create the respective code and assets needed for the GUI. Assists in speeding up the GUI development process in python.
- Created the new layout in Figma, focusing on creating a cleaner and much more visiually appealing interface.
- The design includes rounded rectangles, modern typography, and aligned layout for better readability and user experience.
#### 5.5 Tkinter Designer Conversion Process
- Once completed the design. Used Tkinter Designer to import and generate a Tkinter based layout from the assets from said design. This includes boxes, text fields, buttons, etc.
- Refactored the generated code to make it more readable and maintainable, breaking it down into sections that can be easily integrated for future parts of the project.
#### 5.6 Integrating Old Functionality
- The old GUI functioanlity which included real-time location updates, geofencing, and coordinate based status updates needed to be applied to the new GUI so I could see if there were any issues in the process.
- Verified all dynamic features such as `update_status` function works in new design

---

## 6.0 | User Interaction and Real-Time Updates
#### ~~ 6.1 Dynamic User Input~~ removed
- ~~Added functionality for the app to prompt users to enter names for tracking purposes. The user can enter up to 5 names, which will be displayed on the GUI.~~
- ~~This allows for dynamic addition of users and provides better flexibility in the tracking system.~~

#### 6.2 Real-Time Location Display
- Integrated **TkinterMapView** to display real-time locations on the GUI.
- Used `live_flask.fetch_coordinates()` to retrieve the coordinates of the tracked individuals and update their position on the map.
- Added markers on the map for each user, with their name displayed for easy identification.

#### ~~6.3 Status Updates with MQTT~~ removed
- ~~Transitioned from Flask to **Mosquitto** as an MQTT broker for real-time data updates.~~
- ~~Each mobile device publishes its GPS coordinates to the broker, and the Raspberry Pi GUI subscribes to receive these updates instantly.~~
- ~~Removed Flask server from the project as its functionality was deemed redundant.~~

#### 6.4 Real-Time Status Indicators
- Created visual status indicators for each user (e.g., "isAway" or "isHome") based on their current location relative to predefined geofences.
- Added new icons for "isHome" and "isAway" statuses, which change dynamically depending on the user's location.
- Labels are updated in real-time as new location data is received from the MQTT broker.

---

## 7.0 | Server Integration with PythonAnywhere

### 7.1 Transition to Cloud Hosting
- Replaced local Flask server with a cloud-hosted Flask server on **PythonAnywhere**.
- PythonAnywhere hosts the Flask application and a **MySQL database** that stores user location data.

### 7.2 Mobile Data Communication via Shortcuts App
- Used the **Shortcuts app** on iOS to send live location data to the server:
  - The script captures the phone's **latitude**, **longitude**, and the user's **name**.
  - It sends this data as a **POST request** to the `/update_location` endpoint on the PythonAnywhere-hosted Flask server.
- **Steps in the Shortcuts App**:
  1. Use the `Get Current Location` action to capture the device’s latitude and longitude.
  2. Add a `Text` action to input the user's name.
  3. Use the `Get Contents of URL` action:
     - Set the URL to `https://fifteen598.pythonanywhere.com/update_location`.
     - Configure it to send the data as a **POST request** with the following JSON body:
       ```json
       {
           "name": "<Your Name>",
           "latitude": <latitude>,
           "longitude": <longitude>
       }
       ```
  4. Run the shortcut periodically or on demand to keep the database updated with live location data.

--

## 8.0 | Future Improvements
#### 8.1 Handling Multiple Users
- Plan to refine the GUI to better handle multiple users, possibly by adding different colored markers or customizable labels for each person.
- Future updates may include adding more detailed geofencing features to provide notifications when a user enters or leaves a defined area.

#### 8.2 Optimizing Data Storage
- Considering removing **PocketBase** for data storage if real-time tracking is sufficient for user needs.
- Alternatively, PocketBase could be retained solely for storing historical location data for future analytics.

#### 8.3 Mobile App Integration
- Plan on continuing to develop a simple mobile app for publishing GPS data instead of using third-party apps.
- The app will provide better control over the data and allow for additional features like geofence notifications and manual status updates.

---

## 9.0 | Interactive Geofence Configuration
### 9.1 New Feature: Geofence Setup via Address Input
- Added functionality to set the geofence dynamically using a street address.

### 9.2 Implementation Steps
1. Integrated a popup window accessible via **Button 5** on the GUI:
   - Prompt the user to input an address.
2. Address is processed using the `livetrack.get_coords` function:
   - Converts the input address to geographic coordinates via Google Geocoding API.
3. Updated the geofence logic to dynamically reflect the new coordinates:
   - Changes are reflected on the map with updated geofence markers.

### 9.3 Real-Time Updates
- The map widget updates to display the new geofence and adjust its marker position.
- New geofence is applied dynamically without needing to restart the application.

### 9.4 Benefits
- Improves user interaction by allowing geofence configuration in real-time.
- Reduces manual intervention and enhances demo capabilities for showcasing the project.

---

## 10.0 | Engineering Open House Demo

### 10.1 Demonstration Plan
- **Interactive Features**:
  - Visitors can input addresses to dynamically set geofences.
  - The GUI updates real-time location markers and status indicators to reflect new data.
  - Mobile phones actively send live location data to the server for real-time updates.
- **Focus Areas**:
  - Showcasing dynamic updates via the map widget and user status panel.
  - Highlighting the seamless integration of mobile location updates with the cloud server.

### 10.2 Backup Plan
- Prepare a fallback demonstration using static data to showcase functionality in case of connectivity issues with the cloud-hosted Flask server.

---

## 11.0 | Challenges and Solutions

### 11.1 Database Access
- Moved from local database and Flask server access to **PythonAnywhere** for centralized hosting.
- Flask endpoints are used to fetch and manipulate data stored in the MySQL database.

### 11.2 Real-Time Map Updates
- Addressed issues with integrating dynamic updates in `TkinterMapView` by implementing periodic refresh logic for user markers.

### 11.3 Geofence Integration
- Initial challenges with setting geofences via the GUI were resolved using Google Geocoding API and dynamic map updates.

### 11.4 Was not able to connect to School's WiFi
- Due to assumed security restrictions, the Raspberry Pi was unable to connect to the school's WiFi network. We instead used a mobile hotspot for internet access.

---

## 12.0 | Next Steps

- Add logic for dynamic map centering based on user marker positions.
- Explore options for enhanced mobile app integration.
- Investigate geofence-specific notifications to improve real-time user interaction.
