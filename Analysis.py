import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def cat(x): 
    if ((x >= 0) & (x < 2)):
        return "0-2"
    elif ((x >= 2) & (x < 4)):
        return "2-4"
    elif ((x >= 4) & (x < 6)):
        return "4-6"
    elif ((x >= 6) & (x < 8)):
        return "6-8"
    else:
        return "8-10"

#read data
movie_meter_df =pd.read_csv('moviemeter_data.csv')
IMDb_df =pd.read_csv('IMDb_data.csv')

#explore data
print(movie_meter_df.head())
print(movie_meter_df.info())

#Data Cleaning
for i, rating in enumerate(movie_meter_df['MoviemeterRating']):  
     rating = rating.replace("," , ".")
     movie_meter_df['MoviemeterRating'][i] = rating
     

movie_meter_df['MoviemeterRating'] = list(map(float,movie_meter_df['MoviemeterRating']))
print(movie_meter_df.info())


#Merging the datasets
Merged_data = movie_meter_df.merge(IMDb_df.drop('ReleaseYear', axis=1), on='Title')
Merged_data.to_csv('merged_movie_data.csv', index=False)



#read data
Merged_data_df =pd.read_csv('merged_movie_data.csv')

#The number of movies released in each decade
movies_count_for_decade = Merged_data_df.groupby('ReleaseYear')['Title'].count()
print(movies_count_for_decade)

#Distribution of ratings
Merged_data_df['IMDbRating_Category'] = list(map(cat,Merged_data_df['IMDbRating']))
Merged_data_df.groupby('IMDbRating_Category')['Title'].count().plot(kind = "bar") 
# Show the plot
plt.show()

Merged_data_df['MoviemeterRating_Category'] = list(map(cat,Merged_data_df['MoviemeterRating']))
Merged_data_df.groupby('MoviemeterRating_Category')['Title'].count().plot(kind = "bar") 
plt.show()

#Distribution of movie genres
Merged_data_df.groupby('Genre')['Title'].count().plot(kind = "bar") 













