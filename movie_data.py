from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from plot_scraper import get_plot


# My browser defaults movie titles to my native language, these headers change them back to english
headers = {'Accept-Language': 'en-US,en;q=0.8'}

url = 'http://www.imdb.com/chart/top'
response = requests.get(url, headers = headers)
soup = BeautifulSoup(response.text, 'lxml')
 
movies = soup.select('td.titleColumn')

list_titles = []
list_year = []

# Iterating through IMDb Top 250 and extracting title and release year 
# For more details check out: https://www.geeksforgeeks.org/scrape-imdb-movie-rating-and-details-using-python/
for index in range(0, len(movies)):
     
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    year = re.search('\((.*?)\)', movie_string).group(1)
    list_titles.append(str(movie_title))
    list_year.append(year)

data = {"movie_title": list_titles, "year": list_year}

moviedb = pd.DataFrame(data)

list_plots = []

for title, year in zip(moviedb['movie_title'], moviedb['year']):
    movie_plot = get_plot(title, year)
    list_plots.append(movie_plot)

moviedb['plot'] = list_plots
moviedb = moviedb.dropna()
moviedb.to_csv('moviedb.csv', index=False)
