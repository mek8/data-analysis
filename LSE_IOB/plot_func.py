import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot_prices(file_1, file_2, year, month, day):
    df_1 = pd.read_csv(file_1, sep=';', encoding='latin-1', \
                   names=['seq', 'num', 'time', 'ticker', 'price', 'q', 'vol', 'NA']).drop([0])
    day_to_string = datetime(year, month, day).strftime('%Y-%m-%d')
    df_1['time'] = day_to_string + " " + df_1['time']
    df_1 = df_1.set_index(pd.DatetimeIndex(df_1['time']))
    df_1 = df_1.drop(['seq', 'num', 'time', 'ticker', 'q', 'vol', 'NA'], axis=1)
    df_1.price = df_1.price.astype('float64')

    df_2 = pd.read_csv(file_2, sep=',')
    df_2['Time'] = df_2['Time'].astype(str)
    df_2['Time'] = df_2['Time'].str[:15]
    df_2['Time'] = pd.to_datetime(df_2['Time'])
    df_2 = df_2.drop([0])
    df_2['Time'] = df_2['Time'] + timedelta(hours=2)
    df_2 = df_2.set_index('Time')
    df_2 = df_2.drop(['EventSymbol', '#=TimeAndSale', 'EventTime', 'Sequence', 'ExchangeCode', \
                  'Size', 'BidPrice', 'AskPrice', 'SaleConditions', 'Flags'], axis=1)

    fig, ax = plt.subplots(figsize=(15, 8))

    if file_2[-5:] == 'm.csv':
        ax.plot(df_1.loc[:df_2.index[-1]], label='Quik', marker='.')
        df_1_count = df_1.loc[:df_2.index[-1]].count()
    elif file_2[-5:] == 'a.csv':
        ax.plot(df_1.loc[df_2.index[0]:df_2.index[-1]], label='Quik', marker='.')
        df_1_count = df_1.loc[df_2.index[0]:df_2.index[-1]].count()
    elif file_2[-5:] == 'e.csv':
        ax.plot(df_1.loc[df_2.index[0]:], label='Quik', marker='.')
        df_1_count = df_1.loc[df_2.index[0]:].count()

    ax.plot(df_2, label='DxFeed', marker='^', alpha=0.5)
    ax.legend(loc='upper left')
    plt.ylabel('Price')
    plt.title('{} {}.{}.{}'.format(file_1[:4].upper(), file_1[4:6], file_1[6:8], file_1[8:12]))
    ax.grid()
    plt.show()
    print("Кол-во записей Quik: \n" + str(df_1_count))
    print("Кол-во записей DxFeed: \n" + str(df_2.count()))
