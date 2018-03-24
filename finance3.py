"""By $.Georges Bryan DIFFO.$"""

""" Effectuons quelques manipulations sur les données prisent de la compagnie 'tesla'..."""
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2013,1,1)
end = dt.datetime(2018, 3, 23)

df = web.DataReader('TSLA','google', start, end)

df.to_csv('tesla_finance3.csv')

df = pd.read_csv('tesla_finance3.csv', parse_dates=True, index_col=0)

"""Création d'une nouvelle colonne qui va faire la moyenne "mean()" des prix selon les dates
entrées dans nos variables 'start' et 'end' ; aussi on peut définir 
la période minimale 'min_periods' à 0, de sorte que les premières dates calcule la moyenne 
en tenant compte du 0"""
df['100 Mouving Average'] = df['Close'].rolling(window=100, min_periods=0).mean()

"""S'assure de retirer les Nan dans les résultats du df."""
#df.dropna(inplace=True)
#print(df.head())

""" Construction des axes:: 6 lignes(rowspan) pour 1 colonne(colspan), puis, le graphe débute aux coordonnées (0,0) """
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1) # 'sharex' Va permettre de zommer sur 'bar'
                                                                       # lorsqu'on voudra zommer sur 'Plot'

ax1.plot(df.index, df['Close'])
ax1.plot(df.index, df['100 Mouving Average'])
ax2.bar(df.index, df['Volume'])

plt.show()