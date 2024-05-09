from bs4 import BeautifulSoup

def web_content_div(web_content, ticker_code):
    _web_content_div_ = web_content.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)', 'data-symbol': ticker_code})
    if _web_content_div_:
        price = _web_content_div_['value']
        price_change = _web_content_div_.find_next_sibling('fin-streamer')['value']
        price_percent_change = _web_content_div_.find_next_sibling('fin-streamer').find_next_sibling('fin-streamer')['value']
        return price, price_change, price_percent_change
    else:
        return None, None, None

def web_content_div_2(web_content, symbol):
    price_div = web_content.find('fin-streamer', {'data-test': 'qsp-price', 'data-symbol': symbol})
    if price_div:
        price = price_div.get_text(strip=True)
        price_change_span = web_content.find('fin-streamer', {'data-test': 'qsp-price-change', 'data-symbol': symbol}).find('span')
        price_change = price_change_span.get_text(strip=True)
        price_percent_change_span = web_content.find('fin-streamer', {'data-field': 'regularMarketChangePercent', 'data-symbol': symbol}).find('span')
        price_percent_change = price_percent_change_span.get_text(strip=True)
        return price, price_change, price_percent_change
    else:
        return None, None, None
# Example usage:
html_content = '''<div class="D(ib) Mend(20px)"><fin-streamer class="Fw(b) Fz(36px) Mb(-4px) D(ib)" data-symbol="BRK-B" data-test="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="2" value="406.37" active="">406.37</fin-streamer><fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="BRK-B" data-test="qsp-price-change" data-field="regularMarketChange" data-trend="txt" data-pricehint="2" value="0.22998047" active=""><span class="C($positiveColor)">+0.23</span></fin-streamer> <fin-streamer class="Fw(500) Pstart(8px) Fz(24px)" data-symbol="BRK-B" data-field="regularMarketChangePercent" data-trend="txt" data-pricehint="2" data-template="({fmt})" value="0.0005662591" active=""><span class="e3b14781 f4be3290 f5a023e1">(+0.06%)</span></fin-streamer><fin-streamer class="D(n)" data-symbol="BRK-B" changeev="regularTimeChange" data-field="regularMarketTime" data-trend="none" value="" active="true"></fin-streamer><fin-streamer class="D(n)" data-symbol="BRK-B" changeev="marketState" data-field="marketState" data-trend="none" value="" active="true"></fin-streamer><div id="quote-market-notice" class="C($tertiaryColor) D(b) Fz(12px) Fw(n) Mstart(0)--mobpsm Mt(6px)--mobpsm Whs(n)"><span>At close: May 8 04:02PM EDT</span></div></div>'''

soup = BeautifulSoup(html_content, 'lxml')

# Dynamic ticker code
ticker_code = 'BRK-B'

price, price_change, price_percent_change = web_content_div_2(soup, ticker_code)

print("Price:", price)
print("Price Change:", price_change)
print("Price Percent Change:", price_percent_change)
