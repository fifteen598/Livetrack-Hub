import os
import requests
from geopy import distance

key = os.getenv('GOOGLE_API')

campus_address = '1845 Fairmount St, Wichita, United States'
campus_coordinates = (37.7165348,-97.2959726)
home = (37.688682, -97.336553)

GEOCODE = "https://maps.googleapis.com/maps/api/geocode/json"
DISTMATRIX = "https://maps.googleapis.com/maps/api/distancematrix/json"

# This function takes address, gets & outputs coordinates
def get_coords(address): # input address as a string
        url = f'{GEOCODE}?address={address}&key={key}'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'results' in data and len(data['results']) > 0:
                location = data['results'][0]['geometry']['location']
                return (location['lat'], location['lng'])
        else:
                print("ERROR: could not get coordinates.")
                return None


# This function takes a tuple of coordinates as its input and prints the address at it's location
def get_addr(x,y):
        url = f'{GEOCODE}?latlng={x},{y}&key={key}'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'results' in data and len(data['results']) > 0:
                location = data['results'][0]['formatted_address']
                return location
        else:
                print("ERROR: could not get address.")
                return None


# This function takes two sets of coordinates and prints the distance between them
def get_distance(origin, destination):
        url = f'{DISTMATRIX}?origins={origin[0]},{origin[1]}&destinations={destination[0]},{destination[1]}&units=imperial&key={key}'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'rows' in data and len(data['rows']) > 0:
                elements = data['rows'][0]['elements']
                if len(elements) > 0 and 'distance' in elements[0]:
                        distance = elements[0]['distance']['text']
                        return distance
        else:
                print("ERROR: could not get distance.")
                return None


# This function takes two sets of coordinates and prints the estimted time by distance between them
def get_duration(origin, destination):
        url = f'{DISTMATRIX}?origins={origin[0]},{origin[1]}&destinations={destination[0]},{destination[1]}&units=imperial&key={key}'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'rows' in data and len(data['rows']) > 0:
                elements = data['rows'][0]['elements']
                if len(elements) > 0 and 'duration' in elements[0]:
                        duration = elements[0]['duration']['text']
                        return duration
        else:
                print("ERROR: could not get duration.")

                
#get_coords(campus_address)
#get_addr(*campus_coordinates)
#get_addr(*home)
#get_coords(home)

# get_distance(campus_coordinates, home)
# get_duration(campus_coordinates, home)

# print(distance.distance(campus_coordinates, home).miles)

print(get_addr(*home))

