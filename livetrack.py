import os
import requests

key = os.getenv('GOOGLE_API') 
campus_address = '1845 Fairmount St, Wichita, United States'
campus_coordinates = '37.7165348,-97.2959726'

# This function gets coordinates and returns it from a specific address
def get_coords(address):
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={key}'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'results' in data and len(data['results']) > 0:
                location = data['results'][0]['geometry']['location']
                print(f"Coordinates: {location['lat']}, {location['lng']}")
        else:
                print("ERROR: could not get coordinates.")

# This function gets address and returns it from a tuple of coordinates
def get_addr(coordinates):
        url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={coordinates}&key={key}'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and 'results' in data and len(data['results']) > 0:
                location = data['results'][0]['formatted_address']
                print(f"Formatted Address: {location}")
        else:
                print("ERROR: could not get address.")
                
get_coords(campus_address)
get_addr(campus_coordinates)