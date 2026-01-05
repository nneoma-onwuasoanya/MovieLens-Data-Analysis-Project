# Step 1: Importing Data
import pandas as pd

ratings = pd.read_csv("ratings.csv")
movies  = pd.read_csv("movies.csv")
tags    = pd.read_csv("tags.csv")
links   = pd.read_csv("links.csv")
#checking imported data
movies.head(), ratings.head(), tags.head(), links.head()

# Step 2: Check for Duplicate and Missing values
#check for missing values
ratings.isnull()
movies.isnull()
tags.isnull()
links.isnull()
#Drop duplicate
movies = movies.drop_duplicates().copy()
tags = tags.drop_duplicates().copy()
links = links.drop_duplicates().copy()

# STEP 3: CONVERT TIMESTAMP
ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')
#chek ratings and movie index
print(movies.columns)
print(ratings.columns)

# STEP 4: MERGE RATINGS AND MOVIES USING MOVIEID
df = ratings.merge(movies, on="movieId")
#check merginging
df.head()

# STEP 5: FEATURE ENGINEERING
#import libraries
import re
import numpy as np

1. #EXTRACT YEAR FROM MOVIE TITLE AND CONVERT YEAR TO INTEGER
 def extract_year_from_title(title):
    m = re.search(r'\((\d{4})\)$', str(title))
    if m:
        year = int(m.group(1))
        if 1874 <= year <= pd.Timestamp.now().year + 1:  # sanity check
            return year
    #remove year from title
def strip_year_from_title(title):
    return re.sub(r'\s*\(\d{4}\)\s*$', '', str(title)).strip()
#create column for extracted year and title without year
df['extracted_year'] = df['title'].apply(extract_year_from_title).astype('Int64')
df['title_without_year'] = df['title'].apply(strip_year_from_title)
#viw new columns
df[['title','extracted_year','title_without_year']].head()

#DEFINE THE GENRES, SPLIT WHERE '|'
def split_genres(g):
    return str(g).split('|')
 
 2. #COUNT AND CREATE NUMBER OF GENRES AND MULTI GENRE COLUMN
df['number_genres'] = df['genres'].apply(lambda g: len(split_genres(g))).astype('Int64')
df['multi_genre'] = (df['number_genres'] > 1).astype(int)
#VIEW NEW COLUMN ( NUMBER_GENRES AND MULTI_GENRE)
df[['genres','number_genres','multi_genre']].head()

3. #EXTRACT YEAR, MONTH, DAY OF THE WEEK AND HOUR FROM TIMESTAMP, NEW COLUMNS
df['rating_year']  = df['timestamp'].dt.year
df['rating_month'] = df['timestamp'].dt.month
df['rating_dow']   = df['timestamp'].dt.dayofweek   # 0=Monday
df['rating_hour']  = df['timestamp'].dt.hour
#check columns
df[['timestamp','rating_year','rating_month','rating_dow','rating_hour']].head()

4. #COUNT HOW MANY TAGS EACH MOVIE HAS AND CREATED A COLUMN
tag_counts = tags.groupby('movieId', as_index=False)['tag'].count().rename(columns={'tag':'tag_count'})
#MERGE WITH MOVIE DATA USING MOVIEID
df = df.merge(tag_counts, on='movieId', how='left')
#REPLACE MISSING VALUES AND CONVERT TO INTEGERS
df['tag_count'] = df['tag_count'].fillna(0).astype(int)
#view column
df[['movieId','title','tag_count']].head()

5. #TOP 10 MOST RATED MOVIE
top_movies = (
    df.groupby('title_without_year')['rating']
      .count()
      .sort_values(ascending=False)
      .head(10)
)

top_movies

# Finalize types
num_cols = ['number_genres','multi_genre','rating_year','rating_month','rating_dow','rating_hour','tag_count']
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# STEP 6: EXPLORATORY DATA ANALYSIS
import matplotlib.pyplot as plt

plt.figure(figsize=(6,4))
df['rating'].hist(bins=[0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,], edgecolor='black',color='blue')
plt.title("Distribution of Ratings")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.show()

year_avg = df.groupby('rating_year')['rating'].mean()

plt.figure(figsize=(7,4))
year_avg.plot(kind='line', marker='o', color='darkorange')
plt.title("Average Rating by Rating Year")
plt.xlabel("Rating Year")
plt.ylabel("Average Rating")
plt.show()

year_avg.head()

dow_avg = df.groupby('rating_dow')['rating'].mean()

plt.figure(figsize=(6,4))
dow_avg.plot(kind='bar', color='darkgreen')
plt.title("Average Rating by Day of Week (0=Mon ... 6=Sun)")
plt.xlabel("Day of the Week")
plt.ylabel("Average Rating")
plt.show()

dow_avg

multi_vs_single = df.groupby('multi_genre')['rating'].mean()

plt.figure(figsize=(5,3))
multi_vs_single.plot(kind='bar', color='darkred')
plt.title("Average Rating: Single vs Multi-Genre")
plt.xlabel("0 = Single Genre, 1 = Multi-Genre")
plt.ylabel("Average Rating")
plt.show()

multi_vs_single

release_year_avg = df.groupby('extracted_year')['rating'].mean().dropna()

plt.figure(figsize=(8,4))
release_year_avg.plot(kind='line', marker='o', color='purple')
plt.title("Average Movie Rating by Release Year")
plt.xlabel("Release Year")

plt.figure(figsize=(8,4))
top_movies.plot(kind='bar', color='brown')
plt.title("Top 10 Most Rated Movies")
plt.xlabel("Movie Title")
plt.ylabel("Number of Ratings")
plt.show()

# STEP 7: EXPORT CLEANED DATA
df.to_csv('cleaned_movielens_with_features.csv', index=False)

