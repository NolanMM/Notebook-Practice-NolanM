from binance.client import Client
import pandas as pd


class BinanceDataRetriever:
    def __init__(self, api_key=None, api_secret=None):
        self.client = Client(api_key, api_secret)

    def get_historical_klines(self, symbol, interval, start_str, end_str=None):
        # Request historical klines data from Binance
        klines = self.client.get_historical_klines(symbol, interval, start_str, end_str)

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

    def save_to_csv(self, df, filename):
        df.to_csv(filename)


# Usage
if __name__ == "__main__":
    retriever = BinanceDataRetriever()

    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_1DAY
    start_str = '1 Jan 2017'  # Binance data starts from 2017
    end_str = '1 Jan 2024'

    historical_data = retriever.get_historical_klines(symbol, interval, start_str, end_str)

    retriever.save_to_csv(historical_data, 'historical_binance_data.csv')

    # Display the data
    print(historical_data)
