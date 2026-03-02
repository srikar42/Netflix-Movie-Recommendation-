import streamlit as st
import pandas as pd
import numpy as np
import joblib

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Netflix Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)


# -------------------- CUSTOM CSS --------------------

st.markdown("""
<style>
body {
    background-color: #0E1117;
}

.stApp {
    background-color: #0E1117;
}

h1 {
    color: #E50914;
    text-align: center;
    font-size: 50px;
    font-weight: bold;
}

.stSelectbox label {
    color: white !important;
    font-size: 18px;
}

/* Selectbox black background */
div[data-baseweb="select"] > div {
    background-color: #1c1c1c !important;
    color: white !important;
    border-radius: 10px;
}

div[data-baseweb="select"] input {
    color: white !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #ff2a2a;
    color: white;
}

.movie-title {
    font-size: 16px;
    font-weight: bold;
    text-align: center;
    color: white;
    margin-top: 10px;
}

/* Only animate recommendation posters */
[data-testid="stImage"] img {
    border-radius: 15px;
}

.recommend-img img {
    transition: transform 0.3s ease-in-out;
}

.recommend-img img:hover {
    transform: scale(1.05);
}
""", unsafe_allow_html=True)

# -------------------- LOAD SIMILARITY --------------------
@st.cache_resource
def load_similarity():
    return joblib.load('moviesimilarity.pkl')

similarity = load_similarity()

# -------------------- LOAD DATA --------------------
df = pd.read_csv('tmdbdf.csv')
df = df.head(2000)

# -------------------- HEADER IMAGE --------------------
#st.image('image.webp', width=800)

col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.image('image.webp', width=900)

st.title("🎬 Netflix Movie Recommendation")

# -------------------- MOVIE SELECTION --------------------
movie_name = st.selectbox(
    'Select a Movie',
    df['title'].values
)

# -------------------- RECOMMEND FUNCTION --------------------
def recommend(movie):
    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        recommended_movies.append(df.iloc[i[0]].title)
        poster_path = df.iloc[i[0]]['poster_path']

        if pd.notnull(poster_path):
            recommended_posters.append(
                "https://image.tmdb.org/t/p/w500/" + poster_path
            )
        else:
            recommended_posters.append(
                "https://via.placeholder.com/500x750?text=No+Poster"
            )

    return recommended_posters, recommended_movies

# -------------------- BUTTON ACTION --------------------
if st.button("🎥 Show Recommendations"):

    posters, names = recommend(movie_name)

    st.markdown("## ✨ Top 5 Similar Movies")

    cols = st.columns(5, gap="large")

    for idx, col in enumerate(cols):
        with col:
            st.markdown("<div class='recommend-img'>", unsafe_allow_html=True)
            st.image(posters[idx], use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='movie-title'>{names[idx]}</div>",
                unsafe_allow_html=True
            )