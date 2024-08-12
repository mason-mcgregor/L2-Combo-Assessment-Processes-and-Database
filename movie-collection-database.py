import sqlite3

conn = sqlite3.connect('film-collection.db')

# conn.execute('''CREATE TABLE Genre_Table
# (Genre_ID INTEGER primary key,
# Genre_Title TEXT)''')

# print("Genre table crated successfully")

# conn.execute('''CREATE TABLE Rating_Table
# (Rating_ID INTEGER primary key,
# Rating_Title TEXT)''')

# print("Rating table crated successfully")

conn.execute('''CREATE TABLE Movie_Collection (
    Movie_ID INTEGER PRIMARY KEY,
    Movie_Name TEXT UNIQUE NOT NULL,
    Movie_Release_Date DATE NOT NULL CHECK (Movie_Release_Date > '1888-01-01'),
    Movie_Rating INTEGER NOT NULL,
    Movie_Run_Time INTEGER NOT NULL CHECK (Movie_Run_Time > 0),
    Movie_Genre INTEGER NOT NULL,
    FOREIGN KEY (Movie_Rating) REFERENCES Rating_Table (Rating_ID),
    FOREIGN KEY (Movie_Genre) REFERENCES Genre_Table (Genre_ID)
);
''')

print("table crated successfully")