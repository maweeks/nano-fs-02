#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        DB = psycopg2.connect("dbname=tournament")
        cursor = DB.cursor()
        return DB, cursor
    except:
        print("Failed to connect to the database.")


def deleteMatches():
    """Remove all the match records from the database."""
    DB, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB, cursor = connect()
    cursor.execute("DELETE FROM players;")
    DB.commit()
    DB.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    DB, cursor = connect()
    cursor.execute("DELETE FROM tournaments;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB, cursor = connect()
    cursor.execute("SELECT count(*) FROM players;")
    value = cursor.fetchone()[0]
    DB.close()
    return value


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    tournamentID = getTournamentID()
    if tournamentID != -1:
        status = getTournamentStatus(tournamentID)
        if status == 0:
            DB, cursor = connect()
            cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
            DB.commit()
            DB.close()
        else:
            print("The current tournament is already underway, no more players can be added.")  # NOQA
    else:
        print("""There needs to be a current tournament to add a player.\nCreate a tournament before registering players.""")  # NOQA


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the points the player has won
        matches: the number of matches the player has played
    """
    if getTournamentID() != -1:
        DB, cursor = connect()
        cursor.execute("""SELECT * FROM playerStandingsSorted;""")
        posts = cursor.fetchall()
        DB.close()
        return posts
    else:
        return[]


def reportMatch(pida, pidb, status):
    """Records the outcome of a single match between two players.

    Args:
      pida:  the id number of the player first player
      pidb:  the id number of the player second player
      status: indicates the winner of the match:
                1 - pida won the match
                2 - pidb won the match
                3 - the match ended in a draw
    """
    tournamentID = getTournamentID()
    if tournamentID != -1:
        tStatus = getTournamentStatus(tournamentID)
        if tStatus == 1:
            DB, cursor = connect()
            cursor.execute("""INSERT INTO matches (tid, pida, pidb, status)
                            VALUES (%s, %s, %s, %s)""",
                           (getTournamentID(), pida, pidb, status,))
            DB.commit()
            DB.close()
        else:
            print("The current tournament is not in the match phase, matches cannot be be added.")  # NOQA
    else:
        print("""There needs to be a current tournament to report a match. \nCreate a tournament before reporting matches.""")  # NOQA


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    rows = []
    pairings = []
    for x in range(0, len(standings) / 2):
        pairings += {(standings[2 * x][0], standings[2 * x][1],
                      standings[(2 * x) + 1][0], standings[(2 * x) + 1][1])}
    return pairings


# Extra functions
def activatePlayer(id):
    """Activate an existing player in the current tournament."""
    tournamentID = getTournamentID()
    if tournamentID != -1:
        status = getTournamentStatus(tournamentID)
        if status == 0:
            DB, cursor = connect()
            cursor.execute("""UPDATE players SET (current, multiple) = ('t', 't') WHERE id=(%s)""", (id,))  # NOQA
            DB.commit()
            DB.close()
        else:
            print("The current tournament is already underway, no more players can be added.")  # NOQA
    else:
        print("""There needs to be a current tournament to add a player. \nCreate a tournament before registering players.""")  # NOQA


def beginTournament():
    """
    Changes the current tournament from the player registraion phase
    to the match phase.
    """
    DB, cursor = connect()
    cursor.execute("""UPDATE tournaments SET (status) = (1) WHERE status=0""")
    DB.commit()
    DB.close()


def createTournament(name):
    """Creates a new tournment with the provided name.

    Args:
      name:  the name of the tournament being created"""
    DB, cursor = connect()
    cursor.execute("INSERT INTO tournaments (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()


def deleteMatchesCurrent():
    """Remove all the match records for the current tournament from the database."""  # NOQA
    DB, cursor = connect()
    cursor.execute("DELETE FROM matches WHERE tid = %s;", (getTournamentID(),))
    DB.commit()
    DB.close()


def deletePlayersCurrent():
    """Remove all the player records for the current tournament from the database."""  # NOQA
    DB, cursor = connect()
    cursor.execute("DELETE FROM currentPlayers WHERE multiple = 'f';")
    cursor.execute("""UPDATE currentPlayers SET (current) = ('f')
                      WHERE multiple='t'""")
    DB.commit()
    DB.close()


def endTournament():
    """
    Closes the current tournament so new tournaments
    can be added.
    """
    DB, cursor = connect()
    cursor.execute("""UPDATE tournaments SET (status) = (2) WHERE status=1""")
    cursor.execute("""UPDATE players SET (current) = ('f')
                      WHERE current='t'""")
    DB.commit()
    DB.close()


def getTournamentID():
    """
    Gets the ID of the current tournament.

    Returns:
        the id of the current tournament
        returns -1 if there is no current tournament
    """
    DB, cursor = connect()
    cursor.execute("SELECT id FROM currentTournament;")
    tid = cursor.fetchall()
    if tid != []:
        tid = tid[0][0]
    # Return -1 if there is no current tournament.
    else:
        tid = -1
    DB.close()
    return tid


def getTournamentStatus(id):
    """
    Returns the status of a tournament.

    Args:
        id: the id of the tournament being queried.

    Returns:
        The status of the specified tournament.
    """
    DB, cursor = connect()
    cursor.execute("SELECT status FROM tournaments WHERE id=(%s);", (id,))
    status = cursor.fetchall()
    DB.close()
    if status != []:
        return status[0][0]
    else:
        return []


def printMatches():
    """Print a list of all the matches in the database."""
    DB, cursor = connect()
    cursor.execute("SELECT * FROM matches ORDER BY tid;")
    for row in cursor.fetchall():
        print(row)
    DB.close()


def printPairings():
    """Print a list of all the pairings for the next round."""
    pairings = swissPairings()
    for row in pairings:
        print(row)


def printPlayers():
    """Print a list of all the players in the database."""
    DB, cursor = connect()
    cursor.execute("SELECT * FROM players;")
    for row in cursor.fetchall():
        print(row)
    DB.close()


def printStandings():
    """Print the output of the player standings."""
    for row in playerStandings():
        print(row)


def printTournaments():
    """Print a list of all the matches in the database."""
    DB, cursor = connect()
    cursor.execute("SELECT * FROM tournaments;")
    for row in cursor.fetchall():
        print(row)
    DB.close()


def printMatchesCurrent():
    """Print a list of all the matches in the current tournament."""
    DB, cursor = connect()
    cursor.execute("""SELECT * FROM matches
                      WHERE tid = %s;""", (getTournamentID(),))
    for row in cursor.fetchall():
        print(row)
    DB.close()


def printPlayersCurrent():
    """Print a list of all the matches in the database current tournament."""
    DB, cursor = connect()
    cursor.execute("SELECT * FROM currentPlayers;")
    for row in cursor.fetchall():
        print(row)
    DB.close()
