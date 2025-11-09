# Architecture Documentation

## Overview

The Movie Recommendation System is a content-based filtering application built with Streamlit. It uses TF-IDF (Term Frequency-Inverse Document Frequency) vectorization and cosine similarity to recommend movies based on genre similarity.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                    (Streamlit App)                       │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Data Loading │  │ Vectorization│  │ Similarity   │  │
│  │   (Cached)   │  │   (TF-IDF)   │  │ Computation  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│              movies.csv + config.yaml                    │
└─────────────────────────────────────────────────────────┘
```

## Components

### 1. User Interface Layer
- **Framework**: Streamlit
- **Responsibilities**:
  - Display movie catalog with filtering
  - Accept user input (genre selection, movie selection)
  - Show recommendations with rich metadata
  - Handle user interactions

### 2. Application Logic Layer

#### Data Loading (`load_movies()`)
- Loads movie data from CSV
- Validates data integrity
- Processes genre information
- **Optimization**: Uses `@st.cache_data` for performance

#### Recommendation Engine (`get_recommendations()`)
- **Input**: Selected movie title, movies DataFrame, number of recommendations
- **Process**:
  1. Convert movie genres to TF-IDF vectors
  2. Calculate cosine similarity between selected movie and all others
  3. Sort by similarity score
  4. Return top N recommendations
- **Output**: DataFrame of recommended movies
- **Optimization**: Cached for repeated queries

### 3. Data Layer
- **movies.csv**: Contains movie metadata
  - title: Movie name
  - description: Comma-separated genres
  - year: Release year
  - rating: IMDb-style rating (0-10)
  - director: Director name(s)
- **config.yaml**: Application configuration
  - Theme colors
  - Feature flags
  - Default settings

## Algorithm Details

### TF-IDF Vectorization
```
TF-IDF(genre, movie) = TF(genre, movie) × IDF(genre)

Where:
- TF = (Number of times genre appears in movie) / (Total genres in movie)
- IDF = log(Total movies / Movies containing genre)
```

### Cosine Similarity
```
similarity(A, B) = (A · B) / (||A|| × ||B||)

Where:
- A, B are TF-IDF vectors
- · represents dot product
- ||·|| represents vector magnitude
```

Result ranges from 0 (no similarity) to 1 (identical).

## Data Flow

1. **Initialization**:
   ```
   User visits app → Load movies.csv → Process genres → Cache data
   ```

2. **Genre Filtering**:
   ```
   User selects genre → Filter movies → Display table
   ```

3. **Recommendations**:
   ```
   User selects movie → Compute TF-IDF → Calculate similarities
   → Sort results → Display top 5
   ```

## Performance Optimizations

1. **Caching**:
   - `@st.cache_data` on `load_movies()` - Prevents re-reading CSV
   - `@st.cache_data` on `get_recommendations()` - Caches similarity computations

2. **Lazy Loading**:
   - Background image loaded only if file exists
   - TF-IDF matrix computed only when recommendations requested

3. **Efficient Data Structures**:
   - Pandas DataFrames for vectorized operations
   - Sparse matrices for TF-IDF (scikit-learn default)

## Error Handling

1. **Missing Files**:
   - CSV file check with user-friendly error messages
   - Background image graceful fallback

2. **Invalid Data**:
   - Column validation
   - Empty dataset handling
   - Invalid movie selection protection

3. **Runtime Errors**:
   - Try-catch blocks for recommendation computation
   - Detailed error messages for debugging

## Security Considerations

1. **Input Validation**:
   - Movie titles from dropdown (no free text injection)
   - Genre filtering uses predefined list

2. **Data Integrity**:
   - CSV validation on load
   - Type checking for metadata fields

## Scalability

### Current Limitations
- Linear time complexity for similarity computation: O(n)
- In-memory data storage
- Suitable for datasets up to ~10,000 movies

### Future Improvements
- Add database backend (SQLite, PostgreSQL)
- Implement approximate nearest neighbors (ANN) for large datasets
- Add user rating history and collaborative filtering
- Cache TF-IDF matrix globally instead of per-request

## Testing Strategy

1. **Unit Tests** (`tests/test_recommendations.py`):
   - Data loading and validation
   - Genre extraction
   - TF-IDF computation
   - Similarity calculation
   - Recommendation logic

2. **Integration Tests**:
   - End-to-end recommendation flow
   - CSV data integrity
   - Error handling scenarios

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment Options
1. **Streamlit Cloud**: Direct GitHub integration
2. **Docker**: Containerized deployment
3. **Heroku/AWS**: Cloud platform deployment

## Configuration

Edit `config.yaml` to customize:
- UI colors and theme
- Number of recommendations
- Feature toggles
- Data source paths

## Dependencies

- **streamlit**: Web application framework
- **pandas**: Data manipulation
- **scikit-learn**: TF-IDF and cosine similarity
- **Pillow**: Image processing
- **pyyaml**: Configuration file parsing
