from flask import Flask, request
import threading
import time
import requests
from typing import Dict

POCKETBASE_URL = 'http://127.0.0.1:8090'
COLLECTION_NAME = 'coordinates'

app = Flask(__name__)
coordinate_dictionary = {}
sharing_status = {}  # Add this to track sharing status
@app.route('/update_location', methods=['POST'])

def update_location(): # this is the data that is sent from the client to the server
    data = request.get_json()
    #print("Received Data:", json.dumps(data, indent=2))
    name = data.get('name')
    lat = data.get('latitude')
    long = data.get('longitude')
    if is_sharing(name):
        upsert_record(name, lat, long)
        return "Updated Location", 200
    return "Location sharing disabled", 200

@app.route('/toggle_sharing/<name>', methods=['POST'])
def handle_toggle_sharing(name):
    new_status = toggle_sharing(name)
    return {
        "name": name,
        "sharing": new_status
    }, 200

def toggle_sharing(name: str) -> bool:
    """Toggle location sharing for a user. Returns new sharing status."""
    sharing_status[name] = not sharing_status.get(name, True)
    return sharing_status[name]

def is_sharing(name: str) -> bool:
    """Check if user is currently sharing location."""
    return sharing_status.get(name, True)  # Default to True if not set

def upsert_record(name, lat, long): # this function will either create a new record or update an existing record in the database
    url = f'{POCKETBASE_URL}/api/collections/{COLLECTION_NAME}/records'
    params = {
        'filter': f'name="{name}"'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        records = response.json().get('items', [])

        if records:
            print('Record already exists! Updating info...')
            records = records[0]
            record_id = records['id']
            update_url = f'{POCKETBASE_URL}/api/collections/{COLLECTION_NAME}/records/{record_id}'
            update_data = {'lat': lat, 'long': long}
            requests.patch(update_url, json=update_data)
        else:
            print('Creating new record...')
            data = {'name': name, 'lat': lat, 'long': long}
            requests.post(url, json=data)

def fetch_records(): # this function gets all the records from the database
    url = f'{POCKETBASE_URL}/api/collections/{COLLECTION_NAME}/records'
    response = requests.get(url)
    if response.status_code == 200:
        records = response.json().get('items', [])
        for record in records:
            name = record.get('name')
            lat = record.get('lat')
            long = record.get('long')
            coordinate_dictionary[name] = (lat, long)
    return coordinate_dictionary # when this function is called, it will return the dictionary of all the existing records in the database

def fetch_coordinates(name): # specific record call
    # only return coordinates if sharing is enabled
    if not is_sharing (name):
        return None

    url = f'{POCKETBASE_URL}/api/collections/{COLLECTION_NAME}/records'
    params = {
        'filter': f'name="{name}"'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        records = response.json().get('items', [])
        if records:
            record = records[0]
            lat = record.get('lat')
            long = record.get('long')
            return (lat, long)
    return None

def run_flask():
    app.run(host='0.0.0.0' , port=5000)

def main():
    while True:
        if is_sharing('Adrien'):  # Only print coordinates if sharing is enabled
            coords = fetch_coordinates('Adrien')
            if coords:
                print(coords)
        time.sleep(10)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    main_thread = threading.Thread(target=main)

    flask_thread.start()
    main_thread.start()

    flask_thread.join()
    main_thread.join()
