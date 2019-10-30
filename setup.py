import re
import requests
import json
import sqlite3
from db import UseDatabase

config_db = 'movies.sqlite'


def get_titles() -> list:
    """Create a list of movie titles from db source."""
    try:
        with UseDatabase(config_db) as cursor:
            _SQL = "SELECT title from movies"
            cursor.execute(_SQL)
            contents = cursor.fetchall()
            titles_db = [t for tup in contents for t in tup]
        return titles_db
    except Exception as err:
        print("Something went wrong:", str(err))


def change_cast_name():
    """Change 'cast' column name in database.
    CAST is SQL function, so we would have errors during creating sql query with 'cast' column."""
    try:
        with UseDatabase(config_db) as cursor:
            _SQL = "ALTER TABLE movies RENAME COLUMN cast TO ACTORS"
            cursor.execute(_SQL)
    except sqlite3.OperationalError:
        pass


def data_one_movie_to_db(title: str) -> None:
    """Fulfill data about one movie to database."""
    try:
        with UseDatabase(config_db) as cursor:
            url = "http://www.omdbapi.com/?i=tt3896198&apikey=6b513db6&t=" + title
            headers = {"Accept": "application/json"}
            req = requests.get(url, headers=headers)
            api_content = json.loads(req.content.decode('utf-8'))
            # Because of no BoxOffice key in API for movie 'Ben Hur' (ID 68 in db):
            api_content.setdefault('BoxOffice', 'N/A')
            json_keys = (api_content['Year'], api_content['Runtime'], api_content['Genre'], api_content['Director'],
                         api_content['Actors'], api_content['Writer'], api_content['Language'], api_content['Country'],
                         api_content['Awards'], api_content['imdbRating'], api_content['imdbVotes'],
                         re.sub(r'[^0-9]', '', api_content['BoxOffice']), title)
            _SQL = """UPDATE MOVIES SET YEAR=?, RUNTIME=?, GENRE=?, DIRECTOR=?, ACTORS=?, WRITER=?, LANGUAGE=?,
             COUNTRY=?, AWARDS=?, IMDb_Rating=?, IMDb_votes=?, BOX_OFFICE=? WHERE TITLE=?"""
            cursor.execute(_SQL, json_keys)
    except Exception as err:
        print("Something went wrong:", str(err))


def additional_data_dict(titles: list) -> dict:
    """Create dict with some data about movies to easier data processing."""
    additional_data = {}
    for title in titles:
        url = "http://www.omdbapi.com/?i=tt3896198&apikey=6b513db6&t=" + title
        headers = {"Accept": "application/json"}
        req = requests.get(url, headers=headers)
        api_content = json.loads(req.content.decode('utf-8'))
        # Because of no BoxOffice key in API for movie 'Ben Hur' (ID 68 in db):
        api_content.setdefault('BoxOffice', 'N/A')
        additional_data[title] = {}
        additional_data[title]['imbd_rating'] = float(api_content['imdbRating'])
        if api_content['Runtime'] == 'N/A':
            additional_data[title]['runtime'] = -1
        else:
            additional_data[title]['runtime'] = int(re.sub(r'[^0-9]', '', api_content['Runtime']))
        if api_content['BoxOffice'] == 'N/A':
            additional_data[title]['box_office'] = -1
        else:
            additional_data[title]['box_office'] = int(re.sub(r'[^0-9]', '', api_content['BoxOffice']))
        nominations_oscars = re.search(r'Nominated for (.+?) Oscar', api_content['Awards'])
        if nominations_oscars:
            additional_data[title]['nominations_oscars'] = int(nominations_oscars.group(1))
        else:
            additional_data[title]['nominations_oscars'] = 0
        oscars = re.search(r'Won (.+?) Oscar', api_content['Awards'])
        if oscars:
            additional_data[title]['oscars'] = int(oscars.group(1))
        else:
            additional_data[title]['oscars'] = 0
        nominations_others = re.search(r'(\d+) nomination', api_content['Awards'])
        if nominations_others:
            additional_data[title]['nominations_others'] = int(nominations_others.group(1))
        else:
            additional_data[title]['nominations_others'] = 0
        wins_others = re.search(r'(\d+) win', api_content['Awards'])
        if wins_others:
            additional_data[title]['wins_others'] = int(wins_others.group(1))
        else:
            additional_data[title]['wins_others'] = 0
    return additional_data
