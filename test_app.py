#!/usr/bin/env python3
"""
Quick test script to verify the app works before running Streamlit.
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("🧪 Testing Movie Recommendation App...")
print("="*50)

# Test 1: Load CSV
print("\n1. Testing CSV loading...")
try:
    movies = pd.read_csv('movies.csv')
    print(f"   ✅ Loaded {len(movies)} movies")
    print(f"   ✅ Columns: {list(movies.columns)}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Process genres
print("\n2. Testing genre processing...")
try:
    movies['genres'] = movies['description'].str.split(',').apply(lambda x: [g.strip() for g in x])
    unique_genres = sorted({g for gl in movies['genres'] for g in gl})
    print(f"   ✅ Found {len(unique_genres)} unique genres")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 3: TF-IDF
print("\n3. Testing TF-IDF vectorization...")
try:
    tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df=1, stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['description'])
    print(f"   ✅ TF-IDF matrix shape: {tfidf_matrix.shape}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 4: Similarity computation
print("\n4. Testing similarity computation...")
try:
    similarity_matrix = cosine_similarity(tfidf_matrix)
    print(f"   ✅ Similarity matrix shape: {similarity_matrix.shape}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 5: Recommendations
print("\n5. Testing recommendation generation...")
try:
    test_movie = movies.iloc[0]['title']
    idx = 0
    sim = similarity_matrix[idx]
    sim_idx = [i for i in sim.argsort()[::-1] if i != idx][:5]
    recs = movies.iloc[sim_idx]

    print(f"   ✅ Recommendations for '{test_movie}':")
    for i, (_, row) in enumerate(recs.iterrows(), 1):
        print(f"      {i}. {row['title']} ({row['year']})")
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

print("\n" + "="*50)
print("🎉 All tests passed! App is ready to run!")
print("\nTo start the app, run:")
print("  ./run.sh")
print("\nOr:")
print("  source venv/bin/activate && streamlit run app.py")
