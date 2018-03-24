"""By $.Georges Bryan DIFFO.$"""

import bs4 as bs
import pickle
import datetime as dt
import os
import pandas_datareader.data as wb
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')
"""
La corrélation, un outil de gestion du risque:

La corrélation entre deux actifs financiers, ou plus généralement entre deux variables aléatoires,
est l'intensité de la liaison qu'il existe entre ces deux variables.
Afin de déterminer cette liaison il suffit de calculer le coefficient de corrélation,
qui est tout toujours compris entre +1 et -1.

Plus le coefficient est proche des extrémités et plus les variables sont corrélées,
c'est à dire dépendantes linéairement l'une par rapport à l'autre.
Un corrélation égale à +1 (respectivement -1) implique qu'il existe une relation linéaire positive
(respectivement négative) entre les variables.
Ceci se traduit par l'existence de 2 réels a et b tels que y=ax+b.

Si rho=0, on dit que les deux variables sont dé-corrélées.
C'est à dire qu'il n'existe pas de relation linéaire entre elles
(mais il peut très bien en exister une non linéaire).

En revanche on ne doit pas confondre dé-corrélées avec indépendantes.
En effet, deux variables indépendantes sont obligatoirement dé-corrélées,
mais deux variables dé-corrélées ne sont pas forcément indépendantes.
Il se peut qu'il existe une relation non linéaire entre les deux variables.

Plus on se rapproche de rho=+1 (respectivement rho=-1) et plus les variables sont corrélées
(respectivement anti-corrélées c'est à dire corrélées négativement).

Pour plus de détais: 'https://www.investopedia.com/terms/c/correlation.asp'

"""


"""création d'une table massive de corrélations, afin de déterminer les relations entre compagnies
(Pris de notre fichier 'S&p500_At_Closes.csv') """

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

        df.rename(columns={'close': ticker}, inplace=True)
        df.drop(['open', 'high', 'low', 'volume'], 1, inplace=True)
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count % 10 == 0:
            print(count)
    print(main_df)
    main_df.to_csv('S&p500_At_Closes.csv')


# compile_data()

def visualize_data():
    df = pd.read_csv('S&p500_At_Closes.csv')
    # df['AAPL'].plot(), df[['AAPL','ABC']].plot()
    # plt.show()

    """La méthode corr() va en fait prendre toutes les colonnes de notre .csv, extraire les valeurs
    ('closes' dans notre cas), effectuer les corrélations et créer ces valeurs corrélées.
    """

    # Pour corréler 03 titres par exemple, df_correlation = df[['AAPL','ABC','ACN']].corr()
    df_correlation = df.corr()
    # print(df_correlation.head())

    data = df_correlation.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    """Le cmap est un intervalle de Rouge(negatif), puis jaune(neutre) et enfin vert(positif)"""
    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn) # RYG = RedYellowGreen
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_correlation.columns
    row_labels = df_correlation.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)
    plt.xticks(rotation=90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()

visualize_data()