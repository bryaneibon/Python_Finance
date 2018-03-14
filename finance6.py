"""By $.Georges Bryan DIFFO.$"""

import bs4 as bs
import pickle
import datetime as dt
import os
import pandas_datareader.data as wb
import requests

""" Dans ce script, le but est de créer un répertoire, contenant des .csv de toutes les compagnies
répertoriées à ce jour dans le tableau 's&p500' du lien wikipedia ci-dessous, selon leur OHCL et leur volume
le tout dans la fonction 'get_data_from_iex()'...

Notons que, nous aurions pu effectuer toutes les exécutions sans avoir à sauvegarder les fichiers. Mais le problème
avec cette facon de procéder est que, ca prendrai énormémenent de temps juste pour extraire les données avant de les
analyser.
Alors que ca ne prends que quelques minutes pour les sauvegarder dans des .csv locaux, et quelques secondes pour les
analyser ou les combiner dans un DataFrame...
"""


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
        with open("sp500tickers.pickle", "rb") as f:  # Cette fois ci on lis le tickers, 'rb'...
            tickers = pickle.load(f)

    if not os.path.exists("Stocks_SP500"):  # Si le dossier n'existe pas, on le crée...
        os.makedirs("Stocks_SP500")

    start = dt.datetime(2013, 1, 1)
    end = dt.datetime(2018, 3, 14)
    """Si l'on souhaite ne pas observer les données des 500 compagnies, on peut mettre un délimiteur.
    Par exemple, pour les 100 premières compagnies, on écrira: tickers[:100]"""
    for ticker in tickers:
        print(ticker)
        """ Au cas ou la connexion se coupe, on sauvegarde au moins la progression du téléchargement..."""
        if not os.path.exists("Stocks_SP500/{}.csv".format(ticker)):
            df = wb.DataReader(ticker, 'iex', start, end)  # Les données auraient pu être prisent d'autres sources:
            # 'google', 'morningstar', etc...
            df.to_csv("Stocks_SP500/{}.csv".format(ticker))
        else:
            print("Le symbole: {}, existe déjà dans le fichier".format(ticker))


get_data_from_iex()
