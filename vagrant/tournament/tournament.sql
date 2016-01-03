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
	tid SERIAL REFERENCES tournaments(id),
	pida SERIAL REFERENCES  players(id),
	pidb SERIAL REFERENCES  players(id),
	round INT,
	status INT DEFAULT 0,
	PRIMARY KEY (tid, pida, pidb)
);

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

SELECT * FROM players;
SELECT * FROM tournaments;
SELECT * FROM matches;

\c vagrant;