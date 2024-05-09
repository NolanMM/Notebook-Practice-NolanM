import pandas as pd
import numpy as np
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def web_content_div(web_content, class_path, stock_code):
    price_div = web_content.find('fin-streamer', {'data-testid': 'qsp-price', 'data-symbol': stock_code})
    if price_div:
        price = price_div.get_text(strip=True)
        price_change_span = web_content.find('fin-streamer', {'data-testid': 'qsp-price-change', 'data-symbol': stock_code}).find('span')
        price_change = price_change_span.get_text(strip=True)
        price_percent_change_span = web_content.find('fin-streamer', {'data-testid': 'qsp-price-change-percent', 'data-symbol': stock_code}).find('span')
        price_percent_change = price_percent_change_span.get_text(strip=True)
        return price, price_change, price_percent_change
    else:
        return None, None, None

def web_statistic_div(web_content, class_path, stock_code):
    # find statistic div with class path and data-testid attribute
    statistic_div = web_content.find('div', {'class': class_path, 'data-testid': 'quote-statistics'})
    if statistic_div:
        fin_streamer_tag = statistic_div.find('fin-streamer', {'data-symbol': stock_code, 'data-field': 'regularMarketVolume'})
        if fin_streamer_tag:
            # Extract the value from the span tag inside fin-streamer
            value_span = fin_streamer_tag.find('span')
            if value_span:
                return fin_streamer_tag
            else:
                return None
        else:
            return None
    else:
        return None


def real_time_stock_price(stock_code):
    url = f'https://finance.yahoo.com/quote/{stock_code}?p={stock_code}&.tsrc=fin-srch'
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'html.parser')
        # save the web content to a file with encoding
        with open('web_content.html', 'w', encoding='utf-8') as f:
            f.write(str(web_content))

        prices_class_path = 'container svelte-mgkamr'
        statistic_class_path = 'container svelte-tx3nkj'
        statistic_div = web_statistic_div(web_content, statistic_class_path, stock_code)
        price, change, percent_change = web_content_div(web_content, prices_class_path, stock_code)

    except exceptions as e:
        print("Error:", e)
        price, change, percent_change, statistic_div = None, None, None, None
    return price, change, percent_change, statistic_div


stock_code = "TSLA"
price, change, percent_change, statistic_div = real_time_stock_price(stock_code)
print("Price:", price)
print("Change:", change)
print("Percent Change:", percent_change)
print("Statistic Div:", statistic_div)
