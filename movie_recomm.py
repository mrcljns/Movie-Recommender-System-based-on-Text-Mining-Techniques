import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
from plot_scraper import get_plot
from numpy import dot
from numpy.linalg import norm
from collections import OrderedDict
import copy
import re

def preprocess_text(text):
    """
    Input: scraped plot of a movie
    Purpose: preprocess text (tokenize, removing stopwords, and stemming)
    Output: prepocessed plot of a movie
    """
    tokenizer = RegexpTokenizer(r'\w+')
    en_stopwords = set(stopwords.words('english'))
    porter_stem = PorterStemmer()

    raw = text.lower()
    tokens = tokenizer.tokenize(raw)
    stop_tokens = [token for token in tokens if token not in en_stopwords]
    stemmed_tokens = [porter_stem.stem(token) for token in stop_tokens]

    return stemmed_tokens

def processing_plots(movie_1, movie_2):
    """
    Input: two preprocessed movie plots
    Purpose: Turn preprocessed movie plots to a list of term frequency vectors
    Output: list of tf vectors 
    """
    plot_tokens = []
    plot_tokens.append(movie_1)
    plot_tokens.append(movie_2)
    all_plot_tokens = sum(plot_tokens, [])
    lexicon = sorted(set(all_plot_tokens))
    zero_vector = OrderedDict((token, 0) for token in lexicon)
    text_vectors=[]
    for token in plot_tokens:
        vec=copy.copy(zero_vector)
        token_counts = Counter(token)
        for key, value in token_counts.items():
            vec[key] = value / len(lexicon)
        text_vectors.append([val for val in vec.values()])
    return text_vectors

def cos_sim(results):
    """
    Input: tf vectors
    Puropse: Calculates the cosine similarity
    Output: cosine similarity
    """
    cos_sim = dot(results[0], results[1])/(norm(results[0])*norm(results[1]))
    return cos_sim

moviedb = pd.read_csv('moviedb.csv')
moviedb['plot'] = [preprocess_text(i) for i in moviedb['plot']]

# Input has to be precise in terms of capital letters, spaces and such
movie_input = str(input("Type in movie title: "))
movie_year_input = str(input("(Optional) What year did it come out?: "))
input_plot = get_plot(movie_input, movie_year_input)

try:
    input_plot = preprocess_text(input_plot)

    moviedb_vectors = []

    for title in moviedb['plot']:
        moviedb_vectors.append(processing_plots(input_plot, title))

    result_vectors = [cos_sim(i) for i in moviedb_vectors]

    moviedb['similarity'] = result_vectors

    # Dropping duplicate of the input title (if there's one). This prevents recommending excatly the same title that was
    # used as an input.
    moviedb = moviedb.drop(moviedb[moviedb["movie_title"] == (re.sub(r'\s\([^)]*\)', '', movie_input))].index)

    print("The recommendations are:")
    # Printing 5 closest titles
    print(moviedb.sort_values(by=['similarity'], ascending=False).movie_title.head(5).to_string(index=False))

except:
    print("No such title.")
