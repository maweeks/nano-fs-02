#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM matches;")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM players;")
    DB.commit()
    DB.close()

def deleteTournaments():
    """Remove all the tournament records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM tournaments;")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT count(*) FROM players;")
    value = cursor.fetchall()[0][0]
    DB.close()
    return value

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # TODO: Check for current tournement
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s)",(name,))
    DB.commit()
    DB.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        points: the points the player has won
        matches: the number of matches the player has played
    """
    # TODO: Current tournement
    # TODO: sort 2 - opponant points
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("""SELECT currentPlayers.id, currentPlayers.name,
        CASE WHEN playerCountPoints.points IS NULL THEN 0 ELSE playerCountPoints.points END AS points,
        CASE WHEN playerCountMatches.matches IS NULL THEN 0 ELSE playerCountMatches.matches END AS matches
        FROM currentPlayers
        currentPlayers LEFT JOIN 
        (playerCountMatches LEFT JOIN playerCountPoints ON playerCountMatches.id = playerCountPoints.id)
        ON currentPlayers.id = playerCountMatches.id
        ORDER BY points DESC, id ASC;""")
    posts = cursor.fetchall()
    DB.close()
    return posts


def reportMatch(pida, pidb, status):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("""INSERT INTO matches (tid, pida, pidb, status) VALUES (5, %s, %s, %s)""", (pida, pidb, status,));
    DB.commit()
    DB.close()
 
 
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

# Extra functions

def createTournament(name):
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO tournaments (name) VALUES (%s)",(name,))
    DB.commit()
    DB.close()

def printMatches():
    """Print a list of all the matches in the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM matches ORDER BY tid;")
    for row in cursor.fetchall():
        print(row)
    DB.close()

def printPlayers():
    """Print a list of all the players in the database."""
    DB = connect()
    cursor = DB.cursor()
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
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM tournaments;")
    for row in cursor.fetchall():
        print(row)
    DB.close()

def printMatchesCurrent():
    """Print a list of all the matches in the current tournament."""
    # TODO: Extension

def printPlayersCurrent():
    """Print a list of all the matches in the database current tournament."""
    # TODO: Extension

def deleteMatchesCurrent():
    """Remove all the match records for the current tournament from the database."""
    # TODO: Extension

def deletePlayersCurrent():
    """Remove all the player records for the current tournament from the database."""
    # TODO: Extension
