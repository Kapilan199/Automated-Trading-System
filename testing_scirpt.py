import MetaTrader5 as mt5
import datetime as dt
import pandas as pd
symbol = "GBPUSD"

symbol_info = mt5.symbol_info_tick(symbol).ask


if symbol_info is None:
    print(f"Failed to fetch information for symbol {symbol}")



print(symbol_info)




def get_5m_candles(currency):
    data = mt5.copy_rates_from(currency, mt5.TIMEFRAME_M5, dt.datetime.now() - dt.timedelta(10), 250)   
    data_df = pd.DataFrame(data) 
    data_df.time = pd.to_datetime(data_df.time, unit="s")
    data_df.set_index("time", inplace=True)
    data_df.rename(columns={"open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"},inplace=True)
    return data_df


df = get_5m_candles(symbol)
print(df)

