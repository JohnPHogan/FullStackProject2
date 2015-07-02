-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament

-- CASCADE included to remove foreign key depencies defined below for matches
-- table.  It will cause a NOTE to appear when you run the script, but does
-- not constitute an error.
CREATE TABLE players(
                    id SERIAL PRIMARY KEY,
                    p_name TEXT
);

-- The matches table contains references to player id's from the player's
-- table..  They are defined as foreign keys to the players table's ID data
-- item to ensure data integrity
CREATE TABLE matches(id SERIAL PRIMARY KEY,
                    player1 INT references players(id),
                    player2 INT references players(id),
                    winner INT references players(id)

);

-- player_record
-- A logical view created to combine the data from the players table
-- and the matches table so that you have a simple query to get the following:
--  1 player id
--  2 player name
--  3 the number of matches the player has played in the tournament.  This is
--  summarized by COALESCING the results of a sub query where the count of
--  instances of a player id in either player1 or player 2 occurs in the
--  matches table.
--  4 the number of wins the player has earned
--  The COALESCE function is used to force a value of 0 for the number of wins
--  or the count of matches when the players have not played any matches yet.
-- The GROUP BY statements are required so that the aggregation of the COUNT
-- function can occur and the ORDER BY is included so that the data will always
-- be returned from player with most wins to least wins.  This logic could be
-- done in an application query itself, but I wanted to show that it is also
-- possible to do it in a view.  This makes the application logic simpler.
CREATE VIEW player_record AS
SELECT
    p.id as id,
    p.p_name as p_name,
    (SELECT COALESCE(count(id), 0) as matches_played FROM matches m
    WHERE (p.id = m.player1 or p.id = m.player2)),
    (SELECT COALESCE(COUNT(m.winner), 0) as wins FROM matches m
    WHERE p.id = m.winner)
from
    players p
GROUP BY
    id, p_name, matches_played
ORDER BY
    wins DESC;
