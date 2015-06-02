-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- You have to drop the view before you drop the tables it depends on
DROP TABLE IF EXISTS players;
CREATE TABLE players(
                    id SERIAL PRIMARY KEY,
                    p_name TEXT
);


DROP TABLE IF EXISTS matches;
CREATE TABLE matches(
                    id SERIAL PRIMARY KEY,
                    player_id INT,
                    matches INT DEFAULT 0, 
                    wins INT DEFAULT 0,
                    losses INT DEFAULT 0
);
