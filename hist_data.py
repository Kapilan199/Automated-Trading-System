"""
mt5 historical data collection

@author: Kapilan Ramasamy
"""

import MetaTrader5 as mt5
import datetime as dt
import pandas as pd
import pytz

# need a .txt file with login,pass,server
# need to connect to mt5 terminal also need terminal64.exe 


file_path = 'C:\\Users\\kapil\\OneDrive\\Desktop\\Automated-Trading-System\\key.txt'

try:
    with open(file_path, 'r') as file:
        # Perform actions with the file
        key = file.read().split()
        path = r'C:\Program Files\MetaTrader 5\terminal64.exe'
        # Do something with the file content
        print(key)
except FileNotFoundError:
    print("File not found or path is incorrect.")
except IOError:
    print("Error reading the file.")


# establish MetaTrader 5 connection to a specified trading account
    
# NOTE: add scheduler to further automate the system

try:
    connection = mt5.initialize(path=path, login=int(key[0]), server=key[2], password=key[1])
    if connection:
        print("Connection Established")
except mt5.Error as error:
    print(f"initialize() failed, error code = {error.code}")
    quit()





# Now we must extract historical data
    
 # set time zone to LA
timezone = pytz.timezone("America/Los_Angeles")

# get 200 EURUSD H4 bars starting from 10/1/202 - M/D/Y in Los Angeles time zone

hist_data = mt5.copy_rates_from("EURUSD", mt5.TIMEFRAME_M15, dt.datetime(2023, 10, 1,tzinfo=timezone), 200)

hist_data_df = pd.DataFrame(hist_data)

hist_data_df_time = pd.to_datetime(hist_data_df.time, unit="s")

hist_data_df.time = hist_data_df_time

# inplace means to permanently make the index time

hist_data_df.set_index("time", inplace=True)

print(hist_data_df)