# Step 1: Importing Data
import pandas as pd

ratings = pd.read_csv("ratings.csv")
movies  = pd.read_csv("movies.csv")
tags    = pd.read_csv("tags.csv")
links   = pd.read_csv("links.csv")
#checking imported data
movies.head(), ratings.head(), tags.head(), links.head()
