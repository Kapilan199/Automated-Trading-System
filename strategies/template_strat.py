# this is script takes the moving average of stock based on the past 250 bars
# it then places either a buy or sell order with an appropriate tp and sl

import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import datetime as dt
import time

# 1. get positions
# 2. collect data
# 3. analyze data
# 4. place orders 
# rinse and repeat


# NOTE: Set ticker and position amount

pairs = 'AUDUSD' # currency pairs to be included in the strategy
pos_size = 0.5 # max capital allocated/position size for any currency pair. in MT5 the size is in unit of 10^5


# NOTE: COLLECT POSITIONS AND HISTORICAL DATA

# Gets current positions
def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        pos_df.type = np.where(pos_df.type==0,1,-1) #to distinguish between long and short positions
    else:
        pos_df = pd.DataFrame()
        
    return pos_df


# Gets historical data
def get_5m_candles(currency):
    data = mt5.copy_rates_from("GBPUSD", mt5.TIMEFRAME_M5, dt.datetime.now(), 50)   
    data_df = pd.DataFrame(data) 
    data_df.time = pd.to_datetime(data_df.time, unit="s")
    data_df.set_index("time", inplace=True)
    data_df.rename(columns={"open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"},inplace=True)
    return data_df




# Places market orders
def place_market_order(symbol,vol,buy_sell,sl,tp):
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
        "sl": sl,
        "tp": tp,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    
    result = mt5.order_send(request)
    return result



# NOTE: TECHNICAL ANALYSIS


# calculates moving averages
def calculate_ma(data, window=45):
    """
    Function to calculate the moving average
    """
    data['MA'] = data['Close'].rolling(window=window).mean()
    return data



# NOTE: MAIN


def main():
    pairs = "AUDUSD"
    positions = get_position_df()
    ohlc = get_5m_candles(pairs)
    ohlc = calculate_ma(ohlc)  # Calculate Moving Average

    # Calculate dynamic SL and TP based on moving average
    custom_sl_buy = mt5.symbol_info_tick(pairs).ask - 0.0003  # Set your desired SL for Buy orders
    custom_tp_buy = mt5.symbol_info_tick(pairs).ask + 0.0001  # Set your desired TP for Buy orders
    custom_sl_sell = mt5.symbol_info_tick(pairs).bid + 0.0003  # Set your desired SL for Sell orders
    custom_tp_sell = mt5.symbol_info_tick(pairs).bid - 0.0001  # Set your desired TP for Sell orders

    # Place Buy Order with custom SL and TP
    if ohlc['Close'].iloc[-1] > ohlc['MA'].iloc[-1]:
        if len(positions) == 0 or pairs not in positions['symbol'].values:
            print(place_market_order(pairs, pos_size, "Buy", custom_sl_buy, custom_tp_buy))
            print("buy", pairs)

    # Place Sell Order with custom SL and TP
    elif ohlc['Close'].iloc[-1] < ohlc['MA'].iloc[-1]:
        if len(positions) == 0 or pairs not in positions['symbol'].values:
            print(place_market_order(pairs, pos_size, "Sell", custom_sl_sell, custom_tp_sell))
            print("sell ", pairs)




# NOTE: SCHEDULER

starttime=time.time()
timeout = time.time() + 60*60*1 # one hour 
while time.time() <= timeout:
    try:
        print("passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
      # time.sleep(300 - ((time.time() - starttime) % 300.0)) # 5 minute interval between each new execution
       # time.sleep(20 - ((time.time() - starttime) % 20.0)) # 1 minute interval between each new execution
        # time.sleep(10 - ((time.time() - starttime) % 10.0)) # 1/2 minute interval between each new execution
        time.sleep(1/3 - ((time.time() - starttime) % 1/3)) # 1 seconds interval between each new execution
        
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()