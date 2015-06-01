-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
create table players (
  id serial PRIMARY KEY,
  name text
  );

create table match (
  id serial PRIMARY KEY,
  winner integer,
  loser integer
  );

create table standings (
  player_id integer PRIMARY KEY,
  wins integer DEFAULT 0,
  losses integer DEFAULT 0,
  opponent_wins integer DEFAULT 0
  );
