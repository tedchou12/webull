import json
import requests
import uuid
import hashlib
import time
from datetime import datetime
from pandas import DataFrame, to_datetime

class webull :
    def __init__(self) :
        self.session = requests.session()
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
        }
        # self.auth_method = self.login_prompt
        self.access_token = ''
        self.account_id = ''
        self.refresh_token = ''
        self.trade_token = ''
        self.uuid = ''
        self.did = '1bc0f666c4614a11808a372f14ffe42c'

    def build_req_headers(self, include_trade_token=False, include_time=False):
        '''
        Build default set of header params
        '''
        headers = self.headers
        headers['did'] = self.did
        headers['access_token'] = self.access_token
        if include_trade_token:
            headers['t_token'] = self.trade_token
        if include_time:
            headers['t_time'] = str(round(time.time() * 1000))
        return headers

    '''
    for login purposes password need to be hashed password, figuring out what hash function is used currently.
    '''
    def login(self, username='', password='') :
        # with webull md5 hash salted
        password = ('wl_app-a&b@!423^' + password).encode('utf-8')
        md5_hash = hashlib.md5(password)
        # password = md5_hash.hexdigest()
        data = {'account': username,
                'accountType': 2,
                'deviceId': self.did,
                'pwd': md5_hash.hexdigest(),
                'regionId': 1}
        response = requests.post('https://userapi.webull.com/api/passport/login/account', json=data, headers=self.headers)

        result = response.json()
        if result['success'] == True and result['code'] == '200' :
            self.access_token = result['data']['accessToken']
            self.refresh_token = result['data']['refreshToken']
            self.token_expire = result['data']['tokenExpireTime']
            self.uuid = result['data']['uuid']
            return True
        else :
            return False

    def refresh_login(self) :
        # password = md5_hash.hexdigest()
        headers = self.build_req_headers()

        data = {'refreshToken': self.refresh_token}

        response = requests.post('https://userapi.webull.com/api/passport/refreshToken?refreshToken=' + self.refresh_token, json=data, headers=headers)

        result = response.json()
        if 'accessToken' in result and result['accessToken'] != '' and result['refreshToken'] != '' and result['tokenExpireTime'] != '' :
            self.access_token = result['accessToken']
            self.refresh_token = result['refreshToken']
            self.token_expire = result['tokenExpireTime']
            return True
        else :
            return False


    '''
    get some contact details of your account name, email/phone, region, avatar...etc
    '''
    def get_detail(self) :
        headers = self.build_req_headers()

        response = requests.get('https://userapi.webull.com/api/user', headers=headers)
        result = response.json()

        return result

    '''
    get account id
    call account id before trade actions
    '''
    def get_account_id(self) :
        headers = self.build_req_headers()

        response = requests.get('https://tradeapi.webulltrade.com/api/trade/account/getSecAccountList/v4', headers=headers)
        result = response.json()

        if result['success'] == True :
            self.account_id = str(result['data'][0]['secAccountId'])
            return True
        else :
            return False

    '''
    get important details of account, positions, portfolio stance...etc
    '''
    def get_account(self) :
        headers = self.build_req_headers()

        response = requests.get('https://tradeapi.webulltrade.com/api/trade/v2/home/' + self.account_id , headers=headers)
        result = response.json()

        return result

    '''
    output standing positions of stocks
    '''
    def get_positions(self) :
        data = self.get_account()

        return data['positions']

    '''
    output numbers of portfolio
    '''
    def get_portfolio(self) :
        data = self.get_account()

        output = {}
        for item in data['accountMembers'] :
            output[item['key']] = item['value']

        return output

    '''
    Get open/standing orders
    '''
    def get_current_orders(self) :
        data = self.get_account()

        # output = {}
        # for item in  :
        #     output[item['key']] = item['value']

        return data['openOrders']

    '''
    Historical orders, can be cancelled or filled
    status = Cancelled / Filled / Working / Partially Filled / Pending / Failed / All
    '''
    def get_history_orders(self, status='Cancelled'):
        headers = self.build_req_headers(include_trade_token=True, include_time=True)
        response = requests.get('https://tradeapi.webulltrade.com/api/trade/v2/option/list?secAccountId=' + self.account_id + '&startTime=' + str(1970-0-1) + '&dateType=ORDER&status=' + str(status), headers=headers)

        return response.json()

    '''
    authorize trade, must be done before trade action
    '''
    def get_trade_token(self, password='') :
        headers = self.build_req_headers()

        # with webull md5 hash salted
        password = ('wl_app-a&b@!423^' + password).encode('utf-8')
        md5_hash = hashlib.md5(password)
        # password = md5_hash.hexdigest()
        data = {'pwd': md5_hash.hexdigest()}

        response = requests.post('https://tradeapi.webulltrade.com/api/trade/login', json=data, headers=headers)
        result = response.json()

        if result['success'] == True :
            self.trade_token = result['data']['tradeToken']
            return True
        else :
            return False

    def alerts_list(self):
        '''
        Get alerts
        '''
        headers = self.build_req_headers()
        url = 'https://userapi.webullbroker.com/api/user/warning/v2/query/tickers'
        
        response = requests.get(url, headers=headers)
        result = response.json()
        return result.get('data', [])

    def alerts_remove(self, alert=None, priceAlert=True, smartAlert=True):
        '''
        remove alert
        alert is retrieved from alert_list
        '''
        headers = self.build_req_headers()
        url = 'https://userapi.webullbroker.com/api/user/warning/v2/manage/overlap'

        if alert.get('tickerWarning') and priceAlert:
            alert['tickerWarning']['remove'] = True
            alert['warningInput'] = alert['tickerWarning']

        if alert.get('eventWarning') and smartAlert:
            alert['eventWarning']['remove'] = True
            for rule in alert['eventWarning']['rules']:
                rule['active'] = 'off'
            alert['eventWarningInput'] = alert['eventWarning']

        response = requests.post(url, json=alert, headers=headers)
        if response.status_code != 200:
            raise Exception('alerts_remove failed', response.status_code, response.reason)
        return True
        
    def alerts_add(self, stock=None, frequency=1, interval=1, priceRules=[], smartRules=[]):
        '''
        add price/percent/volume alert
        frequency: 1 is once a day, 2 is once a minute
        interval: 1 is once, 0 is repeating
        priceRules: list of dicts with below attributes per alert
            field: price , percent , volume
            type: price (above/below), percent (above/below), volume (vol in thousands)
            value: price, percent, volume amount
            remark: comment
        rules example:
        priceRules = [{'field': 'price', 'type': 'above', 'value': '900.00', 'remark': 'above'}, {'field': 'price', 'type': 'below',
             'value': '900.00', 'remark': 'below'}]
        smartRules = [{'type':'earnPre','active':'on'},{'type':'fastUp','active':'on'},{'type':'fastDown','active':'on'},
            {'type':'week52Up','active':'on'},{'type':'week52Down','active':'on'},{'type':'day5Down','active':'on'}]
        '''
        headers = self.build_req_headers()
        url = 'https://userapi.webullbroker.com/api/user/warning/v2/manage/overlap'
        
        rule_keys = ['value', 'field', 'remark', 'type', 'active']
        for line, rule in enumerate(priceRules, start=1):
            for key in rule:
                if key not in rule_keys:
                    raise Exception('malformed price alert priceRules found.')
            rule['alertRuleKey'] = line
            rule['active'] = 'on'

        alert_keys = ['earnPre', 'fastUp', 'fastDown', 'week52Up', 'week52Down', 'day5Up', 'day10Up', 'day20Up', 'day5Down', 'day10Down', 'day20Down']
        for rule in smartRules:
            if rule['type'] not in alert_keys:
                raise Exception('malformed smart alert smartRules found.')
        
        try:
            stock_data = self.get_tradable(stock)['data'][0]
            data = {'regionId': stock_data['regionId'],
                'tickerType': stock_data['type'],
                'tickerId': stock_data['tickerId'],
                'tickerSymbol': stock,
                'disSymbol': stock,
                'tinyName': stock_data['name'],
                'tickerName': stock_data['name'],
                'exchangeCode': stock_data['exchangeCode'],
                'showCode': stock_data['disExchangeCode'],
                'disExchangeCode': stock_data['disExchangeCode'],
                'eventWarningInput': {
                    'tickerId': stock_data['tickerId'],
                    'rules': smartRules,
                    'remove': False,
                    'del': False
                    },
                'warningInput': {
                    'warningFrequency': frequency,
                    'warningInterval': interval,
                    'rules': priceRules,
                    'tickerId': stock_data['tickerId']}
                }
        except Exception as e:
            print(f'failed to build alerts_add payload data. error: {e}')
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise Exception('alerts_add failed', response.status_code, response.reason)
        return True

    def get_active_gainer_loser(self, direction='gainer') :
        '''
        gets active / gainer / loser stocks sorted by change
        direction: active / gainer / loser
        '''
        headers = self.build_req_headers()

        if direction == 'gainer':
            url = 'https://securitiesapi.webullbroker.com/api/securities/market/v5/card/stockActivityPc.advanced/list'
        if direction == 'loser':
            url = 'https://securitiesapi.webullbroker.com/api/securities/market/v5/card/stockActivityPc.declined/list'
        if direction == 'active':
            url = 'https://securitiesapi.webullbroker.com/api/securities/market/v5/card/stockActivityPc.active/list'

        params = {'regionId': 6, 'userRegionId': 6}
        response = requests.get(url, params=params, headers=headers)
        result = response.json()
        result = sorted(result, key=lambda k: k['change'], reverse=True)

        return result

    '''
    lookup ticker_id
    '''
    def get_ticker(self, stock='') :
         response = requests.get('https://infoapi.webull.com/api/search/tickers5?keys=' + stock + '&queryNumber=1')
         result = response.json()

         ticker_id = 0
         if len(result['list']) == 1 :
             for item in result['list'] :
                 ticker_id = item['tickerId']
         return ticker_id

    '''
    ordering
    '''
    def place_order(self, stock='', price=0, action='BUY', orderType='LMT', enforce='GTC', quant=0):
         headers = self.build_req_headers(include_trade_token=True, include_time=True)

         data = {'action': action, #  BUY or SELL
                 'lmtPrice': float(price),
                 'orderType': orderType, # "LMT","MKT","STP","STP LMT"
                 'outsideRegularTradingHour': True,
                 'quantity': int(quant),
                 'serialId': str(uuid.uuid4()), #'f9ce2e53-31e2-4590-8d0d-f7266f2b5b4f'
                 'tickerId': self.get_ticker(stock),
                 'timeInForce': enforce} # GTC or DAY or IOC

         response = requests.post('https://tradeapi.webulltrade.com/api/trade/order/' + self.account_id + '/placeStockOrder', json=data, headers=headers)
         result = response.json()

         if result['success'] == True :
             return True
         else :
             return False

    '''
    OTOCO: One-triggers-a-one-cancels-the-others, aka Bracket Ordering
    Submit a buy order, its fill will trigger sell order placement. If one sell fills, it will cancel the other
     sell
    '''
    def place_otoco_order(self, stock='', price='', stop_loss_price='', limit_profit_price='', time_in_force='DAY',
                          quant=0):
        headers = self.build_req_headers(include_trade_token=False, include_time=True)

        data1 = {"newOrders": [
            {"orderType": "LMT", "timeInForce": time_in_force, "quantity": int(quant),
             "outsideRegularTradingHour": False, "action": "BUY", "tickerId": self.get_ticker(stock),
             "lmtPrice": float(price), "comboType": "MASTER"},
            {"orderType": "STP", "timeInForce": time_in_force, "quantity": int(quant),
             "outsideRegularTradingHour": False, "action": "SELL", "tickerId": self.get_ticker(stock),
             "auxPrice": float(stop_loss_price), "comboType": "STOP_LOSS"},
            {"orderType": "LMT", "timeInForce": time_in_force, "quantity": int(quant),
             "outsideRegularTradingHour": False, "action": "SELL", "tickerId": self.get_ticker(stock),
             "lmtPrice": float(limit_profit_price), "comboType": "STOP_PROFIT"}]}

        response1 = requests.post('https://tradeapi.webulltrade.com/api/trade/v2/corder/stock/check/' + self.account_id,
                                  json=data1, headers=headers)
        result1 = response1.json()

        if result1['forward']:
            data2 = {"newOrders": [
                {"orderType": "LMT", "timeInForce": time_in_force, "quantity": int(quant),
                 "outsideRegularTradingHour": False, "action": "BUY", "tickerId": self.get_ticker(stock),
                 "lmtPrice": float(price), "comboType": "MASTER", "serialId": str(uuid.uuid4())},
                {"orderType": "STP", "timeInForce": time_in_force, "quantity": int(quant),
                 "outsideRegularTradingHour": False, "action": "SELL", "tickerId": self.get_ticker(stock),
                 "auxPrice": float(stop_loss_price), "comboType": "STOP_LOSS", "serialId": str(uuid.uuid4())},
                {"orderType": "LMT", "timeInForce": time_in_force, "quantity": int(quant),
                 "outsideRegularTradingHour": False, "action": "SELL", "tickerId": self.get_ticker(stock),
                 "lmtPrice": float(limit_profit_price), "comboType": "STOP_PROFIT", "serialId": str(uuid.uuid4())}],
                "serialId": str(uuid.uuid4())}

            response2 = requests.post(
                'https://tradeapi.webulltrade.com/api/trade/v2/corder/stock/place/' + self.account_id,
                json=data2, headers=headers)

            print("Resp 2: {}".format(response2))
            return True
        else:
            print(result1['checkResultList'][0]['code'])
            print(result1['checkResultList'][0]['msg'])
            return False

    '''
    retract an order
    '''
    def cancel_order(self, order_id=''):
        headers = self.build_req_headers(include_trade_token=True, include_time=True)

        data = {}

        response = requests.post('https://tradeapi.webulltrade.com/api/trade/order/' + self.account_id + '/cancelStockOrder/' + str(order_id) + '/' + str(uuid.uuid4()), json=data, headers=headers)
        result = response.json()

        if result['success'] == True :
            return True
        else :
            return False

    def cancel_otoco_order(self, order_id=''):
        '''
        Retract an otoco order. Cancelling the MASTER order_id cancels the sub orders.
        '''
        headers = self.build_req_headers(include_trade_token=True, include_time=True)

        data = { "serialId": str(uuid.uuid4()), "cancelOrders": [str(order_id)]}

        response = requests.post('https://tradeapi.webulltrade.com/api/trade/v2/corder/stock/modify/' + self.account_id,
                                 json=data, headers=headers)
        return response.json()

    '''
    get price quote
    '''
    def get_quote(self, stock='') :
        response = requests.get('https://quoteapi.webull.com/api/quote/tickerRealTimes/v5/' + str(self.get_ticker(stock)))
        result = response.json()

        return result

    def get_option_quote(self, stock=None, optionId=None) :
        '''
        get option quote
        '''
        headers = self.build_req_headers()
        stock = self.get_ticker(stock)
        url = f'https://quotes-gw.webullbroker.com/api/quote/option/query/list'
        params = {'tickerId': int(stock), 'derivativeIds': int(optionId)}
        return requests.get(url, params=params, headers=headers).json()

    def get_analysis(self, stock=None) :
        '''
        get analysis info and returns a dict of analysis ratings
        '''
        url = f'https://securitiesapi.webullbroker.com/api/securities/ticker/v5/analysis/{self.get_ticker(stock)}'
        return requests.get(url).json()

    def get_financials(self, stock=None) :
        '''
        get financials info and returns a dict of financial info
        '''
        url = f'https://securitiesapi.webullbroker.com/api/securities/financial/index/{self.get_ticker(stock)}'
        return requests.get(url).json()

    def get_news(self, stock=None, Id=0, items=20) :
        '''
        get news and returns a list of articles
        params:
            Id: 0 is latest news article
            items: number of articles to return
        '''
        url = f'https://securitiesapi.webullbroker.com/api/information/news/v5/tickerNews/{self.get_ticker(stock)}'
        params = {'currentNewsId': Id, 'pageSize': items}
        return requests.get(url, params=params).json()

    def get_options_expiration_dates(self, stock=None, count=-1) :
        '''
        returns a list of options expiration dates
        '''
        url = f'https://quoteapi.webullbroker.com/api/quote/option/{self.get_ticker(stock)}/list'
        data = {'count': count}
        return requests.get(url, params=data).json()['expireDateList']

    def get_options(self, stock=None, count=-1, includeWeekly=1, direction='all', expireDate=None, queryAll=0) :
        '''
        get options and returns a dict of options contracts
        params:
            stock: symbol
            count: -1
            includeWeekly: 0 or 1
            direction: all, calls, puts
            expireDate: contract expire date
            queryAll: 0
        '''
        # get next closet expiredate if none is provided
        if not expireDate:
            dates = self.get_options_expiration_dates(stock)[0]['date']
            # ensure we don't provide an option that has < 1 day to expire
            for d in dates:
                if d['days'] > 0:
                    expireDate = d['date']
                    break

        url = f'https://quoteapi.webullbroker.com/api/quote/option/{self.get_ticker(stock)}/list'
        params = {'count': count, 'includeWeekly': includeWeekly, 'direction': direction,
            'expireDate': expireDate, 'unSymbol': stock, 'queryAll': queryAll}
        return requests.get(url, params=params).json()['data']

    def get_options_by_strike_and_expire_date(self, stock=None, expireDate=None, strike=None, direction='all') :
        """
        get a list of options contracts by expire date and strike price
        strike: string
        """
        opts = self.get_options(stock=stock, expireDate=expireDate, direction=direction)
        return [c for c in opts if c['strikePrice'] == strike]

    def place_option_order(self, optionId=None, lmtPrice=None, stpPrice=None, action=None, orderType='LMT', enforce='DAY', quant=0) :
        """
        create buy / sell order
        stock: string
        lmtPrice: float
        stpPrice: float
        action: string BUY / SELL
        optionId: string
        orderType: LMT / STP / STP LMT
        enforce: DAY
        quant: int
        """
        url = f'https://tradeapi.webulltrade.com/api/trade/v2/option/placeOrder/{self.account_id}'
        headers = self.build_req_headers(include_trade_token=True, include_time=True)

        data = {
            'orderType': orderType,
            'serialId': str(uuid.uuid4()),
            'timeInForce': enforce,
            'orders': [{'quantity': quant, 'action': action, 'tickerId': optionId, 'tickerType': 'OPTION'}],
        }

        if orderType == 'LMT' and lmtPrice:
            data['lmtPrice'] = float(lmtPrice)
        if orderType == 'STP' and stpPrice:
            data['auxPrice'] = float(stpPrice)
        if orderType == 'STP LMT' and lmtPrice and stpPrice:
            data['lmtPrice'] = float(lmtPrice)
            data['auxPrice'] = float(stpPrice)

        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise Exception('place_option_order failed', response.status_code, response.reason)
        return True

    def replace_option_order(self, order=None, lmtPrice=None, stpPrice=None, enforce=None, quant=0):
        '''
        order: dict from get_current_orders
        stpPrice: float
        lmtPrice: float
        enforce: DAY
        quant: int
        '''
        headers = self.build_req_headers(include_trade_token=True, include_time=True)

        data = {'comboId': order['comboId'],
                'orderType': order['orderType'],
                'timeInForce': enforce if enforce else order['timeInForce'],
                'serialId': str(uuid.uuid4()), 
                'orders': [{'quantity': quant if int(quant) > 0 else order['totalQuantity'],
                            'action': order['action'],
                            'tickerId': order['ticker']['tickerId'],
                            'tickerType': 'OPTION',
                            'orderId': order['orderId']}]}
        
        if order['orderType'] == 'LMT' and (lmtPrice or order['lmtPrice']):
            data['lmtPrice'] = lmtPrice if lmtPrice else order['lmtPrice']
        if order['orderType'] and (stpPrice or order['auxPrice']):
            data['auxPrice'] = stpPrice if stpPrice else order['auxPrice']
        if order['orderType'] == 'STP LMT' and (stpPrice or order['auxPrice']) and (lmtPrice or order['lmtPrice']):
            data['auxPrice'] = stpPrice if stpPrice else order['auxPrice']
            data['lmtPrice'] = lmtPrice if lmtPrice else order['lmtPrice']
    
        url = f'https://tradeapi.webulltrade.com/api/trade/v2/option/replaceOrder/{self.account_id}'
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            raise Exception('replace_option_order failed', response.status_code, response.reason)
        return True

    def get_bars(self, stock=None, interval='m1', count=1, extendTrading=0) :
        '''
        get bars returns a pandas dataframe
        params:
            interval: m1, m5, m15, m30, h1, h2, h4, d1, w1
            count: number of bars to return
            extendTrading: change to 1 for pre-market and afterhours bars
        '''
        url = f'https://quoteapi.webull.com/api/quote/tickerChartDatas/v5/{self.get_ticker(stock)}'
        params = {'type': interval, 'count': count, 'extendTrading': extendTrading}
        df = DataFrame(columns=['open', 'high', 'low', 'close', 'volume', 'vwap'])
        df.index.name = 'timestamp'
        response = requests.get(url, params=params)
        for row in response.json()[0]['data']:
            row = row.split(',')
            row = ['0' if value == 'null' else value for value in row]
            data = {'open': float(row[1]), 'high': float(row[3]), 'low': float(row[4]),
                'close': float(row[2]), 'volume': float(row[6]), 'vwap': float(row[7])}
            df.loc[datetime.fromtimestamp(int(row[0]))] = data
        return df.iloc[::-1]

    '''
    get
    '''
    def get_tradable(self, stock='') :
        response = requests.get('https://tradeapi.webulltrade.com/api/trade/ticker/broker/permissionV2?tickerId=' + str(self.get_ticker(stock)))
        result = response.json()

        return result

if __name__ == '__main__' :
    webull = webull()
    webull.login('xxxxxx@xxxx.com', 'xxxxx')
    webull.get_trade_token('xxxxxx')
    # set self.account_id first
    webull.get_account_id()
    # webull.place_order('NKTR', 21.0, 1)
    orders = webull.get_current_orders()
    for order in orders :
        # print(order)
        webull.cancel_order(order['orderId'])
    # print(webull.get_serial_id())
    # print(webull.get_ticker('BABA'))
