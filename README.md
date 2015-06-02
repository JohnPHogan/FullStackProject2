Full Stack Development Project 2

This project assumes a postgres database that has already been configured with
a database called tournament.  The tournament.sql file contains the SQL commands
necessary to create the tables needed in order for the project to work.  

A connection to the postgres database is created along with a cursor.  The
embedded SQL depends on the tables that are created by the script, but no
further dependency exists.

The tournament_test.py file executes pre-defined tests for the project.  The
tournament.py file can be run in a standalone mode to actually have a swiss
pairing tournament with multiple rounds run and prints out the results.
