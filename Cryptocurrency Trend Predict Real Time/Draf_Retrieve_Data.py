# Retrive data from yfinance
import yfinance as yf
from datetime import date
import streamlit as st
import plotly.express as px  # interactive charts
import time

start = '2010-01-01'
end = date.today().strftime('%Y-%m-%d')

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# Take user input for Cryptocurrency (default is Bitcoin) ticker symbol is  'bitcoin'
user_input = st.text_input('Enter Stock Ticker', 'bitcoin')

# create dataframes for the cryptocurrency data
chart_placeholder = st.empty()

# Describing the data
st.subheader('Data from 2010 - 2024')
data_description = st.empty()

# Visualizing the data
st.subheader('Closing Price vs Time chart')
closing_price_chart = st.empty()

df = yf.download(user_input, start, end)

# Update data description
data_description.write(df.describe())

# Visualizing the data
fig = px.line(df, x=df.index, y='Close', title='Closing Price vs Time')
closing_price_chart.plotly_chart(fig, use_container_width=True)

# Moving Averages
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()

fig = px.line(df, x=df.index, y='Close', title='Closing Price vs Time with Moving Averages')
fig.add_scatter(x=df.index, y=ma100, mode='lines', name='100-Day MA', line=dict(color='red'))
fig.add_scatter(x=df.index, y=ma200, mode='lines', name='200-Day MA', line=dict(color='green'))
chart_placeholder.plotly_chart(fig, use_container_width=True)
time.sleep(5)