import statistics
import random
import sys
import movie_storage_sql as movie_storage


# Constant Menu to ask user for choice
MENU = '''

********** My Movies Database **********

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
'''


def user_input():
    """
    Ask the user to enter a menu choice (0–9).

    Returns:
        int: The menu choice entered by the user.
    """
    while True:
        try:
            menu_input = int(input("Enter choice (0-9):"))
            return menu_input
        except ValueError:
            print("Bitte eine ganze Zahl eingeben")


def list_movie(movies):
    """
    Print all movies in the collection with their year and rating.

    Args:
        movies (dict): Dictionary of movies with title as key and
                       year/rating as values.
    """
    movie_counter = len(movies)
    print(f"{movie_counter} movies in total")
    for key, value in movies.items():
        print(f"{key}: year: {value["year"]} rating: {value["rating"]} ")


def add_movie(movies):
    """
    Add a new movie to the collection.

    Prompts the user for title, rating, and year. Validates inputs
    and calls movie_storage.add_movie() if valid.

    Args:
        movies (dict): Dictionary of movies (not directly modified,
                       only used for validation).
    """
    try:
        new_movie = input("Enter new movie name: ")

        movie_storage.add_movie(new_movie)
        print(f"Movie {new_movie} successfully added")
    except ValueError as e:
        print(f"Invalid input: {e}")


def delete_movie(movies):
    """
    Delete a movie from the collection.

    Prompts the user for a movie title (case-insensitive).
    Removes it if found, otherwise prints a message.

    Args:
        movies (dict): Dictionary of movies with titles as keys.
    """
    del_movie = input("Enter movie name to delete: ").strip()

    for title in movies:
        if title.lower() == del_movie.lower():
            movie_storage.delete_movie(title)
            print(f"{title} successfully deleted")
            return
    else:
        print(f"{del_movie} not in movie list")



def update_movie(movies):
    """
    Update the rating of an existing movie.

    Args:
        movies (dict): Dictionary of movies with titles as keys.
    """
    update = input("Enter movie name to update")
    if update not in movies:
        print(f"{update} is not in movie list")
        return
    try:
        new_rate = input("Enter new rating to update: ")
        movie_storage.update_movie(update, float(new_rate))
        print(f"{update} successfully updated")
    except ValueError as e:
        print(f"Invalid input: {e}")


def stats(movies):
    """
    Print statistics about the movies collection.
    Handles ratings stored as '7.9/10'.
    """
    ratings = []

    # Konvertiere alle Ratings
    for value in movies.values():
        rating_str = str(value["rating"])
        if rating_str.endswith("/10"):
            rating = float(rating_str.replace("/10", ""))
        else:
            rating = float(rating_str)
        ratings.append(rating)

    if not ratings:
        print("No movies available.")
        return

    average = sum(ratings) / len(ratings)
    median = statistics.median(ratings)

    max_rating = max(ratings)
    best_movies = [title for title, info in movies.items()
                   if str(info["rating"]).startswith(str(max_rating))]

    min_rating = min(ratings)
    worst_movies = [title for title, info in movies.items()
                    if str(info["rating"]).startswith(str(min_rating))]

    # Ausgabe
    print(f"Average rating: {average:.2f}/10")
    print(f"Median rating: {median:.2f}/10")
    print("Best movie(s):")
    for film in best_movies:
        print(f"  - {film} ({max_rating}/10)")

    print("Worst movie(s):")
    for film in worst_movies:
        print(f"  - {film} ({min_rating}/10)")



def rand_movie(movies):
    """
    Pick and display a random movie from the collection.

    Args:
        movies (dict): Dictionary of movies.
    """
    title, value = random.choice(list(movies.items()))
    print(f"Random movie: {title} year: {value["year"]} rating: {value["rating"]}")


def search_movie(movies):
    """
    Search for movies containing a substring in their title.

    Args:
        movies (dict): Dictionary of movies with title, year, rating.
    """
    search = input("Enter part of movie name: ").lower()
    found = False

    for title, value in movies.items():
        if search in title.lower():  # case-insensitive Vergleich
            print(f"{title}, {value["year"]}, {value["rating"]}")
            found = True

    if not found:
        print("No matching movies found.")


def sort_by_rating(movies):
    """
    Print all movies sorted by rating (highest first).

    Args:
        movies (dict): Dictionary of movies.
    """
    # sort movies
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)

    # Output sorted movies
    for title, value in sorted_movies:
        print(f"{title}, {value["year"]}, {value["rating"]}")

def generate_website(movies):
    """
    Generate an HTML website from the movies dictionary.
    """
    # read Template
    with open("_static/index_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # generate Movie-Grid HTML
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

    # replace placeholder
    html_content = template.replace("__TEMPLATE_TITLE__", "My Movie App")
    html_content = html_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # edit css reference to _static
    html_content = html_content.replace('href="style.css"', 'href="_static/style.css"')

    # add charset
    if "<meta charset=" not in html_content:
        html_content = html_content.replace(
            "<head>",
            "<head>\n    <meta charset=\"UTF-8\">",
            1
        )

    # store index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Website was generated successfully.")



def menu():
    """
    Display the menu, get user input, and execute the chosen option.
    """
    print(MENU)
    movies = movie_storage.get_movies()
    menu_choice = user_input()
    if menu_choice == 0:
        print("Bye!")
        sys.exit()
    elif menu_choice == 1:
        list_movie(movies)
    elif menu_choice == 2:
        add_movie(movies)
    elif menu_choice == 3:
        delete_movie(movies)
    elif menu_choice == 4:
        update_movie(movies)
    elif menu_choice == 5:
        stats(movies)
    elif menu_choice == 6:
        rand_movie(movies)
    elif menu_choice == 7:
        search_movie(movies)
    elif menu_choice == 8:
        sort_by_rating(movies)
    elif menu_choice == 9:
        generate_website(movies)

    input("Press enter to continue")


def main():
    """
    Main loop of the program. Keeps showing the menu until the user exits.
    """
    while True:
        menu()


if __name__ == "__main__":
    main()
