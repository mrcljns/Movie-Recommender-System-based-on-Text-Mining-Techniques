# Movie-Recommender-System-based-on-Text-Mining-Techniques-written-in-Python

## General Info
The Purpose of this project is providing movie recommendations based on user's input. First, the program scrapes plot descriptions of the chosen title and every other movie from IMDb Top 250 list. Then, the plot describtions are processed into TF-IDF vectors, which allow to compare the chosen title with every movie form the list. Based on cosine similarity, 5 movies are chosen and returned as recommendations. TF-IDF has its faults, as it will most likely find sequels or movies set in the same universe, but similar plots described with synonymous words might be lost.
