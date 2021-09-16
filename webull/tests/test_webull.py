import pytest
import requests_mock

from unittest.mock import MagicMock
from webull.webull import webull, endpoints

'''

[HOW TO RUN TESTS]

pip install pytest requests_mocks
python -m pytest -v

'''

#####################################################
#################     FIXTURES     ##################
#####################################################

urls = endpoints.urls()

@pytest.fixture
def reqmock():
    with requests_mock.Mocker() as m:
        yield m

@pytest.fixture
def wb():
    return webull()


#####################################################
#################     TESTS     #####################
#####################################################

@pytest.mark.skip(reason="TODO")
def test_alerts_add():
	pass

def test_alerts_list(wb: webull, reqmock):
    # [case 1] unsuccessful alerts_list
    reqmock.get(urls.list_alerts(), text='''
        {
            "success": false
        }
    ''')

    result = wb.alerts_list()
    assert result is None

    # [case 2] successful alerts_list
    reqmock.get(urls.list_alerts(), text='''
        {
            "success": true,
            "data": [
                {
                    "tickerId": 913257472,
                    "tickerSymbol": "SBUX"
                }
            ]
        }
    ''')

    result = wb.alerts_list()
    assert result is not None

@pytest.mark.skip(reason="TODO")
def test_alerts_remove():
	pass

@pytest.mark.skip(reason="TODO")
def test_build_req_headers():
	pass

@pytest.mark.skip(reason="TODO")
def test_cancel_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_cancel_otoco_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_account():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_account_id():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_active_gainer_loser():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_analysis():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_bars():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_calendar():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_current_orders():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_detail():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_dividends():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_financials():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_history_orders():
	pass

def test_get_news(wb: webull, reqmock):
    stock = 'AAPL'
    Id = 0
    items = 20
    ticker = 913256135
    wb.get_ticker = MagicMock(return_value=ticker)
    reqmock.get(urls.stock_id(stock, wb._region_code), text='''
        {
            "categoryId":0,
            "categoryName":"综合",
            "hasMore":true,
            "list":[{
                "tickerId":913256135,
                "exchangeId":96,
                "type":2,
                "name":"Apple",
                "symbol":"AAPL",
                "disSymbol":"AAPL",
                "disExchangeCode":"NASDAQ",
                "exchangeCode":"NSQ",
            }]
        }
    ''')

    reqmock.get(urls.news(stock, Id, items), text='''
        [
          {
            "id": 45810067,
            "title": "US STOCKS-S&P 500, Dow gain on factory data, strong oil prices ",
            "sourceName": "reuters.com",
            "newsTime": "2021-09-15T16:35:33.000+0000",
            "summary": "US STOCKS-S&P 500, Dow gain on factory data, strong oil prices ",
            "newsUrl": "https://pub.webullfintech.com/us/news-html/83c0d98e2cca4165b94addfc3bfdac47.html",
            "siteType": 0,
            "collectSource": "reuters"
          }
        ]
    ''')

    result = wb.get_news(tId=stock, Id=Id, items=items)
    assert result is not None
    assert result[0]['id'] is not None

@pytest.mark.skip(reason="TODO")
def test_get_option_quote():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_options():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_options_by_strike_and_expire_date():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_options_expiration_dates():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_portfolio():
	pass

@pytest.mark.skip(reason="TODO")
def test_get_positions():
    pass

def test_get_quote(wb: webull, reqmock):

    # successful get_quote
    stock = 'AAPL'
    ticker = 913256135
    wb.get_ticker = MagicMock(return_value=ticker)
    reqmock.get(urls.stock_id(stock, wb._region_code), text='''
        {
            "categoryId":0,
            "categoryName":"综合",
            "hasMore":true,
            "list":[{
                "tickerId":913256135,
                "exchangeId":96,
                "type":2,
                "name":"Apple",
                "symbol":"AAPL",
                "disSymbol":"AAPL",
                "disExchangeCode":"NASDAQ",
                "exchangeCode":"NSQ",
            }]
        }
    ''')

    reqmock.get(urls.quotes(ticker), text='''
        {
            "open": "312.15",
            "close": "307.65",
            "high": "315.95",
            "low": "303.21",
            "tickerId": "913256135"
        }
    ''')

    result = wb.get_quote(stock=stock)
    assert result['open']  == '312.15'
    assert result['close'] == '307.65'
    assert result['high']  == '315.95'
    assert result['low']   == '303.21'
    assert result['tickerId'] == '913256135'

    # failed get_quote, no stock or tId provided
    with pytest.raises(ValueError):
        wb.get_quote()

    # failed get_quote, stock symbol doesn't exist
    bad_stock_symbol = '__YOLOSWAG__'
    wb.get_ticker = MagicMock(side_effect=ValueError('TickerId could not be found for stock __YOLOSWAG__'))
    with pytest.raises(ValueError) as e:
        wb.get_quote(bad_stock_symbol)

