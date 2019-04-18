#!/usr/bin/env python3
# logdb.py is an application for the Project: Logs Analysis
# for Udacity Full Stack developer nano degree.
# Application connects to a local postgresql database and
# fetches the following:
#   Most popular articles by views. Variable
#       'number_of_popular_articles' holds number of articles to display.
#   Lists all authors by popularity (views).
#   Days that requests are above a specified error percentage. Variable
#           'percent_of_error' is lowest threshold of errors.
#
# Displays above to terminal
# by: Chris Steigerwald
# date: 18 April 2019

# http://initd.org/psycopg/docs/
import psycopg2

# Global variable for DB to connect to
DBNAME = "news"
# Variable passed into get_popular_articles() to determine
# number of popular articles to display
number_of_popular_articles = 3
# Variable passed into get_log_errors() to determine threshold
# for displaying errors each day
percent_of_error = .01


# Opens connection to DB, performs query, closes connection,
# and prints to terminal number of most popular articles by views
# passed in by.
def get_popular_articles(popular_articles):
    print("Fetching the {} most popular article(s) of all"
          " time by views:".format(popular_articles))
    # Open connection to DB
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = """
        SELECT articles.title, count(*) as num
        FROM articles JOIN log
        ON log.path LIKE CONCAT('%', articles.slug)
        GROUP by articles.title
        ORDER by num DESC LIMIT {};
    """.format(popular_articles)
    # Execute query against DB
    c.execute(query)
    # Variable for saving query (returned as list of tuples)
    results = c.fetchall()
    # Close connection to DB
    db.close
    # Print results of query
    for result in results:
        print("\"%s\" - %s views" % (result[0], result[1]))


# Opens connection to DB, performs query, closes connection,
# and prints to terminal authors by views.
def get_popular_authors():
    print("\nFetching author(s) by popularity (views):")
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = """
        SELECT authors.name, count(*) as num
        FROM articles
        INNER JOIN log ON log.path LIKE CONCAT('%', articles.slug)
        INNER JOIN authors ON authors.id = articles.author
        GROUP BY authors.name
        ORDER BY num DESC;
    """
    c.execute(query)
    results = c.fetchall()
    db.close
    for result in results:
        print("%s - %s views" % (result[0], result[1]))


# Opens connection to DB, performs query, closes connection,
# and prints to days with more than 1% of requests leading to errors.
def get_log_errors(percent_error):
    print("\nFetching day(s) that more than {}% of"
          " requests led to errors:".format(percent_error * 100))
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    query = """
        SELECT TO_CHAR(err.day, 'Mon DD, YYYY' ) as "date",
        ROUND((CAST(err.error_day AS NUMERIC) /
        CAST(total.total_day AS NUMERIC) * 100), 1)  as "percent error"
        FROM
        (
        SELECT date_trunc('day', time) as "day", count(*) as "error_day"
        FROM log
        WHERE (status LIKE  '4%') OR (status LIKE '5%')
        GROUP BY 1
        ORDER BY 1
        ) as err
        join
        (
        SELECT date_trunc('day', time) as "day", count(*) as "total_day"
        FROM log
        GROUP BY 1
        ORDER BY 1
        ) as total on err.day = total.day
        WHERE (CAST(err.error_day AS NUMERIC) /
        CAST(total.total_day AS NUMERIC)) > {};
    """.format(percent_error)
    c.execute(query)
    results = c.fetchall()
    db.close
    for result in results:
        print("%s - %s%% errors" % (result[0], result[1]))


# Main driver of application
def main():
    get_popular_articles(number_of_popular_articles)
    get_popular_authors()
    get_log_errors(percent_of_error)


if __name__ == '__main__':
    main()
