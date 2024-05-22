from binance.client import Client
import pandas as pd
from datetime import datetime

interval_ = Client.KLINE_INTERVAL_1DAY


class BinanceDataRetriever:
    def __init__(self, api_key=None, api_secret=None):
        self.client = Client(api_key, api_secret)
        self.interval_ = Client.KLINE_INTERVAL_1DAY
        self.start_str_ = '1 Jan 2010'

    def get_historical_klines(self, symbol_, end_str__) -> [pd.DataFrame, None]:
        # If end_str_ is not provided, use the current date and time
        if end_str__ is None:
            return None
        end_str_ = end_str__.strftime('%d %b %Y')
        # Request historical klines data from Binance
        klines = self.client.get_historical_klines(symbol_, self.interval_, self.start_str_, end_str_)

        # Convert the data into a DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume',
            'ignore'
        ])

        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        # Drop unnecessary columns
        df.drop(['close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                 'taker_buy_quote_asset_volume', 'ignore'], axis=1, inplace=True)

        return df

    def save_to_csv(self, df, filename) -> None:
        df.to_csv(filename)

# Usage
if __name__ == "__main__":
    retriever = BinanceDataRetriever()

    symbol = 'BTCUSDT'
    # Binance data starts from 2017
    end_str = None  # Will use datetime.now()

    historical_data = retriever.get_historical_klines(symbol, end_str)

    retriever.save_to_csv(historical_data, 'historical_binance_data.csv')

    # Display the data
    print(historical_data)
