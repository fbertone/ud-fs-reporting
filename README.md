# SQL Reporting Tool for Udacity Fullstack Nanodegree

## Description
This Python CLI tool analyse a PostgreSQL DB and outputs a report.
Three different analysis are executed, the objective is to use just an SQL query each,
exploiting table joins and subqueries.

## Set up
* Install PostgreSQL Server
* Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
* Extract the file newsdata.sql from the zip file
* Load the data into the database with the following command:

> psql -d news -f newsdata.sql

## Running the reporting tool
The tool was tested with with Python v. 2.7.

You can run the tool calling the python interpreter:
> python reporting.py
or launching directly the script:
> ./reporting.py

You can find an example of output in output.txt

