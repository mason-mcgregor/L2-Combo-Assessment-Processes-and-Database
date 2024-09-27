"""This fle is used to manage a movie database."""
import sqlite3
import easygui
from tabulate import tabulate
from datetime import datetime

MENU_BUTTONS = ['Add', 'View', 'Search', 'Delete', 'Edit', 'Exit']
MENU_TITLE = "Main menu"
VIEW_HEADERS = ["ID", "Name", "Year", "Rating", "Length", "Genre"]
FILTER_CHOICES = ["Ascending", "Descending",
                  "Id", "Name", "Year", "Rating", "Length", "Genre"]

conn = sqlite3.connect('film-collection.db')
cursor = conn.cursor()

items = ""
edit_repeat = True
secret_message = False
name_changing = False


def search():
    """Search the database based off a searched movie."""
    cursor.execute("""
    SELECT movie_collection_table.id, movie_name,
        movie_release_date, movie_rating, movie_run_time, genre
    FROM movie_collection_table
    INNER JOIN genre_table
    ON movie_collection_table.movie_genre = genre_table.ID
    WHERE movie_collection_table.movie_name LIKE ?
    ORDER BY movie_collection_table.ID ASC
    """, (f'%{searched_movie}%',))

    output = cursor.fetchall()

    if not output:
        easygui.msgbox("No movies found.")
    else:
        global formatted_output
        formatted_output = tabulate(output, headers=VIEW_HEADERS)

        cursor.execute("""
        SELECT movie_name
        FROM movie_collection_table
        WHERE movie_collection_table.movie_name LIKE ?
        """, (f'%{searched_movie}%',))
        global choices
        choices = [row[0] for row in cursor.fetchall()]


def genre_call():
    """Select all the genres from the genre table and add them to a list."""
    cursor.execute("SELECT ID, genre FROM genre_table")
    genres = cursor.fetchall()
    global genre_list
    genre_list = [[genre[0], genre[1]] for genre in genres]


def rating_call():
    """Select all the ratings from the rating table and add them to a list."""
    cursor.execute("SELECT key FROM rating_table")
    ratings = cursor.fetchall()
    global rating_list
    rating_list = [rating[0] for rating in ratings]


def update_movie():
    """Update the values of a selected movie in the database."""
    global edit_movie
    conn.execute(f"""
        UPDATE movie_collection_table
        SET {data_type} = ?
        WHERE movie_name LIKE ?
        """, (new_value, f'%{edit_movie}%'))

    conn.commit()  # Save the changes

    if name_changing == "yes":
        edit_movie = new_name_value

    # Execute the SELECT query based on the (possibly) new movie name
    cursor.execute("""
        SELECT movie_collection_table.id, movie_name,
        movie_release_date, movie_rating, movie_run_time, genre
        FROM movie_collection_table
        INNER JOIN
        genre_table ON movie_collection_table.movie_genre = genre_table.ID
        WHERE movie_collection_table.movie_name LIKE ?
        """, (f'%{edit_movie}%',))

    global updated_output
    updated_output = cursor.fetchall()
    global secret_message
    secret_message = True

    edit_again = easygui.buttonbox("Updated Movie:\n\n"
                                   f"{tabulate(updated_output,headers=VIEW_HEADERS)}"
                                   "\n\nAnother Edit?", choices=['Yes', 'No'])

    if edit_again == "No":
        global edit_repeat
        edit_repeat = False


