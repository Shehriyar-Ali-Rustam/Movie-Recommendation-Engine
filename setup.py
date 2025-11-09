"""
Setup script for Movie Recommendation System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="movie-recommendation-engine",
    version="1.0.0",
    author="Your Name",
    description="A content-based movie recommendation system using TF-IDF and cosine similarity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR-USERNAME/Movie-Recommendation-Engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.32.0,<2.0.0",
        "pandas>=2.0.3,<3.0.0",
        "scikit-learn>=1.3.0,<2.0.0",
        "Pillow>=10.0.1,<11.0.0",
        "pyyaml>=6.0,<7.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0,<9.0.0",
            "pytest-cov>=4.1.0,<6.0.0",
        ],
    },
)
