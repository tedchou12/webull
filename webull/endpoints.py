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
        self.base_userfintech_url = 'https://userapi.webullbroker.com/api'
        self.base_ustrade_url = 'https://ustrade.webullfinance.com/api'
        self.base_paperfintech_url = 'https://act.webullfintech.com/webull-paper-center/api'
        self.base_fintech_gw_url = 'https://quotes-gw.webullfintech.com/api'

    def account(self, account_id):
        return f'{self.base_trade_url}/v2/home/{account_id}'

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

    def bars(self, stock):
        return f'{self.base_quote_url}/quote/tickerChartDatas/v5/{stock}'

    def cancel_order(self, account_id):
        return f'{self.base_trade_url}/order/{account_id}/cancelStockOrder/'

    def modify_otoco_orders(self, account_id):
        return f'{self.base_trade_url}/v2/corder/stock/modify/{account_id}'

    def cancel_otoco_orders(self, account_id, combo_id):
        return f'{self.base_trade_url}/v2/corder/stock/cancel/{account_id}/{combo_id}'

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
        return f'{self.base_user_url}/passport/login/v5/account'

    def get_mfa(self) :
        return f'{self.base_userfintech_url}/passport/v2/verificationCode/send'

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
        return f'{self.base_paperfintech_url}/paper/1/acc/{paper_account_id}'

    def paper_account_id(self):
        return f'{self.base_paper_url}/myaccounts/true'

    def paper_cancel_order(self, paper_account_id, order_id):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/cancel/{order_id}'

    def paper_modify_order(self, paper_account_id, order_id):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/modify/{order_id}'

    def paper_place_order(self, paper_account_id, stock):
        return f'{self.base_paper_url}/paper/1/acc/{paper_account_id}/orderop/place/{stock}'

    def place_option_orders(self, account_id):
        return f'{self.base_ustrade_url}/trade/v2/option/placeOrder/{account_id}'

    def place_orders(self, account_id):
        return f'{self.base_trade_url}/order/{account_id}/placeStockOrder'

    def modify_order(self, account_id, order_id):
        return f'{self.base_trade_url}/order/{account_id}/modifyStockOrder/{order_id}'

    def place_otoco_orders(self, account_id):
        return f'{self.base_trade_url}/v2/corder/stock/place/{account_id}'

    def quotes(self, stock):
        return f'{self.base_options_gw_url}/quotes/ticker/getTickerRealTime?tickerId={stock}&includeSecu=1&includeQuote=1'

    def rankings(self):
        return f'{self.base_securities_url}/securities/market/v5/6/portal'

    def refresh_login(self):
        return f'{self.base_user_url}/passport/refreshToken?refreshToken='

    def remove_alert(self):
        return f'{self.base_userbroker_url}/user/warning/v2/manage/overlap'

    def replace_option_orders(self, account_id):
        return f'{self.base_trade_url}/v2/option/replaceOrder/{account_id}'

    def stock_id(self, stock, region_code):
        return f'{self.base_options_gw_url}/search/pc/tickers?keyword={stock}&pageIndex=1&pageSize=20&regionId={region_code}'

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

    def portfolio_lists(self):
        return f'{self.base_options_gw_url}/personal/portfolio/v2/check'
