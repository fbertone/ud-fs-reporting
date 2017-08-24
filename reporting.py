#!/bin/env python2.7
import datetime
import psycopg2


def get_authors():
    """Return authors ordered by total views"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(
        "select authors.name, aviews.sum \
        from (select author, sum(views) \
            from (select b.author, a.views \
                from (select substring(path from 10) as slug, \
                    count(*) as views \
                from log where path like '/article/%' group by path) as a \
                join articles as b on a.slug = b.slug) \
                    as qry group by author) as aviews \
        join authors on aviews.author = authors.id order by aviews.sum desc")
    return c.fetchall()
    db.close()


def get_top_articles():
    """Return top 3 most viewed articles"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(
        "select * from \
             (select b.title, a.views from \
                 (select substring(path from 10) as slug, count(*) as views \
                 from log where path like '/article/%' \
                     group by path order by views desc limit 3) as a \
                 join articles as b on a.slug = b.slug) \
         as qry order by views desc")
    return c.fetchall()
    db.close()


def get_errors():
    """Return all days with more than 1% request errors"""
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    c.execute(
        "select a.time, b.errors * 100::float / a.total as perc \
         from \
             (select time::date, count(*) as total \
                 from log group by time::date) as a \
             join \
             (select time::date, count(*) as errors \
                 from log where status !~~ '200 OK' group by time::date) as b \
             on a.time = b.time \
          where b.errors * 100::float / a.total > 1")
    return c.fetchall()
    db.close()

print("HERE'S YOUR REPORT!\n")

print("*** Most readed authors: ***\n")
results = get_authors()
for result in results:
    print(result[0] + ": " + str(result[1]) + " views")

print("\n\n*** Top 3 viewed articles: ***\n")
results = get_top_articles()
for result in results:
    print(result[0] + ": " + str(result[1]) + " views")

print("\n\n*** Days with more than 1% request errors: ***\n")
results = get_errors()
for result in results:
    print(str(result[0]) + ": " + "%.2f" % result[1] + "% of errors")
