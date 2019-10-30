import sys
import pprint
from db import UseDatabase
from setup import get_titles, data_one_movie_to_db, additional_data_dict, change_cast_name

config_db = 'movies.sqlite'


class Movies:
    def __init__(self):
        self.titles = get_titles()
        change_cast_name()
        self.main_dict = additional_data_dict(self.titles)

    def complete_all(self) -> str:
        for title in self.titles:
            data_one_movie_to_db(title)
        return "Data about movies was added to database file."

    @staticmethod
    def sort_by(columns: list):
        try:
            result = ', '.join(columns)
            with UseDatabase(config_db) as cursor:
                _SQL = """SELECT title, {} FROM movies ORDER BY {} DESC""".format(result, result)
                cursor.execute(_SQL)
                contents = cursor.fetchall()
            for row in contents:
                for elem in row:
                    print(str(elem).ljust(50), end='')
                print()
        except Exception as err:
            print("Something went wrong:", str(err))

    def filter_by(self, name: str, arg: str = '') -> str:
        try:
            contents = {}
            label = 'Value'
            # For director, actor and language
            if name.lower() in ('director', 'actors', 'language'):
                label = name.title()
                end = "'%" + arg + "%'"
                _SQL = """SELECT title, {} FROM movies WHERE {} LIKE {}""".format(name, name, end)
                with UseDatabase(config_db) as cursor:
                    cursor.execute(_SQL)
                    contents = cursor.fetchall()
            elif name == 'box office':
                label = name.title()
                for title in self.titles:
                    if self.main_dict[title]['box_office'] > 100000000:
                        contents[title] = self.main_dict[title]['box_office']
            elif name == 'only oscars nominates':
                label = "Nominates for Oscar"
                for title in self.titles:
                    if self.main_dict[title]['oscars'] == 0 and self.main_dict[title]['nominations_oscars'] > 0:
                        contents[title] = self.main_dict[title]['nominations_oscars']
            elif name == '80 percent of wins':
                label = "Percent of wins"
                for title in self.titles:
                    try:
                        percent_of_won = ((self.main_dict[title]['oscars'] + self.main_dict[title]['wins_others']) /
                                          (self.main_dict[title]['oscars'] + self.main_dict[title]['wins_others'] +
                                           self.main_dict[title]['nominations_oscars'] +
                                           self.main_dict[title]['nominations_others']))
                    except ZeroDivisionError:
                        percent_of_won = 0
                    if percent_of_won > 0.8:
                        contents[title] = percent_of_won
            print("{:<45} {:<75}".format('Title', label))
            for k, v in contents.items():
                print("{:<45} {:<75}".format(k, v))
            return "\nDone."
        except Exception as err:
            print("Something went wrong:", str(err))

    def compare(self, param: str, *args: list) -> str:
        try:
            contents = {}
            for title in args:
                if title in self.titles:
                    if param == 'awards':
                        contents[title] = self.main_dict[title]['oscars'] + self.main_dict[title]['wins_others']
                    else:
                        contents[title] = self.main_dict[title][param]
            contents = {title: param for title, param in contents.items() if title == max(contents, key=contents.get)}
            print("{:<45} {:<75}".format('Title', 'Value'))
            for k, v in contents.items():
                return "{:<45} {:<75}".format(k, v)
        except Exception as err:
            print("Something went wrong:", str(err))

    @staticmethod
    def add(movie_title: str) -> None:
        """Add new movie to database."""
        try:
            with UseDatabase(config_db) as cursor:
                _SQL = """INSERT INTO MOVIES (TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, ACTORS, WRITER, LANGUAGE, COUNTRY, 
                        AWARDS, IMDb_Rating, IMDb_votes, BOX_OFFICE) VALUES ('{}', NULL, NULL, NULL, NULL, NULL, NULL, 
                        NULL, NULL, NULL, NULL, NULL, NULL)""".format(movie_title)
                cursor.execute(_SQL)
            data_one_movie_to_db(movie_title)
        except Exception as err:
            print("Something went wrong:", str(err))

    def high_scores(self):
        high_scores = {}
        params = ['runtime', 'box_office', 'wins_others', 'nominations_others', 'oscars', 'imbd_rating']
        for param in params:
            title_of_high = max(self.main_dict, key=lambda k: self.main_dict[k][param])
            high_scores[param] = {}
            high_scores[param][title_of_high] = self.main_dict[title_of_high][param]

        for k, n in high_scores.items():
            for t, v in n.items():
                print("{:<25} {:<50} {:<60}".format(k.replace("_", " ").replace("others", "").title(), t, v))
        return "\nDone."


movie = Movies()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--add':
            movie.add(sys.argv[2])
            print(f"The movie {sys.argv[2]} was added.")
        elif sys.argv[1] == '--sort_by':
            movie.sort_by(sys.argv[2:])
        elif sys.argv[1] == '--filter_by':
            if len(sys.argv) == 3:
                print(movie.filter_by(sys.argv[2]))
            else:
                print(movie.filter_by(sys.argv[2], sys.argv[3]))
        elif sys.argv[1] == '--compare':
            print(sys.argv[3:])
            print(movie.compare(sys.argv[2], sys.argv[3], sys.argv[4]))
        elif sys.argv[1] == '--high_scores':
            print(movie.high_scores())
        elif sys.argv[1] == '--complete_data':
            movie.complete_all()
        else:
            print('Wrong command. Please read README.')
