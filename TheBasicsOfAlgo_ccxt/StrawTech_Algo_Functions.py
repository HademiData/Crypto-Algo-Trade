# ALL FUNCTIONS TO BE NEEDED IN MAKING AN ALGORITHIM FOR binance TRADING BOTS



'''
NOTE  --(kill switch function) I marked out three cancel orders in the kill switch function,
# I need to unmark (uncomment) the before live execution of code

'''

# import packages
import pandas as pd
import numpy as np
import onecall 
import datetime
import ccxt
import dontShareConfig
import time 


# connecting my binance dashboard

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})
# THIS ARE DEFAULT VALUES OF THE INPUTS FOR THE FUNCTIONS

symbol = 'BTC/USDT'
pos_size = 100 # 125, 75
target = 35
params = {'timeInForce': 'PostOnly',}
max_loss = -35
vol_decimal = .4

# for volume calc vol_repeat * vol_time == TIME of volume collection
vol_repeat = 11
vol_time = 5
# the time btw trade 
pause_time = 60
# FOR THE df
timeframe = '4h'
limit_of_numberOfBars = 100
sma = 20
index_pos = 1 # change this on what asset


def get_bid_ask(SYMBOL=symbol):

    btc_bin_book = binance.fetch_order_book(SYMBOL) # this helps to fecth the order book for the specified symbol

    #print(btc_bin_book)  #prints the order book
    crypto_bid = btc_bin_book['bids'][0][0]
    crypto_ask = btc_bin_book['asks'][0][0]
    print(f'the best bid: {crypto_bid}, the best ask: {crypto_ask}')
 
    return crypto_bid , crypto_ask



# Returns: df with sma (can customize with below)
# and Calls: get_sma(symbol, timeframe,limit,sma) # if not passed uses the above specified default
def get_SMA(symbol=symbol, timeframe=timeframe, limit_of_numberOfBars=limit_of_numberOfBars, sma=sma):
    print('processing indis...')

    bars = binance.fetch_ohlcv(symbol,timeframe=timeframe, limit_of_numberOfBars=limit_of_numberOfBars)
    # print(bars)
    df_sma = pd.DataFrame(bars, columns=['timestamp','open','high','low', 'close', 'volume'])
    df_sma['timestamp']= pd.to_datetime(df_sma['timestamp'], unit='ms')

    # DAILY SMA - 20 DAY
    df_sma[f'sma{sma}_{timeframe}'] = df_sma.close.rolling(sma).mean()

    # if bid < the 20 day sma then = BEARISH, if bid > 20day sma = BULLISH
    bid = get_bid_ask(symbol)[0]

    # if sma > bid = sell, if sma < bid = buy
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}']>bid, 'sig'] = 'SELL'
    df_sma.loc[df_sma[f'sma{sma}_{timeframe}']<bid, 'sig'] = 'BUY'

    print(df_sma)

    return df_sma





# open_positions() open_positions, openpos_bool, openpos_size, long, index_pos
# TODO  Figure out a way to sort through json (rando) and assign a index
# make a function that loops through dictionary and does

def open_positions(symbol = symbol):

    # what is the position index for that symbol
    if symbol == 'BTC/USDT':
        index_pos= 3
    elif symbol== 'ETH/USDT':
        index_pos= 1
    elif symbol== 'SOL/USDT':
        index_pos= 2
        



    params = {'type':"swap", 'code': 'USD'}
    bin_bal = binance.fetch_balance(params=params)
    open_positions = bin_bal['info']['data']['positions']
    # print(open_positions)

    openpos_side = open_positions[index_pos]['side']
    openpos_size = open_positions[index_pos]['size']
     #prien(open_positions)

    if openpos_side == ('Buy'):
        openpos_bool = True
        long = True
    elif openpos_side == ('Sell'):
        openpos_bool = True
        long = False
    else:
        openpos_bool = False
        long = None

    print(f'open_positons... | openpos_bool {openpos_bool} | openpos_size {openpos_size} | long {long}')
    
    return open_positions, openpos_bool, openpos_size, long, index_pos
    

# this function essentially stops all ongoing trades
# NOTE  -- I marked out three cancel orders in the kill switch function,
# I need to unmark (uncomment) the before live execution of code
# kill switch returns nothing


# kill switch pass in symbol if no symbol uses default

