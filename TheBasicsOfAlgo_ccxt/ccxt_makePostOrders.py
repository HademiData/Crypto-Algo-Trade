# POST ORDERS HELP TO SEND AN ORDER TO AN EXCHANGE AS A LIMIT ORDER
# SOMETIMES IF YOU PUT IN A LIMIT ORDER IT WILL FILL IN AS A MARKET ORDER
# AND IN MOST EXCHANGES YOU WILL HAVE TO PAY THREE TIMES THE PRICE 
# FOR THE MARKET ORDERS BUT SOME EVEN PAY YOU FOR EXECUTING A 
# LIMIT ORDER


# POST ORDERS SOLVE THIS PROBLEM BY SAYING THE ORDER SHOULD BE 
# SENT AS A LIMIT ORDER, BUT IF IT CANT EXECUTE AS A LIMIT ORDER THEN 
# DONT EXECUTE THE ORDER
# LIMIT ORDERS ARE CHEAPER THAN MOST OTHER ORDERS IN MOST EXCHANGES


import ccxt
import dontShareConfig

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})


symbol = 'BTC/USDT'
size = 1
bid = 40000 #e.g buy

# post only order
params = {'timeInForce':'POstOnly',}

binance.create_limit_buy_order(symbol, size, bid, params)
