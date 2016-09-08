
-- Database setup
DROP database tournament;
CREATE database tournament;
\c tournament 
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;            

 
-- player_id | name
CREATE TABLE players (
	id  Serial,
	name varchar(255) NOT NULL,		
	PRIMARY KEY(id)
);

-- match_id | winner | loser
CREATE TABLE matches (																	
	id Serial,
	winner int references players(id) NOT NULL,
	loser int references players(id) NOT NULL
);

--  name | wins | matches
CREATE view v_standings(id, name, num_wins, num_matches)
	as SELECT
	players.id,
	players.name,
	(SELECT COALESCE(wins, 0) as num_wins FROM (SELECT count(matches) as wins from matches where players.id = matches.winner) as wins), 
	(SELECT count(matches) as totalMatches from matches where (players.id = matches.winner or players.id = matches.loser))
	from Players
	ORDER BY num_wins desc;


