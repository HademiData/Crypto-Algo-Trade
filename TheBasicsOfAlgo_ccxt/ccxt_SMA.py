import pandas as pd
import ccxt
import dontShareConfig


# connecting my binance dashboard

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})


# first we get the data

bars = binance.fetch_ohlcv('BTC/USDT', timeframe='15m', limit=500)
df = pd.DataFrame(bars, columns=['timeStamp', 'open', 'high', 'low', 'close', 'volume' ])

print(df)

# making the sma

# e.g 
# 10 SMA
df['sma10'] = df.close.rolling(10).mean()
 
# 30 SMA
df['sma30'] = df.close.rolling(30).mean()

# 100 SMA
df['sma100'] = df.close.rolling(100).mean()