import json
from datetime import date
from requests import Request, Session
import pprint
from dotenv import load_dotenv
import os
import yfinance as yf
import streamlit as st
import plotly.express as px
import time
start = '2010-01-01'
end = date.today().strftime('%Y-%m-%d')

load_dotenv(override=True)  # Load the environment variables from the .env file

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)

# Coinmarketcap API url
url = os.getenv('URL_QUOTE_LATEST')
api = os.getenv('COINMARKETCAP_API_KEY')

user_input = st.text_input('Enter Coin Ticker', 'bitcoin')

parameters = {'slug': user_input,
              'convert': 'USD'}  # API parameters to pass in for retrieving specific cryptocurrency data

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api
}

st.subheader('Data from 2010 - 2024')
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

def get_info():
    session = Session()  # Create new session object to manage API requests
    session.headers.update(headers)  # Update the session headers with the specified headers

    response = session.get(url, params=parameters)  # Receiving the response from the API

    info = json.loads(response.text)

    pprint.pprint(info)


get_info()
