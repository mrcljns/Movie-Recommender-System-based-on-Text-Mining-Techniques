# Movie-Recommender-System-based-on-Text-Mining-Techniques

## General Info
The Purpose of this project is providing movie recommendations based on user's input. First, the program scrapes plot descriptions of the chosen title and every other movie from IMDb Top 250 list. Then, the plot descriptions are processed into TF-IDF vectors, which allow to compare the chosen title with every movie form the list. Based on cosine similarity, 5 movies are chosen and returned as recommendations. TF-IDF has its faults, as it will most likely find sequels or movies set in the same universe, but similar plots described with synonymous words might be lost.

## File Description
* plot_scraper.py contains functions scraping the plot description from Wikipedia using Beautiful Soup 4.9.3
* movie_data.py creates a dataframe of IMDb top 200 and saves it to .csv file
* movie_recomm.py is the main file which reads the .csv file, processes the text, asks the user for a movie and returns recommendations
