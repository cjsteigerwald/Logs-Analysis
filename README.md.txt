# Project: Logs Analysis

---

Logs Analysis is a project for Udacity Full Stack developer nano degree.

This python application uses psycopg2 to connect to a local postgresql data base and fetches the following:

* Most popular articles by views. Variable 'number_of_popular_articles' holds number of articles to display.

* List all authors by popularity (views).

* Days that requests are above a specified error percentage. Variable 'percent_of_error' is lowest threshold of errors.

# Requirements

---

* [Python 3.0](https://www.python.org/download/releases/3.0/)

* [psycopg2](http://initd.org/psycopg/)

* [PostgreSQL](https://www.postgresql.org/)

# Run Application

---

Application is run from command line, run:

`python3 logdb.py`

# License
It is free software, and may be redistributed under the terms specified in the 
[LICENSE](https://choosealicense.com/licenses/mit/) file.