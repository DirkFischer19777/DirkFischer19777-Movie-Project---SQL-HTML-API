import statistics
import random
import sys
import movie_storage_sql as movie_storage

MENU = """
*********** My Movies Database ***********

Menu:
0. Exit program
1. List movies
2. Add movie
3. Delete movie
4. Update movie
5. Stats
6. Random movie
7. Search movie
8. Movies sorted by rating
9. Generate website
10. Switch user
"""

# ---------------- USER LOGIN ---------------- #

def select_user():
    users = movie_storage.get_users()
    print("Welcome to the Movie App! 🎬\n")
    print("Select a user:")
    for idx, u in enumerate(users, 1):
        print(f"{idx}. {u['name']}")
    print(f"{len(users)+1}. Create new user")

    choice = int(input("Enter choice: "))

    if choice == len(users) + 1:
        name = input("Enter new username: ").strip()
        movie_storage.create_user(name)
        return movie_storage.get_user_id(name), name
    else:
        return users[choice-1]["id"], users[choice-1]["name"]

# ---------------- MOVIE FUNCTIONS ---------------- #

def list_movie(movies, username):
    if not movies:
        print(f"📢 {username}, your movie collection is empty.")
        return
    print(f"{len(movies)} movies in total for {username}:")
    for key, value in movies.items():
        print(f"{key}: year: {value['year']} rating: {value['rating']} ")

def add_movie(user_id):
    title = input("Enter new movie name: ")
    movie_storage.add_movie(user_id, title)

def delete_movie(user_id, movies):
    title = input("Enter movie name to delete: ").strip()
    for t in movies:
        if t.lower() == title.lower():
            if movie_storage.delete_movie(user_id, t):
                print(f"{t} successfully deleted")
            return
    print(f"{title} not found in your list")

def update_movie(user_id, movies):
    title = input("Enter movie name to update: ")
    if title not in movies:
        print(f"{title} not in your list")
        return
    try:
        new_rate = float(input("Enter new rating: "))
        if movie_storage.update_movie(user_id, title, new_rate):
            print(f"{title} successfully updated")
    except ValueError:
        print("Invalid rating!")

def stats(movies):
    if not movies:
        print("No movies available.")
        return

    ratings = [float(value["rating"]) for value in movies.values()]
    average = sum(ratings) / len(ratings)
    median = statistics.median(ratings)

    max_rating = max(ratings)
    min_rating = min(ratings)

    best_movies = [t for t, v in movies.items() if float(v["rating"]) == max_rating]
    worst_movies = [t for t, v in movies.items() if float(v["rating"]) == min_rating]

    print(f"Average rating: {average:.2f}/10")
    print(f"Median rating: {median:.2f}/10")
    print("Best movie(s):", ", ".join(best_movies))
    print("Worst movie(s):", ", ".join(worst_movies))

def rand_movie(movies):
    if not movies:
        print("No movies available.")
        return
    title, value = random.choice(list(movies.items()))
    print(f"Random movie: {title} year: {value['year']} rating: {value['rating']}")

def search_movie(movies):
    search = input("Enter part of movie name: ").lower()
    found = [f"{title}, {v['year']}, {v['rating']}" for title, v in movies.items() if search in title.lower()]
    print("\n".join(found) if found else "No matching movies found.")

def sort_by_rating(movies):
    sorted_movies = sorted(movies.items(), key=lambda x: float(x[1]["rating"]), reverse=True)
    for title, value in sorted_movies:
        print(f"{title}, {value['year']}, {value['rating']}")

def generate_website(movies, username):
    with open("_static/index_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    movie_grid = ""
    for title, info in movies.items():
        movie_grid += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{info['poster']}" alt="Poster of {title}">
                <div class="movie-title">{title}</div>
                <div class="movie-year">{info['year']} — Rating: {info['rating']}</div>
            </div>
        </li>
        """

    html_content = template.replace("__TEMPLATE_TITLE__", f"{username}'s Movie App")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
    html_content = html_content.replace('href="style.css"', 'href="_static/style.css"')

    if "<meta charset=" not in html_content:
        html_content = html_content.replace("<head>", "<head>\n    <meta charset=\"UTF-8\">", 1)

    filename = f"{username}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Website for {username} saved as {filename} ✅")

# ---------------- MENU ---------------- #

def menu(user_id, username):
    print(MENU)
    movies = movie_storage.get_movies(user_id)
    choice = int(input("Enter choice: "))

    if choice == 0:
        print("Bye!")
        sys.exit()
    elif choice == 1:
        list_movie(movies, username)
    elif choice == 2:
        add_movie(user_id)
    elif choice == 3:
        delete_movie(user_id, movies)
    elif choice == 4:
        update_movie(user_id, movies)
    elif choice == 5:
        stats(movies)
    elif choice == 6:
        rand_movie(movies)
    elif choice == 7:
        search_movie(movies)
    elif choice == 8:
        sort_by_rating(movies)
    elif choice == 9:
        generate_website(movies, username)
    elif choice == 10:
        return None, None  # triggers user switch

    input("Press enter to continue...")
    return user_id, username

def main():
    user_id, username = select_user()
    while True:
        user_id, username = menu(user_id, username)
        if user_id is None:  # user switched
            user_id, username = select_user()

if __name__ == "__main__":
    main()
