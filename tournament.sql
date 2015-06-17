-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- CASCADE command on initial drop will make a notice print that the constraint
-- on the foreign key in matches is dropped as well.  This should be expected.
DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players(
                    id SERIAL PRIMARY KEY,
                    p_name TEXT
);

--Feedback in the initial review was that making player_id the primary key
--and also a foreign key to the table player's id data item could be done.  
DROP TABLE IF EXISTS matches;
CREATE TABLE matches(
                    player_id INT PRIMARY KEY REFERENCES players(id),
                    matches INT DEFAULT 0,
                    wins INT DEFAULT 0
);
