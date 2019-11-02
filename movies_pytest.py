import movies
import sqlite3
import pytest
import requests
import json


@pytest.fixture()
def setup():
    """Setup a temporary database"""
    conn = sqlite3.connect("test_database.sqlite")
    cursor = conn.cursor()

    # drop table if exists
    cursor.execute("""DROP TABLE IF EXISTS movies""")
    # create a table
    cursor.execute("""CREATE TABLE MOVIES ([ID] INTEGER PRIMARY KEY,[TITLE] text, [YEAR] integer, [RUNTIME] text,
    [GENRE] text, [DIRECTOR] text, "ACTORS" text, [WRITER] text, [LANGUAGE] text, [COUNTRY] text, [AWARDS] text,
    [IMDb_Rating] float, [IMDb_votes] integer, [BOX_OFFICE] integer )""")

    # add 2 movie titles
    cursor.execute("""INSERT INTO MOVIES (TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, ACTORS, WRITER, LANGUAGE, COUNTRY, 
                    AWARDS, IMDb_Rating, IMDb_votes, BOX_OFFICE) VALUES ('Gladiator', NULL, NULL, NULL, NULL, NULL, 
                    NULL, NULL, NULL, NULL, NULL, NULL, NULL)""")
    cursor.execute("""INSERT INTO MOVIES (TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, ACTORS, WRITER, LANGUAGE, COUNTRY, 
                    AWARDS, IMDb_Rating, IMDb_votes, BOX_OFFICE) VALUES ('Se7en', NULL, NULL, NULL, NULL, NULL, 
                    NULL, NULL, NULL, NULL, NULL, NULL, NULL)""")
    # save data to database
    conn.commit()

    # create instance
    movie_test = movies.Movies("test_database.sqlite")
    # complete data about 2 movies
    movie_test.complete_all()
    return movie_test


class TestClass:

    def test_conn_api_ok(self):
        url = "http://www.omdbapi.com/?i=tt3896198&apikey=6b513db6"
        req = requests.get(url)
        result = req.status_code
        expected = 200
        assert result == expected

    def test_api_correct_title(self):
        url = "http://www.omdbapi.com/?i=tt3896198&apikey=6b513db6&t=" + "Se7en"
        headers = {"Accept": "application/json"}
        req = requests.get(url, headers=headers)
        json_response = json.loads(req.content.decode('utf-8'))
        result = json_response['Response']
        expected = 'True'
        assert result == expected

    def test_api_wrong_title(self):
        url = "http://www.omdbapi.com/?i=tt3896198&apikey=6b513db6&t=" + "wrong title"
        headers = {"Accept": "application/json"}
        req = requests.get(url, headers=headers)
        json_response = json.loads(req.content.decode('utf-8'))
        result = json_response['Response']
        expected = 'False'
        assert result == expected

    def test_sort_by(self, setup):
        columns = ['year', 'genre']
        result = setup.sort_by(columns)
        expected = [('Se7en', 1995, 'Crime, Drama, Mystery, Thriller'), ('Gladiator', 2000, 'Action, Adventure, Drama')]
        assert result == expected

    def test_filter_by_good(self, setup):
        name = 'director'
        arg = 'Ridley Scott'
        result = setup.filter_by(name, arg)
        expected = ('Director', {'Gladiator': 'Ridley Scott'})
        assert result == expected

    def test_filter_by_wrong(self, setup):
        name = 'director'
        arg = 'Jan Error'
        result = setup.filter_by(name, arg)
        expected = ('Director', {})
        assert result == expected

    def test_filter_by_only_name(self, setup):
        name = 'only oscars nominates'
        result = setup.filter_by(name)
        expected = ('Nominates for Oscar', {'Se7en': 1})
        assert result == expected

    def test_compare(self, setup):
        result = setup.compare("runtime", "Se7en", "Gladiator")
        expected = {'Gladiator': 155}
        assert result == expected

    def test_compare_wrong(self, setup):
        result = setup.compare("runtime", "wrong", "titles")
        expected = dict()
        assert result == expected

    def test_high_scores(self, setup):
        result = setup.high_scores()
        expected = {'runtime': {'Gladiator': 155}, 'box_office': {'Gladiator': -1}, 'wins_others': {'Gladiator': 53},
                    'nominations_others': {'Gladiator': 101}, 'oscars': {'Gladiator': 5}, 'imdb_rating': {'Se7en': 8.6}}
        assert result == expected


if __name__ == '__main__':
    pass
