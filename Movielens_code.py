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
#EXTRACT YEAR FROM MOVIE TITLE AND CONVERT YEAR TO INTEGER
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


