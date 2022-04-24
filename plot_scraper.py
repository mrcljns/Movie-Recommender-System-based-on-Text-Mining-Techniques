from numpy import NaN
import requests
from bs4 import BeautifulSoup

def get_plot(movie, year = ""):
    """
    Input: title of the movie
    Purpose: scrapes plot of a movie from wikipedia and returns
    Output: plot of the movie
    """
    movie_plot = []
    
    # Many links to movie wikipedia pages contain "release year film" or just "film" in parentheses,
    # so these exceptions handle errors that might occur because of it. If nothing works function retrurns NaN. 
    try:
        try:
            url = "https://en.wikipedia.org/wiki/{}".format(movie.replace(" ", "_"))
            wiki = requests.get(url)
            soup = BeautifulSoup(wiki.text, 'html.parser')
            plot = soup.select('h2 > #Plot')[0]
        except:
            try:
                url = "https://en.wikipedia.org/wiki/{}_({}_film)".format(movie.replace(" ", "_"), year)
                wiki = requests.get(url)
                soup = BeautifulSoup(wiki.text, 'html.parser')
                plot = soup.select('h2 > #Plot')[0]
            except:
                url = "https://en.wikipedia.org/wiki/{}_(film)".format(movie.replace(" ", "_"), year)
                wiki = requests.get(url)
                soup = BeautifulSoup(wiki.text, 'html.parser')
                plot = soup.select('h2 > #Plot')[0]

        # Looping through next siblings after <h2>Plot</h2>, until another h2 header is found.
        # On most movie Wikipedia pages "Plot" is a h2 header, if it's not the case NaN is returned.
        for sib in plot.parent.next_siblings:
            if sib.name == 'p':
                movie_plot.append(sib.text)
            elif sib.name == 'h2':
                break
        return str(' '.join(movie_plot))
    except:
        return NaN




    






