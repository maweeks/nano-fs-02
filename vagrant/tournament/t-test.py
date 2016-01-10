#!/usr/bin/env python
#
# Test script for tournament.py

from tournament import *

# Clear the entire database (not required)
print("\n1")
deleteMatches()
deletePlayers()
deleteTournaments()

printPlayers()
printMatches()
printTournaments()

# Create a new tournament
print("\n2")
createTournament("first")

printTournaments()

# Register players
print("\n3")
registerPlayer("Jim")
registerPlayer("Tom")
registerPlayer("Rob")
registerPlayer("Max")

printPlayers()

# Activate tournament
print("\n4")
beginTournament()

printTournaments()


# Get the first round of matches
print("\n5")
[(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = swissPairings()

printPlayers()

# Report the first round of matches
print("\n6")
reportMatch(pid1, pid2, 1)
reportMatch(pid3, pid4, 2)

printMatches()
printStandings()

# Get the second round of matches
print("\n7")
[(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = swissPairings()

printPlayers()

# Report the second round of matches
print("\n8")
reportMatch(pid1, pid4, 3)
reportMatch(pid2, pid3, 1)

printMatches()

# Check tournament standings
print("\n9")
playerStandings()

printStandings()

# Deactivate the tournament so that another tournament can be created.
print("\n10")
endTournament()

printTournaments()