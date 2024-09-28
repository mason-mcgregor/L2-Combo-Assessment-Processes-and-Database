"""This fle is used to manage a movie database."""
import sqlite3
import easygui
from tabulate import tabulate
from datetime import datetime

MENU_BUTTONS = ['Add', 'View', 'Search', 'Delete', 'Edit', 'Exit'] #Menu buttons
MENU_TITLE = "Main menu" #Main menu title
VIEW_HEADERS = ["ID", "Name", "Year", "Rating", "Length", "Genre"] #Table headers
FILTER_CHOICES = ["Ascending", "Descending",
                  "Id", "Name", "Year", "Rating", "Length", "Genre"] #Options to filter the data by

conn = sqlite3.connect('film-collection.db') #Connect the database
cursor = conn.cursor() #Connect the Cursor

items = "" #Empty for items
edit_repeat = True #Keep the edit loop going
moive_is_updated = False #Movie hasn't been updated
name_changing = False #Name isn't being changed


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
    """, (f'%{searched_movie}%',)) #Select all the data based on "searched movie"

    output = cursor.fetchall() #Assign the data to a "output"

    if not output: #Check if the movie exists in the database
        easygui.msgbox("No movies found.")
    else: #Movie exists
        global formatted_output
        formatted_output = tabulate(output, headers=VIEW_HEADERS) #Displays the data in a table format

        cursor.execute("""
        SELECT movie_name
        FROM movie_collection_table
        WHERE movie_collection_table.movie_name LIKE ?
        """, (f'%{searched_movie}%',)) #Select any similar movies to the searched movie name
        global choices
        choices = [row[0] for row in cursor.fetchall()] #Add the results to a list


def genre_call():
    """Select all the genres from the genre table and add them to a list."""
    cursor.execute("SELECT ID, genre FROM genre_table") #Select all the genres from the genre table
    genres = cursor.fetchall() #Assign the results to "genres"
    global genre_list
    genre_list = [[genre[0], genre[1]] for genre in genres] #Add the results to a list


def rating_call():
    """Select all the ratings from the rating table and add them to a list."""
    cursor.execute("SELECT key FROM rating_table") #Select all the rating from the rating table
    ratings = cursor.fetchall() #Assign the results to "ratings"
    global rating_list
    rating_list = [rating[0] for rating in ratings] #Add the results to a list


def update_movie():
    """Update the values of a selected movie in the database."""
    global edit_movie
    conn.execute(f"""
        UPDATE movie_collection_table
        SET {data_type} = ?
        WHERE movie_name LIKE ?
        """, (new_value, f'%{edit_movie}%')) #Update the data of "Edit Movie"

    conn.commit()  # Save the changes

    if name_changing == "yes": #Check if the movie name is being changed
        edit_movie = new_name_value #Override the old name

    cursor.execute("""
        SELECT movie_collection_table.id, movie_name,
        movie_release_date, movie_rating, movie_run_time, genre
        FROM movie_collection_table
        INNER JOIN
        genre_table ON movie_collection_table.movie_genre = genre_table.ID
        WHERE movie_collection_table.movie_name LIKE ?
        """, (f'%{edit_movie}%',)) #Select the updated movie

    global updated_output
    updated_output = cursor.fetchall() #Assign the results to "updated_output"
    global moive_is_updated
    moive_is_updated = True #Movie has been updated

    edit_again = easygui.buttonbox("Updated Movie:\n\n"
                                   f"{tabulate(updated_output,headers=VIEW_HEADERS)}"
                                   "\n\nAnother Edit?", choices=['Yes', 'No']) #Display the updated movie and ask if the user want to make more changes

    if edit_again == "No": #Check if the user doesn't want to make more changes
        global edit_repeat
        edit_repeat = False #End the loop


while True: #Main Loop

    menu_action = easygui.buttonbox("Welcome to your Movie Catalog!",
                                    title=MENU_TITLE, choices=MENU_BUTTONS) #Main menu screen

    if menu_action == 'View': #Check if the user wants to view the database
        sort = "ASC" #Sort the data by ascending order
        filter = "movie_collection_table.ID" #Filter the data by movie id
        while not sort == "exit": #Loops forever until the user exits
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
                choices=FILTER_CHOICES) #Display the data and sort by "sort" variable and filter by "filter" variable
            if veiw_sort == "Descending": #Check if the user wants to display the data in a Descending Order
                sort = "DESC" #Change order to descending
            elif veiw_sort == "Ascending": #Check if the user wants to display the data in a Ascending Order
                sort = "ASC" #Change order to Ascending
            elif veiw_sort == "Id": #Check if the user wants to filter by ID
                filter = "movie_collection_table.ID" #Change filter to ID
            elif veiw_sort == "Name": #Check if the user wants to filter by Name
                filter = "movie_collection_table.movie_name" #Change filter to Name
            elif veiw_sort == "Year": #Check if the user wants to filter by Year
                filter = "movie_collection_table.movie_release_date" #Change filter to Year
            elif veiw_sort == "Rating":#Check if the user wants to filter by Rating
                filter = "movie_collection_table.movie_rating" #Change filter to Rating
            elif veiw_sort == "Length":#Check if the user wants to filter by Length
                filter = "movie_collection_table.movie_run_time" #Change filter to Length
            elif veiw_sort == "Genre":#Check if the user wants to filter by Genre
                filter = "movie_collection_table.movie_genre" #Change filter to Genre
            else:
                sort = "exit" #End the loop

    if menu_action == 'Add': #Check if the user wants to add to the database

        genre_call() #Get all the genres

        rating_call() #Gent all the ratings

        movie_release_date = [] #Empty list for the release date

        valid_movie_name = False
        while not valid_movie_name: #Loop till a valid movie name
            movie_name = easygui.enterbox("Enter the name of the movie") #Get movie name from the user
            if movie_name is None: #Check if the user has entered a name
                easygui.msgbox("Input Cancelled") 
                break #End the loop

            if movie_name == "": #Check if the user entered a blank name
                easygui.msgbox("Movie name can't be blank, please re-enter")
            else:
                valid_movie_name = True #End the loop
        if movie_name is None: #Check if the user cancelled the input
            continue #Return to the main menu

        valid_movie_date = False
        while not valid_movie_date: #Loop till a valid movie date
            try:
                field_names = ["Day", "Month", "Year"]
                movie_release_date = easygui.multenterbox(
                    "Enter the movie release date", fields=field_names)#Get release date input

                if movie_release_date is None: #Check if the user canceled the input box
                    easygui.msgbox("Input cancelled.")
                    break #End the loop

                if any(field.strip() == "" for field in movie_release_date): #Check if any felid has been left blank
                    easygui.msgbox("A feild has been left blank, re-enter.")
                    continue  #Return to ask the user for the date again

                movie_date = datetime.strptime(
                    f"{movie_release_date[2]}-{movie_release_date[1]}-{movie_release_date[0]}",
                    "%Y-%m-%d").date() #Re-order the date to be valid to insert into the database

                lower_boundary = datetime(1888, 1, 1).date() #Define the earliest date (Jan 1, 1888)
                upper_boundary = datetime.now().date() #Define the current date as the latest date

                if lower_boundary <= movie_date <= upper_boundary: #Check if the date is between Jan 1, 1888 and today's date
                    easygui.msgbox(f"Valid movie release date: {movie_date}")
                else:
                    easygui.msgbox(f"Invalid movie release date: {movie_date}")
                    continue

                valid_movie_date = True #End the loop date is valid

            except (ValueError, TypeError): #Handle incorrect date formats or type errors
                easygui.msgbox("Invalid date format. Please try again.")

        if movie_release_date is None: #Check if the user cancelled the input
            continue #Return to the main menu

        valid_movie_rating = False
        while not valid_movie_rating: #Loop till a valid movie rating
            movie_rating = easygui.choicebox("Movie Rating",
                                             choices=rating_list) #Get the rating from the user
            if movie_rating is None: #Check if the user cancelled the input
                easygui.msgbox("Input Cancelled")
                break #Return to the main menu

            valid_movie_rating = True #End the loop

        if movie_rating is None: #Check if the user cancelled the input
            continue #Return to the main menu

        valid_movie_length = False
        while not valid_movie_length: #Loop till valid movie length
            movie_run_time = easygui.integerbox("Movie Run Time",
                                                lowerbound=1, upperbound=1000) #Get the movie length from the user
            if movie_run_time is None: #Check if the user cancelled the input
                easygui.msgbox("Input Cancelled")
                break #Return to the main menu

            if movie_run_time == "": #Check if the user left the input blank
                easygui.msgbox("Movie length can't be blank, please re-enter")
            else:
                valid_movie_length = True #End the loop

        if movie_run_time is None: #Check if the user cancelled the input
            continue #Return to the main menu

        valid_movie_genre = False
        while not valid_movie_genre: #Loop till valid movie genre
            movie_genre = easygui.choicebox("Movie Genre", choices=genre_list) #Get the movie genre from the user

            if movie_genre is None: #Check if the user cancels the input
                easygui.msgbox("Input Cancelled")
                break #End the loop

            valid_movie_genre = True #End the loop

        if movie_genre is None: #Check if user cancelled the input
            continue #Return to the main menu

        movie_date = ("" + movie_release_date[2] + "-"
                      + movie_release_date[1] +
                      "-" + movie_release_date[0] + "") #Formats the date to be inserted into the database

        movie_genre = movie_genre.replace("[", "") \
            .replace("]", "").split(",")[0] #Formats the movie genre to be inserted ito the data base

        conn.execute(f'''
        INSERT INTO movie_collection_table
        (movie_name, movie_release_date, movie_rating,
                     movie_run_time, movie_genre)
        VALUES
            ('{movie_name}', '{movie_date}',
            '{movie_rating}', '{movie_run_time}', '{movie_genre}')
        ''') #Insert the new movie into the database

        conn.commit() #Save the changes

        cursor.execute(f"""
        SELECT movie_collection_table.id, movie_name,
        movie_release_date, movie_rating, movie_run_time, genre
        FROM movie_collection_table
        INNER JOIN genre_table
        ON movie_collection_table.movie_genre = genre_table.ID
        WHERE movie_collection_table.movie_name LIKE ?
        """, (f'%{movie_name}%',)) #Select the new movie

        added_movie_output = cursor.fetchall()

        added_movie = easygui.msgbox(
            f"Added Movie:\n\n{tabulate(added_movie_output,headers=VIEW_HEADERS)}\n\n") #Display the new movie

    if menu_action == 'Delete': #Check if the user wants to delete from the database
        searched_movie = easygui.enterbox(
            "What is the name of the movie you want to delete?") #Ask the user what movie they want to search

        if searched_movie:
            cursor.execute("""
            SELECT movie_collection_table.id, movie_name,
            movie_release_date, movie_rating, movie_run_time, genre
            FROM movie_collection_table
            INNER JOIN genre_table
            ON movie_collection_table.movie_genre = genre_table.ID
            WHERE movie_collection_table.movie_name LIKE ?
            ORDER BY movie_collection_table.ID ASC
            """, (f'%{searched_movie}%',)) #Select all the data for the searched movie

            output = cursor.fetchall()

            if not output: #Check if there was a movie found
                easygui.msgbox("No movies found.")
            else:
                formatted_output = tabulate(output, headers=VIEW_HEADERS) #Display all related searches

                cursor.execute("""
                SELECT movie_name
                FROM movie_collection_table
                WHERE movie_collection_table.movie_name LIKE ?
                """, (f'%{searched_movie}%',)) #Select the names of all the search results

                choices = [row[0] for row in cursor.fetchall()] #Add the results to a list

                correct_delete_movie = False
                while correct_delete_movie is False: #Loop till the correct movie is deleted
                    deleted_movie = easygui.choicebox(
                        f"Select the movie to delete:\n\n{formatted_output}",
                        choices=choices) #Ask the user what movie they want to delete out of the searched results

                    if deleted_movie is None: #Check if the user has selected a movie
                        easygui.msgbox("Action Cancelled")
                        break #End the loop

                    confirmed_delete_movie = easygui.buttonbox(
                        f"Are you sure you want to delete {deleted_movie}",
                        choices=["Yes", "No"]) #Confirm the delete

                    if confirmed_delete_movie == "Yes": #Check if the user confirmed the delete
                        correct_delete_movie = True #End the loop

                if deleted_movie: #Check if there has been a movie selected for deletion
                    cursor.execute(
                        """DELETE FROM movie_collection_table
                        WHERE movie_name = ?""", (deleted_movie,))
                    conn.commit()  # Don't forget to commit the transaction
                    easygui.msgbox(
                        f"'{deleted_movie}' has been deleted from the database.") #Delete the movie
                else:
                    easygui.msgbox("No movie was selected for deletion.")
        else:
            easygui.msgbox("No movie name entered.")

    if menu_action == 'Search': #Check if the user wants to search the database
        searched_movie = easygui.enterbox(
            "What is the name of the movie you want to Search?") #Ask the user what movie they want to search

        if searched_movie: #Check if the user entered a movie name
            search() #Search for the movie
        else:
            easygui.msgbox("No movie name entered.")

        searched_movie_results = easygui.msgbox(
            f"Searched results:\n\n{formatted_output}") #Display the search results
        if not searched_movie_results:  # Handle cancel or no selection
            continue  # Exit if the user closes the window or doesn't select an option
        
    if menu_action == 'Edit': #Check if the user wants to edit the database
        searched_movie = easygui.enterbox("What is the name of the movie you want to Search?") #Ask the user what movie they want to search

        if searched_movie: #Check if the user searched a movie
            search() #Search for the movie
        else:
            easygui.msgbox("No movie name entered.")

        searched_movie_results = "Edit"
        if searched_movie_results == "Edit": #Check if the user wants to edit
            edit_movie = easygui.choicebox(f"Select the movie to Edit:\n\n{formatted_output}", choices=choices) #Ask what movie to edit
            if not edit_movie:  # Handle if no movie is selected
                easygui.msgbox("No movie selected.")
                continue #Return to the main menu

            cursor.execute(f"""
                SELECT movie_collection_table.id, movie_name, movie_release_date, movie_rating, movie_run_time, genre
                FROM movie_collection_table
                INNER JOIN genre_table ON movie_collection_table.movie_genre = genre_table.ID
                WHERE movie_collection_table.movie_name = ?
            """, (edit_movie,)) #Selects all the data for the selected movie
            
            output = cursor.fetchall()

            while edit_repeat == True: #Loop till the user doesn't want to edit anymore
                
                if moive_is_updated == True: #Check if a movie has already been updated
                    output = updated_output

                edit_catagory = easygui.choicebox(
                    f"""Selected Movie:\n\n{tabulate(output, headers=VIEW_HEADERS)}
                    \n\nSelect the catagory to Edit:""", choices=VIEW_HEADERS) #Ask the user what catagory they want to edit
                if not edit_catagory:  # Handle if no category is selected
                    easygui.msgbox("No category selected.")
                    edit_repeat = False  # Exit if no category is selected

                if edit_catagory == 'ID': #Check if the user selected ID
                    valid_id = False
                    while valid_id == False: #Loop till a valid ID
                        new_id_value = easygui.integerbox(
                            f"Enter new ID for {edit_movie}:",
                              lowerbound=1, upperbound=1000) #Get the new ID from the user

                        cursor.execute("""
                            SELECT id FROM movie_collection_table WHERE id = ?
                        """, (new_id_value,))
                        existing_id = cursor.fetchone() #Check if the new ID already exists in the database

                        if existing_id:  #If the new ID already exist tell the user
                            easygui.msgbox(f"ID {new_id_value} is already taken. Please choose another one.")
                            continue  #Exit to ask for the new ID agian
                        else:
                            valid_id = True #End the loop

                    if new_id_value is None: #Check if the user cancelled the input
                        easygui.msgbox("No ID entered.")
                        continue  # Exit if no ID is entered
                    new_value = new_id_value
                    data_type = "id"
                    name_changing = "no"
                    update_movie() #Update the movie
                   
                elif edit_catagory == 'Name': #Check if the user has selected to edit the name
                    valid_new_movie_name = False
                    while not valid_new_movie_name: #Loop till a valid new movie name
                        new_name_value = easygui.enterbox(f"Enter new Name for {edit_movie}:") #Ask for the new movie name
                        if new_name_value == None: #Check if the user cancelled the input
                            easygui.msgbox("No name entered.")
                            break #End the loop

                        if new_name_value == "": #Check if the user left the input blank
                            easygui.msgbox("Movie name can't be blank, please re-enter")
                        else:
                            valid_new_movie_name = True #End the loop
                    if new_name_value is None: #Check if the user cancelled the input
                        continue #End the loop

                    new_value = new_name_value
                    data_type = "movie_name"
                    name_changing = "yes"
                    update_movie() #Update the movie

                elif edit_catagory == 'Year': #Check if the user has selected to edit the year

                    valid_new_movie_date = False
                    while not valid_new_movie_date: #Loop till valid new date
                        try:
                            field_names = ["Day", "Month", "Year"]
                            new_movie_release_date = easygui.multenterbox("Enter the movie release date", fields=field_names) #Get release date input

                            if new_movie_release_date is None: #Check if the user canceled the input box
                                easygui.msgbox("Input cancelled.")
                                break #End the loop

                            if any(field.strip() == "" for field in new_movie_release_date): #Check if the user has left any feild blank
                                easygui.msgbox("A feild has been left blank, re-enter.")
                                continue  #ASk the user to re-enter the new date

                            new_movie_date = datetime.strptime(f"{new_movie_release_date[2]}-{new_movie_release_date[1]}-{new_movie_release_date[0]}", "%Y-%m-%d").date() #Format the date to be inserted into the database

                            lower_boundary = datetime(1888, 1, 1).date() #Define the earliest date to be Jan 1, 1888
                            upper_boundary = datetime.now().date() #Define the current date as the latest

                            if lower_boundary <= new_movie_date <= upper_boundary: #Check if the date is between Jan 1, 1888 and today's date
                                easygui.msgbox(f"Valid movie release date: {new_movie_date}")
                            else:
                                easygui.msgbox(f"Invalid movie release date: {new_movie_date}")
                                continue #Ask the user to re-enter

                            valid_new_movie_date = True

                        except (ValueError, TypeError): #Handle incorrect date formats or type errors
                            easygui.msgbox("Invalid date format. Please try again.")

                    if new_movie_release_date is None: #Check if the user cancelled the input
                        continue #Return

                    new_value = new_movie_date
                    data_type = "movie_release_date"
                    name_changing = "no"
                    update_movie() #Update the movie

                elif edit_catagory == 'Rating': #Check if the user has selected to edit the rating
                    rating_call() #Get the ratings
                    new_rating_value = easygui.choicebox(f"Select new Rating for {edit_movie}:", choices=rating_list) #Ask the user for the new rating
                    if not new_rating_value: #Check if no rating was selected
                        easygui.msgbox("No rating selected.")
                        continue  # Exit if no rating is selected
                    new_value = new_rating_value
                    data_type = "movie_rating"
                    name_changing = "no"
                    update_movie() #Update the movie

                elif edit_catagory == 'Length': #Check if the user has selected to edit the length
                    new_length_value = easygui.integerbox(f"Enter new Run Time for {edit_movie}:", lowerbound=1, upperbound=1000) #Ask the user for the new length
                    if new_length_value is None: #Check if the user entered a new length
                        easygui.msgbox("No run time entered.")
                        continue  # Exit if no new length is entered
                    new_value = new_length_value
                    data_type = "movie_run_time"
                    name_changing = "no"
                    update_movie() #Update the movie

                elif edit_catagory == 'Genre': #Check if the user has selected to edit the genre
                    genre_call() #Get the genres
                    new_genre_value = easygui.choicebox(f"Select new Rating for {edit_movie}:", choices=genre_list) #Ask the user for the new genre
                    if not new_genre_value: #Check if a new genre was selected
                        easygui.msgbox("No genre selected.")
                        continue  # Exit if no new genre is selected
                    new_value = new_genre_value.replace("[","").replace("]","").split(",")[0] #Format the genre to be inserted into the database
                    data_type = "movie_genre"
                    name_changing = "no"
                    update_movie() #Update the movie

    if menu_action == "Exit":
        quit() #Close the program