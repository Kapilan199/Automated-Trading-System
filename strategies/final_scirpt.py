import MetaTrader5 as mt5
import numpy as np
import pandas as pd
import datetime as dt
import time
import talib


# Set the currency pair and position size
pairs = "AUDUSD"
pos_size = 0.5

# Define function to get current positions
def get_position_df():
    positions = mt5.positions_get()
    if len(positions) > 0:
        pos_df = pd.DataFrame(list(positions), columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        pos_df.type = np.where(pos_df.type == 0, 1, -1)  # to distinguish between long and short positions
    else:
        pos_df = pd.DataFrame()

    return pos_df

# Define function to get historical data
def get_5m_candles(currency):
    data = mt5.copy_rates_from("GBPUSD", mt5.TIMEFRAME_M5, dt.datetime.now(), 50)
    data_df = pd.DataFrame(data)
    data_df.time = pd.to_datetime(data_df.time, unit="s")
    data_df.set_index("time", inplace=True)
    data_df.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"},
                   inplace=True)
    return data_df

# Define function to calculate MACD
def calculate_macd(data):
    macd, signal, _ = talib.MACD(data['Close'])
    data['MACD'] = macd
    data['Signal'] = signal
    return data

# Define function to calculate RSI
def calculate_rsi(data):
    rsi = talib.RSI(data['Close'])
    data['RSI'] = rsi
    return data

# Define function to calculate Bollinger Bands
def calculate_bollinger_bands(data):
    upper_band, middle_band, lower_band = talib.BBANDS(data['Close'])
    data['UpperBand'] = upper_band
    data['MiddleBand'] = middle_band
    data['LowerBand'] = lower_band
    return data

# Define function to place market order
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

# Define function to close position
def close_position(position_id, symbol, price, deviation=20):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "position": position_id,
        "price": price,
        "deviation": deviation,
        "magic": 234000,
        "comment": "python script close",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    result = mt5.order_send(request)
    return result

# Define main function
def main():
    positions = get_position_df()
    ohlc = get_5m_candles(pairs)
    ohlc = calculate_macd(ohlc)
    ohlc = calculate_rsi(ohlc)
    ohlc = calculate_bollinger_bands(ohlc)

    # Set your conditions based on MACD, RSI, and Bollinger Bands
    macd_condition = (ohlc['MACD'] > ohlc['Signal'])
    rsi_condition = (ohlc['RSI'] < 30)  # Example: Buy when RSI is below 30
    bollinger_condition = (ohlc['Close'] < ohlc['LowerBand'])

    # Place Buy Order
    if macd_condition.any() and rsi_condition.any() and bollinger_condition.any():
        if len(positions) == 0 or pairs not in positions['symbol'].values:
            print(place_market_order(pairs, pos_size, "Buy", 0, 0))  # Set your SL and TP values

    # Place Sell Order
    elif not macd_condition.any() and not rsi_condition.any() and not bollinger_condition.any():
        if len(positions) == 0 or pairs not in positions['symbol'].values:
            print(place_market_order(pairs, pos_size, "Sell", 0, 0))  # Set your SL and TP values

    # Close Positions if conditions are not met
    else:
        for index, row in positions.iterrows():
            position_id = row['ticket']
            symbol = row['symbol']
            price = mt5.symbol_info_tick(symbol).bid if row['type'] == -1 else mt5.symbol_info_tick(symbol).ask
            print(close_position(position_id, symbol, price))


# Run the script continuously
starttime = time.time()
timeout = time.time() + 60 * 60 * 1  # one hour
while time.time() <= timeout:
    try:
        print("passthrough at ", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        main()
        time.sleep(1 / 3 - ((time.time() - starttime) % 1 / 3))  # 1 second interval between each new execution

    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        mt5.shutdown()
        exit()

# Shutdown MetaTrader 5 connection
mt5.shutdown()