def test_get_ticker(wb: webull, reqmock):

    # failed get_ticker, stock doesn't exist
    bad_stock_symbol = '__YOLOSWAG__'
    reqmock.get(urls.stock_id(bad_stock_symbol, wb._region_code), text='''
        { "hasMore": false }
    ''')
    with pytest.raises(ValueError) as e:
        wb.get_ticker(bad_stock_symbol)
        assert 'TickerId could not be found for stock {}'.format(bad_stock_symbol) in str(e.value)

    # failed get_ticker, no stock provided
    with pytest.raises(ValueError) as e:
        wb.get_ticker()
        assert 'Stock symbol is required' in str(e.value)

    # successful get_ticker
    good_stock_symbol = 'SBUX'
    reqmock.get(urls.stock_id(good_stock_symbol, wb._region_code), text='''
        {
            "data":[
                {
                    "tickerId":913257472,
                    "exchangeId":96,
                    "type":2,
                    "secType":[61],
                    "regionId":6,
                    "regionCode":"US",
                    "currencyId":247,
                    "currencyCode":"USD",
                    "name":"Starbucks",
                    "symbol":"SBUX",
                    "disSymbol":"SBUX",
                    "disExchangeCode":"NASDAQ",
                    "exchangeCode":"NSQ",
                    "listStatus":1,
                    "template":"stock",
                    "derivativeSupport":1,
                    "tinyName":"Starbucks"
                }
            ],
            "hasMore":false
        }
    ''')
    result = wb.get_ticker('SBUX')
    assert result == 913257472

@pytest.mark.skip(reason="TODO")
def test_get_ticker():
	pass

def test_get_tradable(wb: webull, reqmock):
	# [case 1] get_tradable returns any json object
    stock = 'SBUX'
    reqmock.get(urls.stock_id(stock, wb._region_code), text='''
        {
            "data": [{
                "tickerId": 913257472,
                "symbol": "SBUX"
            }]
        }
    ''')

    reqmock.get(urls.is_tradable("913257472"), text='''
        {
            "json": "object"
        }
    ''')

    resp = wb.get_tradable(stock=stock)
    assert resp is not None

def test_get_trade_token(wb: webull, reqmock):
    # [case 1] get_trade_token fails, access token is expired
    reqmock.post(urls.trade_token(), text='''
        {
            "msg": "AccessToken is expire",
            "traceId": "xxxxxxxxxxxxxxxxxxxxxxxxxx",
            "code": "auth.token.expire",
            "success": false
        }
    ''')

    any_password = '123456'
    resp = wb.get_trade_token(any_password)
    assert resp == False
    assert wb._trade_token == ''

    # [case 2] get_trade_token fails, password is incorrect
    reqmock.post(urls.trade_token(), text='''
        {
            "msg":"'Inner server error", 
            "traceId": "xxxxxxxxxxxxxxxxxxxxxxxxxx", 
            "code": "trade.pwd.invalid", 
            "data": { "fail": 1.0, "retry": 4.0 }, 
            "success": false
        }
    ''')

    bad_password = '123456'
    resp = wb.get_trade_token(bad_password)
    assert resp == False
    assert wb._trade_token == ''

    # [case 3] get_trade_token succeeds, password is correct
    reqmock.post(urls.trade_token(), text='''
        {
            "success": true, 
            "data": {
                "tradeToken": "xxxxxxxxxx",
                "tradeTokenExpireIn": 28800000
            }
        }
    ''')

    good_password = '123456'
    resp = wb.get_trade_token(good_password)
    assert resp == True
    assert wb._trade_token == 'xxxxxxxxxx'

def test_login(reqmock, wb):
    # [case 1] login fails, bad mobile username credentials
    reqmock.post(urls.login(), text='''
        {
            "code": "phone.illegal"
        }
    ''')

    bad_mobile_username = '1112224444'
    resp = wb.login(username=bad_mobile_username, password='xxxxxxxx')
    assert resp['code'] == 'phone.illegal'

    # [case 2] mobile login succeeds
    # actual API response includes more data, but for brevity,
    # this mock response only returns the fields which we are expecting
    reqmock.post(urls.login(), text='''
        {
            "accessToken":"xxxxxxxxxx",
            "uuid":"yyyyyyyyyy",
            "refreshToken":"zzzzzzzzzz",
            "tokenExpireTime":"2020-07 13T00:25:34.235+0000"
        }
    ''')
    # mocking this to cover webull.login internal call to webull.get_account_id
    wb.get_account_id = MagicMock(return_value='11111111')

    resp = wb.login(username='1+1112223333', password='xxxxxxxx')
    assert wb._access_token == 'xxxxxxxxxx'
    assert wb._refresh_token == 'zzzzzzzzzz'
    assert wb._token_expire == '2020-07 13T00:25:34.235+0000'
    assert wb._uuid == 'yyyyyyyyyy'
    assert wb._account_id == '11111111'

    # if username or password is not passed, should raise ValueError
    with pytest.raises(ValueError):
        wb.login()

@pytest.mark.skip(reason="TODO")
def test_login_prompt():
	pass

def test_login_prompt():
	pass

def test_logout(wb, reqmock):
    # successful logout returns a 200 response
    reqmock.get(urls.logout(), status_code=200)
    resp = wb.logout()
    assert resp == 200

def test_modify_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_place_option_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_place_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_place_otoco_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_refresh_login():
	pass

@pytest.mark.skip(reason="TODO")
def test_replace_option_order():
	pass

@pytest.mark.skip(reason="TODO")
def test_run_screener():
	pass
