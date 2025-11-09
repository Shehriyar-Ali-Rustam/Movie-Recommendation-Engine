"""
Movie Recommendation System
A content-based movie recommender using TF-IDF and cosine similarity.
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
import base64
import os
import sys

st.markdown("""
<style>
:root {
    --primary: #8A2BE2;  /* Purple accent */
    --secondary: #221F1F;
    --light: #F5F5F1;
    --dark: #000000;
    --accent: #9932CC;  /* Darker purple */
}

.stApp {
    background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                url("data:image/jpeg;base64,{background_image}") !important;
    background-size: cover !important;
    background-attachment: fixed !important;
    color: var(--light) !important;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--primary) !important;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
}

.stMarkdown, label, div, span, .stDataFrame {
    color: var(--light) !important;
    font-family: 'Arial', sans-serif !important;
}

.stSelectbox, .stTextInput, .stSlider {
    background-color: rgba(245, 245, 241, 0.1) !important;
    border-color: var(--primary) !important;
    color: var(--light) !important;
}

.stDataFrame {
    background-color: rgba(34, 31, 31, 0.8) !important;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    border: 1px solid var(--primary);
}

.stDataFrame th {
    background-color: var(--primary) !important;
    color: var(--light) !important;
    font-weight: bold !important;
}

.stDataFrame td {
    background-color: rgba(245, 245, 241, 0.05) !important;
    color: var(--light) !important;
}

.stButton>button {
    background-color: var(--primary) !important;
    color: white !important;
    border-radius: 4px;
    border: none;
    font-weight: bold;
    padding: 0.5rem 1rem;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: var(--accent) !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.recommendation-card {
    background: rgba(34, 31, 31, 0.8);
    border-left: 4px solid var(--primary);
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 0 8px 8px 0;
    transition: all 0.3s ease;
}

.recommendation-card:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

.movie-title {
    color: var(--primary) !important;
    font-weight: bold;
    font-size: 1.1rem;
}

.movie-description {
    color: var(--light) !important;
    opacity: 0.9;
    font-size: 0.95rem;
}

.header-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-bottom: 3px solid var(--primary);
    margin-bottom: 1rem;
}

