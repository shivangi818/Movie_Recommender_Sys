import streamlit as st
import pickle
import requests
import streamlit.components.v1 as components

# Function to fetch poster using OMDb API
def fetch_poster(movie_title, api_key="32d7c8bb"):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        data = response.json()
        poster_url = data.get('Poster')
        if poster_url and poster_url != "N/A":  # Check if URL is valid
            return poster_url
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster from OMDb: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"

# Load the movie list and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Set page configuration to wide
st.set_page_config(page_title="Movie Recommender System", layout="wide")

# Custom CSS for full-screen display
st.markdown(
    """
    <style>
    .css-1v3fvcr {  /* Class for main container */
        max-width: 100% !important;
        padding: 0 !important;
    }
    .css-1v3fvcr .stApp {
        margin: 0 auto;
        width: 100vw;
        height: 100vh;
    }
    .css-1v3fvcr .stImage img {
        max-width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Movie Recommender System")

# Correctly declare the component
imageCarouselComponent = components.declare_component("image-carousel-component", path=r"C:\Users\shiva\OneDrive\Desktop\new recom\frontend\public")

# Fetch posters for the image carousel
imageUrls = [
    fetch_poster("The Shawshank Redemption"),
    fetch_poster("The Godfather"),
    fetch_poster("The Dark Knight"),
    fetch_poster("Pulp Fiction"),
    fetch_poster("The Lord of the Rings: The Return of the King"),
    fetch_poster("Forrest Gump"),
    fetch_poster("Inception"),
    fetch_poster("Fight Club"),
    fetch_poster("The Matrix"),
    fetch_poster("The Empire Strikes Back"),
    fetch_poster("Interstellar"),
    fetch_poster("The Departed"),
    fetch_poster("Gladiator")
]

# Use the component
imageCarouselComponent(imageUrls=imageUrls, height=300)  # Adjust height as needed

selectvalue = st.selectbox("Select movie from dropdown", movies_list)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommend_movie.append(movie_title)
        poster_url = fetch_poster(movie_title)
        recommend_poster.append(poster_url)
    return recommend_movie, recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])

