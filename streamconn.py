import paho.mqtt.client as mqtt
import threading
import json
from webull import webull

class StreamConn:
    def __init__(self, debug_flg=False):
        self.onsub_lock = threading.RLock()
        self.oncon_lock = threading.RLock()
        self.onmsg_lock = threading.RLock()
        self.price_func = None
        self.order_func = None
        self.debug_flg = debug_flg
        self.total_volume={}
        self.client_order_upd = None
        self.client_streaming_quotes = None


    """
    ====Order status from platpush====
    topic _______: messageId, action, type, title, messageHeaders{popstatus, popvalidtime},
                      data {"tickerId, brokerId, secAccountId, orderId, filledQuantity, orderType,
                        orderStatus, messageProtocolVersion, messageProtocolUri,messageTitle, messageContent}

    ====Price updates from wspush====
    The topic of each message contains the message type and tickerId
    All price messages have a status field defined as F = pre-market, T = market hours, A = after-market
    Topic 102 is the most common streaming message used by the trading app,
        at times 102 for some crazy reason may not show a close price or volume, so it's not useful for a trading app
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

    def _setup_callbacks(self):
        """
        Has to be done this way to have them live in a class and not require self as the first parameter
        Python is kind enough to hold onto a copy of self for the callbacks to use later on
        return: addresses of the call backs
        """
        def on_connect(client, userdata, flags, rc):
            """
            The callback for when the client receives a CONNACK response from the server.
            """
            self.oncon_lock.acquire()
            if self.debug_flg:
                print("Connected with result code "+str(rc))
            if rc != 0:
                raise ValueError("Connection Failed with rc:"+str(rc))
            self.oncon_lock.release()

        def on_order_message(client, userdata, msg):
            #{tickerId, orderId, filledQuantity, orderType, orderStatus}
            self.onmsg_lock.acquire()

            topic = json.loads(msg.topic)
            data = json.loads(msg.payload)
            if self.debug_flg:
                print(f'topic: {topic} ----- payload: {data}')

            if not self.order_func is None:
                self.order_func(topic, data)

            self.onmsg_lock.release()

        def on_price_message(client, userdata, msg):
            self.onmsg_lock.acquire()
            try:
                topic = json.loads(msg.topic)
                data = json.loads(msg.payload)
                if self.debug_flg:
                    print(f'topic: {topic} ----- payload: {data}')

                if not self.price_func is None:
                    self.price_func(topic, data)

            except Exception as e:
                print(e)
                time.sleep(2) #so theres time for message to print
                os._exit(6)

            self.onmsg_lock.release()

        def on_subscribe(client, userdata, mid, granted_qos, properties=None):
            """
            The callback for when the client receives a SUBACK response from the server.
            """
            self.onsub_lock.acquire()
            if self.debug_flg:
                print(f"subscribe accepted with QOS: {granted_qos} with mid: {mid}")
            self.onsub_lock.release()

        def on_unsubscribe(client, userdata, mid):
            """
              The callback for when the client receives a UNSUBACK response from the server.
              """
            self.onsub_lock.acquire()
            if self.debug_flg:
                print(f"unsubscribe accepted with mid: {mid}")
            self.onsub_lock.release()
        #-------- end message callbacks
        return on_connect, on_subscribe, on_price_message, on_order_message, on_unsubscribe


    def connect(self, did, access_token=None):
            if access_token is None:
                say_hello = {"header":
                                 {"did": did,
                                  "hl": "en",
                                  "app": "desktop",
                                  "os": "web",
                                  "osType": "windows"}
                             }
            else:
                say_hello = {"header":
                                 {"access_token": access_token,
                                  "did": did,
                                  "hl": "en",
                                  "app": "desktop",
                                  "os": "web",
                                  "osType": "windows"}
                             }


            #Has to be done this way to have them live in a class and not require self as the first parameter
            #in the callback functions
            on_connect, on_subscribe, on_price_message, on_order_message, on_unsubscribe = self._setup_callbacks()

            if not access_token is None:
                # no need to listen to order updates if you don't have a access token
                # paper trade order updates are not send down this socket, I believe they
                # are polled every 30=60 seconds from the app

                self.client_order_upd = mqtt.Client(did, transport='websockets')
                self.client_order_upd.on_connect = on_connect
                self.client_order_upd.on_subscribe = on_subscribe
                self.client_order_upd.on_message = on_order_message
                self.client_order_upd.tls_set_context()
                # this is a default password that they use in the app
                self.client_order_upd.username_pw_set('test', password='test')
                self.client_order_upd.connect('platpush.webullbroker.com', 443, 30)
                #time.sleep(5)
                self.client_order_upd.loop_start()  # runs in a second thread
                print('say hello')
                self.client_order_upd.subscribe(json.dumps(say_hello))
                #time.sleep(5)

            self.client_streaming_quotes = mqtt.Client(client_id=did, transport='websockets')
            self.client_streaming_quotes.on_connect = on_connect
            self.client_streaming_quotes.on_subscribe = on_subscribe
            self.client_streaming_quotes.on_unsubscribe = on_unsubscribe
            self.client_streaming_quotes.on_message = on_price_message
            self.client_streaming_quotes.tls_set_context()
            #this is a default password that they use in the app
            self.client_streaming_quotes.username_pw_set('test', password='test')
            self.client_streaming_quotes.connect('wspush.webullbroker.com', 443, 30)
            #time.sleep(5)
            self.client_streaming_quotes.loop()
            #print('say hello')
            self.client_streaming_quotes.subscribe(json.dumps(say_hello))
            #time.sleep(5)
            self.client_streaming_quotes.loop()
            #print('sub ticker')


    def run_blocking_loop(self):
            """
            this will never return, you need to put all your processing in the on message function
            """
            self.client_streaming_quotes.loop_forever()

    def run_loop_once(self):
        try:
            self.client_streaming_quotes.loop()
        except Exception as e:
            print(e)
            time.sleep(2)  # so theres time for message to print
            os._exit(6)

    def subscribe(self, tId=None, level=105):
        #you can only use curly brackets for variables in a f string
        self.client_streaming_quotes.subscribe('{'+f'"tickerIds":[{tId}],"type":"{level}"'+'}')
        self.client_streaming_quotes.loop()


    def unsubscribe(self, tId=None, level=105):
        self.client_streaming_quotes.unsubscribe(f'["type={level}&tid={tId}"]')
        #self.client_streaming_quotes.loop() #no need for this, you should already be in a loop


if __name__ == '__main__':
    webull = webull(cmd=True)

    # for demo purpose
    webull.login('xxxxxx@xxxx.com', 'xxxxx')
    webull.get_trade_token('xxxxxx')
    # set self.account_id first
    webull.get_account_id()
    # webull.place_order('NKTR', 21.0, 1)
    orders = webull.get_current_orders()
    for order in orders:
        # print(order)
        webull.cancel_order(order['orderId'])
    # print(webull.get_serial_id())
    # print(webull.get_ticker('BABA'))

    #test streaming
    nyc = timezone('America/New_York')
    def on_price_message(topic, data):
        print (data)
        print(f"Ticker: {topic['tickerId']}, Price: {data['deal']['price']}, Volume: {data['deal']['volume']}", end='', sep='')
        if 'tradeTime' in data:
            print(', tradeTime: ', data['tradeTime'])
        else:
            tradetime = data['deal']['tradeTime']
            current_dt = datetime.today().astimezone(nyc)
            ts = current_dt.replace(hour=int(tradetime[:2]), minute=int(tradetime[3:5]), second=0, microsecond=0)
            print(', tradeTime: ', ts)

    def on_order_message(topic, data):
        print(data)


    conn = StreamConn(debug_flg=True)
    # set these to a processing callback where your algo logic is
    conn.price_func = on_price_message
    conn.order_func = on_order_message

    if not webull.access_token is None and len(webull.access_token) > 1:
        conn.connect(webull.did, access_token=webull.access_token)
    else:
        conn.connect(webull.did)

    conn.subscribe(tId='913256135') #AAPL
    conn.run_loop_once()
    conn.run_blocking_loop() #never returns till script crashes or exits
