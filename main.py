import sqlite3
import easygui

MENU_BUTTONS = ['Add', 'View', 'Search', 'Delete', 'Exit']
MENU_TITLE = "Main menu"

conn = sqlite3.connect('film-collection.db')
cursor = conn.cursor()

output=""

menu_action = easygui.buttonbox("Welcome to your Movie Catalog!", title=MENU_TITLE, choices=MENU_BUTTONS)

if menu_action == 'View':
    for row in cursor.execute("SELECT * FROM movie_collection_table ORDER BY ID ASC"):
        id, movie_name, movie_release_date, movie_rating, movie_run_time, movie_genre = row
        output += f"{row} \n"
    easygui.msgbox(output)
    