# between  30min to 50min of 7hrs long video
def kill_switch(symbol=symbol):
    
    print(f'starting the kill switch for{symbol}')
    openposi = open_positions(symbol)[1] # returns true of false
    long = open_positions(symbol)[3] # true or false
    kill_size = open_positions(symbol)[2]  # size that is open

    print(f'openposi {openposi}, long {long}, size {kill_size}')

    while openposi == True:

        print(f'Initiating Kill switch loop ...')
        temp_df = pd.DataFrame()
        print('created temporary DataFrame')

        #binance.cancel_all_orders(symbol)
        openposi = open_positions(symbol)[1]
        long = open_positions(symbol)[3] # true or false
        kill_size = open_positions(symbol)[2]
        kill_size = int(kill_size)

        ask = get_bid_ask(symbol)[1]
        bid = get_bid_ask(symbol)[0]

        if long == False:
            #binance.create_limit_buy_order(symbol,kill_size, bid, params)
            print(f'just made a BUY to CLOSE order of {kill_size} {symbol} at ${bid}')
            print('reactivating for 30 seconds to see if it fills...')
            time.sleep(30)
        
        elif long == True:
            #binance.create_limit_sell_order(symbol,kill_size, bid, params)
            print(f'just made a SELL to CLOSE order of {kill_size} {symbol} at ${ask}')
            print('reactivating for 30 seconds to see if it fills...')
            time.sleep(30)
        
        else:
            print('ABNORMALITIES OR SOMETHING I DIDNT PREDICT IN KILL SWITCH FUNCTION')

        openposi = open_positions(symbol)[1]


# returns nothing
# sleeps on close
#sleep_on_closed(symbol=symbol, pause_time=pause_time):
# this function pauses in minuites

def sleep_on_closed(symbol=symbol, pause_time=pause_time):

    '''
    this function will pull all the closed orders, the if the last close was 
    in last 59min then it sleeps for 1m

    sincelasttrade = minuits since last trade
    '''

    closed_orders = binance.fetch_closed_orders(symbol)
    #print(closed_orders)
    
    for ord in closed_orders[-1::-1]:

        sincelasttrade = pause_time -1 #how long we pause

        filled = False

        status = ord['info']['ordStatus']
        txttime = ord['info']['transactionTimeNs']
        txttime = int(txttime)
        print(f'for {symbol} this is the status of the order {status} with epoch {txttime}')
        print('next iteration...')
        print('------')

        if  status== 'Filled':
            print('FOUND the order with last fill..')
            print(f"this is the time {txttime} this is the orderstatus {status}")
            orderbook = binance.fetch_order_book(symbol)
            ex_timestamp = orderbook['timestamp'] # in ms
            ex_timestamp = int(ex_timestamp/1000)
            print('---- below is the transaction time then exchange epoch time')
            print(txttime)
            print(ex_timestamp)

            time_spread = (ex_timestamp - txttime)/60

            if time_spread < sincelasttrade:
                # print("time since last trade is less than time spread")
                # if in pos is true, put a close order here
                # if in_pos == True:

                sleepy = round(sincelasttrade-time_spread)*60
                sleepy_min = sleepy/60

                print(f'the time spread is less than{sincelasttrade} mins is been {time_spread}min..  so we SLEEP')
                time.sleep(60)

            else:
                print(f'its been {time_spread}mins since last fill so not sleeping ')
            break

        else:
            continue

    print('done with the sleep on close protocol...')


# EXACTLY 1HR IN THE VIDEO


# this function pulls the order book

def order_book(symbol=symbol, vol_repeat = vol_repeat, vol_time= vol_time):


    print(f'fetching order book data for {symbol}... ')

    df = pd.DataFrame()
    temp_df = pd.DataFrame()

    ob = binance.fetch_order_book(symbol)
    # print(ob)
    bids = ob['bids']
    asks = ob['ask']

    first_bid = bids[0]
    first_ask = asks[0]

    bid_vol_list = []
    ask_vol_list = []

    # if SELL vol > Buy vol AND profit target hit, exit

    # get last 1 min of volume.. and if sell > buy vol do x

# TODO make range a var
# reapat == the amount of times it go through the vol process, and multiplues
# by repeat_time to calc the time
    for x in range(vol_repeat):

        for set in bids:
         # prints(set)
            price = set[0]
            vol = set[1]
            bid_vol_list.append(vol)
            # print(price)
            # print(vol)

            #print(bid_vol_list)
            sum_bidvol = sum(bid_vol_list)
            #print(sum_bidvol)
            temp_df['bid_vol'] = [sum_bidvol]

        for set in asks:
            #print(set)
            price = set[0] #[40000, 344]
            vol = set[1]
            ask_vol_list.append(vol)
            #print(price)
            #print(vol)

            sum_askvol = sum(ask_vol_list)
            temp_df['ask_vol'] = [sum_askvol]

        #print(temp)_df
