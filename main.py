import sqlite3
import easygui
from tabulate import tabulate

MENU_BUTTONS = ['Add', 'View', 'Search', 'Delete', 'Exit']
MENU_TITLE = "Main menu"
VIEW_HEADERS = ["ID","Name","Year","Rating","Length","Genre"]
FILTER_CHOICES = ["Descending","Id", "Name", "Year", "Rating", "Length", "Genre"]

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
   ENTRIES = ["Movie Name", "Movie Release Date", "Movie Rating", "Movie Run Time", "Movie Genre"]
   add_movie_data = easygui.multenterbox("Enter in the details of your Movie!", title="Add Movie", fields=ENTRIES)

if menu_action == 'Search':
    searched_movie = easygui.enterbox("What is the name of your movie?")
    output = cursor.execute(f"SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre FROM movie_collection_table INNER JOIN genre_table ON movie_collection_table.movie_genre=genre_table.ID WHERE movie_collection_table.movie_name LIKE '%{searched_movie}%' ORDER BY movie_collection_table.ID ASC")
    easygui.msgbox(tabulate(output, headers=VIEW_HEADERS))



