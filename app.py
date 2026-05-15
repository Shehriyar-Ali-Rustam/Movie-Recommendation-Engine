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

st.set_page_config(
    page_title="Cinematic — AI Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# MODERN 2026 UI — Glassmorphism, gradient mesh, micro-interactions
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
/* ───── Design tokens ───── */
:root {
    --bg-0: #07060c;
    --bg-1: #0d0b18;
    --bg-2: #14111f;
    --surface: rgba(20, 17, 31, 0.55);
    --surface-hi: rgba(30, 26, 46, 0.72);
    --border: rgba(255, 255, 255, 0.08);
    --border-hi: rgba(255, 255, 255, 0.16);

    --text: #f5f3ff;
    --text-dim: #b9b4d0;
    --text-mute: #7d7895;

    --accent: #a78bfa;          /* violet-400 */
    --accent-2: #f472b6;         /* pink-400 */
    --accent-3: #38bdf8;         /* sky-400 */
    --accent-warm: #fbbf24;      /* amber-400 */

    --gradient-primary: linear-gradient(135deg, #a78bfa 0%, #f472b6 50%, #fb923c 100%);
    --gradient-cool: linear-gradient(135deg, #38bdf8 0%, #a78bfa 100%);
    --gradient-glass: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));

    --shadow-lg: 0 24px 60px -12px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.04);
    --shadow-glow: 0 0 30px rgba(167, 139, 250, 0.25);

    --radius-sm: 10px;
    --radius: 16px;
    --radius-lg: 22px;
    --radius-xl: 28px;
}

/* ───── App canvas ───── */
.stApp {
    background:
        radial-gradient(1200px 700px at 80% -10%, rgba(244, 114, 182, 0.18), transparent 60%),
        radial-gradient(900px 600px at -10% 20%, rgba(56, 189, 248, 0.16), transparent 55%),
        radial-gradient(800px 500px at 50% 110%, rgba(167, 139, 250, 0.22), transparent 60%),
        var(--bg-0) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Animated noise/grain overlay for filmic texture */
.stApp::before {
    content: "";
    position: fixed; inset: 0;
    pointer-events: none;
    background-image: url("data:image/svg+xml;utf8,<svg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3'/></filter><rect width='100%25' height='100%25' filter='url(%23n)' opacity='0.5'/></svg>");
    opacity: 0.035;
    z-index: 0;
    mix-blend-mode: overlay;
}

/* Main content above grain */
.block-container { position: relative; z-index: 1; padding-top: 2rem !important; max-width: 1280px !important;}

/* ───── Typography ───── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', 'Inter', sans-serif !important;
    color: var(--text) !important;
    letter-spacing: -0.02em !important;
    font-weight: 700 !important;
}

p, label, span, div, .stMarkdown {
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden !important; }

/* ───── Hero ───── */
.hero {
    position: relative;
    text-align: center;
    padding: 3.5rem 1.5rem 2.5rem;
    margin-bottom: 1.5rem;
    border-radius: var(--radius-xl);
    background: var(--gradient-glass);
    border: 1px solid var(--border);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; inset: -2px;
    background: conic-gradient(from 180deg at 50% 50%, rgba(167,139,250,0.0), rgba(244,114,182,0.3), rgba(56,189,248,0.0), rgba(167,139,250,0.4), rgba(167,139,250,0.0));
    filter: blur(40px);
    opacity: 0.5;
    z-index: -1;
    animation: rotate 18s linear infinite;
}
@keyframes rotate { to { transform: rotate(360deg); } }

.hero-eyebrow {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--border-hi);
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim) !important;
    margin-bottom: 1.25rem;
    backdrop-filter: blur(10px);
}
.hero-eyebrow .dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #34d399;
    box-shadow: 0 0 8px #34d399;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

