# Webull
APIs for webull, you are free to use, but code not extensively checked and Webull may update the APIs or the endpoints at any time.
https://www.webull.com/

Feel free to sign-up for a webull account through here, you will be able to help me to get referral stocks. You can also get 2 stocks for free:

https://www.webull.com/activity?inviteCode=oqJvTY3rJNyR&source=invite_gw&inviteSource=wb_oversea

Sorry for procrastinating in answering the questions and updating the packages. But if you really like the package or really like to motivate me. Materialist appreciations would really motivate me to responding you faster 😂:

[<img src="https://miro.medium.com/max/1476/1*KGh1GBqI9R0TfSsSPHGpNg.png" width="200px">](https://www.buymeacoffee.com/tedchou12)


# Install

```
pip install webull

or

python3 -m pip install webull
```

# Run tests

```
pip install pytest requests_mock
python -m pytest -v
```

# Usage

How to login with your email

Webull has made Multi-Factor Authentication (MFA) mandatory since 2020/05/28, if you are having issues, take a look at here:
https://github.com/tedchou12/webull/wiki/MFA-&-Security

Or Authenticate without Login completely 2021/02/14:
https://github.com/tedchou12/webull/wiki/Workaround-for-Login

```
from webull import webull # for paper trading, import 'paper_webull'

wb = webull()
wb.login('test@test.com', 'pa$$w0rd')

```

How to login with your mobile
```
from webull import webull # for paper trading, import 'paper_webull'

wb = webull()
wb.login('+1-1112223333', 'pa$$w0rd') # phone must be in format +[country_code]-[your number]

```

How to order stock
```
from webull import webull
wb = webull()
wb.login('test@test.com', 'pa$$w0rd')

wb.get_trade_token('123456')
wb.place_order(stock='AAPL', price=90.0, qty=2)
```

How to check standing orders
```
from webull import webull
wb = webull()
wb.login('test@test.com', 'pa$$w0rd')

wb.get_trade_token('123456')
orders = wb.get_current_orders()
```

How to cancel standing orders
```
from webull import webull
wb = webull()
wb.login('test@test.com', 'pa$$w0rd')

wb.get_trade_token('123456')
wb.cancel_all_orders()
```

# FAQ
Thank you so much, I have received Emails and messages on reddit from many traders/developers that liked this project. Thanks to many that helped and contributed to this project too! There are quite a few repeated questions on the same topic, so I have utilized the Wiki section for them. If you have troubles regarding *Login/MFA Logins*, *Real Time Quote Data*, *What is Trade PIN/Trade Token*, or *How to buy me a coffee* please take a look at the Wiki pages first. https://github.com/tedchou12/webull/wiki

# Stream Quotes
https://github.com/tedchou12/webull/wiki/How-to-use-Streaming-Quotes%3F

# Disclaimer
This software is not extensively tested, please use at your own risk.

# Developers
If you are interested to join and help me improve this, feel free to message me.
