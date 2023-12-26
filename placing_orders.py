"""
mt5 placing and closing orders

@author: Kapilan Ramasamy
"""

import MetaTrader5 as mt5


def market_order(symbol, vol, buy_sell):
#    if buy_sell
    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY
    else:
        direction = mt5.ORDER_TYPE_SELL
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": vol,
        "price": mt5.symbol_info_tick(symbol).ask,
        "type": direction,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    order_status = mt5.order_send(request) 
    return order_status


market_order("USDCAD", 0.03,"buy")


def limit_order(symbol, vol, buy_sell, pips_away):
#    if buy_sell
    pip_unit = 10*mt5.symbol_info(symbol).point

    if buy_sell.capitalize()[0] == "B":
        direction = mt5.ORDER_TYPE_BUY_LIMIT
        price = mt5.symbol_info_tick(symbol).ask - pips_away*pip_unit
    else:
        direction = mt5.ORDER_TYPE_SELL_LIMIT
        price = mt5.symbol_info_tick(symbol).ask + pips_away*pip_unit

    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": vol,
        "price": mt5.symbol_info_tick(symbol).ask,
        "type": direction,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    order_status = mt5.order_send(request) 
    return order_status



limit_order("USDCAD", 0.03, "buy", 6)