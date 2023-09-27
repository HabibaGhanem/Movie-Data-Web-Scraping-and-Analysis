import pandas as pd

#merged_dataset
movie_dataset = pd.read_csv('/content/moviemeter_data.csv')
imdb_dataset = pd.read_csv('/content/IMDb_data.csv')
merged_dataset = pd.merge(movie_dataset,imdb_dataset, on='ReleaseYear')
merged_dataset.to_csv('merged_dataset.csv', index = False)
merged_dataset.head(20)

#sorted_dataset

merged_dataset = pd.read_csv('/content/merged_movie_data.csv')
sorted_dataset = merged_dataset.sort_values(by = ['Title', 'MoviemeterRating', 'IMDbRating'])
sorted_dataset.reset_index(drop=True)
sorted_dataset.to_csv('sorted_dataset.csv',index=False)

#Remove duplicated rows
deduplicated_dataset = sorted_dataset.drop_duplicates()
deduplicated_rows = deduplicated_dataset[deduplicated_dataset.duplicated()]
if not deduplicated_rows.empty:
  print("Duplicated rows found")
  print(deduplicated_rows)
else:
  print("no")