/* Add some glow effect to purple elements */
.glow {
    text-shadow: 0 0 5px rgba(138, 43, 226, 0.5);
}
</style>
""", unsafe_allow_html=True)

def get_image_base64(path):
    """
    Convert an image file to base64 encoding.

    Args:
        path (str): Path to the image file

    Returns:
        str: Base64 encoded image string

    Raises:
        FileNotFoundError: If the image file doesn't exist
    """
    try:
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        st.error(f"⚠️ Background image not found at: {path}")
        return ""

# Check if background image exists
if os.path.exists("movie.jpeg"):
    background_image = get_image_base64("movie.jpeg")
else:
    background_image = ""
    st.warning("Background image 'movie.jpeg' not found. Using default background.")

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                url("data:image/jpeg;base64,{background_image}") !important;
}}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_movies(csv_path="movies.csv"):
    """
    Load and preprocess the movie dataset.

    Args:
        csv_path (str): Path to the CSV file containing movie data

    Returns:
        tuple: (DataFrame of movies, list of unique genres)

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        SystemExit: If required columns are missing
    """
    if not os.path.exists(csv_path):
        st.error(f"⚠️ Movie dataset not found at: {csv_path}")
        st.info("Please ensure 'movies.csv' is in the same directory as this script.")
        sys.exit(1)

    try:
        movies_df = pd.read_csv(csv_path)

        # Validate required columns
        required_columns = ['title', 'description']
        if not all(col in movies_df.columns for col in required_columns):
            st.error(f"CSV file must contain columns: {required_columns}")
            sys.exit(1)

        # Process genres
        movies_df['genres'] = movies_df['description'].str.split(',').apply(lambda x: [g.strip() for g in x])
        unique_genres_list = sorted({g for gl in movies_df['genres'] for g in gl})

        return movies_df, unique_genres_list
    except Exception as e:
        st.error(f"Error loading movie data: {str(e)}")
        sys.exit(1)

@st.cache_data
def compute_similarity_matrix(movies_df):
    """
    Pre-compute the TF-IDF similarity matrix for better performance.

    Args:
        movies_df (pd.DataFrame): DataFrame containing movie data

    Returns:
        tuple: (similarity_matrix, tfidf_vectorizer)
    """
    # Enhanced TF-IDF with bigrams for better matching
    tfidf = TfidfVectorizer(
        ngram_range=(1, 2),  # Use unigrams and bigrams
        min_df=1,
        stop_words='english'
    )
    tfidf_matrix = tfidf.fit_transform(movies_df['description'])

    # Compute full similarity matrix (cached for performance)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    return similarity_matrix, tfidf

@st.cache_data
def get_hybrid_recommendations(movie_title, movies_df, similarity_matrix, top_n=5,
                               rating_weight=0.3, year_weight=0.1, genre_weight=0.6):
    """
    Get movie recommendations using hybrid approach (genre + rating + recency).

    Args:
        movie_title (str): Title of the movie to base recommendations on
        movies_df (pd.DataFrame): DataFrame containing movie data
        similarity_matrix (np.ndarray): Pre-computed similarity matrix
        top_n (int): Number of recommendations to return
        rating_weight (float): Weight for rating similarity (0-1)
        year_weight (float): Weight for year similarity (0-1)
        genre_weight (float): Weight for genre similarity (0-1)

    Returns:
        pd.DataFrame: DataFrame with top N recommended movies and similarity scores

    Raises:
        ValueError: If movie title is not found
    """
    try:
        # Find index of selected movie
        idx = movies_df[movies_df['title'] == movie_title].index[0]

        # Get genre-based similarity from pre-computed matrix
        genre_sim = similarity_matrix[idx]

        # Normalize ratings and years for similarity calculation
        rating_sim = np.zeros(len(movies_df))
        year_sim = np.zeros(len(movies_df))

        if 'rating' in movies_df.columns and pd.notna(movies_df.iloc[idx]['rating']):
            selected_rating = movies_df.iloc[idx]['rating']
            ratings = movies_df['rating'].fillna(movies_df['rating'].mean())
            # Rating similarity: closer ratings = higher similarity
            rating_diff = np.abs(ratings - selected_rating)
            rating_sim = 1 - (rating_diff / 10.0)  # Normalize to 0-1

        if 'year' in movies_df.columns and pd.notna(movies_df.iloc[idx]['year']):
            selected_year = movies_df.iloc[idx]['year']
            years = movies_df['year'].fillna(movies_df['year'].median())
            # Year similarity: more recent and closer in time = higher similarity
            year_diff = np.abs(years - selected_year)
            year_sim = 1 - (year_diff / 100.0)  # Normalize approximately
            year_sim = np.clip(year_sim, 0, 1)  # Clip to 0-1 range

        # Combine similarities with weights
        combined_sim = (
            genre_weight * genre_sim +
            rating_weight * rating_sim +
            year_weight * year_sim
        )

        # Get indices of top N similar movies (excluding the selected movie)
        sim_scores = list(enumerate(combined_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_idx = [i for i, score in sim_scores if i != idx][:top_n]
        sim_values = [score for i, score in sim_scores if i != idx][:top_n]

        # Create result DataFrame with similarity scores
        result = movies_df.iloc[sim_idx].copy()
        result['similarity_score'] = [round(score * 100, 1) for score in sim_values]

        return result
    except IndexError:
        raise ValueError(f"Movie '{movie_title}' not found in database")

# Load movie data with caching
movies, unique_genres = load_movies()

# Pre-compute similarity matrix for faster recommendations
similarity_matrix, tfidf_vectorizer = compute_similarity_matrix(movies)

st.markdown(
    """
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='margin-bottom: 0.5rem;' class='glow'>
            <span style='color: #8A2BE2;'>CINEMATIC</span> RECOMMENDER
        </h1>
        <p style='color: #F5F5F1; font-size: 1.1rem;'>
            Discover your next favorite movie with AI-powered recommendations
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for advanced options
with st.sidebar:
    st.markdown("### ⚙️ Settings")

    st.markdown("#### Recommendation Weights")
    genre_weight = st.slider("Genre Match", 0.0, 1.0, 0.6, 0.1,
                              help="How much to prioritize genre similarity")
    rating_weight = st.slider("Rating Similarity", 0.0, 1.0, 0.3, 0.1,
                               help="How much to prioritize similar ratings")
    year_weight = st.slider("Release Year", 0.0, 1.0, 0.1, 0.1,
                             help="How much to prioritize movies from similar era")

    num_recommendations = st.slider("Number of Recommendations", 3, 20, 5,
                                    help="How many movies to recommend")

    st.markdown("---")
    st.markdown("#### 📊 Dataset Info")
    st.write(f"**Total Movies:** {len(movies)}")
    st.write(f"**Genres:** {len(unique_genres)}")
    if 'year' in movies.columns:
        st.write(f"**Year Range:** {int(movies['year'].min())} - {int(movies['year'].max())}")

# Top Rated Movies Section
st.markdown("### ⭐ Top Rated Movies")
col1, col2, col3 = st.columns(3)

