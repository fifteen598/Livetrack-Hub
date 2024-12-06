from flask import Flask, request
import threading
import time
import requests

POCKETBASE_URL = 'http://127.0.0.1:8090'
COLLECTION_NAME = 'coordinates'

app = Flask(__name__)
coordinate_dictionary = {}
@app.route('/update_location', methods=['POST'])

def update_location(): # this is the data that is sent from the client to the server
    data = request.get_json()
    #print("Received Data:", json.dumps(data, indent=2))
    name = data.get('name')
    lat = data.get('latitude')
    long = data.get('longitude')
    upsert_record(name, lat, long) # takes the data it receives and updates the record in   the database
    return "Updated Location", 200 

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
        return {record['name']: (float(record['lat']), float(record['long'])) for record in records}
    return {} # when this function is called, it will return the dictionary of all the existing records in the database

def fetch_coordinates(name): # specific record call
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


def run_flask():
    print("Running Flask...")
    app.run(host='0.0.0.0' , port=5000) # we can access this server remotely 

# this is where we will be calling the functions to update, fetch, and display the records
def main():
    while True:
        print("Returned records:")
        print(fetch_coordinates('Adrien'))
        time.sleep(10)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    main_thread = threading.Thread(target=main)

    flask_thread.start()
    main_thread.start()

    flask_thread.join()
    main_thread.join()
