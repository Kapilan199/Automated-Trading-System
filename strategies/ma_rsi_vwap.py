import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import datetime as dt
import time

# Get positions, collect data, analyze data, place orders, rinse, and repeat...

# Functions to retrieve positions and historical data

def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        pos_df.type = np.where(pos_df.type == 0, 1, -1)  # distinguish between long and short positions
    else:
        pos_df = pd.DataFrame()
        
    return pos_df


def get_5m_candles(currency):
    data = mt5.copy_rates_from(currency, mt5.TIMEFRAME_M5, dt.datetime.now(), 50)   
    data_df = pd.DataFrame(data) 
    data_df.time = pd.to_datetime(data_df.time, unit="s")
    data_df.set_index("time", inplace=True)
    data_df.rename(columns={"open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"},inplace=True)
    return data_df


def calculate_ma(data, window=45):
    data['MA'] = data['Close'].rolling(window=window).mean()
    return data


def calculate_rsi(data, window_length=14):
    delta = data['Close'].diff()
    up = delta.where(delta > 0, 0)
    down = -delta.where(delta < 0, 0)
    average_gain = up.rolling(window=window_length).mean()
    average_loss = down.rolling(window=window_length).mean().abs()
    relative_strength = average_gain / average_loss
    rsi = 100 - (100 / (1 + relative_strength))
    return rsi


def calculate_vwap(data):
    if 'Volume' in data.columns:  # Check if 'Volume' column exists
        data['Cumulative_PV'] = (data['Close'] * data['Volume']).cumsum()
        data['Cumulative_Volume'] = data['Volume'].cumsum()
        data['VWAP'] = data['Cumulative_PV'] / data['Cumulative_Volume']
    else:
        print("Error: 'Volume' column not found in the DataFrame.")
    return data



def place_market_order(symbol, vol, buy_sell, sl, tp):
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


def main():
    pairs = "AUDUSD"
    positions = get_position_df()
    ohlc = get_5m_candles(pairs)
    ohlc = calculate_ma(ohlc)  # Calculate Moving Average
    ohlc['RSI'] = calculate_rsi(ohlc)  # Calculate RSI

    custom_sl_buy = mt5.symbol_info_tick(pairs).ask - 0.0003  # Set your desired SL for Buy orders
    custom_tp_buy = mt5.symbol_info_tick(pairs).ask + 0.0003  # Set your desired TP for Buy orders
    custom_sl_sell = mt5.symbol_info_tick(pairs).bid + 0.0003  # Set your desired SL for Sell orders
    custom_tp_sell = mt5.symbol_info_tick(pairs).bid - 0.0003  # Set your desired TP for Sell orders

    if ohlc['Close'].iloc[-1] > ohlc['MA'].iloc[-1] and ohlc['RSI'].iloc[-1] > 70:
        if len(positions) == 0 or pairs not in positions['symbol'].values:
            print(place_market_order(pairs, pos_size, "Buy", custom_sl_buy, custom_tp_buy))
            print("buy", pairs)

    elif ohlc['Close'].iloc[-1] < ohlc['MA'].iloc[-1] and ohlc['RSI'].iloc[-1] < 30:
        if len(positions) == 0 or pairs not in positions['symbol'].values:
            print(place_market_order(pairs, pos_size, "Sell", custom_sl_sell, custom_tp_sell))
            print("sell ", pairs)


starttime = time.time()
timeout = time.time() + 60*60*1  # one hour
while time.time() <= timeout:
    try:
        print("passthrough at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
        time.sleep(1/3 - ((time.time() - starttime) % 1/3))  # 1 second interval between each new execution
        
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        exit()
