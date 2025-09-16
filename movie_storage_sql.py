from sqlalchemy import create_engine, text
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Database
DB_URL = "sqlite:///movies.db"
engine = create_engine(DB_URL, echo=False)

# Setup database
with engine.connect() as connection:
    # Users table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """))

    # Movies table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL,
            UNIQUE(user_id, title),
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """))
    connection.commit()

# ---------------- USERS ---------------- #

def get_users():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, name FROM users"))
        return [{"id": row[0], "name": row[1]} for row in result.fetchall()]

def create_user(name):
    with engine.connect() as connection:
        connection.execute(text("INSERT INTO users (name) VALUES (:name)"), {"name": name})
        connection.commit()

def get_user_id(name):
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id FROM users WHERE name = :name"), {"name": name}).fetchone()
        return result[0] if result else None

# ---------------- MOVIES ---------------- #

def get_movies(user_id):
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster FROM movies WHERE user_id = :uid"),
            {"uid": user_id}
        )
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster": row[3]} for row in movies}

def add_movie(user_id, title):
    URL = "http://www.omdbapi.com/"
    params = {"t": title, "apikey": API_KEY}

    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ API not accessible: {e}")
        return

    data = response.json()
    if data.get("Response") == "False":
        print(f" Movie not found: {data.get('Error', 'Unknown error')}")
        return

    title = data["Title"]
    year = int(data["Year"])
    rating_str = data["imdbRating"]
    try:
        rating = float(rating_str)
    except:
        rating = 0.0
    poster = data["Poster"]

    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (user_id, title, year, rating, poster) VALUES (:uid, :title, :year, :rating, :poster)"),
                {"uid": user_id, "title": title, "year": year, "rating": rating, "poster": poster}
            )
            connection.commit()
            print(f"✅ Movie '{title}' added to your collection!")
        except Exception as e:
            print(f"Error adding movie: {e}")

def delete_movie(user_id, title):
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE user_id = :uid AND title = :title"),
            {"uid": user_id, "title": title}
        )
        connection.commit()
        return result.rowcount > 0

def update_movie(user_id, title, rating):
    with engine.connect() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE user_id = :uid AND title = :title"),
            {"uid": user_id, "title": title, "rating": rating}
        )
        connection.commit()
        return result.rowcount > 0
