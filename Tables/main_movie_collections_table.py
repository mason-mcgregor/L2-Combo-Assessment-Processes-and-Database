import sqlite3

conn = sqlite3.connect('film-collection.db')

conn.execute('''
    CREATE TABLE movie_collection_table(
        id INTEGER PRIMARY KEY,
        movie_name TEXT UNIQUE NOT NULL,
        movie_release_date DATE NOT NULL CHECK (movie_release_date > '1888-01-01'),
        movie_rating TEXT NOT NULL,
        movie_run_time INTEGER NOT NULL CHECK (movie_run_time > 1),
        movie_genre TEXT NOT NULL,
        CONSTRAINT fk_movie_rating FOREIGN KEY (movie_rating) REFERENCES rating_table (key),
        CONSTRAINT fk_movie_genre FOREIGN KEY (movie_genre) REFERENCES genre_table (key)
    );
''')

print("Table created successfully")

conn.execute('''
    INSERT INTO movie_collection_table (movie_name, movie_release_date, movie_rating, movie_run_time, movie_genre)
    VALUES
        ('Ghostbusters', '2016-07-11', 'PG', 116, 'C'),
        ('The Legend of Tarzan', '2016-07-01', 'PG', 109, 'A'),
        ('Jason Bourne', '2016-07-29', 'PG', 123, 'A'),
        ('The Nice Guys', '2016-05-20', 'R16', 116, 'C'),
        ('The Secret Life of Pets', '2016-07-08', 'G', 91, 'An'),
        ('Star Trek Beyond', '2016-07-22', 'PG', 120, 'A'),
        ('Batman v Superman', '2016-03-24', 'PG', 151, 'A'),
        ('Finding Dory', '2016-06-16', 'G', 103, 'An'),
        ('Zootopia', '2016-04-07', 'G', 108, 'An'),
        ('The BFG', '2016-07-01', 'PG', 90, 'F'),
        ('A Monster Calls', '2016-10-07', 'PG', 108, 'F'),
        ('Independence Day: Resurgence', '2016-06-24', 'PG', 120, 'A'),
        ('The Green Room', '2016-04-15', 'R16', 94, 'Cr'),
        ('Doctor Strange', '2016-10-27', 'PG', 130, 'F'),
        ('The Jungle Book', '2016-04-21', 'PG', 105, 'F'),
        ('Alice Through the Looking Glass', '2016-05-27', 'PG', 118, 'F'),
        ('Imperium', '2016-05-19', 'R16', 109, 'Cr'),
        ('The Infiltrator', '2016-07-13', 'R16', 127, 'Cr'),
        ('Mad Max: Fury Road', '2015-05-14', 'R16', 120, 'A'),
        ('Spectre', '2015-10-26', 'PG', 145, 'A'),
        ('Jurassic World', '2015-06-12', 'PG', 100, 'A'),
        ('The Intern', '2015-09-24', 'PG', 121, 'C'),
        ('Ted 2', '2015-06-26', 'R16', 121, 'C'),
        ('Trainwreck', '2015-07-17', 'R16', 122, 'C'),
        ('Inside Out', '2015-06-19', 'PG', 94, 'An'),
        ('The Good Dinosaur', '2015-11-25', 'G', 101, 'An'),
        ('Divergent', '2014-04-10', 'PG', 121, 'A'),
        ('The Maze Runner', '2014-09-19', 'PG', 115, 'A'),
        ('Birdman', '2014-10-17', 'R', 119, 'C'),
        ('Guardians of the Galaxy', '2014-08-07', 'PG', 121, 'F'),
        ('The Lego Movie', '2014-02-07', 'PG', 100, 'An'),
        ('Big Hero 6', '2014-12-26', 'PG', 108, 'An'),
        ('The Drop', '2014-09-12', 'R16', 106, 'Cr');
''')

print("Data entered successfully")

conn.commit()
conn.close()
