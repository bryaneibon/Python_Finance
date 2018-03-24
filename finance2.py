"""By $.Georges Bryan DIFFO.$"""

""" Les informations obtenues de Tesla sont ensuite mis dans un DataFrame, que l'on peut observer via un graphe..."""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2013,1,1)
end = dt.datetime(2018, 3, 23)

df = web.DataReader('TSLA','google', start, end)
#print(df.tail(80))

df.to_csv('tesla_finance2.csv')


"""parse_dates devient le nouvel index. il remplace 0,1,2, etc... avec index_col=0, pour 
que le graphe ait les 'Dates' en abscisse... """
df = pd.read_csv('tesla_finance2.csv', parse_dates=True, index_col=0)
#print(df.head())

"""Si l'on souhaite voir les prix à la fermeture, on peut faire: 'df['Close'].plot()' 
ou même, définir un certains nombres de colonnes avec: 'df[['Open','Close']].plot()' """
df.plot()
plt.show()
