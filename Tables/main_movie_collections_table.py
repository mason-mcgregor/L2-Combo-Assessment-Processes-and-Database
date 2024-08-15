import sqlite3

conn = sqlite3.connect('film-collection.db')

conn.execute('''
    CREATE TABLE genre_table(
        id INTEGER PRIMARY KEY,
        key TEXT NOT NULL UNIQUE,
        genre TEXT NOT NULL
);
''')