# TODO - change sleep to val
        time.sleep(vol_time) # change back to 5 later
        df = df.append(temp_df)
        print(df)
        print(' ')
        print('------')
        print(' ')

    print(f'done collecting volume data for bids and asks.. ')
    print('calculating the sums...')
    total_bidvol = df['bid_vol'].sum()
    total_askvol = df['ask_vol'].sum()
    seconds = vol_time* vol_repeat
    mins = round(seconds / 60, 2)
    print(f'last {mins}mins for {symbol} this is total Bid Vol: {total_bidvol} |total ask vol: {total_askvol}')

    if total_bidvol > total_askvol:
        control_dec = (total_askvol / total_bidvol)
        print(f'Bulls are in control: {control_dec}...')
        # if bulls are in control, use regular target
        bullish = True
    else:

        control_dec = (total_bidvol/total_askvol)
        print(f'Bears are in control: {control_dec}')
        bullish = False

    # open_positions() open_position, openpos_bool, openpos_size, long

    open_posi = open_positions(symbol)
    openpos_tf = open_posi[1]
    long = open_posi[3]
    print(f'openpos_tf: {openpos_tf} || long: {long} ')

    # if target is hit, check book vol
    # if book vol is < .4.. stay in pos... Sleep?
    # need to check to see if long or short

    if openpos_tf == True:
        if long == True:
            print('we are in a long position...')
            if control_dec < vol_decimal: # vol_decimal set to .4 at top for default
                vol_under_dec = True
                # print('going to sleep for a minuite.. cuz under vol decimal')
                # time.sleep(6) # change to 60
            else:
                print('volume is not under dec so setting vol_under_dec to False')
                vol_under_dec = False
        else:
            print('we are in a short position...')
            if control_dec < vol_decimal: # vol_decimal se to 0.4 at top
                vol_under_dec = True
                # print('going to sleep for a minuite.. cuz under vol decimal')
                # time.sleep(6) # change to 60
            else:
                print('volume is not under dec so setting vol_under_dec to False')
                vol_under_dec = False
    else:
        print('we are not in position...')
        vol_under_dec = None

    
    # when vol_under_dec == FALSE AND target hit, then exit
    print(vol_under_dec)

    return vol_under_dec

                


# pnl_close [0] pnlclose and [1] in_pos [2]size [3] long TF

#  1:11:57 on  tutorial video
def pnl_close(symbol=symbol):

    print(f'checking to see if its time to exit for {symbol}... ')
    params= {'type':'swap', 'code': 'USDT'}
    pos_dict = binance.fetch_positions(params=params)
    #print(pos_dict)

    index_pos = open_positions( symbol )[4]
    pos_dict = pos_dict[index_pos] #btc [3] [0] = doge, [1] ape
    side = pos_dict['side']
    size = pos_dict['contracts']
    entry_price = float(pos_dict['entryPrice'])
    leverage = float(pos_dict['leverage'])

    current_price = get_bid_ask(symbol)[0]

    print(f'side: {side} | entry_price: {entry_price}| leverage: {leverage}')
    # short or long

    if side == 'long':
        diff = current_price - entry_price
        long = True
    else:
        diff = entry_price - current_price
        long = False

    try:
        perc = round(((diff/entry_price) * leverage) ,10)
    except:
        perc = 0

    perc = 100*perc
    print(f'for {symbol}this is our PNL percentage: {(perc)}%')

    pnlclose = False
    in_pos  = False

    if perc >0:
        in_pos = True
        print(f'for {symbol} we are in a winning position')
        if perc > target:
            print(':) :) we are in profit  and hit target.. checking volume to see if we')
            pnlclose = True
            vol_under_dec = order_book(symbol) #return TRUE OR FALSE TF
            if vol_under_dec == True:
                print(f'volume is under the decimal threshold we set of {vol_decimal}')
                time.sleep(30)
            else:
                print(':) :) starting the kill switch beacause we hit our target')
                kill_switch()
        else:
            print('we have not hit our target yet')

    elif perc < 0: # -10 or -20 e.t.c
        
        in_pos = True

        if perc <= max_loss: # under -55, -56
            print(f'we need to exit now down {perc}.. so starting kill switch protocol')
            kill_switch()

        else:
            print(f'we are in a losing position of {perc}.. but not yet in  max loss')

    else:
        print('we are not in position')

    if in_pos == True:

        # breakes over .8 over 15m sma, then close pos (STOP LOSS)

        # pull in 15m sma
        #call: get_SMA(symbol, timeframe, limit_of_numberOfBars, sma)
        timeframe = '15m'
        df_f = get_SMA(symbol, timeframe, 100, 20)  # F15_sma IS NOT DEFINED
        #print(df_f)
        # df_f('sma20_15') # last value of this

        last_sma15 = df_f.iloc[-1][f'sma{sma}_{timeframe}']
        last_sma15 = int(last_sma15)
        print(last_sma15)
        # pull current bid
        curr_bid = get_bid_ask(symbol)[0]
        curr_bid = int(curr_bid)
        print(curr_bid)

        sl_val = last_sma15 * 1.008
        print(sl_val)

# NOTE- TURN KILL SWITCH ON

        # 5/11 - REMOVED THE BELOW AND IMPLEMENTING A 55% STOP LOSS
           # in the pnl section
        #if curr_bid > sl_val:
        #    print('current bid is above stop loss value.. starting KILL SWITCH..')
        #    kill_switch(symbol)
        #else:
        #     print('chilling in position..')
    else:
        print('we are not in position..')


    print(f' for {symbol} we just finished checking PNL close..')

    return pnlclose, in_pos, size, long

    
#open_positions(), open_positions, openpos_bool, openpos_size, long, index_pos
#pnl_close('BTC/USDT')     

     









        





        


