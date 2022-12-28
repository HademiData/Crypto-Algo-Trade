import ccxt
import dontShareConfig
from datetime import datetime
import time



binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})


symbol = 'BTC/USDT'
size = 1

ask = 36000

bid = 35800

#FIRST MAKE SELL OPEN
binance.create_limit_sell_order(symbol, size, ask)

stop_price = (bid * 10000) + 10000
stop_trigger =  stop_price +20000



# let 35800 be bid
# MAKE ACTUAL STOPLOSS AFTER YOU MAKE THE ORDER
sl_params =  {
    'clordID': 'stop-loss-order-then-limit',
    'timeInforce': 'postOnly',
    'symbol':'BTC/USDT',
    'side': 'Buy',
    'orderType':'StopLimit',
    'triggerType': 'ByLastPrice',
    'stopPxEp': stop_trigger,
    'priceEp': stop_price,
    'orderQty': size

}    # stoploss params

#  Now to create stop order
'''
stop = binance.create_order(symbol, type='limit', side='buy', amount=size, price=stop_price, params=sl_params)
'''



