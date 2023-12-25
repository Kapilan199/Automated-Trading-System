"""
mt5 placing and closing orders

@author: Kapilan Ramasamy
"""

import MetaTrader5 as mt5


def market_order(symbol, vol):
#    if buy_sell
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": vol,
        "price": mt5.symbol_info_tick(symbol).ask,
        "type": mt5.ORDER_TYPE_BUY,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    order_status = mt5.order_send(request) 
    return order_status


market_order("USDCAD", 0.03)
