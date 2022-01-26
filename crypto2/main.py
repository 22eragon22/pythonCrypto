import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import cryptocompare.cryptocompare as cc
from functools import partial
from tkinter import *

API_KEY = 'da8423bc3b8f28e5f1819b6a8ba2122c190ecf7d750ff01e18b72e92733504c3'
CURRENCY = 'USD'
TIMELIMIT = 180  # in days

# sets the api key
cc_item = cc._set_api_key_parameter(API_KEY)


# calculates average value of a coin in a specified time period
def average_value(coin: str) -> float:
    total = 0
    try:
        data = cc.get_historical_price_day(coin, currency=CURRENCY, limit=TIMELIMIT)
        for value in data:
            total += value['close']
    except:
        print("Something is wrong with the API - class: average_value")
        return
    avg = total / len(data)
    return avg


# historical data about specific cryptocurrency
def get_historical_information(crypto_currency: str):

    # defining date format that will be displayed
    date_fo = pd.DataFrame.from_dict(cc.get_historical_price_day(crypto_currency,
                                                                 currency=CURRENCY,
                                                                 limit=TIMELIMIT))
    date_fo['time'] = pd.to_datetime(date_fo['time'], unit='s')
    date_fo.set_index('time', inplace=True)

    # making the graph of cryptocurrency
    register_matplotlib_converters()
    plt.figure()
    plt.title('{}'.format(crypto_currency))
    plt.plot(date_fo.index, date_fo.close)
    plt.xlabel("Period of time (last {} days)".format(TIMELIMIT))
    plt.ylabel("Price per unit (in {})".format(CURRENCY))
    plt.axhline(y=average_value(crypto_currency), color='black', linestyle='--', label='avg. value')
    plt.legend()
    plt.show()


# calculates average values of specified coins and returns them as a list
def calc_average_values_of_specific_coins() -> list:

    # if you want any other cryptocurrency, just add/change values in here
    coins = ['BTC', 'ETH', 'LUNA',
             'FTM', 'SOL', 'BUSD',
             'ATOM', 'BNB', 'ADA',
             'DOGE']  # top 10 right now

    list_of_coin_values = []

    for coin in coins:
        price = cc.get_price(coin, currency=CURRENCY, full=False)
        price = price[coin][CURRENCY]
        average = average_value(coin)
        percentage_of_difference = round(100 * ((price - average) / average), 2)
        coin_data = {
            'crypto_currency': coin,
            'percentage_of_difference': percentage_of_difference
        }

        list_of_coin_values.append(coin_data)
    list_of_coin_values = sorted(list_of_coin_values, key=lambda d: d['percentage_of_difference'])
    return list_of_coin_values


window = Tk()
Label(window, text="Current prices compared to the last 180 days:\n").pack()
list_of_average = calc_average_values_of_specific_coins()
for element in list_of_average:
    Button(window,
           width=25,
           height=2,
           text=element['crypto_currency'] + "   " + str(element['percentage_of_difference']) + "%",
           bg='grey',
           fg="white",
           command=partial(get_historical_information, element['crypto_currency'])).pack(padx=1, pady=2)

window.mainloop()
