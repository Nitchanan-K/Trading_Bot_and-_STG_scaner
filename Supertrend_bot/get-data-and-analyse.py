import pandas as pd
import ta
from ta.volatility import BollingerBands,AverageTrueRange
import ccxt
import config


exchange_id = 'kraken'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': config.API_Key,
    'secret': config.Secret_Key,
})

#market = exchange.load_markets()

bars = exchange.fetch_ohlcv('ETH/USD', limit=51)

df = pd.DataFrame(bars[:-1],columns=['timestamp','open','high','low','close','volume'])
#print(df)

bb_indicator = BollingerBands(df['close'],window=20)
df['upper_band'] = bb_indicator.bollinger_hband()
df['lower_band'] = bb_indicator.bollinger_lband()
df['moving_average'] = bb_indicator.bollinger_mavg()




# ATR
atr_indicator = AverageTrueRange(df['high'],df['low'],df['close'])
df['atr'] = atr_indicator.average_true_range()

# df
print(df)