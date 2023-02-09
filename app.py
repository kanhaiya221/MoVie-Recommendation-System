import pickle
import pandas as pd
import streamlit as st
import  requests

###Content based reccomender system##


#################################   Design ########

st.set_page_config(layout="wide")
st.title('Movie Recommendation Engine')

# title_alignment

st.markdown("""
<style>
#movie-recommendation-engine {
  text-align: center
}
</style>
""" , unsafe_allow_html=True)

#####################Background Image###############################



def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2019/04/24/11/27/flowers-4151900_960_720.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()




#####################################

#Function to Fetch poster
def fetch_poster(movie_id):
     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bb72e2ad94c7607106096b9b7e92e62f&language=en-US'.format(movie_id))
     data = response.json()

     return "https://image.tmdb.org/t/p/original" + data['poster_path']



#Movies reccomendation function
def recommendation(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    reccommended_movies = []
    reccommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        #fech poster from API
        reccommended_movies.append(movies.iloc[i[0]].title)
        reccommended_movies_posters.append(fetch_poster(movie_id))
    return reccommended_movies , reccommended_movies_posters


#Movies list to shown to user

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)

#Featching similarity index

similarity = pickle.load(open('similarity.pkl', 'rb'))


#Drop down menu for selection of movie name

selected_movie_name  = st.selectbox(
    'Select the movie you like?',
    movies['title'])

################################################
st.markdown( """
<style>
.reportview-container .markdown-text-container {
    font-family: monospace;
}
.css-184tjsw p {
    color: dimgray;
    font-family: fantasy;
    font-size: 25px;
}
</style>
""",
    unsafe_allow_html=True,
)

########################################

#Button for action of recommendation
if st.button('Reccomend'):
    recommendations , posters  = recommendation(selected_movie_name)

    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        st.success(recommendations[0])
        st.image(posters[0])

    with col2:
        st.info(recommendations[1])
        st.image(posters[1])

    with col3:
        st.success(recommendations[2])
        st.image(posters[2])

    with col4:
        st.info(recommendations[3])
        st.image(posters[3])

    with col5:
        st.success(recommendations[4])
        st.image(posters[4])







