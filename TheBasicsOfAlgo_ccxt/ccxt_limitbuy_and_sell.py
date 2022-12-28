import ccxt
import dontShareConfig

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})


symbol = 'BTC/USDT'
size = 1
bid = 35863 #e.g buy
ask = 35913 # e.g sell
# CREATE LIMIT BUY ORDER (SAYING YOU WANT TO BUY AT A PARTICULAR ORDER)

"""
buy_order = binance.create_limit_buy_order(symbol, size, bid)
print(buy_order) # gets all the details about the order

# CREATE LIMIT SELL ORDER (SAYING YOU WANT TO SELL AT A PARTICULAR OREDR)

sell_order = binance.create_limit_sell_order(symbol, size, ask)
print(sell_order) # gets all the details about the order

"""