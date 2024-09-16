import sqlite3
import easygui
from tabulate import tabulate

MENU_BUTTONS = ['Add', 'View', 'Search', 'Delete', 'Exit']
MENU_TITLE = "Main menu"
VIEW_HEADERS = ["ID","Name","Year","Rating","Length","Genre"]
FILTER_CHOICES = ["Ascending", "Descending","Id", "Name", "Year", "Rating", "Length", "Genre"]

conn = sqlite3.connect('film-collection.db')
cursor = conn.cursor()

items =""

menu_action = easygui.buttonbox("Welcome to your Movie Catalog!", title=MENU_TITLE, choices=MENU_BUTTONS)

if menu_action == 'View':
    sort = "ASC"
    filter = "movie_collection_table.ID"
    while not sort == "exit":
        output = cursor.execute(f"SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre FROM movie_collection_table INNER JOIN genre_table ON movie_collection_table.movie_genre=genre_table.ID ORDER BY {filter} {sort}")
        veiw_sort = easygui.choicebox(tabulate(output, headers=VIEW_HEADERS), choices=FILTER_CHOICES)
        if veiw_sort == "Descending":
            sort = "DESC"
        elif veiw_sort == "Ascending":
            sort = "ASC"
        elif veiw_sort == "Id":
            filter = "movie_collection_table.ID"
        elif veiw_sort == "Name":
            filter = "movie_collection_table.movie_name"
        elif veiw_sort == "Year":
            filter = "movie_collection_table.movie_release_date"
        elif veiw_sort == "Rating":
            filter = "movie_collection_table.movie_rating"
        elif veiw_sort == "Length":
            filter = "movie_collection_table.movie_run_time"
        elif veiw_sort == "Genre":
            filter = "movie_collection_table.movie_genre"
        else:
            sort = "exit"

if menu_action == 'Add':

    cursor.execute("SELECT genre FROM genre_table")
    genres = cursor.fetchall()
    genre_list = [genre[0] for genre in genres]

    cursor.execute("SELECT key FROM rating_table")
    ratings = cursor.fetchall()
    rating_list = [rating[0] for rating in ratings]

    feild_names = ["Day", "Month", "Year"]
    movie_release_date = []
    movie_name = easygui.enterbox("Eneter the name of the movie")
    movie_release_date = easygui.multenterbox("ENter the movie release date", fields=feild_names)
    movie_rating = easygui.choicebox("Movie Rating", choices=rating_list)
    movie_run_time = easygui.integerbox("Movie Run Time", upperbound=1000)
    movie_genre = easygui.choicebox("Movie Genre", choices=genre_list)

    movie_date = (""+movie_release_date[2]+"-"+movie_release_date[1]+"-"+movie_release_date[0]+"")

    conn.execute(f'''
    INSERT INTO movie_collection_table (movie_name, movie_release_date, movie_rating, movie_run_time, movie_genre)
    VALUES
        ('{movie_name}', '{movie_date}', '{movie_rating}', '{movie_run_time}', '{movie_genre}')              
    ''')

    conn.commit()
    conn.close()

if menu_action == 'Delete':
    searched_movie = easygui.enterbox("What is the name of the movie you want to delete?")

    if searched_movie:
        # Fetch the movie details based on the user's input
        cursor.execute(f"""
        SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre 
        FROM movie_collection_table 
        INNER JOIN genre_table 
        ON movie_collection_table.movie_genre = genre_table.ID 
        WHERE movie_collection_table.movie_name LIKE ?
        ORDER BY movie_collection_table.ID ASC
        """, (f'%{searched_movie}%',))

        # Fetch all matching results
        output = cursor.fetchall()

        # If no results are found, show a message
        if not output:
            easygui.msgbox("No movies found.")
        else:
            # Display the movies in a table format with headers
            VIEW_HEADERS = ['ID', 'Name', 'Release Date', 'Rating', 'Run Time', 'Genre']
            formatted_output = tabulate(output, headers=VIEW_HEADERS, tablefmt="simple_grid")

            # Get a list of movie names for the choicebox
            cursor.execute(f"""
            SELECT movie_name 
            FROM movie_collection_table 
            WHERE movie_collection_table.movie_name LIKE ?
            """, (f'%{searched_movie}%',))
            
            choices = [row[0] for row in cursor.fetchall()]

            # Show the choicebox with the list of movies to delete
            deleted_movie = easygui.choicebox(f"Select the movie to delete:\n\n{formatted_output}", choices=choices)

            if deleted_movie:
                # Delete the selected movie
                cursor.execute("DELETE FROM movie_collection_table WHERE movie_name = ?", (deleted_movie,))
                conn.commit()  # Don't forget to commit the transaction
                easygui.msgbox(f"'{deleted_movie}' has been deleted from the database.")
            else:
                easygui.msgbox("No movie was selected for deletion.")
    else:
        easygui.msgbox("No movie name entered.")

if menu_action == 'Search':
    searched_movie = easygui.enterbox("What is the name of your movie?")
    output = cursor.execute(f"SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre FROM movie_collection_table INNER JOIN genre_table ON movie_collection_table.movie_genre=genre_table.ID WHERE movie_collection_table.movie_name LIKE '%{searched_movie}%' ORDER BY movie_collection_table.ID ASC")
    easygui.msgbox(tabulate(output, headers=VIEW_HEADERS))



