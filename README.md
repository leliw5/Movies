[![LinkedIn][linkedin-shield]][linkedin-url]


<p align="center">
  <h1 align="center">Movies</h1>

<!-- TABLE OF CONTENTS -->
# Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
# About The Project

Script allows you download data about movies from IMDb.
You can sort, filter, compare, add and check the high scores of movies on your list as well.

## Built With

* Python 3.7
* [OMDb API][omdb_api]
* [requests][requests]

<!-- GETTING STARTED -->
# Getting Started

To get a local copy up and running follow these simple steps.

## Prerequisites

You need to install Third Party Package:
* requests
```
pip install requests
```

## Installation
 
Clone the repository Movies
```
git https:://github.com/leliw5/Movies.git
```
** You can change default list of movies titles - edit `movies.sqlite` file (e.g. using _DB Browser for SQLite_).

<!-- USAGE EXAMPLES -->
# Usage

## Complete movie data
Complete movie data from  in your `movies.sqlite` file.
```
python movies.py --complete_data
```

## Sort movies
Sort movie data from your `movies.sqlite` file.
You can sort by one or more columns.
```
python movies.py --sort_by argument1 *argument *argument
```
`*` - optional parameter
<br><br>
<b>Available arguments</b>:<br>
`title`, `year`, `runtime`, `genre`, `director`, `actors`, `writer`, `language`, `country`, `awards`, 
`imdb_rating`, `imdb_votes`, `box_office`

Example input:
```
python movies.py --sort_by title year
```

## Filter movies
Filter movie data by:
- Director
```
python movies.py --filter_by director "first_name last_name"
```
- Actor
```
python movies.py --filter_by actor "first_name last_name"
```
- Movies that was nominated  for Oscar but did not win any.
```
python movies.py --filter_by "only oscars nominates"
```
- Movies that won more than 80% of nominations
```
python movies.py --filter_by "80 percent of wins"
```
- Movies that earned more than 100,000,000 $
```
python movies.py --filter_by "box office"
```
- Only movies in certain Language
```
python movies.py --filter_by language "language"
```

## Compare movies
Compare movies by:
- IMDb Rating 
- Box office earnings
- Number of awards won
- Runtime

```
python movies.py --compare parameter "title_1" "title_2"
```
<b>Available parameters</b>:<br>
`runtime`, `awards`, `imdb_rating`, `box_office`

Example input:
```
python movies.py --compare imdb_rating "Joker" "Se7en"
```

## Add movie
Add new movie to your `movies.sqlite` file. It automatically downloads movie data as well.

```
python movies.py --add "title_1"
```

Example input:
```
python movies.py --add "Casino"
```

## High score
Show current high scores in:
- Runtime
- Box office earnings
- Most awards won
- Most nominations
- Most Oscars
- Highest IMDB Rating

```
python movies.py --high_scores
```

<!-- CONTACT -->
# Contact

Project Link: [https://github.com/leliw5/Movies](https://github.com/leliw5/Movies)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/mateusz-leliwa/
[omdb_api]: http://www.omdbapi.com
[requests]: https://pypi.org/project/requests
