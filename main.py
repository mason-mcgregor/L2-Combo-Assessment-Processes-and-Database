import sqlite3
import easygui

MENU_BUTTONS = ['Add', 'View', 'Search', 'Delete', 'Exit']
MENU_TITLE = "Main menu"

conn = sqlite3.connect('film-collection.db')
cursor = conn.cursor()


output = ""
items =""

menu_action = easygui.buttonbox("Welcome to your Movie Catalog!", title=MENU_TITLE, choices=MENU_BUTTONS)

if menu_action == 'View':
    for row in cursor.execute("SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre FROM movie_collection_table INNER JOIN genre_table ON movie_collection_table.movie_genre=genre_table.ID ORDER BY movie_collection_table.ID ASC"):
        id, movie_name, movie_release_date, movie_rating, movie_run_time, genre = row
        for item in row:
            items += f"{item} "
        output += f"{items} \n"
        items = ""
        
    easygui.msgbox(output)

if menu_action == 'Add':
    new_movie_name = easygui.enterbox("What is the movie name?")
    new_movie_release_date = easygui.enterbox("When was the movie released?")
    new_movie_rating = easygui.enterbox("What is the movies rating?")
    new_movie_run_time = easygui.enterbox("How long does the movie run for?")
    new_movie_genre =easygui.enterbox("What Genre is the movie?")



