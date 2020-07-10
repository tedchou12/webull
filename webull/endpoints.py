class urls :
    def __init__(self) :
        self.base_info_url = 'https://infoapi.webull.com/api'
        self.base_options_url = 'https://quoteapi.webullbroker.com/api'
        self.base_options_gw_url = 'https://quotes-gw.webullbroker.com/api'
        self.base_paper_url = 'https://act.webullbroker.com/webull-paper-center/api'
        self.base_quote_url = 'https://quoteapi.webullbroker.com/api'
        self.base_securities_url = 'https://securitiesapi.webullbroker.com/api'
        self.base_trade_url = 'https://tradeapi.webulltrade.com/api/trade'
        self.base_user_url = 'https://userapi.webull.com/api'
        self.base_userbroker_url = 'https://userapi.webullbroker.com/api'

    def account(self, account_id):
        return f'{self.base_trade_url}/v2/home/{account_id}'

    def account_id(self):
        return f'{self.base_trade_url}/account/getSecAccountList/v4'

    def active_gainers_losers(self, direction):
        if direction == 'gainer':
            url = 'advanced'
        elif direction == 'loser':
            url = 'declined'
        else:
            url = 'active'
        return f'{self.base_securities_url}/securities/market/v5/card/stockActivityPc.{url}/list'

    def add_alert(self):
        return f'{self.base_userbroker_url}/user/warning/v2/manage/overlap'

    def analysis(self, stock):
        return f'{self.base_securities_url}/securities/ticker/v5/analysis/{stock}'

    def bars(self, stock):
        return f'{self.base_quote_url}/quote/tickerChartDatas/v5/{stock}'

    def cancel_order(self, account_id):
        return f'{self.base_trade_url}/order/{account_id}/cancelStockOrder/'

    def cancel_otoco_orders(self, account_id):
        return f'{self.base_trade_url}/v2/corder/stock/modify/{account_id}'

    def check_otoco_orders(self, account_id):
        return f'{self.base_trade_url}/v2/corder/stock/check/{account_id}'

    def dividends(self, account_id):
        return f'{self.base_trade_url}/v2/account/{account_id}/dividends?direct=in'

    def fundamentals(self, stock):
        return f'{self.base_securities_url}/securities/financial/index/{stock}'

    def is_tradable(self, stock):
        return f'{self.base_trade_url}/ticker/broker/permissionV2?tickerId={stock}'

    def list_alerts(self):
        return f'{self.base_userbroker_url}/user/warning/v2/query/tickers'

    def login(self):
        return f'{self.base_user_url}/passport/login/v3/account'

    def get_mfa(self, account, account_type, device_id, code_type, region_code):
        return f'{self.base_user_url}/passport/verificationCode/sendCode?account={account}&accountType={account_type}&deviceId={device_id}&codeType={code_type}&regionCode={region_code}'

    def logout(self):
        return f'{self.base_userbroker_url}/passport/login/logout'

    def news(self, stock):
        return f'{self.base_securities_url}/information/news/v5/tickerNews/{stock}'

    def option_quotes(self):
        return f'{self.base_options_gw_url}/quote/option/query/list'

    def options(self, stock):
        return f'{self.base_options_url}/quote/option/{stock}/list'

    def options_exp_date(self, stock):
        return f'{self.base_options_url}/quote/option/{stock}/list'

    def orders(self, account_id, page_size):
        return f'{self.base_trade_url}/v2/option/list?secAccountId={account_id}&startTime=1970-0-1&dateType=ORDER&pageSize={page_size}&status='

    def paper_orders(self, paper_account_id, page_size):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/order?&startTime=1970-0-1&dateType=ORDER&pageSize={page_size}&status='

    def paper_account(self, paper_account_id):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}'

    def paper_account_id(self):
        return f'{self.base_paper_url}/myaccounts/true'

    def paper_cancel_order(self, paper_account_id, order_id):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/cancel/{order_id}'

    def paper_modify_order(self, paper_account_id, order_id):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/modify/{order_id}'

    def paper_place_order(self, paper_account_id, stock):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/place/{stock}'

    def place_option_orders(self, account_id):
        return f'{self.base_trade_url}/v2/option/placeOrder/{account_id}'

    def place_orders(self, account_id):
        return f'{self.base_trade_url}/order/{account_id}/placeStockOrder'

    def modify_order(self, account_id, order_id):
        return f'{self.base_trade_url}/order/{account_id}/modifyStockOrder/{order_id}'

    def place_otoco_orders(self, account_id):
        return f'{self.base_trade_url}/v2/corder/stock/place/{account_id}'

    def quotes(self, stock):
        return f'{self.base_quote_url}/quote/tickerRealTimes/v5/{stock}'

    def rankings(self):
        return f'{self.base_securities_url}/securities/market/v5/6/portal'

    def refresh_login(self):
        return f'{self.base_user_url}/passport/refreshToken?refreshToken='

    def remove_alert(self):
        return f'{self.base_userbroker_url}/user/warning/v2/manage/overlap'

    def replace_option_orders(self, account_id):
        return f'{self.base_trade_url}/v2/option/replaceOrder/{account_id}'

    def stock_id(self, stock):
        return f'{self.base_options_gw_url}/search/pc/tickers?keyword={stock}&pageIndex=1&pageSize=1'

    def trade_token(self):
        return f'{self.base_trade_url}/login'

    def user(self):
        return f'{self.base_user_url}/user'

    def screener(self):
        return f'{self.base_userbroker_url}/wlas/screener/ng/query'

    def social_posts(self, topic, num=100):
        return f'{self.base_user_url}/social/feed/topic/{topic}/posts?size={num}'

    def social_home(self, topic, num=100):
        return f'{self.base_user_url}/social/feed/topic/{topic}/home?size={num}'