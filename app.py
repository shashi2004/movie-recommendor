import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=c71f54268029fc25af73a64e75906b63&language=en-US'
    )
    data = response.json()  # ✅ parentheses added
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        # fetch poster from API
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies,recommended_movie_posters


movies_dict = pickle.load(open('movies_dict.pkl','rb'))

movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values
)

if st.button('Recommend'):
     names,posters = recommend(selected_movie_name)

     col1, col2, col3, col4, col5 = st.columns(5)

     cols = [col1, col2, col3, col4, col5]
     for i in range(5):
         with cols[i]:
             st.image(posters[i])
             st.markdown(
                 f"""
                 <p style='
                     font-size:13px; 
                     text-align:center; 
                     word-wrap:break-word; 
                     overflow-wrap:break-word;
                     max-width:120px; 
                     margin:auto;
                 '>{names[i]}</p>
                 """,
                 unsafe_allow_html=True
             )
