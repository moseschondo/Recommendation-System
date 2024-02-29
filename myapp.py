import streamlit as st
# import pickle as pkl
import pandas as pd
# import numpy as np
import warnings

warnings.filterwarnings("ignore")

st.sidebar.image("mm.jpg", width=100)

st.sidebar.header("About this app:")
st.sidebar.write("""This is my first data app. \n
This app helps in recommending movies to Users whereby a user enters the title of the movie he/she knows. 
And clicks the search button to see recommendations.\n 
The correlation shows how the recommended movies are related to the one searched in a scale of -1 to 1 where one indicated almost 
similar and -1 indicates dissimilar movies. \n
 I'm still working on it, I'm trying to find a good dataset that will have most of the popular movies and an
API which  will add the movies stickers and a link from which the users can to download the movies.
""")

# Loading the data
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

movie_df = movies.merge(ratings, on="movieId")

dataframe = pd.DataFrame(movie_df)

st.title("MOVIE RECOMMENDATION SYSTEM")
# title = st.text_input("Enter the movie title: ")

movie_ratings = pd.DataFrame(dataframe.groupby("title")["rating"].mean())
movie_ratings["no' of ratings"] = pd.DataFrame(dataframe.groupby("title")["rating"].count())
movie_ratings.head()

# movie_matrix = dataframe.pivot_table(index="userId", columns="title", values="rating")
movie_name = st.text_input("Enter the movie title: ")
if not movie_name:
    st.write("No title is provided")
    exit()


def recommend():
    movie_matrix = dataframe.pivot_table(index="userId", columns="title", values="rating")
    movie_title = movie_matrix[movie_name]
    similar_to_movie_title = movie_matrix.corrwith(movie_title)
    corr_movie_title = pd.DataFrame(similar_to_movie_title, columns=["Correlation"])
    corr_movie_title.dropna(inplace=True)
    corr_movie_title.sort_values("Correlation", ascending=False)
    filtering = corr_movie_title.join(movie_ratings["no' of ratings"])
    recommended = corr_movie_title[filtering["no' of ratings"] > 10].sort_values("Correlation", ascending=False).head()
    return recommended


recommend()

if st.button("Search"):
    output = recommend()
    st.write(output)
