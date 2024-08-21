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
    



