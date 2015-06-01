ment.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()

    cursor.execute("delete from match")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()

    cursor.execute("delete from players")
    cursor.execute("delete from standings")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()

    cursor.execute("select count(*) from players")
    amount_of_players = cursor.fetchall()
    db.close()

    return amount_of_players[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()

    """ Insert new player into players table """
    cursor.execute("insert into players ( name ) values ( %s )",  ( name, ) )
    db.commit()

    """ Set the player_id from the players table """
    cursor.execute("select id from players where name = %s", ( name, ) )
    player_id = cursor.fetchone()[0]

    """ Insert player_id into standings tables """
    cursor.execute("insert into standings ( player_id  ) values ( %s )",  ( player_id, ) )
    db.commit()

    db.close()


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
    db = connect()
    cursor = db.cursor()

    cursor.execute("SELECT \
        players.id, \
        players.name, \
        standings.wins, \
        (coalesce(standings.wins) + coalesce(standings.losses)) as matches \
        FROM \
        players, standings \
        WHERE \
        players.id = standings.player_id \
        ORDER BY \
        wins desc, standings.opponent_wins desc")
    player_standings = cursor.fetchall()
    db.close()

    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()

    """ Update match table with results """
    cursor.execute("INSERT \
        INTO match \
        ( winner, loser ) \
        VALUES \
        ( %s, %s )",  ( winner, loser) )

    """ update winner in standings """
    cursor.execute("UPDATE \
        standings \
        SET wins = wins+1 \
        WHERE \
        player_id = %s", (winner, ))

    """ update loser in standings """
    cursor.execute("UPDATE \
        standings \
        SET losses = losses+1 \
        WHERE \
        player_id = %s", (loser, ))

    """ update opponent_wins in standings """
    cursor.execute("UPDATE \
        standings \
        SET opponent_wins = opponent_wins+1 \
        WHERE \
        player_id = %s", (loser, ))
    db.commit()

    db.close()


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
    db = connect()
    cursor = db.cursor()

    pairings = []

    cursor.execute("SELECT \
       players.id, \
       players.name \
       FROM \
       players, standings \
       WHERE \
       players.id = standings.player_id \
       ORDER BY \
       standings.wins desc, standings.opponent_wins desc")
    standings = cursor.fetchall()

    while standings:
        first_player = standings.pop(0)
        second_player = standings.pop(0)
        pairings.append(first_player + second_player)

    db.close()
    print "debug: ", pairings
    return pairings
