#!/usr/bin/env python
#
# Test script for tournament.py

from tournament import *

# Clear the entire database (not required)
print("1")
deleteMatches()
deletePlayers()
deleteTournaments()

# Create a new tournament
print("2")
createTournament("first")

# Register players
print("3")
registerPlayer("Jim")
registerPlayer("Tom")
registerPlayer("Rob")
registerPlayer("Max")

# Activate tournament
print("4")
beginTournament()

# Get the first round of matches
print("5")
[(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = swissPairings()

# Report the first round of matches
print("6")
reportMatch(pid1, pid2, 1)
reportMatch(pid3, pid4, 2)

# Get the second round of matches
print("7")
[(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = swissPairings()

# Report the second round of matches
print("8")
reportMatch(pid1, pid2, 2)
reportMatch(pid3, pid4, 3)

# Check tournament standings
print("9")
playerStandings()

# Deactivate the tournament so that another tournament can be created.
print("10")
endTournament()

# Create a new tournament
print("11")
createTournament("second")

printTournaments()

# Register players
print("\n12")
registerPlayer("Jam")
registerPlayer("Tim")
registerPlayer("Rib")
activatePlayer(pid2)

printPlayers()

# Activate tournament
print("\n13")
beginTournament()

printTournaments()

# Get the first round of matches
print("\n14")
[(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = swissPairings()

printPlayers()

# Report the first round of matches
print("\n15")
reportMatch(pid1, pid2, 1)
reportMatch(pid3, pid4, 2)

printMatches()
printStandings()

# Get the second round of matches
print("\n16")
[(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = swissPairings()

printPairings()

# Report the second round of matches
print("\n17")
reportMatch(pid1, pid2, 2)
reportMatch(pid3, pid4, 1)

printMatchesCurrent()

# Check tournament standings
print("\n18")
playerStandings()

printStandings()

# Deactivate the tournament so that another tournament can be created.
print("\n19")
endTournament()

printTournaments()
