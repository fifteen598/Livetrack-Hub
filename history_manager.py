import json
from datetime import datetime, timedelta
from pathlib import Path

class HistoryManager:
    def __init__(self):
        self.history_file = Path('location_history.json')
        self.history_data = self.load_history()

    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_location(self, lat, lng, accuracy):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'lat': lat,
            'lng': lng,
            'accuracy': accuracy
        }
        self.history_data.append(entry)
        
        # Keep only last 500 entries
        if len(self.history_data) > 500:
            self.history_data = self.history_data[-500:]
            
        with open(self.history_file, 'w') as f:
            json.dump(self.history_data, f)

    def get_history(self, hours=24):
        now = datetime.now()
        cutoff = now - timedelta(hours=hours) if hours != 'all' else None
        
        return [entry for entry in self.history_data 
                if cutoff is None or 
                datetime.fromisoformat(entry['timestamp']) > cutoff]