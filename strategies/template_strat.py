import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import datetime as dt
import time
import copy





def place_market_order(symbol,vol,buy_sell):
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    else:
        direction = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": vol,
        "type": direction,
        "price": price,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    return result


def main():
    pass

starttime=time.time()
timeout = time.time() + 60*60*1 # one hour 
while time.time() <= timeout:
    try:
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
      # time.sleep(300 - ((time.time() - starttime) % 300.0)) # 5 minute interval between each new execution
        time.sleep(20 - ((time.time() - starttime) % 20.0)) # 1 minute interval between each new execution
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()