import pandas as pd
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from collections import Counter
from plot_scraper import get_plot
from numpy import dot
from numpy.linalg import norm
from collections import OrderedDict
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

def tf_idf(movie, lexicon, df):
    """
    Input: preprocessed movie plot
    Purpose: Turn preprocessed movie plot to a vector of tf-idf
    Output: list of tf vectors 
    """
    vec = OrderedDict((token, 0) for token in lexicon)
    text_vectors=[]
    token_counts = Counter(movie)
    for key, value in token_counts.items():
        vec[key] = value / (len(lexicon)*df[key])
    for val in vec.values():
        text_vectors.append(val)
    return text_vectors

def doc_freq(plots, input):
    """
    Input: pandas data frame column and input plot
    Purpose: Calculate document frequency values
    Output: Dictionary containing document frequency values
    """
    df = {}
    for i in range(len(plots)):
        for token in plots[i]:
            try:
                df[token].add(i)
            except:
                df[token] = {i}
    for token in input:
        try:
                df[token].add(i)
        except:
                df[token] = {i}
    for word in df:
        df[word] = len(df[word])/len(plots)
    return df

def cos_sim(movie, input):
    """
    Input: tf vectors
    Purpose: Calculates the cosine similarity
    Output: cosine similarity
    """
    cos_sim = dot(movie, input)/(norm(movie)*norm(input))
    return cos_sim

moviedb = pd.read_csv('moviedb.csv')
moviedb['plot'] = [preprocess_text(i) for i in moviedb['plot']]

# Input has to be precise in terms of capital letters, spaces and such
movie_input = str(input("Type in movie title: "))
movie_year_input = str(input("(Optional) What year did it come out?: "))
input_plot = get_plot(movie_input, movie_year_input)


input_plot = preprocess_text(input_plot)

df = doc_freq(moviedb['plot'], input_plot)

all_plot_tokens = sum(moviedb['plot'], []) + input_plot

lexicon = sorted(set(all_plot_tokens))

moviedb_vectors = []

for title in moviedb['plot']:
   moviedb_vectors.append(tf_idf(title, lexicon, df))

input_vector = tf_idf(input_plot, lexicon, df)

result_vectors = [cos_sim(i, input_vector) for i in moviedb_vectors]

moviedb['similarity'] = result_vectors

    # Dropping duplicate of the input title (if there's one). This prevents recommending excatly the same title that was
    # used as an input.
moviedb = moviedb.drop(moviedb[moviedb["movie_title"] == (re.sub(r'\s\([^)]*\)', '', movie_input))].index)

print("The recommendations are:")
    # Printing 5 closest titles
print(moviedb.sort_values(by=['similarity'], ascending=False).movie_title.head(5).to_string(index=False))
