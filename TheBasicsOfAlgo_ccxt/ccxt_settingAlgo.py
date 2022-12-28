# import packages
import pandas as pd
import numpy as np
import onecall 
import datetime
import ccxt
import dontShareConfig



# connecting my binance dashboard

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})

# check connection by checking balance

#print(binance.fetch_balance())

# get bid and ask


#get_bid_ask() # calls the function


# How to make a post only order {meaning that we are not doing market orders only limit orders}


symbol = 'BTC/USDT'
pos_size = 1
mybid = get_bid_ask()[0]
mybid = mybid-1000


params = {'test': True,}


#params = {'timeInForce': 'PostOnly',}


#binance.create_limit_buy_order(symbol, pos_size, mybid, params)
#print('we just made an order....')




# HOW TO MAKE MARKET BUY AND SELL ORDER


# example for buy 
symbol = 'BTC/USDT'
size = 1

#order = binance.create_market_buy_order(symbol,size)
#print(order)





# example for sell
#

#order = binance.create_market_sell_order(symbol,size)
#print(order)


# HOW TO CANCEL CRYPTO ORDERS



# always specify the symbol you are to work with
#e.g

#binance.fetch_order_book(symbol)  # this cancels all  the orders you have

#print(ccxt.exchanges)

#test = ccxt.binance()

#balance = test.load_markets()

#print(list(balance.items())[:1])

import sklearn



