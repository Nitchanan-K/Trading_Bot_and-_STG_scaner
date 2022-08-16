import numpy
import websocket, json, pprint, talib
import config
from binance.client import Client
from binance.enums import *

# define socket
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

# set client
#client = Client(config.API_KEY, config.API_SECRET, tld='us')

#
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = 'ETHUSD'
TRADE_QUANTITY = 0.05

closes = []
in_position = False

def order():

    pass




def on_open(ws):
    print("opened connection")

def on_close(ws):
    print("close connection")

def on_message(ws, message):
    global closes

    print("received message")
    json_message = json.loads(message)
    #pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print(f"candle closed at {close}")
        closes.append(float(close))
        print('closes')
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes,RSI_PERIOD)
            print(rsi)
            last_rsi = rsi[-1]
            print(f"the current rsi is {last_rsi}")


            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                    print("SELL TIME! RSI over 70")
                    # put binance buy logic
                    order_succeeded = order()
                    if order_succeeded:
                        in_position = False

                else:
                    print("It is overbought!, but we don't own any. Nothing to do")


            if last_rsi < RSI_OVERSOLD:
                    if in_position:
                        print(" It is oversold!, but yoo already own it, nothing to do.")
                    else:
                        print("BUY TIME! RSI lower 30")
                        # binance buy logic
                        order_succeeded = order()
                        if order_succeeded:
                            in_position = True

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()






