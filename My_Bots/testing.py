from binance import Binance

import dontShareConfig



GoodGrace = Binance('BTC/USDT', dontShareConfig.apiKey,dontShareConfig.apiSecret )

a = GoodGrace.ohlcv('BTC/USDT','1m')
print( GoodGrace.position())