.hero h1 {
    font-size: clamp(2.5rem, 6vw, 4.5rem) !important;
    line-height: 1.05 !important;
    margin: 0 0 0.75rem 0 !important;
    font-weight: 800 !important;
}
.hero h1 .grad {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
}
.hero p.lede {
    font-size: clamp(1rem, 1.5vw, 1.2rem);
    color: var(--text-dim) !important;
    max-width: 640px;
    margin: 0 auto !important;
    line-height: 1.6;
}

/* ───── Section headings ───── */
.section-title {
    display: flex; align-items: center; gap: 12px;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin: 2.25rem 0 1rem 0 !important;
}
.section-title .bar {
    width: 4px; height: 22px;
    background: var(--gradient-primary);
    border-radius: 2px;
}
.section-title .count {
    margin-left: auto;
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text-mute) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ───── Glass card primitive ───── */
.glass {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}
.glass:hover {
    background: var(--surface-hi);
    border-color: var(--border-hi);
    transform: translateY(-2px);
}

/* ───── Top-rated grid cards ───── */
.top-card {
    position: relative;
    padding: 1.1rem 1.2rem;
    margin-bottom: 0.85rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden;
}
.top-card::before {
    content: "";
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--gradient-primary);
    opacity: 0.5;
    transition: opacity 0.3s;
}
.top-card:hover {
    transform: translateY(-3px);
    border-color: var(--border-hi);
    box-shadow: var(--shadow-lg);
}
.top-card:hover::before { opacity: 1; }
.top-card .rank {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem;
    color: var(--text-mute) !important;
    letter-spacing: 0.08em;
}
.top-card .title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.02rem;
    font-weight: 600;
    color: var(--text) !important;
    margin: 4px 0 6px 0;
    line-height: 1.3;
}
.top-card .meta {
    display: flex; align-items: center; gap: 10px;
    font-size: 0.82rem;
    color: var(--text-dim) !important;
}
.top-card .rating-chip {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 2px 9px;
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.18), rgba(251, 191, 36, 0.08));
    border: 1px solid rgba(251, 191, 36, 0.3);
    border-radius: 999px;
    color: #fbbf24 !important;
    font-weight: 600;
    font-size: 0.78rem;
}

/* ───── Recommendation cards ───── */
.rec-card {
    position: relative;
    padding: 1.4rem 1.5rem;
    margin: 0.7rem 0;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    overflow: hidden;
    animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) backwards;
}
@keyframes slideUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.rec-card::before {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(120deg, rgba(167,139,250,0.0) 0%, rgba(167,139,250,0.06) 50%, rgba(244,114,182,0.0) 100%);
    opacity: 0;
    transition: opacity 0.4s;
    pointer-events: none;
}
.rec-card:hover {
    transform: translateX(4px);
    border-color: rgba(167, 139, 250, 0.4);
    box-shadow: var(--shadow-lg), var(--shadow-glow);
}
.rec-card:hover::before { opacity: 1; }

