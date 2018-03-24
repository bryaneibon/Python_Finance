"""By $.Georges Bryan DIFFO.$"""

"""Ce script nous donne les informations sur les 5 dernières années de la compagnie 'Tesla' via 'Google Finance' """

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web


# Définissons un style d'affichage...
style.use('ggplot')

start = dt.datetime(2013,1,1)
end = dt.datetime(2018, 3, 23)


# Les infos seront prisent de Google dans notre cas.
"""
# Notons que ces infos sont disponibles de plusieurs plateformes aussi telles que:

Google Finance : 'google'
Morningstar: 'morningstar'
IEX: 'iex'
Robinhood: 'robinhood'
Enigma: "s'inscrire à 'http://public.enigma.com/signup' afin d'obtenir une clé d'accès"
Quandl: 'quandl'
St.Louis FED (FRED): 'fred'
Kenneth French’s data library: 'famafrench'
World Bank...
OECD...
Eurostat...
Thrift Savings Plan...
Nasdaq Trader symbol definitions...
Stooq...
MOEX...

Voir: 'https://pandas-datareader.readthedocs.io/en/latest/remote_data.html' pour plus de détails...
"""

# Dataframe... En y associant un Ticker : Le Ticker ici
# représente le symbole de la compagnie, pouvant être à 3 à 4 lettres
# Dans notre cas, se sera Tesla, de symbole 'TSLA'.
df = web.DataReader('TSLA','google', start, end)

"""Nous renvoie les 80 dernières lignes sous forme de DataFrame..."""
#print(df.tail(80))

"Sauvegardons les infos pris dans l'intervalle de 'start' à 'end' dans un CSV."
df.to_csv('tesla.csv')


