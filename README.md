# Exploratory Data Analysis (EDA) on MovieLens-Dataset
## EXECUTIVE SUMMARY
In this project stage, i successfully ingested and explored the MovieLens dataset, extracting valuable features and insights that will inform a movie recommendation system. I merged disparate data sources (movies, ratings, tags) and created new columns (such as release year, time of rating, genre counts, and tag counts) to enrich the information available for each user-movie interaction using python.

### Dataset Description:
The dataset consists of four CSV files:
1. ratings.csv: Contains user ratings for movies. Each record includes:
userId: User identifier.
movieId: Movie identifier.
rating: Rating given (from 0.5 to 5).
timestamp: Timestamp of the rating.

2. movies.csv: Contains metadata for each movie. Each record includes:
movieId: Movie identifier.
title: Movie title with the release year in parentheses (e.g., Toy Story (1995)).
genres: Pipe-separated list of genres (e.g., Adventure|Animation|Children|Comedy|Fantasy).

3. tags.csv: Contains user-generated tags for movies. Each record includes:
userId: User identifier.
movieId: Movie identifier.
tag: Tag applied by the user.
timestamp: Timestamp of when the tag was applied.

4.links.csv: Contains mappings between movieId and external database identifiers (IMDb and TMDb). Each record includes:
movieId: Movie identifier.
imdbId: IMDb movie identifier.
tmdbId: TMDb movie identifier.

### Feature Engineering
Several features were engineered from the raw data to enhance analysis and support recommendation models:
Release Year: Extracted from the movie title using a regular expression to get the four-digit year in parentheses.
Title without Year: A cleaned version of the movie title without the release year.
Timestamp Features: Converted Unix timestamps into datetime format, extracting year, month, day of week, and hour of day from the timestamp.
Genre Count: The number of genres associated with each movie.
Multi-Genre Indicator: A binary flag indicating whether a movie belongs to more than one genre.