.rec-card .rec-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.25rem !important;
    font-weight: 700;
    color: var(--text) !important;
    margin-bottom: 0.5rem;
    letter-spacing: -0.01em;
}
.rec-card .rec-title .year {
    color: var(--text-mute) !important;
    font-weight: 500;
    font-size: 1rem;
}
.rec-card .rec-meta {
    display: flex; flex-wrap: wrap; gap: 8px;
    margin-top: 0.6rem;
}
.chip {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 11px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid var(--border);
    color: var(--text-dim) !important;
}
.chip.genre { background: rgba(167, 139, 250, 0.12); border-color: rgba(167, 139, 250, 0.28); color: #c4b5fd !important; }
.chip.rating { background: rgba(251, 191, 36, 0.12); border-color: rgba(251, 191, 36, 0.3); color: #fbbf24 !important; }
.chip.director { background: rgba(56, 189, 248, 0.1); border-color: rgba(56, 189, 248, 0.28); color: #7dd3fc !important; }
.chip.match { background: linear-gradient(135deg, rgba(244,114,182,0.15), rgba(167,139,250,0.15)); border-color: rgba(244, 114, 182, 0.35); color: #f9a8d4 !important; font-weight: 600; }

/* Score ring on the right */
.rec-row { display: flex; align-items: center; justify-content: space-between; gap: 1rem; }
.score-pill {
    flex-shrink: 0;
    display: inline-flex; align-items: baseline; gap: 4px;
    padding: 8px 14px;
    border-radius: var(--radius-sm);
    background: var(--gradient-primary);
    color: white !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700;
    font-size: 0.95rem;
    box-shadow: 0 6px 20px rgba(167, 139, 250, 0.35);
}
.score-pill .pct { font-size: 0.7rem; opacity: 0.85; }

/* ───── Streamlit widget overrides ───── */
/* Selectbox */
div[data-baseweb="select"] > div {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    backdrop-filter: blur(20px) !important;
    color: var(--text) !important;
    transition: all 0.25s ease !important;
    min-height: 48px !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(167, 139, 250, 0.5) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
}
div[data-baseweb="popover"] {
    background: var(--bg-2) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-lg) !important;
}
ul[role="listbox"] li:hover { background: rgba(167, 139, 250, 0.12) !important; }

/* Text input */
.stTextInput input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Inter', sans-serif !important;
    backdrop-filter: blur(20px);
    transition: all 0.25s ease !important;
    min-height: 48px !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.15) !important;
}
.stTextInput input::placeholder { color: var(--text-mute) !important; }

/* Sliders */
.stSlider [data-baseweb="slider"] > div > div { background: var(--gradient-primary) !important; }
.stSlider [role="slider"] {
    background: white !important;
    border: 2px solid var(--accent) !important;
    box-shadow: 0 4px 12px rgba(167, 139, 250, 0.4) !important;
}

/* Buttons */
.stButton > button {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.5rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 10px 30px -8px rgba(167, 139, 250, 0.5), 0 0 0 1px rgba(255, 255, 255, 0.08) inset !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: ""; position: absolute; inset: 0;
    background: linear-gradient(120deg, transparent 30%, rgba(255,255,255,0.25) 50%, transparent 70%);
    transform: translateX(-100%);
    transition: transform 0.6s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 40px -8px rgba(167, 139, 250, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.12) inset !important;
}
.stButton > button:hover::before { transform: translateX(100%); }
.stButton > button:active { transform: translateY(0); }

/* DataFrame */
.stDataFrame {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
    background: var(--surface) !important;
    backdrop-filter: blur(20px);
}
.stDataFrame [data-testid="stTable"] { background: transparent !important; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(13, 11, 24, 0.92), rgba(7, 6, 12, 0.92)) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: blur(30px) !important;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem !important; }
section[data-testid="stSidebar"] h3, section[data-testid="stSidebar"] h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: var(--border) !important;
    margin: 1.25rem 0 !important;
}

