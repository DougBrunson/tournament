#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament

import psycopg2
import database


def deleteMatches():
    """Remove all the match records from the database.
    Args: None
    """
    db, c = database.connect()
    query = 'DELETE FROM matches'
    c.execute(query)
    database.disconnect(db, commit=True)


def deletePlayers():
    """Remove all the player records from the database.
    Args: None
    """
    db, c = database.connect()
    query = 'delete from players'
    c.execute(query)
    database.disconnect(db, commit=True)


def countPlayers():
    """Returns the number of players currently registered.
        Args: None
        Returns: (long) player_count
    """

    db, c = database.connect()
    query = 'select * from players'
    c.execute(query)

    # refactor if num players is large to reduce db usage
    player_count = len(c.fetchall())
    database.disconnect(db)

    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
    Args:
      name: the player's full name (need not be unique).
    """
    db, c = database.connect()
    c.execute('INSERT INTO players VALUES(default, %s)', (name,))
    database.disconnect(db, True)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db, c = database.connect()
    query = "select * from v_standings;"
    c.execute(query)
    res = c.fetchall()
    database.disconnect(db)
    return res


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, c = database.connect()
    query = 'INSERT INTO matches Values(default, %s, %s)'
    c.execute(query, (winner, loser,))
    database.disconnect(db, True)


def merge_pairs(a, b):
    """Utility method to flatten inner tuples"""
    a = list(a)
    a.extend(list(b))
    return tuple(a)


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
    db, c = database.connect()
    query = "select id, name from v_standings;"
    c.execute(query)
    p = c.fetchall()
    database.disconnect(db)
    return [merge_pairs(i, j) for i, j in zip(p[::2], p[1::2])]
