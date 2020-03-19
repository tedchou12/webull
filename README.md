# Webull
APIs for webull, you are free to use, but code not extensively checked and Webull may update the APIs or the endpoints at any time.
https://www.webull.com/

# Usage
How to use this package.

How to login and get account details
```
webull = webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_account_id()
webull.get_trade_token('123456')
print(webull.get_account())
```

How to order stock
```
webull = webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_account_id()
webull.get_trade_token('123456')
webull.place_order('NDAQ', 90.0, 2) //stock_ticker_symbol, price, quantity
```

How to check standing orders
```
webull = webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_account_id()
webull.get_trade_token('123456')
orders = webull.get_current_orders()
for order in orders :
  print(order)
```

How to cancel standing orders
```
webull = webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_account_id()
webull.get_trade_token('123456')
orders = webull.get_current_orders()
for order in orders :
  if order['statusCode'] == 'Working' :
    webull.cancel_order(order['orderId'])
```

## How to use Streaming Quotes
The streaming quotes utilize the mqtt "internet of things" format over tls 1.2 encrypted binary websockets, you must install paho-mqtt >=1.5 from pypi to get this working.

Warning::  most messages sent with price data like topic 102 are sketchy at best and seem to change what they are sending, based on ticker, exchange, or if its afterhours; for ex. AAPL will send price & volume in same message 2 or 3 times a second, while a penny biotech will not send any pricing data via this topic; topic 105 is the default, due to this issue. if your getting too much data, change to topic 102 to get more aggragated pricing data and see what ya get

# Stream Quotes
https://github.com/tedchou12/webull/wiki/How-to-use-Streaming-Quotes%3F

# Disclaimer
This software is not extensively tested, please use at your own risk.

# Developers
If you are interested to join and help me improve this, feel free to message me.
