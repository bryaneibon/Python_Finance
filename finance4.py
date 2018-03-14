"""By $.Georges Bryan DIFFO.$"""

""" Visualisation graphique des données OHLC de Tesla..."""
import datetime as dt
import matplotlib.pyplot as plt
# 'from matplotlib.finance import candlestick_ohlc' n'est plus supporté
# et a été remplacé par 'mpl_finance'...
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from matplotlib import style
import pandas as pd
import pandas_datareader.data as wb

style.use('ggplot')

start = dt.datetime(2013,1,1)
end = dt.datetime(2018, 3, 14)

df = wb.DataReader('TSLA','google', start, end)

df.to_csv('tesla_finance4.csv')

df = pd.read_csv('tesla_finance4.csv', parse_dates=True, index_col=0)

""" 'resample' pour 10 jours ohlc: Open, High, Low, Close...
 ohlc() est un attribut de la classe 'Series', permettant de filtrer les infos qu'on a sur le stock...
 On obtient ici une moyenne sur les 10 jours, en rapports avec les données que l'on souhaite extraire..."""
df_ohlc = df['Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum() # Somme des Volumes après 10 jours.

df_ohlc.reset_index(inplace=True) # On modifie l'index ici pour qu'il soit des entiers autoincrémentés.
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
#print(df_ohlc.head())


""" Construction des axes:: 6 lignes(rowspan) pour 1 colonne(colspan), puis, le graphe débute aux coordonnées (0,0) """
ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1) # 'sharex' Va permettre de zommer sur 'bar'
                                                                       # lorsqu'on voudra zommer sur 'Plot'
ax1.xaxis_date()
candlestick_ohlc(ax1, df_ohlc.values,width=2, colorup='k')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values,0, color='k')
plt.show()
