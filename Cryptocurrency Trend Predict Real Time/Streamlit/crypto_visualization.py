import os
import streamlit as st
import asyncio
import seaborn as sns
from matplotlib import pyplot as plt
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
df_real_time = None


# Function to read and visualize historical data
def display_historical_data(_selected_symbol):
    selected_symbol_ = _selected_symbol.strip()
    cached_data = data_cache.get_data(selected_symbol_)

    if cached_data is not None:
        df_historical = cached_data
    else:
        df_dict = Process_Data_Centre.get_data_by_currency_ticket(selected_symbol_)
        df_historical = df_dict['historical_data_frame_ticket']
        data_cache.set_data(selected_symbol_, df_historical)

    # # Plot Open and Close Prices
    # st.subheader("Open and Close Prices Over Time")
    # plt.figure(figsize=(14, 7))
    # sns.lineplot(data=df_historical, x='timestamp', y='open', label='Open Price')
    # sns.lineplot(data=df_historical, x='timestamp', y='close', label='Close Price')
    # plt.legend()
    # plt.title('Open and Close Prices Over Time')
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # st.pyplot(plt)
    #
    # # Plot High and Low Prices
    # st.subheader("High and Low Prices Over Time")
    # plt.figure(figsize=(14, 7))
    # sns.lineplot(data=df_historical, x='timestamp', y='high', label='High Price')
    # sns.lineplot(data=df_historical, x='timestamp', y='low', label='Low Price')
    # plt.legend()
    # plt.title('High and Low Prices Over Time')
    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # st.pyplot(plt)
    #
    # # Plot Volume
    # st.subheader("Volume Over Time")
    # plt.figure(figsize=(14, 7))
    # sns.lineplot(data=df_historical, x='timestamp', y='volume', label='Volume')
    # plt.legend()
    # plt.title('Volume Over Time')
    # plt.xlabel('Date')
    # plt.ylabel('Volume')
    # st.pyplot(plt)

    return df_historical


# Function to update and display real-time data
async def display_real_time_data(container_, _selected_symbol):
    while True:
        selected_symbol_ = _selected_symbol.strip()
        df_real_time_ = Process_Data_Centre.update_real_time_data(selected_symbol_)
        df_real_time_ = df_real_time_.toPandas()
        df_real_time_ = df_real_time_.sort_values(by=column_3_name)

        fig = px.line(df_real_time_, x=column_3_name, y=column_1_name, title=f"{selected_symbol_} Price Current Time")
        container_.plotly_chart(fig, use_container_width=True)

        await asyncio.sleep(1)

# Streamlit async loop to read and visualize data
container = st.empty()

if st.button("Load Data"):
    _df_historical_ = display_historical_data(selected_symbol)
    # Show _df_historical_ data frame
    st.write(_df_historical_)
    asyncio.run(display_real_time_data(container, selected_symbol))

# Properly end the Spark session when done
Process_Data_Centre.end_session()
