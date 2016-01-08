#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

# Clear the entire database
deleteMatches()
deletePlayers()
deleteTournaments()

# Create a new tournament
createTournament("first")

# Register players
registerPlayer("Jim")
registerPlayer("Tom")
registerPlayer("Rob")
registerPlayer("Max")

# Activate tournament
beginTournament()

# Get the first round of matches
swissPairings()

# Report the first round of matches
reportMatch(1, 2, 1)
reportMatch(3, 4, 2)

# Get the second round of matches
swissPairings()

# Report the second round of matches
reportMatch(1, 4, 2)
reportMatch(2, 3, 3)

# Check tournament standings
playerStandings()

# Deactivate the tournament so that another tournament can be created.
endTournament()