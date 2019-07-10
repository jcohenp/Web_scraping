DROP TABLE IF EXISTS `teams_informations`;
DROP TABLE IF EXISTS `trophies`;
DROP TABLE IF EXISTS `matches`;
DROP TABLE IF EXISTS `top_players`;
DROP TABLE IF EXISTS `players_from_api`;

CREATE TABLE `teams_informations`
(
  `team_id` int PRIMARY KEY,
  `league` varchar(20),
  `name` varchar(50),
  `founded` int,
  `address` varchar(255),
  `email` varchar(50),
  `venue_name` varchar(50),
  `venue_capacity` int
);

CREATE TABLE `trophies`
(
  `team_id` int PRIMARY KEY,
  `championships` int,
  `cups` int,
  `UEFA_Champions_League` int,
  FOREIGN KEY (`team_id`) REFERENCES teams_informations(`team_id`)
);


CREATE TABLE `matches`
(
  `id_match` int PRIMARY KEY,
  `day` varchar(10),
  `date_match` date,
  `team_a_id` int,
  `team_b_id` int,
  `score` varchar(10),
  FOREIGN KEY (`team_a_id`) REFERENCES teams_informations(team_id),
  FOREIGN KEY (`team_b_id`) REFERENCES teams_informations(team_id)
);

CREATE TABLE `top_players`
(
  `id_player` int PRIMARY KEY,
  `name` varchar(60),
  `team_id` int,
  `goals` int,
  `first_goals` int,
  FOREIGN KEY (team_id) REFERENCES teams_informations(team_id)
);


CREATE TABLE `players_from_api`
(
  id_player int PRIMARY KEY,
  team_id int,
  player_name varchar(50),
  player_position varchar(20),
  nationality varchar(20),
  role varchar(20),
  FOREIGN KEY (id_player) REFERENCES top_players(id_player),
  FOREIGN KEY (team_id) REFERENCES teams_informations(team_id)
);