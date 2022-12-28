# this strategy for trading 
# is simply when the price gets higher than the last resistance
# or the price get lower than the last support,
# let's make a trade then.



# time stamp on video of  7hrs long is 1:32:46 

# how the tutor does it
# symbol used BTC
# timeframe 15mins chart
#STRATEGY

# first, calculate or get the last 3 days of data
# second then find the support and resistance 15mins
# then on retest place orders [this means we are going long and short]

# notes
'''add support and resistance from 
   your hand done analysis to my_algo_functions file
   '''


import pandas as pd
import numpy as np
import onecall 
import datetime
import ccxt
import dontShareConfig
import time 
import StrawTech_Algo_Functions as n


binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})
# THIS ARE DEFAULT VALUES OF THE INPUTS FOR THE FUNCTIONS

symbol = 'BTC/USDT'
pos_size = 10 # 125, 75
target = 9
max_loss = -8

index_pos = 1 # change this on what asset

# the time btw trade
pause_time = 10


vol_decimal = .4
params = {'timeInForce': 'PostOnly',}
# for volume calc vol_repeat * vol_time == TIME of volume collection
vol_repeat = 11
vol_time = 5

# FOR THE df
timeframe = '4h'
limit_of_numberOfBars = 100
sma = 20




# PULLING THE BID AND ASK

askbid = n.get_bid_ask(symbol)
ask = askbid[1]
bid = askbid[0]

print(f'for {symbol}... ask: {ask} | bid: {bid}')


#  PULL IN THE DATA [DF_SMA -- CAUSE IT HAS ALL THE DATA WE NEED]
# and Calls: get_sma(symbol, timeframe,limit,sma) # if not passed uses the above specified default
df_sma = n.get_SMA(symbol, '15m', 500, 20)

# PULL IN OPEN POSITIONS

open_pos = n.open_positions(symbol)

# CALCULATE SUPPORT AND RESISTANCE BASED ON CLOSE



# calculate the retest, where the orders are made

# PULL IN THE PNL CLOSE
# returns: pnl_close [0] pnlclose and [1] in_pos [2]size [3] long TF
# pass in just the symbol
pnl_close = n.pnl_close(symbol)

# PULL SLEEP ON CLOSE


# PULL KILL SWITCH
# returns: kill_switch() nothing
# kill_switch: pass in the symbol if no symbol ust use default
kill_switch = n.kill_switch()



# then run bot


# stoped at 2:01:28 time on the 7hr long video