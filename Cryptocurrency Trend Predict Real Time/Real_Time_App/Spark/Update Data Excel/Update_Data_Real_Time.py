import websocket
import json
import pandas as pd
from binance.client import Client
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("BinanceStreamProcessor") \
    .getOrCreate()

# Initialize Binance client
client = Client()

# Get exchange information and filter for symbols ending with 'USDT'
dict_ = client.get_exchange_info()
syms = [i['symbol'] for i in dict_['symbols'] if i['symbol'].endswith('USDT')]

# Prepare WebSocket stream assets
assets = [coin.lower() + '@kline_1m' for coin in syms]
relevant_assets = '/'.join(assets)

# Define schema for incoming data
schema = StructType([
    StructField("price", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("event_time", TimestampType(), True)
])


def manipulate(data):
    value_data = data['data']['k']
    price, sym = value_data['c'], value_data['s']
    event_time = pd.to_datetime([data['data']['E']], unit='ms')[0]
    return [(price, sym, event_time)]


def on_message(ws, message):
    json_message = json.loads(message)
    data = manipulate(json_message)
    df = spark.createDataFrame(data, schema=schema)
    df.write.mode("append").csv("CoinPrices.csv")


# WebSocket URL
socket = "wss://stream.binance.com:9443/stream?streams=" + relevant_assets

# Start WebSocket connection
ws = websocket.WebSocketApp(socket, on_message=on_message)
ws.run_forever()
