#!/usr/bin/env python2.7
import datetime
import psycopg2


# database to use
DBNAME = "dbname=news"


def db_connect():
    """ Creates and returns a connection to the database defined by DBNAME,
       as well as a cursor for the database.

        Returns:
            db, c - a tuple. The first element is a connection to the database.
                    The second element is a cursor for the database.
    """

    db = psycopg2.connect(DBNAME)
    c = db.cursor()
    return db, c


def execute_query(query):
    """ execute_query takes an SQL query as a parameter.
        Executes the query and returns the results as a list of tuples.
        args:
            query - an SQL query statement to be executed.

        returns:
            A list of tuples containing the results of the query.
    """

    try:
        db, c = db_connect()
        c.execute(query)
        results = c.fetchall()
        db.close()
        return results
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def print_top_articles():
    """Prints out the top 3 articles of all time."""

    query = """select b.title, a.views from
             (select substring(path from 10) as slug, count(*) as views
             from log where path like '/article/%'
                 group by path) as a
             join articles as b on a.slug = b.slug
             order by a.views desc limit 3"""

    results = execute_query(query)

    print("\n\n*** Top 3 viewed articles: ***\n")
    for title, views in results:
        print('\"{}\": {} views'.format(title, views))


def print_top_authors():
    """Prints a list of authors ranked by article views."""

    query = """select authors.name, aviews.sum
        from (select author, sum(views)
            from (select b.author, a.views
                from (select substring(path from 10) as slug,
                    count(*) as views
                from log where path like '/article/%' group by path) as a
                join articles as b on a.slug = b.slug)
                    as qry group by author) as aviews
        join authors on aviews.author = authors.id order by aviews.sum desc"""

    results = execute_query(query)

    print("\n\n*** Most readed authors: ***\n")
    for author, views in results:
        print('\"{}\": {} views'.format(author, views))


def print_errors_over_one():
    """ Prints out the days where more than 1% of logged access requests
        were errors.
    """

    query = """select a.time, b.errors * 100::float / a.total as perc
         from
             (select time::date, count(*) as total
                 from log group by time::date) as a
             join
             (select time::date, count(*) as errors
                 from log where status !~~ '200 OK' group by time::date) as b
             on a.time = b.time
          where b.errors * 100::float / a.total > 1"""
    results = execute_query(query)

    print("\n\n*** Days with more than 1% request errors: ***\n")
    for day, errors in results:
        print(str(day) + ": " + "%.2f" % errors + "% of errors")


if __name__ == '__main__':
    print("HERE'S YOUR REPORT!")
    print_top_articles()
    print_top_authors()
    print_errors_over_one()