/* Sidebar metric chips */
.metric-chip {
    display: flex; justify-content: space-between; align-items: center;
    padding: 12px 14px;
    margin-bottom: 8px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    backdrop-filter: blur(10px);
    transition: all 0.25s ease;
}
.metric-chip:hover { border-color: var(--border-hi); }
.metric-chip .label {
    font-size: 0.78rem;
    color: var(--text-mute) !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    font-weight: 500;
}
.metric-chip .value {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.1rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Alerts */
div[data-baseweb="notification"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    backdrop-filter: blur(20px) !important;
}

/* Footer */
.app-footer {
    margin-top: 4rem;
    padding: 2rem;
    text-align: center;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    backdrop-filter: blur(20px);
}
.app-footer .brand {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.15rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.app-footer .stack {
    display: inline-flex; flex-wrap: wrap; gap: 6px; justify-content: center;
    margin-top: 0.6rem;
}
.app-footer .tag {
    padding: 3px 10px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border);
    border-radius: 999px;
    font-size: 0.72rem;
    color: var(--text-mute) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Subhead under selects */
.field-label {
    display: block;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-dim) !important;
    margin-bottom: 0.45rem;
    letter-spacing: 0.02em;
}

/* Recommend result intro */
.result-intro {
    margin: 1.5rem 0 0.5rem;
    padding: 1.1rem 1.25rem;
    background: var(--gradient-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    backdrop-filter: blur(20px);
}
.result-intro .lbl {
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-mute) !important;
    font-weight: 500;
}
.result-intro .seed {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.4rem;
    font-weight: 700;
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 4px;
}

/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg-0); }
::-webkit-scrollbar-thumb { background: rgba(167, 139, 250, 0.3); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(167, 139, 250, 0.5); }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_movies(csv_path="movies.csv"):
    """Load and preprocess the movie dataset."""
    if not os.path.exists(csv_path):
        st.error(f"Movie dataset not found at: {csv_path}")
        st.info("Please ensure 'movies.csv' is in the same directory as this script.")
        sys.exit(1)

    try:
        movies_df = pd.read_csv(csv_path)
        required_columns = ['title', 'description']
        if not all(col in movies_df.columns for col in required_columns):
            st.error(f"CSV file must contain columns: {required_columns}")
            sys.exit(1)

        movies_df['genres'] = movies_df['description'].str.split(',').apply(lambda x: [g.strip() for g in x])
        unique_genres_list = sorted({g for gl in movies_df['genres'] for g in gl})
        return movies_df, unique_genres_list
    except Exception as e:
        st.error(f"Error loading movie data: {str(e)}")
        sys.exit(1)


@st.cache_data
def compute_similarity_matrix(movies_df):
    """Pre-compute the TF-IDF similarity matrix for better performance."""
    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['description'])
    similarity_matrix = cosine_similarity(tfidf_matrix)
    return similarity_matrix, tfidf