if 'rating' in movies.columns:
    top_rated = movies.nlargest(9, 'rating')[['title', 'rating', 'year']].reset_index(drop=True)

    for i, (idx, movie_row) in enumerate(top_rated.iterrows()):
        with [col1, col2, col3][i % 3]:
            year_str = f"({int(movie_row['year'])})" if pd.notna(movie_row['year']) else ""
            st.markdown(
                f"""
                <div style='background: rgba(138, 43, 226, 0.1); padding: 0.5rem; border-radius: 5px; margin-bottom: 0.5rem;'>
                    <div style='font-size: 0.9rem; font-weight: bold; color: #8A2BE2;'>{i+1}. {movie_row['title']} {year_str}</div>
                    <div style='font-size: 0.85rem; color: #FFD700;'>⭐ {movie_row['rating']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

st.markdown("---")

# Add search functionality
st.markdown("### 🔍 Search Movies")
search_term = st.text_input("Search by title or director:", "",
                            help="Type to search movies by title or director name", key="search_input")

# Filter by search term
if search_term:
    filtered_by_search = movies[
        movies['title'].str.contains(search_term, case=False, na=False) |
        (movies['director'].str.contains(search_term, case=False, na=False) if 'director' in movies.columns else False)
    ]
    if not filtered_by_search.empty:
        st.success(f"Found {len(filtered_by_search)} movie(s) matching '{search_term}'")
    else:
        st.warning(f"No movies found matching '{search_term}'")
else:
    filtered_by_search = movies

st.markdown("### 🎬 Browse by Genre")
genre = st.selectbox(
    "Filter movies by genre:",
    ["All"] + unique_genres,
    help="Select a genre to filter movies"
)

# Apply both search and genre filters
filtered = filtered_by_search.copy()
if genre != "All":
    filtered = filtered[filtered['genres'].apply(lambda gs: genre in gs)]

if not filtered.empty:
    # Prepare display columns
    display_cols = ['title', 'description']
    rename_dict = {'title': 'Movie Title', 'description': 'Genres'}

    # Add optional columns if they exist
    if 'year' in filtered.columns:
        display_cols.append('year')
        rename_dict['year'] = 'Year'
    if 'rating' in filtered.columns:
        display_cols.append('rating')
        rename_dict['rating'] = 'Rating'
    if 'director' in filtered.columns:
        display_cols.append('director')
        rename_dict['director'] = 'Director'

    st.dataframe(
        filtered[display_cols].rename(columns=rename_dict),
        height=300,
        use_container_width=True
    )
else:
    st.warning("No movies found in this genre. Please select another genre.")

st.markdown("""
    <div style='margin: 2rem 0 1rem 0;'>
        <h3 style='border-bottom: 2px solid #8A2BE2; padding-bottom: 0.5rem;' class='glow'>
            🍿 Get Personalized Recommendations
        </h3>
    </div>
""", unsafe_allow_html=True)

movie = st.selectbox(
    "Select a movie you like:",
    filtered['title'].tolist(),
    index=0 if filtered.empty else None,
    help="Choose a movie to get similar recommendations"
)

if st.button("🎯 Get Recommendations", key="recommend_btn", use_container_width=True):
    if movie:
        try:
            # Use hybrid recommendations with user-configured weights
            recommendations = get_hybrid_recommendations(
                movie, movies, similarity_matrix,
                top_n=num_recommendations,
                rating_weight=rating_weight,
                year_weight=year_weight,
                genre_weight=genre_weight
            )

            st.markdown(
                f"""
                <div style='margin: 1.5rem 0;'>
                    <h4 style='color: #F5F5F1;'>
                        Because you liked <span style='color: #8A2BE2; font-style: italic;' class='glow'>"{movie}"</span>, you might enjoy:
                    </h4>
                </div>
                """,
                unsafe_allow_html=True
            )

            for idx, row in recommendations.iterrows():
                # Build movie info with optional metadata
                movie_info = f"<div class='movie-title glow'>{row['title']}"
                if 'year' in row and pd.notna(row['year']):
                    movie_info += f" ({int(row['year'])})"
                movie_info += "</div>"

                movie_meta = f"<div class='movie-description'>{row['description']}"
                if 'rating' in row and pd.notna(row['rating']):
                    movie_meta += f" • ⭐ {row['rating']}"
                if 'director' in row and pd.notna(row['director']):
                    movie_meta += f" • 🎬 {row['director']}"
                if 'similarity_score' in row:
                    movie_meta += f" • 🎯 {row['similarity_score']}% match"
                movie_meta += "</div>"

                st.markdown(
                    f"""
                    <div class='recommendation-card'>
                        {movie_info}
                        {movie_meta}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        except ValueError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please select a movie first")

st.markdown(
    f"""
    <div style='text-align: center; margin-top: 3rem; padding: 1rem; background: rgba(138, 43, 226, 0.05); border-radius: 10px;'>
        <div style='color: #8A2BE2; font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;'>
            🎬 Advanced AI Movie Recommender
        </div>
        <div style='color: #F5F5F1; opacity: 0.8; font-size: 0.9rem;'>
            Hybrid Content-Based Filtering • TF-IDF with N-grams • {len(movies)} Movies • {len(unique_genres)} Genres
        </div>
        <div style='color: #F5F5F1; opacity: 0.6; font-size: 0.85rem; margin-top: 0.5rem;'>
            Using advanced machine learning for personalized recommendations
        </div>
    </div>
    """,
    unsafe_allow_html=True
)