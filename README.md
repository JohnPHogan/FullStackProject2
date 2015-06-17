Full Stack Development Project 2

This project assumes a postgres database that has already been configured with
a database called tournament.  The tournament.sql file contains the SQL commands
necessary to create the tables needed in order for the project to work.

From the command line, type in the following:

$ psql -d tournament -f tournament.sql

The command will return the following:

psql:tournament.sql:11: NOTICE:  drop cascades to constraint matches_player_id_fkey on table matches

This shows that the sql command to drop the table players also cascades to drop
any constraints on that table.  Since the matches table defines player_id to be
a foreign key of the id data item from the players table, this is the correct
action to occur.

A connection to the postgres database is created along with a cursor.  The
embedded SQL depends on the tables that are created by the script, but no
further dependency exists.

The tournament_test.py file executes pre-defined tests for the project.  The
tournament.py file can be run in a standalone mode to actually have a swiss
pairing tournament with multiple rounds run and prints out the results.
