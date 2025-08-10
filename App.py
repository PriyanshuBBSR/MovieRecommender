import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create a session with retry logic
session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = session.get(url)
    data = data.json()
    poster_path = data.get('poster_path')
    full_path = f"https://image.tmdb.org/t/p/w300/{poster_path}"
    return full_path

def recommend(movie):
    movie_index=movies[movies.title==movie].index[0]
    distances=sorted(list(enumerate(similarity[movie_index])),reverse=True, key=lambda x:x[1])
    recommended=[]
    recommended_posters=[]
    for i in distances[1:6]:
        movie_id=movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        #fetch posters
        recommended_posters.append(fetch_poster(movie_id))
    return recommended ,recommended_posters


movies_dict=pickle.load(open('movies.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender')
selected_movie_name = st.selectbox(
"Which Movie You wanna watch?",
movies['title'].values
)
if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters=recommend(selected_movie_name)
    col1, col2, col3,col4,col5= st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])