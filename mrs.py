import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PIL import Image
import base64

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
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
background_image = get_image_base64("movie.jpeg")

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0, 0, 0, 0.85), rgba(0, 0, 0, 0.85)), 
                url("data:image/jpeg;base64,{background_image}") !important;
}}
</style>
""", unsafe_allow_html=True)

movies = pd.read_csv("movies.csv")
movies['genres'] = movies['description'].str.split(',').apply(lambda x: [g.strip() for g in x])
unique_genres = sorted({g for gl in movies['genres'] for g in gl})

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

st.markdown("### 🎬 Find Movies by Genre")
genre = st.selectbox(
    "Browse movies by genre:",
    ["All"] + unique_genres,
    help="Select a genre to filter movies"
)

filtered = movies if genre == "All" else movies[movies['genres'].apply(lambda gs: genre in gs)]

if not filtered.empty:
    st.dataframe(
        filtered[['title', 'description']].rename(columns={'title': 'Movie Title', 'description': 'Description'}),
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

if st.button("Get Recommendations", key="recommend_btn"):
    if movie:
        tfidf = TfidfVectorizer().fit_transform(movies['description'])
        idx = movies[movies['title'] == movie].index[0]
        sim = cosine_similarity(tfidf[idx], tfidf).flatten()
        sim_idx = [i for i in sim.argsort()[::-1] if i != idx][:5]
        
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
        
        for _, row in movies.iloc[sim_idx].iterrows():
            st.markdown(
                f"""
                <div class='recommendation-card'>
                    <div class='movie-title glow'>{row['title']}</div>
                    <div class='movie-description'>{row['description']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Please select a movie first")

st.markdown(
    """
    <div style='text-align: center; margin-top: 3rem; color: #F5F5F1; opacity: 0.7; font-size: 0.9rem;'>
        Powered by AI Recommendation Engine • Content-Based Filtering
    </div>
    """,
    unsafe_allow_html=True
)