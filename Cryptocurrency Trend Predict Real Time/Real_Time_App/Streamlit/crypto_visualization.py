import streamlit as st
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import plotly.express as px

# Initialize Spark session
spark = SparkSession.builder \
    .appName("StreamlitSparkVisualization") \
    .getOrCreate()

# Streamlit app configuration
st.title("Real-time Cryptocurrency Prices")
selected_symbol = st.selectbox("Select Cryptocurrency", ['BTCUSDT', 'ETHUSDT', 'BNBUSDT'])


# Function to read and visualize data
def display_data():
    df = spark.read.parquet("crypto_prices.parquet")
    filtered_df = df.filter(col("symbol") == selected_symbol)
    pandas_df = filtered_df.toPandas()
    fig = px.line(pandas_df, x='event_time', y='price', title=f"{selected_symbol} Price Over Time")
    st.plotly_chart(fig)


# Streamlit loop to read and visualize data
if st.button("Load Data"):
    display_data()


