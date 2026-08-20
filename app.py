import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv
load_dotenv()
my_api_key = os.getenv("API_KEY")

movies_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={my_api_key}&language=en-US')
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index=movies[movies["title"]==movie].index[0] 
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movies_list:
        #fetch poster
        movie_id=movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster
              



st.set_page_config(
    page_title="CineSense",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .movie-title {
        text-align: center;
        font-size: 16px;
        font-weight: 600;
        height: 48px;
        margin-top: 10px;
    }

    .stButton > button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem;
    }

    div[data-testid="stImage"] img {
        border-radius: 12px;
        aspect-ratio: 2 / 3;
        object-fit: cover;
    }
</style>
""", unsafe_allow_html=True)



st.markdown('<h1 class="main-title">🎬 CineSense</h1>',
            unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">Discover movies you’ll love.</p>',
    unsafe_allow_html=True
)


selected_movie_name = st.selectbox(
    "🍿 Choose a movie",
    movies["title"].values,
    index=None,
    placeholder="Search or select a movie..."
)


if st.button("✨ Get Recommendations", width="stretch"):

    if selected_movie_name:

        with st.spinner("Finding movies for you..."):
            names, posters = recommend(selected_movie_name)

        st.markdown("## Recommended for you")

        cols = st.columns(5)

        for i, col in enumerate(cols):
            with col:
                st.image(
                    posters[i],
                    width="stretch"
                )

                st.markdown(
                    f'<div class="movie-title">{names[i]}</div>',
                    unsafe_allow_html=True
                )

    else:
        st.warning("Please select a movie first.")