while True:

    menu_action = easygui.buttonbox("Welcome to your Movie Catalog!",
                                    title=MENU_TITLE, choices=MENU_BUTTONS)

    if menu_action == 'View':
        sort = "ASC"
        filter = "movie_collection_table.ID"
        while not sort == "exit":
            output = cursor.execute(f"""
            SELECT
            movie_collection_table.id, movie_name, movie_release_date,
            movie_rating, movie_run_time, genre
            FROM movie_collection_table
            INNER JOIN genre_table ON
            movie_collection_table.movie_genre=genre_table.ID
            ORDER BY {filter} {sort}""")
            veiw_sort = easygui.choicebox(
                tabulate(output, headers=VIEW_HEADERS),
                choices=FILTER_CHOICES)
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

        genre_call()

        rating_call()

        movie_release_date = []

        valid_movie_name = False
        while not valid_movie_name:
            movie_name = easygui.enterbox("Enter the name of the movie")
            if movie_name is None:
                easygui.msgbox("Input Cancelled")
                break
            # test input for validity
            if movie_name == "":
                easygui.msgbox("Movie name can't be blank, please re-enter")
            else:
                valid_movie_name = True
        if movie_name is None:
            continue

        valid_movie_date = False
        while not valid_movie_date:
            try:
                field_names = ["Day", "Month", "Year"]
                # Get release date input
                movie_release_date = easygui.multenterbox(
                    "Enter the movie release date", fields=field_names)

                # Check if the user canceled the input box
                if movie_release_date is None:
                    easygui.msgbox("Input cancelled.")
                    break

                # Test input for validity before parsing the date
                if any(field.strip() == "" for field in movie_release_date):
                    easygui.msgbox("A feild has been left blank, re-enter.")
                    continue  # Skip to the next iteration of the loop

                # Try to parse the date only after ensuring valid input
                movie_date = datetime.strptime(f"{movie_release_date[2]}-{movie_release_date[1]}-{movie_release_date[0]}", "%Y-%m-%d").date()

                # Define the lower boundary (Jan 1, 1888)
                lower_boundary = datetime(1888, 1, 1).date()
                # Define the current date as the upper boundary
                upper_boundary = datetime.now().date()

                # Check if the date is between Jan 1, 1888 and today's date
                if lower_boundary <= movie_date <= upper_boundary:
                    easygui.msgbox(f"Valid movie release date: {movie_date}")
                else:
                    easygui.msgbox(f"Invalid movie release date: {movie_date}")
                    continue

                # If the parsing is successful, set valid_movie_date to True
                valid_movie_date = True

            except (ValueError, TypeError):
                # Handle incorrect date formats or type errors
                easygui.msgbox("Invalid date format. Please try again.")

        if movie_release_date is None:
            continue

        valid_movie_rating = False
        while not valid_movie_rating:
            movie_rating = easygui.choicebox("Movie Rating",
                                             choices=rating_list)
            if movie_rating is None:
                easygui.msgbox("Input Cancelled")
                break

            valid_movie_rating = True

        if movie_rating is None:
            continue

        valid_movie_length = False
        while not valid_movie_length:
            movie_run_time = easygui.integerbox("Movie Run Time",
                                                lowerbound=1, upperbound=1000)
            if movie_run_time is None:
                easygui.msgbox("Input Cancelled")
                break
            # test input for validity
            if movie_run_time == "":
                easygui.msgbox("Movie length can't be blank, please re-enter")
            else:
                valid_movie_length = True
        if movie_run_time is None:
            continue

        valid_movie_genre = False
        while not valid_movie_genre:
            movie_genre = easygui.choicebox("Movie Genre", choices=genre_list)

            if movie_genre is None:
                easygui.msgbox("Input Cancelled")
                break

            valid_movie_genre = True

        if movie_genre is None:
            continue

        movie_date = ("" + movie_release_date[2] + "-"
                      + movie_release_date[1] +
                      "-" + movie_release_date[0] + "")

        movie_genre = movie_genre.replace("[", "") \
            .replace("]", "").split(",")[0]

        conn.execute(f'''
        INSERT INTO movie_collection_table
        (movie_name, movie_release_date, movie_rating,
                     movie_run_time, movie_genre)
        VALUES
            ('{movie_name}', '{movie_date}',
            '{movie_rating}', '{movie_run_time}', '{movie_genre}')
        ''')

        conn.commit()

        cursor.execute(f"""
        SELECT movie_collection_table.id, movie_name,
        movie_release_date, movie_rating, movie_run_time, genre
        FROM movie_collection_table
        INNER JOIN genre_table
        ON movie_collection_table.movie_genre = genre_table.ID
        WHERE movie_collection_table.movie_name LIKE ?
        """, (f'%{movie_name}%',))

        added_movie_output = cursor.fetchall()

        added_movie = easygui.msgbox(f"Added Movie:\n\n{tabulate(added_movie_output,headers=VIEW_HEADERS)}\n\n")

    if menu_action == 'Delete':
        searched_movie = easygui.enterbox("What is the name of the movie you want to delete?")     

        if searched_movie:
            cursor.execute(f"""
            SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre 
            FROM movie_collection_table 
            INNER JOIN genre_table 
            ON movie_collection_table.movie_genre = genre_table.ID 
            WHERE movie_collection_table.movie_name LIKE ?
            ORDER BY movie_collection_table.ID ASC
            """, (f'%{searched_movie}%',))

            output = cursor.fetchall()

            if not output:
                easygui.msgbox("No movies found.")
            else:
                formatted_output = tabulate(output, headers=VIEW_HEADERS)

                cursor.execute(f"""
                SELECT movie_name 
                FROM movie_collection_table 
                WHERE movie_collection_table.movie_name LIKE ?
                """, (f'%{searched_movie}%',))
                
                choices = [row[0] for row in cursor.fetchall()]

                correct_delete_movie = False
                while correct_delete_movie == False:
                    deleted_movie = easygui.choicebox(f"Select the movie to delete:\n\n{formatted_output}", choices=choices)

                    if deleted_movie == None:
                        easygui.msgbox("Action Cancelled")
                        break

                    confirmed_delete_movie = easygui.buttonbox(f"Are you sure you want to delete {deleted_movie}", choices=["Yes", "No"])

                    if confirmed_delete_movie == "Yes":
                        correct_delete_movie = True


                if deleted_movie:
                    cursor.execute("DELETE FROM movie_collection_table WHERE movie_name = ?", (deleted_movie,))
                    conn.commit()  # Don't forget to commit the transaction
                    easygui.msgbox(f"'{deleted_movie}' has been deleted from the database.")
                else:
                    easygui.msgbox("No movie was selected for deletion.")
        else:
            easygui.msgbox("No movie name entered.")

    if menu_action == 'Search':
        searched_movie = easygui.enterbox("What is the name of the movie you want to Search?")

        if searched_movie:
            search()
        else:
            easygui.msgbox("No movie name entered.")
        
        searched_movie_results = easygui.buttonbox(f"Searched results:\n\n{formatted_output}", choices=["Edit", "Delete"])
        if not searched_movie_results:  # Handle cancel or no selection
            continue  # Exit if the user closes the window or doesn't select an option
        
    if menu_action == 'Edit':
        searched_movie = easygui.enterbox("What is the name of the movie you want to Search?")

        if searched_movie:
            search()
        else:
            easygui.msgbox("No movie name entered.")
        
        searched_movie_results = easygui.buttonbox(f"Searched results:\n\n{formatted_output}", choices=["Edit", "Delete"])
        if not searched_movie_results:  # Handle cancel or no selection
            continue  # Exit if the user closes the window or doesn't select an option

        if searched_movie_results == "Edit":
            edit_movie = easygui.choicebox(f"Select the movie to Edit:\n\n{formatted_output}", choices=choices)
            if not edit_movie:  # Handle if no movie is selected
                easygui.msgbox("No movie selected.")
                continue

            cursor.execute(f"""
                SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre
                FROM movie_collection_table
                INNER JOIN genre_table ON movie_collection_table.movie_genre = genre_table.ID
                WHERE movie_collection_table.movie_name = ?
            """, (edit_movie,))
            
            output = cursor.fetchall()

            while edit_repeat == True:
                
                if secret_message == True:
                    output = updated_output

                edit_catagory = easygui.choicebox(f"Selected Movie:\n\n{tabulate(output, headers=VIEW_HEADERS)}\n\nSelect the catagory to Edit:", choices=VIEW_HEADERS)
                if not edit_catagory:  # Handle if no category is selected
                    easygui.msgbox("No category selected.")
                    edit_repeat = False  # Exit if no category is selected

                if edit_catagory == 'ID':
                    valid_id = False
                    while valid_id == False:
                        new_id_value = easygui.integerbox(f"Enter new ID for {edit_movie}:", lowerbound=1, upperbound=1000)

                        # Check if the new ID already exists in the database
                        cursor.execute("""
                            SELECT id FROM movie_collection_table WHERE id = ?
                        """, (new_id_value,))
                        existing_id = cursor.fetchone()

                        if existing_id:  # If ID exists, notify the user
                            easygui.msgbox(f"ID {new_id_value} is already taken. Please choose another one.")
                            continue  # Exit to prompt for another ID
                        else:
                            valid_id = True

                    if new_id_value is None:
                        easygui.msgbox("No ID entered.")
                        continue  # Exit if no ID is entered
                    new_value = new_id_value
                    data_type = "id"
                    name_changing = "no"
                    update_movie()
                   
                elif edit_catagory == 'Name':
                    valid_new_movie_name = False
                    while not valid_new_movie_name:
                        new_name_value = easygui.enterbox(f"Enter new Name for {edit_movie}:")
                        if new_name_value == None:
                            easygui.msgbox("No name entered.")
                            break
                        # test input for validity
                        if new_name_value == "":
                            easygui.msgbox("Movie name can't be blank, please re-enter")
                        else:
                            valid_new_movie_name = True
                    if new_name_value is None:
                        continue        

                    new_value = new_name_value
                    data_type = "movie_name"
                    name_changing = "yes"
                    update_movie()

                elif edit_catagory == 'Year':

                    valid_new_movie_date = False
                    while not valid_new_movie_date:
                        try:
                            field_names = ["Day", "Month", "Year"]
                            # Get release date input
                            new_movie_release_date = easygui.multenterbox("ENter the movie release date", fields=field_names)

                            # Check if the user canceled the input box
                            if new_movie_release_date is None:
                                easygui.msgbox("Input cancelled.")
                                break

                            # Test input for validity before parsing the date
                            if any(field.strip() == "" for field in new_movie_release_date):
                                easygui.msgbox("A feild has been left blank, re-enter.")
                                continue  # Skip to the next iteration of the loop

                            # Try to parse the date only after ensuring valid input
                            new_movie_date = datetime.strptime(f"{new_movie_release_date[2]}-{new_movie_release_date[1]}-{new_movie_release_date[0]}", "%Y-%m-%d").date()

                            # Define the lower boundary (Jan 1, 1888)
                            lower_boundary = datetime(1888, 1, 1).date()
                            # Define the current date as the upper boundary
                            upper_boundary = datetime.now().date()

                            # Check if the date is between Jan 1, 1888 and today's date
                            if lower_boundary <= new_movie_date <= upper_boundary:
                                easygui.msgbox(f"Valid movie release date: {new_movie_date}")
                            else:
                                easygui.msgbox(f"Invalid movie release date: {new_movie_date}")
                                continue

                            # If the parsing is successful, set valid_movie_date to True
                            valid_new_movie_date = True

                        except (ValueError, TypeError):
                            # Handle incorrect date formats or type errors
                            easygui.msgbox("Invalid date format. Please try again.")

                        
                    if new_movie_release_date is None:
                        continue   

                    new_value = new_movie_date
                    data_type = "movie_release_date"
                    name_changing = "no"
                    update_movie()

                elif edit_catagory == 'Rating':
                    rating_call()
                    new_rating_value = easygui.choicebox(f"Select new Rating for {edit_movie}:", choices=rating_list)
                    if not new_rating_value:
                        easygui.msgbox("No rating selected.")
                        continue  # Exit if no rating is selected
                    new_value = new_rating_value
                    data_type = "movie_rating"
                    name_changing = "no"
                    update_movie()

                elif edit_catagory == 'Length':
                    new_length_value = easygui.integerbox(f"Enter new Run Time for {edit_movie}:", lowerbound=1, upperbound=1000)
                    if new_length_value is None:
                        easygui.msgbox("No run time entered.")
                        continue  # Exit if no run time is entered
                    new_value = new_length_value
                    data_type = "movie_run_time"
                    name_changing = "no"
                    update_movie()

                elif edit_catagory == 'Genre':
                    genre_call()
                    new_genre_value = easygui.choicebox(f"Select new Rating for {edit_movie}:", choices=genre_list)
                    if not new_genre_value:
                        easygui.msgbox("No genre selected.")
                        continue  # Exit if no genre is selected
                    new_value = new_genre_value.replace("[","").replace("]","").split(",")[0]
                    data_type = "movie_genre"
                    name_changing = "no"
                    update_movie() 

    if menu_action == "Exit":
        easygui.msgbox("Bye")
        quit()