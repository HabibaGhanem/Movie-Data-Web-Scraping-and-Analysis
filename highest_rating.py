import pandas as pd

sorted_dataset = pd.read_csv('sorted_dataset.csv')
top_rated_movies = sorted_dataset.head(1)
top_rated_movies


lowest_rated_movie = sorted_dataset.tail(1)
lowest_rated_movie
