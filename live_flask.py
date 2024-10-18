from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/update_location', methods=['POST'])

def update_location():
    data = request.get_json()
    #print("Recieved data: ", json.dumps(data, indent=2))

    address = data.get('address')

    with open('real_time_coordinates.txt', 'w') as file:
        file.write(f"{address}")

    return "Updated location", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
