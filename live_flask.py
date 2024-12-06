from flask import Flask, request
import requests

FLASK_SERVER_URL = 'https://fifteen598.pythonanywhere.com'

app = Flask(__name__)

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.get_json()
    name = data.get('name')
    lat = data.get('latitude')
    lng = data.get('longitude')
    response = requests.post(f"{FLASK_SERVER_URL}/update_location", json={
        'name': name,
        'latitude': lat,
        'longitude': lng
    })
    return response.text, response.status_code

def fetch_records():
    response = requests.get(f"{FLASK_SERVER_URL}/fetch_records")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching records: {response.status_code} {response.text}")

def fetch_coordinates(name):
    response = requests.get(f"{FLASK_SERVER_URL}/fetch_coordinates", params={'name': name})
    if response.status_code == 200:
        data = response.json()
        return (data['latitude'], data['longitude'])
    else:
        raise Exception(f"Error fetching coordinates: {response.status_code} {response.text}")

