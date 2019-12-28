import os
import matplotlib.pyplot as plt
import pandas as pd
from sqrt.ema_indicator import EMAIndicator
from sqrt.utils import *


if __name__ == '__main__':
    DAY = 24 * 60
    starting_date = pd.to_datetime("2018-01-01 00:00:00")
    data_path = "../data/"
    data_files = os.listdir(data_path)
    data_files.sort()
    pairs = []
    candletables = []

    for item in data_files:
        info = item.split("_")[1].split('-')[1]
        if info == 'BSV':
            continue
        if len(pairs) == 0 or pairs[-1] != info:
            pairs.append(info)
            candletables.append(pd.read_csv(data_path + item, index_col='Time', encoding='cp949'))
        else:
            candletables[-1] = pd.concat([candletables[-1], pd.read_csv(data_path + item, index_col='Time', encoding='cp949')])

    for i in range(len(candletables)):
        candletables[i].index = pd.to_datetime(candletables[i].index, format="%d-%m월-%Y %H:%M:%S.000")
        candletables[i] = candletables[i].loc[candletables[i].index >= starting_date]

    prices, price_returns, price_norms = compute_price_returns(candletables, pairs)
    ema = EMAIndicator(candletables, pairs, 5 * DAY, 20 * DAY, prices, price_returns, price_norms)
    mdd, sharpe, sortino, cumret = evaluate(price_returns, ema.signal(), pairs, 0)
    print(f"mdd = {mdd}, sharpe = {sharpe}, sortino = {sortino}")
    cumret.plot()
   

