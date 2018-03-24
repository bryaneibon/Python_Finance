"""By $.Georges Bryan DIFFO.$"""

import bs4 as bs
import pickle
import datetime as dt
import os
import pandas_datareader.data as wb
import requests
import pandas as pd

""" Il s'agit ici de prendre toutes les données des différents DataFrame, 
et les combiner dans le même,  via la fonction 'compile_data()'...

Cette fonction va en fait combiner toutes les informations sur les prix d'actions
à la fermeture, et les combiner dans un seul .csv, pour les 500 compagnies..."""


def save_sp500_tickers():
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    rows = table.findAll('tr')[1:]
    for row in rows:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers, '\n', len(tickers), '{}'.format('compagnies').capitalize())
    return tickers


def get_data_from_iex(reload_sp500=False):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)

    if not os.path.exists("Stocks_SP500"):
        os.makedirs("Stocks_SP500")

    start = dt.datetime(2013, 1, 1)
    end = dt.datetime(2018, 3, 14)

    for ticker in tickers:
        if not os.path.exists("Stocks_SP500/{}.csv".format(ticker)):
            df = wb.DataReader(ticker, 'iex', start, end)
            df.to_csv("Stocks_SP500/{}.csv".format(ticker))
        else:
            print("Le fichier: {}.csv, existe déjà dans le repertoire".format(ticker))


# get_data_from_iex()

def compile_data():
    with open("sp500tickers.pickle", "rb") as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()

    for count, ticker in enumerate(tickers):
        df = pd.read_csv("Stocks_SP500/{}.csv".format(ticker))
        df.set_index('date', inplace=True)

        df.rename(columns={'close': ticker}, inplace=True)  # C'est les infos à la fermeture que l'on souhaite afficher.
        df.drop(['open', 'high', 'low', 'volume'], 1, inplace=True)  # On exclut ces colonnes, puis,
        # 'close' n'existe plus ici ('df.rename')...

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df)
    main_df.to_csv('S&p500_At_Closes.csv')


compile_data()
