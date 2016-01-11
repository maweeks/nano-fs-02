-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'tournament'
  AND pid <> pg_backend_pid();
  
\c vagrant;

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE tournaments(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    status INT DEFAULT 0
);


CREATE TABLE players(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20),
    current BOOLEAN DEFAULT 't',
    multiple BOOLEAN DEFAULT 'f'
);


CREATE TABLE matches(
    mid SERIAL,
    tid INT REFERENCES tournaments(id) ON DELETE CASCADE,
    pida INT REFERENCES  players(id) ON DELETE CASCADE,
    pidb INT REFERENCES  players(id) ON DELETE CASCADE,
    status INT,
    PRIMARY KEY (mid, tid, pida, pidb)
);

CREATE VIEW currentMatches AS
    SELECT tid, pida, pidb, status FROM matches,
        (SELECT id FROM tournaments WHERE status < 2) AS tournamentID
    WHERE tid = id;

CREATE VIEW currentPlayers AS
    SELECT * FROM players WHERE current = 't';

CREATE VIEW currentTournament AS
    SELECT * FROM tournaments WHERE status < 2;

CREATE VIEW playerCountDraws AS
    SELECT pida AS id, sum(countA) AS count FROM
        (SELECT pida, count(pida) AS countA FROM currentMatches WHERE status = 3 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM currentMatches WHERE status = 3 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountLoses AS
    SELECT pida AS id, sum(countA) AS count FROM
        (SELECT pida, count(pida) AS countA FROM currentMatches WHERE status = 2 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM currentMatches WHERE status = 1 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountWins AS
    SELECT pida AS id, sum(countA) AS count FROM
        (SELECT pida, count(pida) AS countA FROM currentMatches WHERE status = 1 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM currentMatches WHERE status = 2 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountMatches AS
    SELECT pida AS id, sum(countA) AS matches FROM
        (SELECT pida, count(pida) AS countA FROM currentMatches GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM currentMatches GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountPoints AS
    SELECT id, sum(count) AS points FROM
        ((SELECT id, (count*3) AS count FROM playerCountWins)
        UNION ALL
        (SELECT id, count AS count FROM playerCountDraws)) AS points
        GROUP BY id ORDER BY id;

CREATE VIEW playerStandings AS
    SELECT currentPlayers.id, currentPlayers.name,
        CASE WHEN playerCountPoints.points IS NULL THEN 0 ELSE playerCountPoints.points END AS points,
        CASE WHEN playerCountMatches.matches IS NULL THEN 0 ELSE playerCountMatches.matches END AS matches
        FROM currentPlayers
        currentPlayers LEFT JOIN 
        (playerCountMatches LEFT JOIN playerCountPoints ON playerCountMatches.id = playerCountPoints.id)
        ON currentPlayers.id = playerCountMatches.id
        ORDER BY points DESC, id ASC;

CREATE VIEW playerOMP AS
    SELECT standings.id, sum(standings.points) AS omp FROM
        ((SELECT pida AS pid, pidb AS oid FROM currentMatches)
        UNION ALL
        (SELECT pidb AS pid, pida AS oid FROM currentMatches)) AS allMatches
        FULL JOIN 
        (SELECT * FROM playerStandings) AS standings
        ON allMatches.oid = standings.id
        GROUP BY standings.id;

CREATE VIEW playerStandingsSorted AS
    SELECT playerStandings.id, playerStandings.name, playerStandings.points, playerStandings.matches FROM playerStandings
                playerStandings JOIN playerOMP ON playerStandings.id = playerOMP.id
                ORDER BY playerStandings.points DESC, playerOMP.omp DESC, playerStandings.id;

-- \d
-- SELECT * FROM players;
-- SELECT * FROM tournaments;
-- SELECT * FROM matches;
-- SELECT * FROM playerOMP;
-- SELECT * FROM playerStandings;
-- SELECT * FROM playerStandingsSorted;

-- \c vagrant;