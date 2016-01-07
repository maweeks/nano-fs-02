#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

print("1")
printMatches()
printPlayers()
printTournaments()

print("\n2")
deleteMatches()
deletePlayers()
deleteTournaments()
printMatches()
printPlayers()
printTournaments()

print("\n3")
createTournament("x")
registerPlayer("A")
registerPlayer("S")
registerPlayer("D")
registerPlayer("F")

printMatches()
printPlayers()
printTournaments()
printStandings()

print("\n4")
printPlayersCurrent()
printMatchesCurrent()
printPlayers()
printPlayersCurrent()
printPlayers()
