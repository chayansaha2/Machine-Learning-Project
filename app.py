import pickle
import streamlit as st
import requests
import pandas as pd

#test
# ---------------- BACKGROUND FUNCTION ---------------- #
def set_bg(url):
    st.markdown(
        f"""
        <style>
        /* Base app styling */
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
                              url("{url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        /* Typography colors - targeted to prevent breaking widgets */
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp p, .stApp label {{
            color: #ffffff !important;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }}

        /* --- Aesthetic Dropdown/Selectbox Tuning --- */
        /* Main input box */
        div[data-baseweb="select"] > div {{
            background-color: rgba(255, 255, 255, 0.15) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
        }}

        /* Input text inside the box */
        div[data-baseweb="select"] div {{
            color: #ffffff !important;
        }}

        /* The dropdown menu container */
        ul[role="listbox"] {{
            background-color: rgba(20, 20, 20, 0.85) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }}

        /* Individual items inside the dropdown list */
        ul[role="listbox"] li {{
            color: #ffffff !important;
            background-color: transparent !important;
            transition: background 0.2s ease;
        }}

        /* Hover state for list options */
        ul[role="listbox"] li:hover {{
            background-color: rgba(255, 75, 75, 0.6) !important;
            color: #ffffff !important;
        }}

        /* --- Button Styling --- */
        .stButton>button {{
            background-color: #ff4b4b;
            color: white !important;
            border: none;
            border-radius: 8px;
            height: 3em;
            width: 100%;
            font-size: 16px;
            font-weight: bold;
            box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.3);
            transition: all 0.3s ease;
        }}

        .stButton>button:hover {{
            background-color: #ff3333;
            transform: translateY(-2px);
            box-shadow: 0px 6px 20px rgba(255, 75, 75, 0.5);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------- FETCH POSTER ---------------- #
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"


# ---------------- RECOMMEND FUNCTION ---------------- #
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),
                       reverse=True,
                       key=lambda x: x[1])

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# ---------------- DEFAULT BACKGROUND ---------------- #
# Placed early so layout initializes cleanly
set_bg("https://image.tmdb.org/t/p/original/qJ2tW6WMUDux911r6m7haRef0WH.jpg")

# ---------------- UI TITLE ---------------- #
st.markdown(
    "<h1 style='text-align: center; margin-bottom: 20px;'>🎬 Movie Recommender System</h1>",
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ---------------- #
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
movie_list = movies['title'].values

selected_movie = st.selectbox(
    "Type or select a movie",
    movie_list
)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- BUTTON & RECOMMENDATIONS ---------------- #
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    if posters:
        # Dynamic background change
        set_bg(posters[0])

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]

        for idx, col in enumerate(cols):
            with col:
                st.image(posters[idx])
                # Aesthetic text wrap layout for movie titles
                st.markdown(f"<p style='text-align:center; font-size:14px; font-weight:500;'>{names[idx]}</p>",
                            unsafe_allow_html=True)
    else:
        st.error("Movie not found!")

# ---------------- HIDE FOOTER ---------------- #
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)