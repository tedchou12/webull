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
The streaming quotes utilize the mqtt "internet of things" format over tls 1.2 encrypted binary websockets, you must install paho-mqtt >=1.5 from pypy to get this working.

Warning::  most messages sent with price data like topic 102 are sketchy at best and seem to change what they are sending, based on ticker, exchange, or if its afterhours; for ex. AAPL will send price & volume in same message 2 or 3 times a second, while a penny biotech will not send any pricing data via this topic; topic 105 is the default, due to this issue. if your getting too much data, change to topic 102 to get more aggragated pricing data and see what ya get


Step 1: create callback functions
```
def on_price_message(topic, data):
    print (data)
	#the following fields will vary by topic number you recieve (topic 105 in this case)
    print(f"Ticker: {topic['tickerId']}, Price: {data['deal']['price']}, "
        + f"Volume: {data['deal']['volume']}, Trade time: {data['tradeTime']}")
	#all your algo precessing code goes here

def on_order_message(topic, data):
    print(data)

```

Step 2: create the connection object
```
conn = StreamConn(debug_flg=True)

conn.price_func = on_price_message
conn.order_func = on_order_message
```

Step 3: open the connection, add access token if you have it set in webull object
```
webull = webull()
#if you pay a subscription fee for OPRA, level 2, etc, or want to get updates on order fills 
#you can log into to webull (as shown in examples above) and pass the access token to the connect call 
#(paper trade orders do not update via the websockets, they are polled ever 30 or 60 seconds in the app)

if not webull.access_token is None and len(webull.access_token) > 1:
    conn.connect(webull.did, access_token=webull.access_token)
else:
    conn.connect(webull.did)
```	

Step 4: Subscribe to the ticker ids that you need
```
    conn.subscribe(tId='913256135') #AAPL
    conn.run_loop_once()
```

Step 5: Start the processing loop
```
conn.run_blocking_loop() #never returns till script crashes or exits
```


Heres a breakdown of the data fields in the the various topics:
```
The topic of each message contains the message type and tickerId, order status messages only have
a single numeric topic, unlike price uppdates where the topic includes the tickerId and message type
 
    ====Order status from platpush====
    123456789: messageId, action, type, title, messageHeaders{popstatus, popvalidtime}, 
                      data {"tickerId, brokerId, secAccountId, orderId, filledQuantity, orderType, 
                        orderStatus, messageProtocolVersion, messageProtocolUri,messageTitle, messageContent} 
                        

    ====Price updates from wspush====
    All price messages have a status field defined as F = pre-market, T = market hours, A = after-market
	
    Topic 102 is the most common streaming message used by the trading app, 
			at times, Topic 102 for some crazy reason may not show a close price or volume,
			so it's not useful for a trading app
    High/low/open/close/volume are usually totals for the day
    Most message have these common fields: transId, pubId, tickerId, tradeStamp, trdSeq, status
    topic 101:  T: close, change, marketValue, changeRatio
    topic 102:  F/A: pPrice,  pChange, pChRatio,
                T: high(optional), low(optional), open(optional), close(optional), volume(optional), 
                    vibrateRatio, turnoverRate(optional), change, changeRatio, marketValue
    topic 103:  F/A: deal:{trdBs(always N), volume, tradeTime(H:M:S), price} 
                T: deal:{trdBs, volume, tradeTime(H:M:S), price}
    topic 104:  F/T/A: askList:[{price, volume}], bidList:[{price, volume}]
    topic 105:  Seems to be 102 and 103
    topic 106:  Seems to be 102 (and 103 sometimes depending on symbol/exchange)
    topic 107:  Seems to be 103 and 104
    topic 108:  Seems to be 103 and 104 and T: depth:{ntvAggAskList:[{price:, volume}], ntvAggBidList:[{price:,volume:}]}}
    """


# Disclaimer
This software is not extensively tested, please use at your own risk.

# Developers
If you are interested to join and help me improve this, feel free to message me.
