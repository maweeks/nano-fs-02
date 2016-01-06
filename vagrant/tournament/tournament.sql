-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

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
    current BOOLEAN DEFAULT 't'
);


CREATE TABLE matches(
    tid INT REFERENCES tournaments(id) ON DELETE CASCADE,
    pida INT REFERENCES  players(id) ON DELETE CASCADE,
    pidb INT REFERENCES  players(id) ON DELETE CASCADE,
    status INT,
    PRIMARY KEY (tid, pida, pidb)
);

-- TODO: for current tournament
CREATE VIEW currentPlayers AS
    SELECT * FROM players;

CREATE VIEW playerCountDraws AS
    SELECT pida AS id, sum(countA) AS count FROM
        (SELECT pida, count(pida) AS countA FROM matches WHERE status = 3 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches WHERE status = 3 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountLoses AS
    SELECT pida AS id, sum(countA) AS count FROM
        (SELECT pida, count(pida) AS countA FROM matches WHERE status = 2 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches WHERE status = 1 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountWins AS
    SELECT pida AS id, sum(countA) AS count FROM
        (SELECT pida, count(pida) AS countA FROM matches WHERE status = 1 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches WHERE status = 2 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountMatches AS
    SELECT pida AS id, sum(countA) AS matches FROM
        (SELECT pida, count(pida) AS countA FROM matches GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountPoints AS
    SELECT id, sum(count) AS points FROM
        ((SELECT id, (count*3) AS count FROM playerCountWins)
        UNION ALL
        (SELECT id, count AS count FROM playerCountDraws)) AS points
        GROUP BY id ORDER BY id;

INSERT INTO players(name) VALUES ('q');
INSERT INTO players(name) VALUES ('w');
INSERT INTO players(name) VALUES ('e');
INSERT INTO players(name) VALUES ('r');
INSERT INTO players(name) VALUES ('t');
INSERT INTO players(name) VALUES ('y');

INSERT INTO tournaments(name) VALUES ('a');
INSERT INTO tournaments(name) VALUES ('s');
INSERT INTO tournaments(name) VALUES ('d');
INSERT INTO tournaments(name) VALUES ('f');

INSERT INTO matches(tid, pida, pidb, status) VALUES (1, 1, 2, 1);
INSERT INTO matches(tid, pida, pidb, status) VALUES (1, 3, 4, 2);
INSERT INTO matches(tid, pida, pidb, status) VALUES (1, 5, 6, 3);
INSERT INTO matches(tid, pida, pidb, status) VALUES (1, 1, 3, 3);
INSERT INTO matches(tid, pida, pidb, status) VALUES (1, 1, 4, 3);
INSERT INTO matches(tid, pida, pidb, status) VALUES (1, 1, 6, 2);
INSERT INTO matches(tid, pida, pidb, status) VALUES (1, 2, 6, 2);

\d
SELECT * FROM players;
SELECT * FROM tournaments;
SELECT * FROM matches;

\c vagrant;