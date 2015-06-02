#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


class tournament():

    # Create a connection to the tournament database
    def connect(self):
        self.conn = psycopg2.connect("dbname=tournament")
        self.cursor = self.conn.cursor()
        return self.conn

    def close(self):
        self.conn.close()

    # Delete the matches in the database
    def deleteMatches(self):
        """Remove all the match records from the database."""
        self.cursor.execute("DELETE FROM matches;")
        self.conn.commit()

    # Delete the players from the database
    def deletePlayers(self):
        """Remove all the player records from the database."""
        self.cursor.execute("DELETE FROM players;")
        self.conn.commit()

    # count the number of players in the database
    def countPlayers(self):
        """Returns the number of players currently registered."""
        self.cursor.execute("select * from players;")
        result = self.cursor.rowcount
        return result

    # register a player for a tournament
    def registerPlayer(self, name):
        """Adds a player to the tournament database.
        The database assigns a unique serial id number for the player.
        (This should be handled by your SQL database schema, not in your
        Python code.)

        Args:
          name: the player's full name (need not be unique).
        """
        sql_string = "INSERT INTO players (p_name) VALUES (%s) RETURNING ID;"
        self.cursor.execute(sql_string, (name,))
        # Get the newly created player_id
        player_id = self.cursor.fetchone()[0]
        match_query = "INSERT INTO matches (player_id) VALUES (%s);"
        self.cursor.execute(match_query, (player_id,))
        self.conn.commit()

    # report player standings in the tournament
    def playerStandings(self):
        """Returns a list of the players and their win records, sorted by wins.

        The first entry in the list should be the player in first place, or a
        player tied for first place if there is currently a tie.

        Returns:
          A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
        """
        sql_string = '''select p.id, p.p_name, m.wins, m.matches
                        from matches as m,
                        players as p where p.id = m.player_id
                        ORDER BY m.wins DESC'''
        self.cursor.execute(sql_string)
        return self.cursor.fetchall()

    # report on the outcome of a single match
    def reportMatch(self, winner, loser):
        """Records the outcome of a single match between two players.

        Args:
          winner:  the id number of the player who won
          loser:  the id number of the player who lost
        """
        winner_sql = '''UPDATE matches

                    SET matches = matches + 1,
                    wins = wins + 1
                    WHERE player_id = %s;'''
        self.cursor.execute(winner_sql, (winner,))
        loser_sql = '''UPDATE matches
                    SET matches = matches + 1,
                    losses = losses + 1
                    WHERE player_id = %s;'''
        self.cursor.execute(loser_sql, (loser,))
        self.conn.commit()

    # generate the swiss pairings for a round
    def swissPairings(self):
        """Returns a list of pairs of players for the next round of a match.
        Assuming that there are an even number of players registered, each
        player appears exactly once in the pairings.  Each player is paired
        with another player with an equal or nearly-equal win record, that is,
        a player adjacent to him or her in the standings.

        Returns:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        pairing_sql = '''select p.id as id, p.p_name as name, m.wins as wins
                        from matches as m,
                        players as p where p.id = m.player_id
                        ORDER BY wins DESC'''
        self.cursor.execute(pairing_sql)
        player_order = self.cursor.fetchall()
        limit = self.cursor.rowcount
        player_pairing = []
        i = 0

        for row in player_order:
            if i % 2 == 0:
                player1_id = row[0]
                player1_name = row[1]
            else:
                player2_id = row[0]
                player2_name = row[1]
                player_pairing.append((player1_id,
                                       player1_name,
                                       player2_id,
                                       player2_name))

            i += 1
        return player_pairing

# Code added to execute rounds of a tournament

if __name__ == '__main__':
    import random
    tourn = tournament()

    tourn.connect()
    tourn.deleteMatches()
    tourn.deletePlayers()
    tourn.registerPlayer("John Pertwee")
    tourn.registerPlayer("Peter Davidson")
    tourn.registerPlayer("Tom Baker")
    tourn.registerPlayer("Christopher Eccleston")
    tourn.registerPlayer("David Tennant")
    tourn.registerPlayer("Matt Smith")

    registered_players = tourn.countPlayers()
    rounds = 3
    # get a list of players with the default standings
    standings = tourn.playerStandings()
    [id1, id2, id3, id4, id5, id6] = [row[0] for row in standings]

    tourn.reportMatch(id4, id1)
    tourn.reportMatch(id2, id5)
    tourn.reportMatch(id3, id6)

    counter = 1
    while (counter <= rounds):
        pairings = tourn.swissPairings()

        [(pid1, pname1, pid2, pname2),
         (pid3, pname3, pid4, pname4),
         (pid5, pname5, pid6, pname6)] = pairings

        print "Round %d" % (counter)
        print "%s vs %s" % (pname1, pname2)
        print "%s vs %s" % (pname3, pname4)
        print "%s vs %s" % (pname5, pname6)

        tourn.reportMatch(pid1, pid2)
        tourn.reportMatch(pid3, pid4)
        tourn.reportMatch(pid5, pid6)
        counter += 1

    standings = tourn.playerStandings()

    print "\n Final Standings"
    for row in standings:
        print "Name %s Wins %d" % (row[1], row[2])

    tourn.close()
    
