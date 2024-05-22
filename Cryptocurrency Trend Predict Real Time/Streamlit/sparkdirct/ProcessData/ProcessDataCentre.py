from datetime import datetime
import pandas as pd
from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os
from sparkdirct.ProcessData.RetriveHistoricalCurrencyData import BinanceDataRetriever

load_dotenv(override=True)

# Load environment variables
postgres_v = os.getenv("POSTGRES_VERSION")
postgres_url = os.getenv("POSTGRES_URL")
postgres_user = os.getenv("POSTGRES_USER")
postgres_pass = os.getenv("POSTGRES_PASSWORD")
postgres_table = os.getenv("POSTGRES_TABLE")
output_path = os.getenv("OUTPUT_PATH")
column_2_name = os.getenv("COLUMN_2")

postgresql_url = postgres_url
postgresql_properties = {
    "user": postgres_user,
    "password": postgres_pass,
    "driver": "org.postgresql.Driver"
}


class Process_Data_Centre:
    def __init__(self, spark_session):
        self.spark = spark_session

    def uniques_value_in_column(self, column) -> list:
        df = self.spark.read \
            .jdbc(postgresql_url, postgres_table, properties={
                "user": postgres_user,
                "password": postgres_pass,
                "driver": "org.postgresql.Driver"
            })

        uniques_value_in_column_ = df.select(column).distinct().collect()
        # Convert to list
        uniques_value_in_column_ = [row[column] for row in uniques_value_in_column_]
        return uniques_value_in_column_

    def update_real_time_data(self, currency_ticket):
        df = self.spark.read \
            .jdbc(postgresql_url, postgres_table, properties={
                "user": postgres_user,
                "password": postgres_pass,
                "driver": "org.postgresql.Driver"
            })
        return df.filter(df[column_2_name] == currency_ticket)

    def get_data_by_currency_ticket(self, currency_ticket) -> dict:
        end_time_ = datetime.now()
        retriever = BinanceDataRetriever()
        historical_data = retriever.get_historical_klines(currency_ticket, end_time_)

        df = self.spark.read \
            .jdbc(postgresql_url, postgres_table, properties={
                "user": postgres_user,
                "password": postgres_pass,
                "driver": "org.postgresql.Driver"
            })
        df = df.filter(df[column_2_name] == currency_ticket)
        # Add 2 data frames into a dictionary
        data_frames = {
            'historical_data_frame_ticket': historical_data,
            'real_time_data_frame_ticket': df
        }
        return data_frames

    def end_session(self):
        self.spark.stop()
        print("Spark session stopped successfully")














