import os
import streamlit as st
import asyncio
from pyspark.sql import SparkSession
import plotly.express as px
from dotenv import load_dotenv
from sparkdirct.ProcessData.ProcessDataCentre import Process_Data_Centre
from datetime import datetime
from Services.data_cache import DataCache

start_time = datetime.now()

# Load environment variables
load_dotenv(override=True)
column_1_name = os.getenv("COLUMN_1")
column_2_name = os.getenv("COLUMN_2")
column_3_name = os.getenv("COLUMN_3")
postgres_v = os.getenv("POSTGRES_VERSION")
postgres_url = os.getenv("POSTGRES_URL")
postgres_user = os.getenv("POSTGRES_USER")
postgres_pass = os.getenv("POSTGRES_PASSWORD")
postgres_table = os.getenv("POSTGRES_TABLE")
output_path = os.getenv("OUTPUT_PATH")


# Initialize Spark session with PostgresSQL driver
spark = SparkSession.builder \
    .appName("StreamlitSparkVisualization") \
    .config("spark.jars.packages", postgres_v) \
    .getOrCreate()

# Initialize DataCache
data_cache = DataCache(output_path)

# Streamlit app configuration
st.title("Real-time Cryptocurrency Prices")
Process_Data_Centre = Process_Data_Centre(spark)
unique_symbols = Process_Data_Centre.uniques_value_in_column(column_2_name)
selected_symbol = st.selectbox("Select Cryptocurrency", unique_symbols)


# Function to read and visualize data
async def display_data(container_):
    while True:
        selected_symbol_ = selected_symbol.strip()
        cached_data = data_cache.get_data(selected_symbol_)

        if cached_data is not None:
            pandas_df = cached_data
        else:
            df = Process_Data_Centre.get_data_by_currency_ticket(selected_symbol_)
            pandas_df = df.toPandas()
            pandas_df = pandas_df.sort_values(by=column_3_name)
            data_cache.set_data(selected_symbol_, pandas_df)

        pandas_df = pandas_df[pandas_df[column_3_name] > start_time]

        if len(pandas_df) > 1000:
            pandas_df = pandas_df.iloc[::10, :]

        fig = px.line(pandas_df, x=column_3_name, y=column_1_name, title=f"{selected_symbol_} Price Over Time")
        container_.plotly_chart(fig, use_container_width=True)

        await asyncio.sleep(1)

# Streamlit async loop to read and visualize data
container = st.empty()

if st.button("Load Data"):
    asyncio.run(display_data(container))

# Properly end the Spark session when done
Process_Data_Centre.end_session()
