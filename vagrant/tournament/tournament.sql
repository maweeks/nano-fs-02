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
    tid SERIAL REFERENCES tournaments(id) ON DELETE CASCADE,
    pida SERIAL REFERENCES  players(id) ON DELETE CASCADE,
    pidb SERIAL REFERENCES  players(id) ON DELETE CASCADE,
    round INT,
    status INT DEFAULT 0,
    PRIMARY KEY (tid, pida, pidb)
);

-- CREATE VIEW playerCountDraws AS
--     SELECT (CASE WHEN pida IS NULL THEN pidb ELSE pida END) AS pid, 
--         (CASE WHEN countA IS NULL THEN 0 ELSE countA END + 
--         CASE WHEN countB IS NULL THEN 0 ELSE countB END) AS draws FROM
--         (SELECT pida, count(pida) AS countA FROM matches WHERE status = 3 GROUP BY pida) AS xa
--         FULL OUTER JOIN
--         (SELECT pidb, count(pidb) AS countB FROM matches WHERE status = 3 GROUP BY pidb) AS xb
--         ON xa.pida = xb.pidb;

CREATE VIEW playerCountDraws AS
    SELECT pida AS pid, sum(countA) AS draws FROM
        (SELECT pida, count(pida) AS countA FROM matches WHERE status = 3 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches WHERE status = 3 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountLoses AS
    SELECT pida AS pid, sum(countA) AS loses FROM
        (SELECT pida, count(pida) AS countA FROM matches WHERE status = 1 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches WHERE status = 2 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountWins AS
    SELECT pida AS pid, sum(countA) AS wins FROM
        (SELECT pida, count(pida) AS countA FROM matches WHERE status = 2 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches WHERE status = 1 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

CREATE VIEW playerCountMatches AS
    SELECT pida AS pid, sum(countA) AS matches FROM
        (SELECT pida, count(pida) AS countA FROM matches WHERE status != 0 GROUP BY pida
        UNION ALL
        SELECT pidb, count(pidb) AS countB FROM matches WHERE status != 0 GROUP BY pidb) AS counts
        GROUP BY pida ORDER BY pida;

\d

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

INSERT INTO matches(tid, pida, pidb, round) VALUES (1, 1, 2, 1);
INSERT INTO matches(tid, pida, pidb, round) VALUES (1, 3, 4, 1);
INSERT INTO matches(tid, pida, pidb, round) VALUES (1, 5, 6, 1);
INSERT INTO matches(tid, pida, pidb, round, status) VALUES (1, 1, 3, 2, 3);
INSERT INTO matches(tid, pida, pidb, round, status) VALUES (1, 1, 4, 2, 3);
INSERT INTO matches(tid, pida, pidb, round, status) VALUES (1, 1, 5, 2, 1);
INSERT INTO matches(tid, pida, pidb, round, status) VALUES (1, 1, 6, 2, 2);
INSERT INTO matches(tid, pida, pidb, round, status) VALUES (1, 2, 6, 2, 2);

SELECT * FROM players;
SELECT * FROM tournaments;
SELECT * FROM matches;

\c vagrant;