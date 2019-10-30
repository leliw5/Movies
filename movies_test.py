import movies
import sqlite3
import unittest


class MoviesTest(unittest.TestCase):

    def setUp(self) -> None:
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
        self.movie_test = movies.Movies("test_database.sqlite")
        # complete data about 2 movies
        self.movie_test.complete_all()

    def test_sort_by(self):
        columns = ['year', 'genre']
        result = self.movie_test.sort_by(columns)
        expected = [('Se7en', 1995, 'Crime, Drama, Mystery, Thriller'), ('Gladiator', 2000, 'Action, Adventure, Drama')]
        self.assertEqual(result, expected)

    def test_filter_by_good(self):
        name = 'director'
        arg = 'Ridley Scott'
        result = self.movie_test.filter_by(name, arg)
        expected = ('Director', [('Gladiator', 'Ridley Scott')])
        self.assertEqual(result, expected)

    def test_filter_by_wrong(self):
        name = 'director'
        arg = 'Jan Error'
        result = self.movie_test.filter_by(name, arg)
        expected = ('Director', [])
        self.assertEqual(result, expected)

    def test_filter_by_only_name(self):
        name = 'only oscars nominates'
        result = self.movie_test.filter_by(name)
        expected = ('Nominates for Oscar', {'Se7en': 1})
        self.assertEqual(result, expected)

    def test_compare(self):
        result = self.movie_test.compare("runtime", "Se7en", "Gladiator")
        expected = {'Gladiator': 155}
        self.assertEqual(result, expected)

    def test_compare_wrong(self):
        result = self.movie_test.compare("wrong", "Se7en", "Gladiator")
        expected = None
        self.assertEqual(result, expected)

    def test_high_scores(self):
        result = self.movie_test.high_scores()
        expected = {'runtime': {'Gladiator': 155}, 'box_office': {'Gladiator': -1}, 'wins_others': {'Gladiator': 53},
                    'nominations_others': {'Gladiator': 101}, 'oscars': {'Gladiator': 5}, 'imdb_rating': {'Se7en': 8.6}}
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
