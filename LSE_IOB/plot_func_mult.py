import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot_prices_mult(file_1, year, month, day, *args):
    df_1 = pd.read_csv(file_1, sep=';', encoding='latin-1', \
                   names=['seq', 'num', 'time', 'ticker', 'price', 'q', 'vol', 'NA']).drop([0])
    day_to_string = datetime(year, month, day).strftime('%Y-%m-%d')
    df_1['time'] = day_to_string + " " + df_1['time']
    df_1 = df_1.set_index(pd.DatetimeIndex(df_1['time']))
    df_1 = df_1.drop(['seq', 'num', 'time', 'ticker', 'q', 'vol', 'NA'], axis=1)
    df_1.price = df_1.price.astype('float64')

    i = 2
    d = {}
    for f in args:
        d['df' + str(i)] =  pd.read_csv(f, sep=',')
        d['df' + str(i)]['Time'] = d['df' + str(i)]['Time'].astype(str).str[:15]
        d['df' + str(i)]['Time'] = pd.to_datetime(d['df' + str(i)]['Time'])
        d['df' + str(i)] = d['df' + str(i)].drop([0])
        d['df' + str(i)]['Time'] = d['df' + str(i)]['Time'] + timedelta(hours=2)
        d['df' + str(i)] = d['df' + str(i)].set_index('Time')
        d['df' + str(i)] = d['df' + str(i)].drop(['EventSymbol', '#=TimeAndSale', 'EventTime', 'Sequence', 'ExchangeCode', \
                      'Size', 'BidPrice', 'AskPrice', 'SaleConditions', 'Flags'], axis=1)

        i += 1

    board_list = [('*', 'CHIX'), ('^', 'BATE'), ('x', 'BXTR')]

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot(df_1[d['df2'].index[0]:d['df2'].index[-1]], label='Quik', marker='o')
    j = 0
    for val in d.values():
        ax.plot(val, label='DxFeed ' + board_list[j][1], marker=board_list[j][0], linestyle='--', alpha=0.5)
        j += 1
    ax.legend(loc='upper left')
    ax.grid()
    plt.ylabel('Price')
    plt.title('{} {}.{}.{}'.format(file_1[:4].upper(), file_1[4:6], file_1[6:8], file_1[8:12]))
    plt.show()

    print('Кол-во записей Quik: \n' + str(df_1[d['df2'].index[0]:d['df2'].index[-1]].count()))
    j = 0
    for val in d.values():
        print('Кол-во записей DxFeed {}: \n{}'.format(board_list[j][1], val.count()))
        j += 1
