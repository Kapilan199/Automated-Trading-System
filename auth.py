
import MetaTrader5 as mt5
import os 

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

if mt5.initialize(path=path, login=int(key[0]), server=key[2],password=key[1]):
    print("Connection Established")
else:
    print("initialize() failed, error code =",mt5.last_error())
