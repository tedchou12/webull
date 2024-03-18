class urls :
    def __init__(self) :
        self.base_info_url = 'https://infoapi.webull.com/api'
        self.base_options_url = 'https://quoteapi.webullbroker.com/api'
        self.base_options_gw_url = 'https://quotes-gw.webullbroker.com/api'
        self.base_paper_url = 'https://act.webullbroker.com/webull-paper-center/api'
        self.base_quote_url = 'https://quoteapi.webullbroker.com/api'
        self.base_securities_url = 'https://securitiesapi.webullbroker.com/api'
        self.base_trade_url = 'https://tradeapi.webullbroker.com/api/trade'
        self.base_user_url = 'https://userapi.webull.com/api'
        self.base_userbroker_url = 'https://userapi.webullbroker.com/api'
        self.base_ustrade_url = 'https://ustrade.webullfinance.com/api'
        self.base_paperfintech_url = 'https://act.webullfintech.com/webull-paper-center/api'
        self.base_fintech_gw_url = 'https://quotes-gw.webullfintech.com/api'
        self.base_userfintech_url = 'https://u1suser.webullfintech.com/api'
        self.base_new_trade_url = 'https://trade.webullfintech.com/api'
        self.base_ustradebroker_url = 'https://ustrade.webullbroker.com/api'
        self.base_securitiesfintech_url = 'https://securitiesapi.webullfintech.com/api'

    def account(self, account_id):
        return f'{self.base_trade_url}/v3/home/{account_id}'

    def account_id(self):
        return f'{self.base_trade_url}/account/getSecAccountList/v5'

    def account_activities(self, account_id):
        return f'{self.base_ustrade_url}/trade/v2/funds/{account_id}/activities'

    def active_gainers_losers(self, direction, region_code, rank_type, num) :
          if direction == 'gainer' :
              url = 'topGainers'
          elif direction == 'loser' :
              url = 'dropGainers'
          else :
              url = 'topActive'
          return f'{self.base_fintech_gw_url}/wlas/ranking/{url}?regionId={region_code}&rankType={rank_type}&pageIndex=1&pageSize={num}'

    def add_alert(self):
        return f'{self.base_userbroker_url}/user/warning/v2/manage/overlap'

    def analysis(self, stock):
        return f'{self.base_securities_url}/securities/ticker/v5/analysis/{stock}'

    def analysis_shortinterest(self, stock):
        return f'{self.base_securities_url}/securities/stock/{stock}/shortInterest'

    def analysis_institutional_holding(self, stock):
        return f'{self.base_securities_url}/securities/stock/v5/{stock}/institutionalHolding'

    def analysis_etf_holding(self, stock, has_num, page_size):
        return f'{self.base_securities_url}/securities/stock/v5/{stock}/belongEtf?hasNum={has_num}&pageSize={page_size}'

    def analysis_capital_flow(self, stock, show_hist):
        return f'{self.base_securities_url}/wlas/capitalflow/ticker?tickerId={stock}&showHis={show_hist}'

    def bars(self, stock, interval='d1', count=1200, timestamp=None):
        #new
        return f'{self.base_fintech_gw_url}/quote/charts/query?tickerIds={stock}&type={interval}&count={count}&timestamp={timestamp}'
        #old
        return f'{self.base_quote_url}/quote/tickerChartDatas/v5/{stock}'

    def bars_crypto(self, stock):
        return f'{self.base_fintech_gw_url}/crypto/charts/query?tickerIds={stock}'

    def cancel_order(self, account_id):
        return f'{self.base_ustrade_url}/trade/order/{account_id}/cancelStockOrder/'

    def modify_otoco_orders(self, account_id):
        return f'{self.base_ustrade_url}/trade/v2/corder/stock/modify/{account_id}'

    def cancel_otoco_orders(self, account_id, combo_id):
        return f'{self.base_ustrade_url}/trade/v2/corder/stock/cancel/{account_id}/{combo_id}'

    def check_otoco_orders(self, account_id):
        return f'{self.base_ustrade_url}/trade/v2/corder/stock/check/{account_id}'

    def place_otoco_orders(self, account_id):
        return f'{self.base_ustrade_url}/trade/v2/corder/stock/place/{account_id}'

    def dividends(self, account_id):
        return f'{self.base_trade_url}/v2/account/{account_id}/dividends?direct=in'

    def fundamentals(self, stock):
        return f'{self.base_securities_url}/securities/financial/index/{stock}'

    def is_tradable(self, stock):
        return f'{self.base_trade_url}/ticker/broker/permissionV2?tickerId={stock}'

    def list_alerts(self):
        return f'{self.base_userbroker_url}/user/warning/v2/query/tickers'

    def login(self):
        return f'{self.base_userfintech_url}/user/v1/login/account/v2'

    def get_mfa(self):
        #return f'{self.base_userfintech_url}/user/v1/verificationCode/send/v2'
        return f'{self.base_user_url}/user/v1/verificationCode/send/v2'

    def check_mfa(self):
        return f'{self.base_userfintech_url}/user/v1/verificationCode/checkCode'

    def get_security(self, username, account_type, region_code, event, time, url=0) :
        if url == 1 :
            url = 'getPrivacyQuestion'
        else :
            url = 'getSecurityQuestion'

        return f'{self.base_user_url}/user/risk/{url}?account={username}&accountType={account_type}&regionId={region_code}&event={event}&v={time}'

    def next_security(self, username, account_type, region_code, event, time, url=0) :
        if url == 1 :
            url = 'nextPrivacyQuestion'
        else :
            url = 'nextSecurityQuestion'

        return f'{self.base_user_url}/user/risk/{url}?account={username}&accountType={account_type}&regionId={region_code}&event={event}&v={time}'

    def check_security(self) :
        return f'{self.base_user_url}/user/risk/checkAnswer'

    def logout(self):
        return f'{self.base_userfintech_url}/user/v1/logout'

    def news(self, stock, Id, items):
        return f'{self.base_fintech_gw_url}/information/news/tickerNews?tickerId={stock}&currentNewsId={Id}&pageSize={items}'

    def option_quotes(self):
        return f'{self.base_options_gw_url}/quote/option/query/list'

    def options(self, stock):
        return f'{self.base_options_url}/quote/option/{stock}/list'

    def options_exp_date(self, stock):
        return f'{self.base_options_url}/quote/option/{stock}/list'

    #new function 22/05/01
    def options_exp_dat_new(self):
        return f'{self.base_fintech_gw_url}/quote/option/strategy/list'

    def options_bars(self, derivativeId):
        return f'{self.base_options_gw_url}/quote/option/chart/query?derivativeId={derivativeId}'

    def orders(self, account_id, page_size):
        return f'{self.base_ustradebroker_url}/trade/v2/option/list?secAccountId={account_id}&dateType=ORDER&pageSize={page_size}&status='

    def history(self, account_id):
        return f'{self.base_ustrade_url}/trading/v1/webull/order/list?secAccountId={account_id}'

    def paper_orders(self, paper_account_id, page_size):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/order?&startTime=1970-0-1&dateType=ORDER&pageSize={page_size}&status='

    def paper_account(self, paper_account_id):
        return f'{self.base_paperfintech_url}/paper/1/acc/{paper_account_id}'

    def paper_account_id(self):
        return f'{self.base_paperfintech_url}/myaccounts/true'

    def paper_cancel_order(self, paper_account_id, order_id):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/cancel/{order_id}'

    def paper_modify_order(self, paper_account_id, order_id):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/modify/{order_id}'

    def paper_place_order(self, paper_account_id, stock):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/place/{stock}'

    def place_option_orders(self, account_id):
        return f'{self.base_ustrade_url}/trade/v2/option/placeOrder/{account_id}'

    def place_orders(self, account_id):
        return f'{self.base_ustrade_url}/trade/order/{account_id}/placeStockOrder'

    def modify_order(self, account_id, order_id):
        return f'{self.base_ustrade_url}/trading/v1/webull/order/stockOrderModify?secAccountId={account_id}'

    def quotes(self, stock):
        return f'{self.base_options_gw_url}/quotes/ticker/getTickerRealTime?tickerId={stock}&includeSecu=1&includeQuote=1'

    def rankings(self):
        return f'{self.base_securities_url}/securities/market/v5/6/portal'

    def refresh_login(self, refresh_token):
        return f'{self.base_user_url}/passport/refreshToken?refreshToken={refresh_token}'

    def remove_alert(self):
        return f'{self.base_userbroker_url}/user/warning/v2/manage/overlap'

    def replace_option_orders(self, account_id):
        return f'{self.base_trade_url}/v2/option/replaceOrder/{account_id}'

    def stock_detail(self, stock) :
        return f'{self.base_fintech_gw_url}/stock/tickerRealTime/getQuote?tickerId={stock}&includeSecu=1&includeQuote=1&more=1'

    def stock_id(self, stock, region_code):
        return f'{self.base_options_gw_url}/search/pc/tickers?keyword={stock}&pageIndex=1&pageSize=20&regionId={region_code}'

    def trade_token(self):
        return f'{self.base_new_trade_url}/trading/v1/global/trade/login'

    def user(self):
        return f'{self.base_user_url}/user'

    def screener(self):
        return f'{self.base_userbroker_url}/wlas/screener/ng/query'

    def social_posts(self, topic, num=100):
        return f'{self.base_user_url}/social/feed/topic/{topic}/posts?size={num}'

    def social_home(self, topic, num=100):
        return f'{self.base_user_url}/social/feed/topic/{topic}/home?size={num}'

    def portfolio_lists(self):
        return f'{self.base_options_gw_url}/personal/portfolio/v2/check'

    def press_releases(self, stock, typeIds=None, num=50):
        typeIdsString = ''
        if typeIds is not None:
            typeIdsString = '&typeIds=' + typeIds
        return f'{self.base_securitiesfintech_url}/securities/announcement/{stock}/list?lastAnnouncementId=0&limit={num}{typeIdsString}&options=2'

    def calendar_events(self, event, region_code, start_date, page=1, num=50):
        return f'{self.base_fintech_gw_url}/bgw/explore/calendar/{event}?regionId={region_code}&pageIndex={page}&pageSize={num}&startDate={start_date}'

    def get_all_tickers(self, region_code, user_region_code) :
        return f'{self.base_securitiesfintech_url}/securities/market/v5/card/stockActivityPc.advanced/list?regionId={region_code}&userRegionId={user_region_code}&hasNum=0&pageSize=9999'
