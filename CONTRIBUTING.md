# Contributing to Movie Recommendation System

Thank you for your interest in contributing! Here are some guidelines to help you get started.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Movie-Recommendation-Engine.git
   cd Movie-Recommendation-Engine
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

Run the test suite with pytest:
```bash
pytest
```

For coverage report:
```bash
pytest --cov=. --cov-report=html
```

## Code Style

- Follow PEP 8 guidelines
- Add docstrings to all functions and classes
- Keep functions focused and concise
- Add type hints where appropriate

## Adding New Features

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and add tests

3. Run tests to ensure everything works:
   ```bash
   pytest
   ```

4. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: description of your feature"
   ```

5. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request

## Adding Movies to the Dataset

To add new movies to `movies.csv`, follow this format:
```csv
title,description,year,rating,director
Movie Name,"Genre1, Genre2, Genre3",YEAR,RATING,"Director Name"
```

## Reporting Bugs

Please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

## Feature Requests

Create an issue describing:
- The feature you'd like
- Why it would be useful
- Possible implementation approach

Thank you for contributing!
