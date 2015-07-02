#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


class tournament():

    ''' create the connection to the database and the cursor when the class
    is initialized.
    '''
    def __init__(self):
        self.conn = psycopg2.connect("dbname=tournament")
        self.cursor = self.conn.cursor()

    ''' make sure to call this before ending program to make sure database
    connection is properly closed.
    '''
    def close(self):
        self.conn.close()

    # Delete the matches in the database
    def deleteMatches(self):
        """Remove all the match records from the database."""
        self.cursor.execute("TRUNCATE matches;")
        self.conn.commit()

    # Delete the players from the database
    def deletePlayers(self):

        # This is required to support foreign key in matches table.
        self.deleteMatches()
        '''Now that the possible constraint error is removed, delete rows
        of data in the players table.  You must include CASCADE clause
        due to the foreign key dependencies.
        '''
        self.cursor.execute("TRUNCATE players CASCADE;")
        self.conn.commit()

    # count the number of players in the database
    def countPlayers(self):
        """Returns the number of players currently registered."""
        self.cursor.execute("select count(id) as player_count from players;")
        result = self.cursor.fetchone()[0]
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
        sql_string = "INSERT INTO players (p_name) VALUES (%s);"
        self.cursor.execute(sql_string, (name,))
        self.conn.commit()

    # report player standings in the tournament
    def playerStandings(self):
        """Returns a list of the players and their win records, sorted by
        wins.

        The first entry in the list should be the player in first place,
        or a player tied for first place if there is currently a tie.

        Returns:
          A list of tuples, each of which contains (id, name, wins,
          matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played
        """
        sql_string = '''select id, p_name, wins, matches_played from
                        player_record'''
        self.cursor.execute(sql_string)
        return self.cursor.fetchall()

    # report on the outcome of a single match
    def reportMatch(self, winner, loser):
        """Records the outcome of a single match between two players.

        Args:
          winner:  the id number of the player who won
          loser:  the id number of the player who lost
        """
        result_sql = '''INSERT INTO matches (winner, loser)
                        VALUES (%s, %s);'''
        self.cursor.execute(result_sql, (winner, loser,))
        self.conn.commit()

    # generate the swiss pairings for a round
    def swissPairings(self):
        """Returns a list of pairs of players for the next round of a
        match.  Assuming that there are an even number of players
        registered, each player appears exactly once in the pairings.
        Each player is paired with another player with an equal or
        nearly-equal win record, that is, a player adjacent to him or
        her in the standings.

        Returns:
          A list of tuples, each of which contains (id1, name1, id2, name2)
            id1: the first player's unique id
            name1: the first player's name
            id2: the second player's unique id
            name2: the second player's name
        """
        '''Query to get the following:
            The ID, name and wins from the player_record view.  The sort
            order is defined in the player_record view logic.
        '''
        pairing_sql = '''select id, p_name, wins from player_record'''
        self.cursor.execute(pairing_sql)

        # This returns the players sorted in descending order by wins.
        player_order = self.cursor.fetchall()

        # Disable spurious pylint warning on following line
        # pylint: disable=unbalanced-tuple-unpacking
        player_pairing = []
        i = 0

        ''' This loop will go through and read a row of data from the
        query.  The desired result is to pair two rows from the query
        into each single set of data you want to return in the list.
        The modulus function in the IF Statement allows you to split
        the rows into the correct information (winner or player2).
        When the player2 data is found, player1 and player2 data is
        appended as a single entry to the list.
        '''
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

''' Code added to execute rounds of a tournament.  This was not part of
the original requirements, but was just added to satisfy curiosity on
whether or not you would be able to actually run the code.
'''

if __name__ == '__main__':
    tourn = tournament()

    # Do the deletes to clear the tables
    tourn.deleteMatches()
    tourn.deletePlayers()
    # add a group of players
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
    [id1, id2, id3, id4, id5, id6] = [data[0] for data in standings]
    # execute the first round
    tourn.reportMatch(id4, id1)
    tourn.reportMatch(id2, id5)
    tourn.reportMatch(id3, id6)

    counter = 1
    while (counter <= rounds):
        pairings = tourn.swissPairings()
        # set the pairing for the round.  Disable spurious pylint warning
        # pylint: disable=unbalanced-tuple-unpacking
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
    for final_result in standings:
        print "Name %s Wins %d" % (final_result[1], final_result[2])

    tourn.close()
