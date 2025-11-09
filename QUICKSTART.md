# Quick Start Guide

## 1-Minute Setup

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/Movie-Recommendation-Engine.git
cd Movie-Recommendation-Engine

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## First Steps

### 1. Explore Top-Rated Movies
Browse the **Top Rated Movies** section to see the highest-rated films in the dataset.

### 2. Search for a Movie
Use the **Search** feature to find movies by:
- Title (e.g., "Inception")
- Director (e.g., "Christopher Nolan")

### 3. Filter by Genre
Select a genre from the dropdown to see all movies in that category:
- Action, Drama, Sci-Fi, Comedy, Horror, etc.

### 4. Get Recommendations
1. Select a movie you like
2. Click **"Get Recommendations"**
3. View 5 similar movies with match percentages

### 5. Customize Recommendations (Sidebar)
Adjust the weights to fine-tune recommendations:
- **Genre Match**: How important is genre similarity?
- **Rating Similarity**: Prefer similarly-rated movies?
- **Release Year**: Consider when movies were made?

## Pro Tips

### Finding Similar Movies
If you like "The Dark Knight", you'll get recommendations like:
- Batman Begins (same series, similar genres)
- The Departed (similar rating, crime/drama)
- Other Christopher Nolan films

### Adjusting Weights
- **More genre variety**: Lower genre weight, increase year/rating
- **Only similar genres**: Set genre weight to 1.0
- **Quality focus**: Increase rating weight to 0.5+

### Search Shortcuts
- Type "Nolan" to see all Christopher Nolan films
- Type "2019" to find movies from that year (in titles)
- Type partial names: "Matrix" finds all Matrix movies

## Features at a Glance

| Feature | Description | Location |
|---------|-------------|----------|
| Top Rated | See 9 highest-rated movies | Top of main page |
| Search | Find by title/director | Search box |
| Genre Filter | Browse by category | Dropdown menu |
| Recommendations | Get 5-20 similar movies | After movie selection |
| Similarity Score | See match percentage | In recommendations |
| Custom Weights | Adjust algorithm | Sidebar sliders |
| Dataset Info | View statistics | Bottom of sidebar |

## Troubleshooting

**App won't start?**
- Ensure Python 3.8+ installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`

**No recommendations?**
- Make sure you selected a movie first
- Try clicking the button again

**Search not working?**
- Clear the search box to see all movies
- Try searching for part of the name

## Next Steps

1. Try different genres to discover new movies
2. Experiment with recommendation weights
3. Compare recommendations for similar movies
4. Add your own movies to `movies.csv`

Enjoy discovering your next favorite film! 🎬
