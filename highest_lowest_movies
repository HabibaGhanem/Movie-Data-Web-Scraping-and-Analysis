import pandas as pd

sorted_dataset = pd.read_csv('sorted_dataset.csv')
sorted_dataset['Genre'] = sorted_dataset['Genre'].str.split(',')
all_Genres = [genre for genre in sorted_dataset['Genre'] for genre in genre] 
all_Genres
genres_count = pd.Series(all_Genres).value_counts()
most_common_genre = genres_count.idxmax()
print("Most common genre:", most_common_genre)
print("Count:",genres_count[most_common_genre])