@st.cache_data
def get_hybrid_recommendations(movie_title, movies_df, similarity_matrix, top_n=5,
                               rating_weight=0.3, year_weight=0.1, genre_weight=0.6):
    """Get movie recommendations using hybrid approach (genre + rating + recency)."""
    try:
        idx = movies_df[movies_df['title'] == movie_title].index[0]
        genre_sim = similarity_matrix[idx]
        rating_sim = np.zeros(len(movies_df))
        year_sim = np.zeros(len(movies_df))

        if 'rating' in movies_df.columns and pd.notna(movies_df.iloc[idx]['rating']):
            selected_rating = movies_df.iloc[idx]['rating']
            ratings = movies_df['rating'].fillna(movies_df['rating'].mean())
            rating_diff = np.abs(ratings - selected_rating)
            rating_sim = 1 - (rating_diff / 10.0)

        if 'year' in movies_df.columns and pd.notna(movies_df.iloc[idx]['year']):
            selected_year = movies_df.iloc[idx]['year']
            years = movies_df['year'].fillna(movies_df['year'].median())
            year_diff = np.abs(years - selected_year)
            year_sim = 1 - (year_diff / 100.0)
            year_sim = np.clip(year_sim, 0, 1)

        combined_sim = (
            genre_weight * genre_sim +
            rating_weight * rating_sim +
            year_weight * year_sim
        )

        sim_scores = list(enumerate(combined_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_idx = [i for i, score in sim_scores if i != idx][:top_n]
        sim_values = [score for i, score in sim_scores if i != idx][:top_n]

        result = movies_df.iloc[sim_idx].copy()
        result['similarity_score'] = [round(score * 100, 1) for score in sim_values]
        return result
    except IndexError:
        raise ValueError(f"Movie '{movie_title}' not found in database")


# ─────────────────────────────────────────────────────────────────────────────
# Load data
# ─────────────────────────────────────────────────────────────────────────────
movies, unique_genres = load_movies()
similarity_matrix, tfidf_vectorizer = compute_similarity_matrix(movies)

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <span class="hero-eyebrow"><span class="dot"></span> AI-Powered · TF-IDF + Hybrid Scoring</span>
        <h1>Discover your next<br/><span class="grad">favorite film.</span></h1>
        <p class="lede">An intelligent recommender that blends genre, rating, and era —
        crafted with modern machine learning to surface films you'll actually love.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙ Tuning")
    st.markdown('<span class="field-label">Adjust how the engine weighs each signal.</span>', unsafe_allow_html=True)

    genre_weight = st.slider("Genre match", 0.0, 1.0, 0.6, 0.1)
    rating_weight = st.slider("Rating similarity", 0.0, 1.0, 0.3, 0.1)
    year_weight = st.slider("Release era", 0.0, 1.0, 0.1, 0.1)
    num_recommendations = st.slider("Results", 3, 20, 5)

    st.markdown("---")
    st.markdown("### Library")

    year_range = ""
    if 'year' in movies.columns:
        year_range = f"{int(movies['year'].min())}–{int(movies['year'].max())}"

    st.markdown(
        f"""
        <div class="metric-chip"><span class="label">Movies</span><span class="value">{len(movies)}</span></div>
        <div class="metric-chip"><span class="label">Genres</span><span class="value">{len(unique_genres)}</span></div>
        {f'<div class="metric-chip"><span class="label">Era</span><span class="value">{year_range}</span></div>' if year_range else ''}
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
# TOP RATED
# ─────────────────────────────────────────────────────────────────────────────
if 'rating' in movies.columns:
    st.markdown(
        '<div class="section-title"><span class="bar"></span>Top rated<span class="count">TOP 9</span></div>',
        unsafe_allow_html=True,
    )

    top_rated = movies.nlargest(9, 'rating')[['title', 'rating', 'year']].reset_index(drop=True)
    cols = st.columns(3, gap="small")

    for i, (_, movie_row) in enumerate(top_rated.iterrows()):
        with cols[i % 3]:
            year_str = f"{int(movie_row['year'])}" if pd.notna(movie_row['year']) else "—"
            st.markdown(
                f"""
                <div class="top-card">
                    <div class="rank">#{i+1:02d}</div>
                    <div class="title">{movie_row['title']}</div>
                    <div class="meta">
                        <span class="rating-chip">★ {movie_row['rating']}</span>
                        <span>{year_str}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ─────────────────────────────────────────────────────────────────────────────
# SEARCH + GENRE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title"><span class="bar"></span>Explore the library</div>',
    unsafe_allow_html=True,
)

search_col, genre_col = st.columns([2, 1], gap="medium")

with search_col:
    st.markdown('<span class="field-label">Search</span>', unsafe_allow_html=True)
    search_term = st.text_input(
        "Search",
        "",
        placeholder="Search by title or director…",
        label_visibility="collapsed",
        key="search_input",
    )

with genre_col:
    st.markdown('<span class="field-label">Filter by genre</span>', unsafe_allow_html=True)
    genre = st.selectbox(
        "Genre",
        ["All"] + unique_genres,
        label_visibility="collapsed",
    )

if search_term:
    filtered_by_search = movies[
        movies['title'].str.contains(search_term, case=False, na=False) |
        (movies['director'].str.contains(search_term, case=False, na=False) if 'director' in movies.columns else False)
    ]
else:
    filtered_by_search = movies

filtered = filtered_by_search.copy()
if genre != "All":
    filtered = filtered[filtered['genres'].apply(lambda gs: genre in gs)]

# Status line
status_parts = []
if search_term:
    status_parts.append(f'matching <strong style="color:var(--accent)">"{search_term}"</strong>')
if genre != "All":
    status_parts.append(f'in <strong style="color:var(--accent)">{genre}</strong>')
status_text = " ".join(status_parts) if status_parts else "in the catalog"
st.markdown(
    f"""<div style="color: var(--text-mute); font-size: 0.85rem; margin: 0.5rem 0 1rem; font-family: 'JetBrains Mono', monospace;">
    → {len(filtered)} {'movie' if len(filtered) == 1 else 'movies'} {status_text}
    </div>""",
    unsafe_allow_html=True,
)

if not filtered.empty:
    display_cols = ['title', 'description']
    rename_dict = {'title': 'Title', 'description': 'Genres'}
    if 'year' in filtered.columns:
        display_cols.append('year'); rename_dict['year'] = 'Year'
    if 'rating' in filtered.columns:
        display_cols.append('rating'); rename_dict['rating'] = 'Rating'
    if 'director' in filtered.columns:
        display_cols.append('director'); rename_dict['director'] = 'Director'

    st.dataframe(
        filtered[display_cols].rename(columns=rename_dict),
        height=320,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.warning("No movies match your filters. Try a broader search.")

# ─────────────────────────────────────────────────────────────────────────────
# RECOMMENDATIONS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title"><span class="bar"></span>Personalized for you</div>',
    unsafe_allow_html=True,
)

pick_col, btn_col = st.columns([3, 1], gap="medium")

with pick_col:
    st.markdown('<span class="field-label">Pick a movie you love</span>', unsafe_allow_html=True)
    movie = st.selectbox(
        "Movie",
        filtered['title'].tolist() if not filtered.empty else [],
        index=0 if filtered.empty else None,
        label_visibility="collapsed",
        placeholder="Select a film…",
    )

with btn_col:
    st.markdown('<span class="field-label">&nbsp;</span>', unsafe_allow_html=True)
    get_recs = st.button("Get recommendations →", key="recommend_btn", use_container_width=True)

if get_recs:
    if movie:
        try:
            with st.spinner(""):
                recommendations = get_hybrid_recommendations(
                    movie, movies, similarity_matrix,
                    top_n=num_recommendations,
                    rating_weight=rating_weight,
                    year_weight=year_weight,
                    genre_weight=genre_weight,
                )

            st.markdown(
                f"""
                <div class="result-intro">
                    <div class="lbl">Because you liked</div>
                    <div class="seed">{movie}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for offset, (_, row) in enumerate(recommendations.iterrows()):
                year_html = f' <span class="year">({int(row["year"])})</span>' if 'year' in row and pd.notna(row['year']) else ''

                chips = []
                if pd.notna(row.get('description')):
                    for g in [g.strip() for g in str(row['description']).split(',')][:4]:
                        chips.append(f'<span class="chip genre">{g}</span>')
                if 'rating' in row and pd.notna(row['rating']):
                    chips.append(f'<span class="chip rating">★ {row["rating"]}</span>')
                if 'director' in row and pd.notna(row['director']):
                    chips.append(f'<span class="chip director">🎬 {row["director"]}</span>')

                score_html = ""
                if 'similarity_score' in row:
                    score_html = f'<div class="score-pill">{row["similarity_score"]}<span class="pct">%</span></div>'

                st.markdown(
                    f"""
                    <div class="rec-card" style="animation-delay: {offset * 0.06}s;">
                        <div class="rec-row">
                            <div style="flex:1; min-width:0;">
                                <div class="rec-title">{row['title']}{year_html}</div>
                                <div class="rec-meta">{''.join(chips)}</div>
                            </div>
                            {score_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        except ValueError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please select a movie first.")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    f"""
    <div class="app-footer">
        <div class="brand">CINEMATIC · AI MOVIE RECOMMENDER</div>
        <div style="color: var(--text-dim); font-size: 0.88rem;">
            Hybrid content-based filtering · TF-IDF with bigrams · Cosine similarity
        </div>
        <div class="stack">
            <span class="tag">{len(movies)} movies</span>
            <span class="tag">{len(unique_genres)} genres</span>
            <span class="tag">scikit-learn</span>
            <span class="tag">streamlit</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
