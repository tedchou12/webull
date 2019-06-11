# webull
APIs for webull, you are free to use, but code not extensively checked and Webull may update the APIs or the endpoints at any time.

# usage
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
orders = webull.get_orders()
for order in orders :
  print(order)
```

How to cancel standing orders
```
webull = webull()
webull.login('test@test.com', 'pa$$w0rd')
webull.get_account_id()
webull.get_trade_token('123456')
orders = webull.get_orders()
for order in orders :
  if order['statusCode'] == 'Working' :
    webull.cancel_order(order['orderId'], '')
```
