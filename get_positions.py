"""
mt5 placing and closing orders

@author: Kapilan Ramasamy
"""
import MetaTrader5 as mt5
import pandas as pd


def get_positions():
    positions = mt5.positions_get()

    if len(positions) > 0:
        pos_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())
        pos_df.time = pd.to_datetime(pos_df.time, unit="s")
        pos_df.drop(['time_msc', 'time_update', 'time_update_msc'], axis=1, inplace = True)
    else:
        pos_df = pd.DataFrame()

    return pos_df


print(get_positions())


def get_orders():
    orders = mt5.orders_get()

    if len(orders) > 0:
        order_df = pd.DataFrame(orders, columns=orders[0]._asdict().keys())
        order_df.time_setup = pd.to_datetime(order_df.time_setup, unit="s")
        order_df.drop(['time_msc', 'time_update', 'time_update_msc'], axis=1, inplace = True)
    else:
        order_df = pd.DataFrame()

    return order_df

print(get_orders())