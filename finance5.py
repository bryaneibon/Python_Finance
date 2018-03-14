"""By $.Georges Bryan DIFFO.$"""

import bs4 as bs
import pickle  # Pour la sauvegarde notre fichier 'sp500tickers'...
import requests

""" Ici, le but est d'obtenir une liste des 500 compagnies les mieux cotés en bourse en temps réel... 
Pour ce cas particulier nous utiliserons Wikipedia: https://en.wikipedia.org/wiki/List_of_S%26P_500_companies, 
et 'html.parser', afin d'aider à la recherche des données.
"""
def save_sp500_tickers():
    response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    rows = table.findAll('tr')[1:]
    for row in rows:
        """ '('td')[0]' car on souhaite obtenir le symbole de la compagnie... 
        Si j'avais mis à la place "('td')[1]", la liste contiendrai 
        plutot les noms de compagnies; comme alignés dans le lien Wikipedia ci-dessus..."""

        ticker = row.findAll('td')[0].text
        tickers.append(ticker)

    """Pour la sauvegarde de notre fichier"""
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    print(tickers, '\n', len(tickers), '{}'.format('compagnies').capitalize())
    return tickers


save_sp500_tickers()