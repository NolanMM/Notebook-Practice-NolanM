import os
import pickle
from datetime import datetime

class DataCache:
    def __init__(self, output_path):
        self.output_path = output_path
        self.cache = self.load_cache()

    def load_cache(self):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        if os.path.exists(self.output_path):
            try:
                with open(self.output_path, 'rb') as cache_file:
                    return pickle.load(cache_file)
            except PermissionError:
                print(f"Permission denied: {self.output_path}")
                return {}
        return {}

    def save_cache(self):
        try:
            with open(self.output_path, 'wb') as cache_file:
                pickle.dump(self.cache, cache_file)
        except PermissionError:
            print(f"Permission denied: {self.output_path}")

    def get_composite_key(self, symbol, date):
        return f"{symbol}_{date}"

    def get_data(self, symbol):
        today_date = datetime.today().strftime('%Y-%m-%d')
        composite_key = self.get_composite_key(symbol, today_date)

        if composite_key in self.cache:
            return self.cache[composite_key]
        return None

    def set_data(self, symbol, data):
        today_date = datetime.today().strftime('%Y-%m-%d')
        composite_key = self.get_composite_key(symbol, today_date)
        self.cache[composite_key] = data
        self.save_cache()
