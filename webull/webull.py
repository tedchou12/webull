import argparse
import collections
import getpass
import hashlib
import json
import os
import pickle
import requests
import time
import uuid

from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from pandas import DataFrame, to_datetime
from pytz import timezone

from . import endpoints


class webull:

    def __init__(self):
        self._session = requests.session()
        self._headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json',
        }
        self._access_token = ''
        self._account_id = ''
        self._refresh_token = ''
        self._token_expire = ''
        self._trade_token = ''
        self._uuid = ''
        self._did = self._get_did()
        self._urls = endpoints.urls()

    def _get_did(self):
        '''
        Makes a unique device id from a random uuid (uuid.uuid4).
        if the pickle file doesn't exist, this func will generate a random 32 character hex string
        uuid and save it in a pickle file for future use. if the file already exists it will
        load the pickle file to reuse the did. Having a unique did appears to be very important
        for the MQTT web socket protocol
        :return: hex string of a 32 digit uuid
        '''
        filename = 'did.bin'
        if os.path.exists(filename):
            did = pickle.load(open(filename,'rb'))
        else:
            did = uuid.uuid4().hex
            pickle.dump(did, open(filename, 'wb'))
        return did


    def build_req_headers(self, include_trade_token=False, include_time=False):
        '''
        Build default set of header params
        '''
        headers = self._headers
        headers['did'] = self._did
        headers['access_token'] = self._access_token
        if include_trade_token:
            headers['t_token'] = self._trade_token
        if include_time:
            headers['t_time'] = str(round(time.time() * 1000))
        return headers


    def login(self, username='', password='', device_name='', mfa=''):
        '''
        Login with email or phone number

        phone numbers must be a str in the following form
        US '+1-XXXXXXX'
        CH '+86-XXXXXXXXXXX'
        '''

        if not username or not password:
            raise ValueError('username or password is empty')

        # with webull md5 hash salted
        password = ('wl_app-a&b@!423^' + password).encode('utf-8')
        md5_hash = hashlib.md5(password)

        try:
          validate_email(username)
          accountType = 2 # email
        except EmailNotValidError as _e:
          accountType = 1 # phone

        if device_name == '' :
            device_name = 'default_string'

        data = {
            'account': username,
            'accountType': accountType,
            'deviceId': self._did,
            'deviceName': device_name,
            'grade': 1,
            'pwd': md5_hash.hexdigest(),
            'regionId': 1
        }

        if mfa != '' :
            data['extInfo'] = {'verificationCode': mfa}
            headers = self.build_req_headers()
        else :
            headers = self._headers
        response = requests.post(self._urls.login(), json=data, headers=headers)
        result = response.json()
        if 'accessToken' in result :
            self._access_token = result['accessToken']
            self._refresh_token = result['refreshToken']
            self._token_expire = result['tokenExpireTime']
            self._uuid = result['uuid']
            self._account_id = self.get_account_id()
        return result

    def get_mfa(self, username):
        try:
          validate_email(username)
          accountType = 2 # email
        except EmailNotValidError as _e:
          accountType = 1 # phone

        response = requests.get(self._urls.get_mfa(username, str(accountType), str(self._did), str(5), str(1)), headers=self._headers)


    def login_prompt(self):
        '''
        End login session
        '''
        uname = input('Enter Webull Username:')
        pwd = getpass.getpass('Enter Webull Password:')
        self.trade_pin = getpass.getpass('Enter 6 digit Webull Trade PIN:')
        self.login(uname, pwd)
        return self.get_trade_token(self.trade_pin)

    def logout(self):
        '''
        End login session
        '''
        headers = self.build_req_headers()
        response = requests.get(self._urls.logout(), headers=headers)
        return response.status_code

    def refresh_login(self):
        '''
        Refresh login token
        '''
        headers = self.build_req_headers()
        data = {'refreshToken': self._refresh_token}

        response = requests.post(self._urls.refresh_login() + self._refresh_token, json=data, headers=headers)
        result = response.json()
        if 'accessToken' in result and result['accessToken'] != '' and result['refreshToken'] != '' and result['tokenExpireTime'] != '':
            self._access_token = result['accessToken']
            self._refresh_token = result['refreshToken']
            self._token_expire = result['tokenExpireTime']
        return result


    def get_detail(self):
        '''
        get some contact details of your account name, email/phone, region, avatar...etc
        '''
        headers = self.build_req_headers()

        response = requests.get(self._urls.user(), headers=headers)
        result = response.json()

        return result


    def get_account_id(self):
        '''
        get account id
        call account id before trade actions
        '''
        headers = self.build_req_headers()

        response = requests.get(self._urls.account_id(), headers=headers)
        result = response.json()
        if result['success']:
            id = str(result['data'][0]['secAccountId'])
            return id
        else:
            return None


    def get_account(self):
        '''
        get important details of account, positions, portfolio stance...etc
        '''
        headers = self.build_req_headers()
        response = requests.get(self._urls.account(self._account_id), headers=headers)
        result = response.json()
        return result


    def get_positions(self):
        '''
        output standing positions of stocks
        '''
        data = self.get_account()
        return data['positions']


    def get_portfolio(self):
        '''
        output numbers of portfolio
        '''
        data = self.get_account()
        output = {}
        for item in data['accountMembers']:
            output[item['key']] = item['value']
        return output


    def get_current_orders(self):
        '''
        Get open/standing orders
        '''
        data = self.get_account()
        return data['openOrders']


    def get_history_orders(self, status='Cancelled', count=20):
        '''
        Historical orders, can be cancelled or filled
        status = Cancelled / Filled / Working / Partially Filled / Pending / Failed / All
        '''
        headers = self.build_req_headers(include_trade_token=True, include_time=True)
        response = requests.get(self._urls.orders(self._account_id, count) + str(status), headers=headers)
        return response.json()


    def get_trade_token(self, password=''):
        '''
        Trading related
        authorize trade, must be done before trade action
        '''
        headers = self.build_req_headers()

        # with webull md5 hash salted
        password = ('wl_app-a&b@!423^' + password).encode('utf-8')
        md5_hash = hashlib.md5(password)
        data = {'pwd': md5_hash.hexdigest()}

        response = requests.post(self._urls.trade_token(), json=data, headers=headers)
        result = response.json()
        if result['success']:
            self._trade_token = result['data']['tradeToken']
            return True
        else:
            return False


    def get_ticker(self, stock=''):
        '''
        Lookup ticker_id
        '''
        ticker_id = 0
        if stock and isinstance(stock, str):
            response = requests.get(self._urls.stock_id(stock))
            result = response.json()
            if result.get('data'):
                for item in result['data']: # implies multiple tickers, but only assigns last one?
                    ticker_id = item['tickerId']
            else:
                raise ValueError('TickerId could not be found for stock {}'.format(stock))
        else:
            raise ValueError('Stock symbol is required')
        return ticker_id


    def place_order(self, stock=None, tId=None, price=0, action='BUY',
            orderType='LMT', enforce='GTC', qty=0, outsideRegularTradingHour=True):
        '''
        Place an order

        action: BUY / SELL
        ordertype : LMT / MKT / STP / STP LMT
        timeinforce:  GTC / DAY / IOC
        outsideRegularTradingHour: True / False
        '''
        if not tId is None:
            pass
        elif not stock is None:
            tId = self.get_ticker(stock)
        else:
            raise ValueError('Must provide a stock symbol or a stock id')

        headers = self.build_req_headers(include_trade_token=True, include_time=True)
        data = {
            'action': action,
            'lmtPrice': float(price),
            'orderType': orderType,
            'outsideRegularTradingHour': outsideRegularTradingHour,
            'quantity': int(qty),
            'serialId': str(uuid.uuid4()),
            'tickerId': tId,
            'timeInForce': enforce
        }

        # Market orders do not support extended hours trading.
        if orderType == 'MKT':
            data['outsideRegularTradingHour'] = False

        response = requests.post(self._urls.place_orders(self._account_id), json=data, headers=headers)
        return response.json()


    def modify_order(self, order=None, price=0, action=None, orderType=None, enforce=None, quant=0, outsideRegularTradingHour=None):
        '''
        Modify an order

        action: BUY / SELL
        ordertype : LMT / MKT / STP / STP LMT
        timeinforce:  GTC / DAY / IOC
        outsideRegularTradingHour: True / False
        '''
        if not order:
            raise ValueError('Must provide an order')

        headers = self.build_req_headers(include_trade_token=True, include_time=True)

        modifiedAction = action or order['action']
        modifiedLmtPrice = float(price or order['lmtPrice'])
        modifiedOrderType = orderType or order['orderType']
        modifiedOutsideRegularTradingHour = outsideRegularTradingHour if type(outsideRegularTradingHour) == bool else order['outsideRegularTradingHour']
        modifiedEnforce = enforce or order['timeInForce']
        modifiedQuant = int(quant or order['quantity'])

        data = {
            'action': modifiedAction,
            'lmtPrice': modifiedLmtPrice,
            'orderType': modifiedOrderType,
            'quantity': modifiedQuant,
            'comboType': 'NORMAL',
            'outsideRegularTradingHour': modifiedOutsideRegularTradingHour,
            'serialId': str(uuid.uuid4()),
            'tickerId': order['ticker']['tickerId'],
            'timeInForce': modifiedEnforce
        }
        #Market orders do not support extended hours trading.
        if data['orderType'] == 'MKT':
            data['outsideRegularTradingHour'] = False

        response = requests.put(self._urls.modify_order(self._account_id, order['orderId']), json=data, headers=headers)

        return response.json()


    def place_otoco_order(self, stock='', price='', stop_loss_price='', limit_profit_price='',
        time_in_force='DAY', quant=0):
        '''
        OTOCO: One-triggers-a-one-cancels-the-others, aka Bracket Ordering
        Submit a buy order, its fill will trigger sell order placement. If one sell fills, it will cancel the other
         sell
        '''
        headers = self.build_req_headers(include_trade_token=False, include_time=True)
        data1 = {
            'newOrders': [
                {'orderType': 'LMT', 'timeInForce': time_in_force, 'quantity': int(quant),
                 'outsideRegularTradingHour': False, 'action': 'BUY', 'tickerId': self.get_ticker(stock),
                 'lmtPrice': float(price), 'comboType': 'MASTER'},
                {'orderType': 'STP', 'timeInForce': time_in_force, 'quantity': int(quant),
                 'outsideRegularTradingHour': False, 'action': 'SELL', 'tickerId': self.get_ticker(stock),
                 'auxPrice': float(stop_loss_price), 'comboType': 'STOP_LOSS'},
                {'orderType': 'LMT', 'timeInForce': time_in_force, 'quantity': int(quant),
                 'outsideRegularTradingHour': False, 'action': 'SELL', 'tickerId': self.get_ticker(stock),
                 'lmtPrice': float(limit_profit_price), 'comboType': 'STOP_PROFIT'}
            ]
        }

        response1 = requests.post(self._urls.check_otoco_orders(self._account_id), json=data1, headers=headers)
        result1 = response1.json()

        if result1['forward']:
            data2 = {
                'newOrders': [
                    {'orderType': 'LMT', 'timeInForce': time_in_force, 'quantity': int(quant),
                     'outsideRegularTradingHour': False, 'action': 'BUY', 'tickerId': self.get_ticker(stock),
                     'lmtPrice': float(price), 'comboType': 'MASTER', 'serialId': str(uuid.uuid4())},
                    {'orderType': 'STP', 'timeInForce': time_in_force, 'quantity': int(quant),
                     'outsideRegularTradingHour': False, 'action': 'SELL', 'tickerId': self.get_ticker(stock),
                     'auxPrice': float(stop_loss_price), 'comboType': 'STOP_LOSS', 'serialId': str(uuid.uuid4())},
                    {'orderType': 'LMT', 'timeInForce': time_in_force, 'quantity': int(quant),
                     'outsideRegularTradingHour': False, 'action': 'SELL', 'tickerId': self.get_ticker(stock),
                     'lmtPrice': float(limit_profit_price), 'comboType': 'STOP_PROFIT', 'serialId': str(uuid.uuid4())}],
                    'serialId': str(uuid.uuid4())
                }

            response2 = requests.post(self._urls.place_otoco_orders(self._account_id), json=data2, headers=headers)

            print('Resp 2: {}'.format(response2))
            return True
        else:
            print(result1['checkResultList'][0]['code'])
            print(result1['checkResultList'][0]['msg'])
            return False


    def cancel_order(self, order_id=''):
        '''
        Cancel an order
        '''
        headers = self.build_req_headers(include_trade_token=True, include_time=True)
        data = {}
        response = requests.post(self._urls.cancel_order(self._account_id) + str(order_id) + '/' + str(uuid.uuid4()), json=data, headers=headers)
        result = response.json()
        return result['success']


    def cancel_all_orders(self):
        '''
        Cancels all open (aka 'working') orders
        '''
        open_orders = self.get_current_orders()
        for order in open_orders:
            self.cancel_order(order['orderId'])

    def cancel_otoco_order(self, order_id=''):
        '''
        Retract an otoco order. Cancelling the MASTER order_id cancels the sub orders.
        '''
        headers = self.build_req_headers(include_trade_token=True, include_time=True)
        data = { 'serialId': str(uuid.uuid4()), 'cancelOrders': [str(order_id)]}
        response = requests.post(self._urls.cancel_otoco_orders(self._account_id), json=data, headers=headers)
        return response.json()

    def get_quote(self, stock=None, tId=None) :
        '''
        get price quote
        tId: ticker ID str
        '''
        if not stock and not tId:
            raise ValueError('Must provide a stock symbol or a stock id')

        if stock:
            try:
                tId = str(self.get_ticker(stock))
            except ValueError as _e:
                raise ValueError("Could not find ticker for stock {}".format(stock))
        response = requests.get(self._urls.quotes(tId))
        result = response.json()
        return result

    def get_option_quote(self, stock=None, tId=None, optionId=None):
        '''
        get option quote
        '''
        if not stock and not tId:
            raise ValueError('Must provide a stock symbol or a stock id')

        if stock:
            try:
                tId = str(self.get_ticker(stock))
            except ValueError as _e:
                raise ValueError("Could not find ticker for stock {}".format(stock))
        headers = self.build_req_headers()
        params = {'tickerId': tId, 'derivativeIds': optionId}
        return requests.get(self._urls.option_quotes(), params=params, headers=headers).json()

    def get_options_expiration_dates(self, stock=None, count=-1):
        '''
        returns a list of options expiration dates
        '''
        data = {'count': count}
        return requests.get(self._urls.options_exp_date(self.get_ticker(stock)), params=data).json()['expireDateList']

    def get_options(self, stock=None, count=-1, includeWeekly=1, direction='all', expireDate=None, queryAll=0):
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

        params = {'count': count, 'includeWeekly': includeWeekly, 'direction': direction,
                'expireDate': expireDate, 'unSymbol': stock, 'queryAll': queryAll}
        return requests.get(self._urls.options(self.get_ticker(stock)), params=params).json()['data']

    def get_options_by_strike_and_expire_date(self, stock=None, expireDate=None, strike=None, direction='all'):
        '''
        get a list of options contracts by expire date and strike price
        strike: string
        '''
        opts = self.get_options(stock=stock, expireDate=expireDate, direction=direction)
        return [c for c in opts if c['strikePrice'] == strike]

    def place_option_order(self, optionId=None, lmtPrice=None, stpPrice=None, action=None, orderType='LMT', enforce='DAY', quant=0):
        '''
        create buy / sell order
        stock: string
        lmtPrice: float
        stpPrice: float
        action: string BUY / SELL
        optionId: string
        orderType: LMT / STP / STP LMT
        enforce: DAY
        quant: int
        '''
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

        response = requests.post(self._urls.place_option_orders(self._account_id), json=data, headers=headers)
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
        data = {
            'comboId': order['comboId'],
            'orderType': order['orderType'],
            'timeInForce': enforce or order['timeInForce'],
            'serialId': str(uuid.uuid4()),
            'orders': [{'quantity': quant or order['totalQuantity'],
                        'action': order['action'],
                        'tickerId': order['ticker']['tickerId'],
                        'tickerType': 'OPTION',
                        'orderId': order['orderId']}]
        }

        if order['orderType'] == 'LMT' and (lmtPrice or order['lmtPrice']):
            data['lmtPrice'] = lmtPrice or order['lmtPrice']
        if order['orderType'] and (stpPrice or order['auxPrice']):
            data['auxPrice'] = stpPrice or order['auxPrice']
        if order['orderType'] == 'STP LMT' and (stpPrice or order['auxPrice']) and (lmtPrice or order['lmtPrice']):
            data['auxPrice'] = stpPrice or order['auxPrice']
            data['lmtPrice'] = lmtPrice or order['lmtPrice']

        response = requests.post(self._urls.replace_option_orders(self._account_id), json=data, headers=headers)
        if response.status_code != 200:
            raise Exception('replace_option_order failed', response.status_code, response.reason)
        return True


    def get_tradable(self, stock=''):
        '''
        get if stock is tradable
        '''
        response = requests.get(self._urls.is_tradable(self.get_ticker(stock)))
        return response.json()


    def alerts_list(self):
        '''
        Get alerts
        '''
        headers = self.build_req_headers()

        response = requests.get(self._urls.list_alerts(), headers=headers)
        result = response.json()
        return result.get('data', [])

    def alerts_remove(self, alert=None, priceAlert=True, smartAlert=True):
        '''
        remove alert
        alert is retrieved from alert_list
        '''
        headers = self.build_req_headers()

        if alert.get('tickerWarning') and priceAlert:
            alert['tickerWarning']['remove'] = True
            alert['warningInput'] = alert['tickerWarning']

        if alert.get('eventWarning') and smartAlert:
            alert['eventWarning']['remove'] = True
            for rule in alert['eventWarning']['rules']:
                rule['active'] = 'off'
            alert['eventWarningInput'] = alert['eventWarning']

        response = requests.post(self._urls.remove_alert(), json=alert, headers=headers)
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
            data = {
                'regionId': stock_data['regionId'],
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
                    'tickerId': stock_data['tickerId']
                }
            }
        except Exception as e:
            print(f'failed to build alerts_add payload data. error: {e}')

        response = requests.post(self._urls.add_alert(), json=data, headers=headers)
        if response.status_code != 200:
            raise Exception('alerts_add failed', response.status_code, response.reason)
        return True

    def get_active_gainer_loser(self, direction='gainer', count=20):
        '''
        gets active / gainer / loser stocks sorted by change
        direction: active / gainer / loser
        '''
        headers = self.build_req_headers()

        params = {'regionId': 6, 'userRegionId': 6, 'pageSize': count}
        response = requests.get(self._urls.active_gainers_losers(direction), params=params, headers=headers)
        result = response.json()
        result = sorted(result, key=lambda k: k['change'], reverse=True)
        return result


    def run_screener(self, region=None, price_lte=None, price_gte=None, pct_chg_gte=None, pct_chg_lte=None, sort=None,
                     sort_dir=None, vol_lte=None, vol_gte=None):
        '''
        Notice the fact that endpoints are reversed on lte and gte, but this function makes it work correctly
        Also screeners are not sent by name, just the parameters are sent
        example: run_screener( price_lte=.10, price_gte=5, pct_chg_lte=.035, pct_chg_gte=.51)
        just a start, add more as you need it
        '''

        jdict = collections.defaultdict(dict)
        jdict['fetch'] = 200
        jdict['rules'] = collections.defaultdict(str)
        jdict['sort'] = collections.defaultdict(str)
        jdict['attach'] = {'hkexPrivilege': 'true'}  #unknown meaning, was in network trace

        jdict['rules']['wlas.screener.rule.region'] = 'securities.region.name.6'
        if not price_lte is None and not price_gte is None:
            # lte and gte are backwards
            jdict['rules']['wlas.screener.rule.price'] = 'gte=' + str(price_lte) + '&lte=' + str(price_gte)

        if not vol_lte is None and not vol_gte is None:
            # lte and gte are backwards
            jdict['rules']['wlas.screener.rule.volume'] = 'gte=' + str(vol_lte) + '&lte=' + str(vol_gte)

        if not pct_chg_lte is None and not pct_chg_gte is None:
            # lte and gte are backwards
            jdict['rules']['wlas.screener.rule.changeRatio'] = 'gte=' + str(pct_chg_lte) + '&lte=' + str(pct_chg_gte)

        if sort is None:
            jdict['sort']['rule'] = 'wlas.screener.rule.price'
        if sort_dir is None:
            jdict['sort']['desc'] = 'true'

        # jdict = self._ddict2dict(jdict)
        response = requests.post(self._urls.screener(), json=jdict)
        result = response.json()
        return result

    def get_analysis(self, stock=None):
        '''
        get analysis info and returns a dict of analysis ratings
        '''
        return requests.get(self._urls.analysis(self.get_ticker(stock))).json()

    def get_financials(self, stock=None):
        '''
        get financials info and returns a dict of financial info
        '''
        return requests.get(self._urls.fundamentals(self.get_ticker(stock))).json()

    def get_news(self, stock=None, Id=0, items=20):
        '''
        get news and returns a list of articles
        params:
            Id: 0 is latest news article
            items: number of articles to return
        '''
        params = {'currentNewsId': Id, 'pageSize': items}
        return requests.get(self._urls.news(self.get_ticker(stock)), params=params).json()

    def get_bars(self, stock=None, tId = None, interval='m1', count=1, extendTrading=0, timeStamp=None):
        '''
        get bars returns a pandas dataframe
        params:
            interval: m1, m5, m15, m30, h1, h2, h4, d1, w1
            count: number of bars to return
            extendTrading: change to 1 for pre-market and afterhours bars
            timeStamp: If epoc timestamp is provided, return bar count up to timestamp. If not set default to current time.
        '''
        if not tId is None:
            pass
        elif not stock is None:
            tId = self.get_ticker(stock)
        else:
            raise ValueError('Must provide a stock symbol or a stock id')

        params = {'type': interval, 'count': count, 'extendTrading': extendTrading, 'timestamp': timeStamp}
        df = DataFrame(columns=['open', 'high', 'low', 'close', 'volume', 'vwap'])
        df.index.name = 'timestamp'
        response = requests.get(self._urls.bars(tId), params=params)
        result = response.json()
        time_zone = timezone(result[0]['timeZone'])
        for row in result[0]['data']:
            row = row.split(',')
            row = ['0' if value == 'null' else value for value in row]
            data = {
                'open': float(row[1]),
                'high': float(row[3]),
                'low': float(row[4]),
                'close': float(row[2]),
                'volume': float(row[6]),
                'vwap': float(row[7])
            }
            #convert to a panda datetime64 which has extra features like floor and resample
            df.loc[to_datetime(datetime.fromtimestamp(int(row[0])).astimezone(time_zone))] = data
        return df.iloc[::-1]

    def get_calendar(self,stock=None, tId=None):
        '''
        There doesn't seem to be a way to get the times the market is open outside of the charts.
        So, best way to tell if the market is open is to pass in a popular stock like AAPL then
        and see the open and close hours as would be marked on the chart
        and see if the last trade date is the same day as today's date
        :param stock:
        :param tId:
        :return: dict of 'market open', 'market close', 'last trade date'
        '''
        if not tId is None:
            pass
        elif not stock is None:
            tId = self.get_ticker(stock)
        else:
            raise ValueError('Must provide a stock symbol or a stock id')

        params = {'type': 'm1', 'count': 1, 'extendTrading': 0}
        response = requests.get(self._urls.bars(tId), params=params)
        result = response.json()
        time_zone = timezone(result[0]['timeZone'])
        last_trade_date = datetime.fromtimestamp(int(result[0]['data'][0].split(',')[0])).astimezone(time_zone)
        today = datetime.today().astimezone()  #use no time zone to have it pull in local time zone

        if last_trade_date.date() < today.date():
            # don't know what today's open and close times are, since no trade for today yet
            return {'market open': None, 'market close': None, 'trading day': False}

        for d in result[0]['dates']:
            if d['type'] == 'T':
                market_open = today.replace(
                    hour=int(d['start'].split(':')[0]),
                    minute=int(d['start'].split(':')[1]),
                    second=0)
                market_open -= timedelta(microseconds=market_open.microsecond)
                market_open = market_open.astimezone(time_zone)  #set to market timezone

                market_close = today.replace(
                    hour=int(d['end'].split(':')[0]),
                    minute=int(d['end'].split(':')[1]),
                    second=0)
                market_close -= timedelta(microseconds=market_close.microsecond)
                market_close = market_close.astimezone(time_zone) #set to market timezone

                #this implies that we have waited a few minutes from the open before trading
                return {'market open': market_open ,  'market close':market_close, 'trading day':True}
        #otherwise
        return None

    def get_dividends(self):
        ''' Return account's dividend info '''
        headers = self.build_req_headers()
        data = {}
        response = requests.post(self._urls.dividends(self._account_id), json=data, headers=headers)
        return response.json()

    def get_five_min_ranking(self, extendTrading=0):
        '''
        get 5 minute trend ranking
        '''
        rank = []
        headers = self.build_req_headers()
        params = {'regionId': 6, 'userRegionId': 6, 'platform': 'pc', 'limitCards': 'latestActivityPc'}
        response = requests.get(self._urls.rankings(), params=params, headers=headers)
        result = response.json()[0].get('data')
        if extendTrading:
            for data in result:
                if data['id'] == 'latestActivityPc.faList':
                    rank = data['data']
        else:
            for data in result:
                if data['id'] == 'latestActivityPc.5minutes':
                    rank = data['data']
        return rank



