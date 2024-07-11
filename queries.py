# pylint: disable=C0103, missing-docstring

import sqlite3

def detailed_movies(db):
    query = """
    SELECT m.title , m.genres, d.name
    FROM movies m
    JOIN directors d ON m.director_id = d.id
    """
    conn = sqlite3.connect('data/movies.sqlite')
    db = conn.cursor()
    db.execute(query)
    results = db.fetchall()
    print(results)
    return results


def late_released_movies(db):
    query = '''
    SELECT m.title
    FROM movies m
    JOIN directors d ON m.director_id = d.id
    WHERE m.start_year > d.death_year
    '''
    conn = sqlite3.connect('data/movies.sqlite')
    db = conn.cursor()
    db.execute(query)
    temp = db.fetchall()
    results = []
    for i in temp:
        results.append(i[0])
    print(results)
    return results


def stats_on(db, genre_name):
    '''return a dict of stats for a given genre
    total count of movies and the average duration'''
    query = """
    SELECT m.genres,COUNT(m.title),AVG(m.minutes)
    FROM movies m
    WHERE UPPER(m.genres) LIKE ?
    """
    conn = sqlite3.connect('data/movies.sqlite')
    db = conn.cursor()
    db.execute(query,(genre_name,))
    i = db.fetchone()
    results = {
        'genre' : i[0],
        'number_of_movies':i[1],
        'avg_length': round(i[2],2)
            }
    print(results)
    return results



def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = """
    SELECT d.name, COUNT(m.title)
    FROM directors d
    JOIN movies m ON d.id = m.director_id
    WHERE UPPER(m.genres) LIKE ?
    GROUP BY d.name
    ORDER BY COUNT(m.title) DESC, d.name ASC
    """
    conn = sqlite3.connect('data/movies.sqlite')
    db = conn.cursor()
    db.execute(query,(genre_name,))
    i = db.fetchall()
    results = i[0:5]
    print(results)
    return results

def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    query = """

    SELECT
            (minutes / 30+1)*30 time_range,
            COUNT(*)
        FROM movies
        WHERE minutes IS NOT NULL
        GROUP BY time_range
    """
    conn = sqlite3.connect('data/movies.sqlite')
    db = conn.cursor()
    db.execute(query)
    results = db.fetchall()
    print(results)
    return results

def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = """
    SELECT
	d.name,
	(m.start_year - d.birth_year)
    FROM
        directors d
    JOIN movies m ON d.id = m.director_id
    WHERE (m.start_year - d.birth_year) < 30
    ORDER BY (m.start_year - d.birth_year) ASC
    """
    conn = sqlite3.connect('data/movies.sqlite')
    db = conn.cursor()
    db.execute(query)
    results = db.fetchall()[0:5]
    print(results)
    return results
