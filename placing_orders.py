"""
mt5 historical data collection

@author: Kapilan Ramasamy
"""

import MetaTrader5 as mt5

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
    
# add scheduler to further automate the systemI

try:
    connection = mt5.initialize(path=path, login=int(key[0]), server=key[2], password=key[1])
    if connection:
        print("Connection Established")
except mt5.Error as error:
    print(f"initialize() failed, error code = {error.code}")
    quit()



def market_order(symbol, vol):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": vol,
        "price": mt5.symbol_info_tick(symbol),
        "type": mt5.ORDER_TYPE_BUY,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    order_status = mt5.order_send(request) 
    return order_status


market_order("USDCAD", 0.03)
