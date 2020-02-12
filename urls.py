base_info_url = 'https://infoapi.webull.com/api'
base_options_url = 'https://quoteapi.webullbroker.com/api'
base_paper_url = 'https://act.webullbroker.com/webull-paper-center/api'
base_quote_url = 'https://quoteapi.webull.com/api'
base_securities_url = 'https://securitiesapi.webullbroker.com/api'
base_trade_url = 'https://tradeapi.webulltrade.com/api/trade'
base_user_url = 'https://userapi.webull.com/api'

def account(account_id):
    return f'{base_trade_url}/v2/home/{account_id}'

def account_id():
    return f'{base_trade_url}/account/getSecAccountList/v4'

def analysis(stock):
    return f'{base_securities_url}/securities/ticker/v5/analysis/{stock}'

def cancel_order(account_id):
    return f'{base_trade_url}/order/{account_id}/cancelStockOrder/'

def dividends(account_id):
    return f'{base_trade_url}/v2/account/{account_id}/dividends?direct=in'

def fundamentals(stock):
    return f'{base_securities_url}/securities/financial/index/{stock}'

def is_tradable(stock):
    return f'{base_trade_url}/ticker/broker/permissionV2?tickerId={stock}'

def login():
    return f'{base_user_url}/passport/login/account'

def logout():
    """ update """
    return f'{base_user_url}/passport/logout/account'

def news(stock):
    return f'{base_securities_url}/information/news/v5/tickerNews/{stock}'

def options_exp_date(stock):
    return f'{base_options_url}/quote/option/{stock}/list'

def orders(account_id):
    return f'{base_trade_url}/v2/option/list?secAccountId={account_id}&startTime=1970-0-1&dateType=ORDER&status='

def paper_account(paper_account_id):
    return f'{base_paper_url}/paper/1/acc/{paper_account_id}'

def paper_account_id():
    return f'{base_paper_url}/myaccounts/true'

def place_option_orders(account_id):
    return f'{base_trade_url}/v2/option/checkOrder/{account_id}'

def place_orders(account_id):
    return f'{base_trade_url}/order/{account_id}/placeStockOrder'

def quotes(stock):
    return f'{base_quote_url}/quote/tickerRealTimes/v5/{stock}'

def refresh_login():
    return f'{base_user_url}/passport/refreshToken?refreshToken='

def stock_id(stock):
    return f'{base_info_url}/search/tickers5?keys={stock}&queryNumber=1'

def trade_token():
    return f'{base_trade_url}/login'

def user():
    return f'{base_user_url}/user'
