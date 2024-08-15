import sqlite3

conn = sqlite3.connect('film-collection.db')

conn.execute('''
    CREATE TABLE genre_table(
        id INTEGER PRIMARY KEY,
        key TEXT NOT NULL UNIQUE,
        genre TEXT NOT NULL
);
''')

print("Table created successfully")

conn.execute('''
    INSERT INTO genre_table (key, genre)
    VALUES
        ('A', 'Action'),
        ('An', 'Animation'),
        ('C', 'Comedy'),
        ('Cr', 'Crime'),
        ('D', 'Drama'),
        ('F', 'Fantasy'),
        ('H', 'Horror'),
        ('R', 'Romance'),
        ('Sci-Fi', 'Science Fiction'),
        ('T', 'Thriller'),
        ('M', 'Mystery');     
''')

print("Data entered successfully")

conn.commit()
conn.close()