''' Paper support '''
class paper_webull(webull):

    def __init__(self):
        super().__init__()

    def get_account(self):
        ''' Get important details of paper account '''
        headers = self.build_req_headers()
        response = requests.get(self._urls.paper_account(self._account_id), headers=headers)
        return response.json()

    def get_account_id(self):
        ''' Get paper account id: call this before paper account actions'''
        headers = self.build_req_headers()
        response = requests.get(self._urls.paper_account_id(), headers=headers)
        result = response.json()
        id = result[0]['id']
        return id

    def get_current_orders(self):
        ''' Open paper trading orders '''
        return self.get_account()['openOrders']

    def get_history_orders(self, status='Cancelled', count=20):
        headers = self.build_req_headers(include_trade_token=True, include_time=True)
        response = requests.get(self._urls.paper_orders(self._account_id, count) + str(status), headers=headers)
        return response.json()

    def get_positions(self):
        ''' Current positions in paper trading account. '''
        return self.get_account()['positions']

    def place_order(self, stock=None, tId=None, price=0, action='BUY', orderType='LMT', enforce='GTC', quant=0):
        ''' Place a paper account order. '''
        if not tId is None:
            pass
        elif not stock is None:
            tId = self.get_ticker(stock)
        else:
            raise ValueError('Must provide a stock symbol or a stock id')

        headers = self.build_req_headers(include_trade_token=True, include_time=True)

        data = {
            'action': action, #  BUY or SELL
            'lmtPrice': float(price),
            'orderType': orderType, # 'LMT','MKT'
            'outsideRegularTradingHour': True,
            'quantity': int(quant),
            'serialId': str(uuid.uuid4()),
            'tickerId': tId,
            'timeInForce': enforce  # GTC or DAY
        }

        #Market orders do not support extended hours trading.
        if orderType == 'MKT':
            data['outsideRegularTradingHour'] = False

        response = requests.post(self._urls.paper_place_order(self._account_id, tId), json=data, headers=headers)
        return response.json()

    def modify_order(self, order, price=0, action='BUY', orderType='LMT', enforce='GTC', quant=0):
        ''' Modify a paper account order. '''
        headers = self.build_req_headers()

        data = {
            'action': action, #  BUY or SELL
            'lmtPrice': float(price),
            'orderType':orderType,
            'comboType': 'NORMAL', # 'LMT','MKT'
            'outsideRegularTradingHour': True,
            'serialId': str(uuid.uuid4()),
            'tickerId': order['ticker']['tickerId'],
            'timeInForce': enforce # GTC or DAY
        }

        if quant == 0 or quant == order['totalQuantity']:
            data['quantity'] = order['totalQuantity']
        else:
            data['quantity'] = int(quant)

        response = requests.post(self._urls.paper_modify_order(self._account_id, order['orderId']), json=data,
                                 headers=headers)
        if response:
            return True
        else:
            print("Modify didn't succeed. {} {}".format(response, response.json()))
            return False

    def cancel_order(self, order_id):
        ''' Cancel a paper account order. '''
        headers = self.build_req_headers()
        response = requests.post(self._urls.paper_cancel_order(self._account_id, order_id),
                                 headers=headers)
        return bool(response)

    def get_social_posts(self, topic, num=100):
        headers = self.build_req_headers()

        response = requests.get(self._urls.social_posts(topic, num), headers=headers)
        result = response.json()
        return result


    def get_social_home(self, topic, num=100):
        headers = self.build_req_headers()

        response = requests.get(self._urls.social_home(topic, num), headers=headers)
        result = response.json()
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Interface with Webull. Paper trading is not the default.')
    parser.add_argument('-p', '--use-paper', help='Use paper account instead.', action='store_true')
    args = parser.parse_args()

    if args.use_paper:
        wb = paper_webull()
    else:
        wb = webull()
