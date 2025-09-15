from sqlalchemy import create_engine, text
import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT UNIQUE NOT NULL
        )
    """))
    connection.commit()

def get_movies():
    """Retrieve all movies from the database as a dict like in JSON version."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}

def add_movie(title):
    """Add a new movie to the database, handling API errors."""
    URL = "http://www.omdbapi.com/"
    params = {"t": title, "apikey" : API_KEY  }

    # secure API-request
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ API is not accessible: {e}")
        return

    data = response.json()
    # Movie not found
    if data.get("Response") == "False":
        print(f"❌ Movie not found: {data.get('Error', 'Unknown error')}")
        return

    title = data["Title"]
    year = data["Year"]
    rating = data["Ratings"][0]["Value"]
    poster = data["Poster"]


    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
                {"title": title, "year": year, "rating": rating, "poster": poster}
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error adding movie: {e}")

def delete_movie(title):
    """Delete a movie from the database by title."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"),
            {"title": title}
        )
        connection.commit()

        if result.rowcount > 0:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")

def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE title = :title"),
            {"title": title, "rating": rating}
        )
        connection.commit()

        if result.rowcount > 0:
            print(f"Movie '{title}' updated successfully.")
        else:
            print(f"Movie '{title}' not found.")

