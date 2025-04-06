# test_history_data.py
import json
from datetime import datetime, timedelta

history = []
now = datetime.now()

for i in range(10):
    entry_time = now - timedelta(hours=i*4)
    history.append({
        'timestamp': entry_time.isoformat(),
        'lat': 37.71783 + (i * 0.0001),
        'lng': -97.29209 - (i * 0.0001),
        'accuracy': 10.0
    })

with open('location_history.json', 'w') as f:
    json.dump(history, f)

print("Sample history data created successfully!")