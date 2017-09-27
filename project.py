#! /usr/bin/env python

import psycopg2
import bleach

DBNAME = "news"

""" Query to return the three most popular articles """
query1 = "select ar.title , count(*) as Total_Count from articles ar  \
         join log l on l.path like concat('%', ar.slug, '%')  \
         where l.status like '%200%'\
         group by ar.title, l.path  \
         order by Total_Count desc limit 3"

""" Query to return the three most popular authors """
query2 = "select au.name,count(*) as Total_count from articles ar \
          join log l on l.path like concat('%', ar.slug, '%')   \
         join authors au on au.id = ar.author \
          where l.status like '%200%' group by au.name \
         order by Total_Count desc"

""" Query to return the maximum error rates on a particular day """
query3 = """select  date::text, round(rate,2)::text as rate
from (  with a as(select count(*)::decimal as error,date(time) from public.log
where status like '404%'
group by date(time) order by date(time)),b as
(select count(*)::decimal as success,date(time) from public.log
group by date(time) order by date(time))
select date, ((a.error/b.success) *100.0)::decimal as rate
from a join b using(date)  ) as finalvalue where rate > 1.0"""


def get_posts(query, val):
    """ Connects to db and return all the required results
    based on the query statement"""

    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    posts = c.fetchall()
    printOutput(posts, val)
    db.close()


def printOutput(posts, val):
    """ Printing outputs for each of the query"""
    for index in range(len(posts)):
        if val == "views":
            print posts[index][0] + " - " + str(posts[index][1]) + " views"
        else:
            print posts[index][0] + " - " + str(posts[index][1]) + "%"

    print '\n'


print "The three most popular articles of all time"
get_posts(query1, "views")
print "Most popular article authors of all time"
get_posts(query2, "views")
print "On which days did more than 1% of requests lead to error"
get_posts(query3, "rate")
