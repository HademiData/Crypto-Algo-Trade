import ccxt
import dontShareConfig
from datetime import datetime
import time

# REFRENCE VIDEO YOUTUBE : MOON DEV (HOW TO CODE AN ACCUMULATION ALGO)



# connecting my binance dashboard

binance = ccxt.binance({
    'enableRateLimit': True,
    'apiKey':dontShareConfig.apiKey,
    'secret':dontShareConfig.apiSecret
})


# AN ACCUMULATION ALGORITHIM BUYS EVERY X SECONDS OR MINUITES OR
# DAYS THIS X IS SPECIFIED BY THE TRADER


# firstly we get the order book
# getting the best bid and ask also

symbol = 'BTC/USDT'
def get_bid_ask(symbol):

    # Note that the symbol is the pairs you are trading
    # e.g "BTC/USDT" ' OR 'BNB/USDT'


    book = binance.fetch_order_book(symbol) # this helps to fecth the order book for the specified symbol

    #print(btc_bin_book)  #prints the order book
    btc_bid = book['bids'][0][0]
    btc_ask = book['asks'][0][0]
    print(f'the best bid: {btc_bid}, the best ask: {btc_ask}')
    return btc_bid , btc_ask

go = False
sleep = 10

while go == True:

    bid = get_bid_ask()[0]
    ask = get_bid_ask()[1]

    print(bid)
    # now for this example we want to buy accumulate but you can reverse this code a little  and sell accumulate
    lowbid = bid-20 # reverse the bid

    # Now we want to create the order (in this case we do limt buy order you can do market buy, but limit is what is done here)
    size = 1
    binance.create_limit_buy_order(symbol, size, lowbid)

    print(f'just made an order and now sleeping for {sleep} seconds')
    time.sleep(sleep)

    





