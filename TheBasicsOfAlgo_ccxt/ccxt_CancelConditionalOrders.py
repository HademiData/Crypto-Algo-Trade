# this cancels the condiitional orders e.g stoplosses

import ccxt
import dontShareConfig


# connecting my binance dashboard

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})

# CANCEL ORDERS
binance.cancel_all_orders('BTC/USDT')



# CANCELS ALL THE CONDITIONALS
params = {'untriggered': True}
binance.cancel_all_orders('BTC/USDT', params)

