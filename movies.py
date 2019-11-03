import sys
from db import UseDatabase
from setup import get_titles, data_one_movie_to_db, additional_data_dict, change_cast_name


class Movies:
    def __init__(self, config_db):
        self.config_db = config_db
        self.titles = get_titles(self.config_db)
        change_cast_name(self.config_db)
        self.main_dict = additional_data_dict(self.titles)

    def complete_all(self) -> str:
        """Complete movie data from IMDb to database file."""
        for title in self.titles:
            data_one_movie_to_db(self.config_db, title)
        return "Data about movies was added to database file."

    def sort_by(self, columns: list) -> list:
        """Sort movie data from database by multiple columns."""
        try:
            result = ', '.join(columns)
            with UseDatabase(self.config_db) as cursor:
                _SQL = """SELECT title, {} FROM movies ORDER BY {} DESC""".format(result, result)
                cursor.execute(_SQL)
                contents = cursor.fetchall()
            return contents
        except Exception as err:
            print("Something went wrong:", str(err))

    def filter_by(self, name: str, arg: str = '') -> str and dict:
        """Filter movie data."""
        try:
            contents = {}
            label_f = 'Value'
            # For director, actor and language
            if name.lower() in ('director', 'actors', 'language'):
                label_f = name.title()
                end = "'%" + arg + "%'"
                _SQL = """SELECT title, {} FROM movies WHERE {} LIKE {}""".format(name, name, end)
                with UseDatabase(self.config_db) as cursor:
                    cursor.execute(_SQL)
                    contents = dict(cursor.fetchall())
            elif name == 'box office':
                label_f = name.title()
                for title in self.titles:
                    if self.main_dict[title]['box_office'] > 100000000:
                        contents[title] = self.main_dict[title]['box_office']
            elif name == 'only oscars nominates':
                label_f = "Nominates for Oscar"
                for title in self.titles:
                    if self.main_dict[title]['oscars'] == 0 and self.main_dict[title]['nominations_oscars'] > 0:
                        contents[title] = self.main_dict[title]['nominations_oscars']
            elif name == '80 percent of wins':
                label_f = "Percent of wins"
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
            return label_f, contents
        except Exception as err:
            print("Something went wrong:", str(err))

    def compare(self, param: str, *args: str) -> dict:
        """Compare movies by: IMDb Rating, Box office earnings, Number of awards won, Runtime."""
        try:
            contents = {}
            for title in args:
                if title in self.titles:
                    if param == 'awards':
                        contents[title] = self.main_dict[title]['oscars'] + self.main_dict[title]['wins_others']
                    else:
                        contents[title] = self.main_dict[title][param]
            contents = {title: param for title, param in contents.items() if title == max(contents, key=contents.get)}
            return contents
        except Exception as err:
            print("Something went wrong:", str(err))

    def add(self, movie_title: str) -> None:
        """Add new movie to database. It automatically downloads movie data as well."""
        try:
            with UseDatabase(self.config_db) as cursor:
                _SQL = """INSERT INTO MOVIES (TITLE, YEAR, RUNTIME, GENRE, DIRECTOR, ACTORS, WRITER, LANGUAGE, COUNTRY, 
                        AWARDS, IMDb_Rating, IMDb_votes, BOX_OFFICE) VALUES ('{}', NULL, NULL, NULL, NULL, NULL, NULL, 
                        NULL, NULL, NULL, NULL, NULL, NULL)""".format(movie_title)
                cursor.execute(_SQL)
            data_one_movie_to_db(self.config_db, movie_title)
        except Exception as err:
            print("Something went wrong:", str(err))

    def high_scores(self) -> dict:
        """Show current high scores."""
        high_scores = {}
        params = ['runtime', 'box_office', 'wins_others', 'nominations_others', 'oscars', 'imdb_rating']
        for param in params:
            title_of_high = max(self.main_dict, key=lambda k: self.main_dict[k][param])
            high_scores[param] = {}
            high_scores[param][title_of_high] = self.main_dict[title_of_high][param]
        return high_scores


if __name__ == '__main__':
    movie = Movies('movies.sqlite')
    if len(sys.argv) > 1:
        if sys.argv[1] == '--add':
            movie.add(sys.argv[2].tile())
            print(f"The movie {sys.argv[2]} was added to database.")
        elif sys.argv[1] == '--sort_by':
            sort_result = movie.sort_by(sys.argv[2:])
            for row in sort_result:
                for elem in row:
                    print(str(elem).ljust(45), end='')
                print()
        elif sys.argv[1] == '--filter_by':
            if len(sys.argv) == 3:
                label, filter_result = movie.filter_by(sys.argv[2])
            else:
                label, filter_result = movie.filter_by(sys.argv[2], sys.argv[3])
            print("{:<45} {:<75}".format('Title', label))
            for k, v in filter_result.items():
                print("{:<45} {:<75}".format(k, v))
        elif sys.argv[1] == '--compare':
            compare_result = movie.compare(sys.argv[2], sys.argv[3].title(), sys.argv[4].title())
            print("{:<45} {:<75}".format('Title', 'Value'))
            for k, v in compare_result.items():
                print("{:<45} {:<75}".format(k, v))
        elif sys.argv[1] == '--high_scores':
            high_scores_result = movie.high_scores()
            for k, n in high_scores_result.items():
                for t, v in n.items():
                    print("{:<25} {:<50} {:<60}".format(k.replace("_", " ").replace("others", "").title(), t, v))
        elif sys.argv[1] == '--complete_data':
            movie.complete_all()
        else:
            print('Wrong command. Please read README on GitHub.')
