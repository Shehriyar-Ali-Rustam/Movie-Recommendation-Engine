"""
Unit tests for movie recommendation system.
"""

import pytest
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestMovieRecommendations:
    """Test suite for movie recommendation functionality."""

    @pytest.fixture
    def sample_movies(self):
        """Create sample movie data for testing."""
        data = {
            'title': [
                'The Dark Knight',
                'Batman Begins',
                'The Matrix',
                'Inception',
                'Toy Story'
            ],
            'description': [
                'Action, Crime, Drama',
                'Action, Crime, Drama',
                'Action, Sci-Fi',
                'Action, Adventure, Sci-Fi',
                'Animation, Adventure, Comedy'
            ],
            'year': [2008, 2005, 1999, 2010, 1995],
            'rating': [9.0, 8.2, 8.7, 8.8, 8.3],
            'director': [
                'Christopher Nolan',
                'Christopher Nolan',
                'Lana Wachowski, Lilly Wachowski',
                'Christopher Nolan',
                'John Lasseter'
            ]
        }
        return pd.DataFrame(data)

    def test_dataframe_structure(self, sample_movies):
        """Test that the movie DataFrame has the correct structure."""
        assert 'title' in sample_movies.columns
        assert 'description' in sample_movies.columns
        assert len(sample_movies) > 0

    def test_genre_extraction(self, sample_movies):
        """Test genre extraction from description."""
        sample_movies['genres'] = sample_movies['description'].str.split(',').apply(
            lambda x: [g.strip() for g in x]
        )
        assert isinstance(sample_movies.iloc[0]['genres'], list)
        assert 'Action' in sample_movies.iloc[0]['genres']

    def test_tfidf_vectorization(self, sample_movies):
        """Test TF-IDF vectorization of movie descriptions."""
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(sample_movies['description'])
        assert tfidf_matrix.shape[0] == len(sample_movies)
        assert tfidf_matrix.shape[1] > 0

    def test_cosine_similarity_calculation(self, sample_movies):
        """Test cosine similarity computation."""
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(sample_movies['description'])

        # Calculate similarity for first movie
        sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix).flatten()

        # Similarity with itself should be 1.0
        assert abs(sim[0] - 1.0) < 0.001
        # Should have similarity scores for all movies
        assert len(sim) == len(sample_movies)
        # All similarities should be between 0 and 1
        assert all(0 <= s <= 1 for s in sim)

    def test_recommendation_logic(self, sample_movies):
        """Test the core recommendation logic."""
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(sample_movies['description'])

        # Get recommendations for 'The Dark Knight' (index 0)
        idx = 0
        sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
        sim_idx = [i for i in sim.argsort()[::-1] if i != idx][:3]

        recommendations = sample_movies.iloc[sim_idx]

        # Should get 3 recommendations
        assert len(recommendations) <= 3
        # Should not include the selected movie
        assert 'The Dark Knight' not in recommendations['title'].values
        # Most similar should be 'Batman Begins' (same genres)
        assert recommendations.iloc[0]['title'] == 'Batman Begins'

    def test_unique_genres(self, sample_movies):
        """Test extraction of unique genres."""
        sample_movies['genres'] = sample_movies['description'].str.split(',').apply(
            lambda x: [g.strip() for g in x]
        )
        unique_genres = sorted({g for gl in sample_movies['genres'] for g in gl})

        assert 'Action' in unique_genres
        assert 'Drama' in unique_genres
        assert 'Animation' in unique_genres
        assert len(unique_genres) > 0

    def test_genre_filtering(self, sample_movies):
        """Test filtering movies by genre."""
        sample_movies['genres'] = sample_movies['description'].str.split(',').apply(
            lambda x: [g.strip() for g in x]
        )

        # Filter for Action movies
        action_movies = sample_movies[
            sample_movies['genres'].apply(lambda gs: 'Action' in gs)
        ]

        assert len(action_movies) == 4  # All except Toy Story
        assert 'Toy Story' not in action_movies['title'].values

    def test_empty_recommendations(self, sample_movies):
        """Test handling of edge cases."""
        # Test with single movie dataset
        single_movie = sample_movies.head(1)
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(single_movie['description'])

        idx = 0
        sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
        sim_idx = [i for i in sim.argsort()[::-1] if i != idx][:5]

        # Should return empty list for single movie
        assert len(sim_idx) == 0

    def test_movie_metadata(self, sample_movies):
        """Test that movie metadata is properly stored."""
        assert sample_movies.iloc[0]['year'] == 2008
        assert sample_movies.iloc[0]['rating'] == 9.0
        assert 'Christopher Nolan' in sample_movies.iloc[0]['director']


class TestDataValidation:
    """Test suite for data validation."""

    def test_csv_file_exists(self):
        """Test that the movies.csv file exists."""
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'movies.csv')
        assert os.path.exists(csv_path), "movies.csv file not found"

    def test_csv_data_integrity(self):
        """Test that the CSV has required columns."""
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'movies.csv')
        df = pd.read_csv(csv_path)

        required_columns = ['title', 'description']
        for col in required_columns:
            assert col in df.columns, f"Required column '{col}' not found"

        # Check for no empty titles
        assert not df['title'].isna().any(), "Found movies with empty titles"
        assert not df['description'].isna().any(), "Found movies with empty descriptions"

    def test_csv_data_quality(self):
        """Test data quality in the CSV."""
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'movies.csv')
        df = pd.read_csv(csv_path)

        # Check that we have a reasonable number of movies
        assert len(df) >= 10, "Dataset should have at least 10 movies"

        # Check that ratings are in valid range (if present)
        if 'rating' in df.columns:
            valid_ratings = df['rating'].dropna()
            assert all(0 <= r <= 10 for r in valid_ratings), "Ratings should be between 0 and 10"

        # Check that years are reasonable (if present)
        if 'year' in df.columns:
            valid_years = df['year'].dropna()
            assert all(1900 <= y <= 2030 for y in valid_years), "Years should be reasonable"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
