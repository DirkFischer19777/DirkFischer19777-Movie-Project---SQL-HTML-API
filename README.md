# 🎬 Movie Project

The **Movie Project** is a Python application for storing and managing movies in an SQLite database.  
Users can create accounts and build their own collections of favorite movies.  

---

## ✨ Features
- User management (each user has their own movie collection)
- Store movies with title, year, rating, and poster
- Automatic relationship between users and movies via foreign keys
- Database powered by **SQLite**, accessed through **SQLAlchemy**
- Simple CLI menu for user interaction
- API integration (e.g., for fetching posters or movie details)
- Generate user specific HTML-Page

---

## 🎯 Purpose
This project was created as a learning environment to practice:
- SQL (tables, queries, joins, foreign keys, constraints)
- Python (object orientation, database interaction, error handling)
- Flask / HTML (optional extension for a web interface)
- Working with APIs (fetching movie data from external sources)

---

## ⚙️ Setup

### Requirements
- Python 3.12 or newer  
- `pip` (Python package manager)

### Installation
1. Clone or download the repository:
   ```bash
   git clone https://github.com/username/movie-project.git
   cd movie-project
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

3. Install dependencies:
    ```bash
   pip install -r requirements.txt
4. Create a .env file (if using API keys):
   ```bash
   API_KEY=your_api_key_here
--- 
### ▶️ Usage
1. Run the program:
   ```bash
    python main.py
2. Available menu options:
- Create a new user or log in
- Add movies
- List your movies
- Delete movies
- Export data 

