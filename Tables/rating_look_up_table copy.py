import sqlite3

conn = sqlite3.connect('film-collection.db')

conn.execute('''
    CREATE TABLE rating_table(
        id INTEGER PRIMARY KEY,
        key TEXT NOT NULL UNIQUE,
        rating TEXT NOT NULL
);
''')

print("Table created successfully")

conn.execute('''
    INSERT INTO rating_table (key, rating)
    VALUES
        ('G', 'General'),
        ('PG', 'Parental Guidance'),
        ('M', 'Mature'),
        ('R13', 'Restricted to persons 13 years and over'),
        ('R16', 'Restricted to persons 16 years and over'),
        ('R18', 'Restricted to persons 18 years and over'),
        ('RP13', 'Restricted to persons 13 years and over unless accompanied by a parent or guardian'),
        ('RP16', 'Restricted to persons 16 years and over unless accompanied by a parent or guardian');     
''')

print("Data entered successfully")

conn.commit()
conn.close()