import ccxt
import pandas as pd
pd.set_option('display.max_rows',None)


# get data
exchange = ccxt.binanceus()
bars = exchange.fetch_ohlcv('ETH/USDT',limit=300,timeframe='1m')

# pass in data frame
df = pd.DataFrame(bars[:-1], columns=['timestamp','open','high','low','close','volume'])
# convert uint timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'],unit='ms')

'''
MAKE TR 
TR = MAX[( high - low), abs(high - previous_close), abs(low - previous_close)]
TR = MAXIMUM of those numbers
'''

# make function return TR
def make_tr(df):
    df['previous_close'] = df['close'].shift(1)
    # make high-low
    df['high-low'] = df['high'] - df['low']
    # make high pc
    df['high-pc'] = abs(df['high'] - df['previous_close'])
    # make low pc
    df['low-pc'] = abs(df['low'] - df['previous_close'])
    # TR
    tr = df[['high-low', 'high-pc', 'low-pc']].max(axis=1)

    return tr



# make TR colum
#df['tr'] = make_tr(df)
#print(df)

# make ATR fucntion
def atr(df,period=14):
    df['tr'] = make_tr(df)

    the_atr = df['tr'].rolling(period).mean()

    return the_atr

def supertrend(df,period=7,multiplier=3):
    print("calculating supertrend")
    # basic upper band  =  ( (high + low ) /2) + (multiplier * ATR)
    # basic lower band  =  ( (high + low ) /2) - (multiplier * ATR)
    df['atr'] = atr(df,period)
    df['upperband'] = ( (df['high'] + df['low']) /2) + (multiplier * df['atr'])
    df['lowerband'] = ( (df['high'] + df['low']) /2) - (multiplier * df['atr'])
    # make up trend check colum
    df['in_uptrend'] = True

    for current in range(1, len(df.index)):
        previous = current - 1

        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]

            if df['in_uptrend'][current] and df['lowerband'][current] < df['lowerband'][previous]:
                df['lowerband'][current] = df['lowerband'][previous]

            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]

    print(df)

supertrend(df,period=5)






