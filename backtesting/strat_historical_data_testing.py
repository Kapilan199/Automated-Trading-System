import MetaTrader5 as mt5
import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


symbol = "GBPUSD"


def get_5m_candles(currency):
    data = mt5.copy_rates_from(currency, mt5.TIMEFRAME_M5, dt.datetime.now() - dt.timedelta(10), 1250)   
    data_df = pd.DataFrame(data) 
    data_df.time = pd.to_datetime(data_df.time, unit="s")
    data_df.set_index("time", inplace=True)
    data_df.rename(columns={"open":"Open","high":"High","low":"Low","close":"Close","volume":"Volume"},inplace=True)
    return data_df




# Assuming you have a DataFrame 'historical_data' containing historical GBPUSD data



def calculate_ma(data, window=50):
    """
    Function to calculate the moving average
    """
    data['MA'] = data['Close'].rolling(window=window).mean()
    return data

def backtest_strategy(data):
    data = calculate_ma(data)  # Calculate Moving Average
    data['Signal'] = np.where(data['Close'] > data['MA'], 1, -1)  # Buy: Close > MA, Sell: Close < MA

    # Simulate Trades based on Signals
    positions = data['Signal'].shift(1)  # Enter position one period after the signal
    data['Position'] = positions

    # Calculate Performance Metrics
    # Calculate profit/loss based on position changes and track other performance metrics

    return data  # Return updated DataFrame with signals and positions

# Backtest on historical data
historical_data = get_5m_candles(symbol)
backtested_data = backtest_strategy(historical_data)

# Calculate and display performance metrics based on backtested_data
# Analyze strategy performance and make adjustments if needed




# Graph and display results

plt.figure(figsize=(10, 6))
plt.plot(backtested_data['Close'], label='Closing Prices', color='blue')
plt.plot(backtested_data['MA'], label='Moving Average', color='red')
plt.title('GBPUSD Closing Prices vs Moving Average')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.show()


#conclusion:
# if the ma is less the price then the price will go up -> BUY
# likewise if the ma is greater than the price then the price will go down -> SELL