import MetaTrader5 as mt5

symbol = "USDCAD"

symbol_info = mt5.symbol_info_tick(symbol).ask


if symbol_info is None:
    print(f"Failed to fetch information for symbol {symbol}")



print(symbol_info)
