DROP TABLE IF EXISTS `trophies`;
DROP TABLE IF EXISTS `matches`;
DROP TABLE IF EXISTS `top_players`;
DROP TABLE IF EXISTS `teams_informations`;


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
  `Premier_League` int,
  `League_Cup` int,
  `UEFA_Champions_League` int,
  `Bundesliga` int,
  `Super_Cup` int,
  `Serie_A` int,
  `La_Liga` int,
  `Ligue_1` int,
  `Coupe_de_France` int,
  FOREIGN KEY (`team_id`) REFERENCES teams_informations(`team_id`)
);


CREATE TABLE `matches`
(
  `day` varchar(10),
  `date_match` date,
  `team_a_id` int,
  `team_b_id` int,
  `score` varchar(10),
  PRIMARY KEY (`date_match`, `team_a_id`, `team_b_id`),
  FOREIGN KEY (`team_a_id`) REFERENCES teams_informations(team_id),
  FOREIGN KEY (`team_b_id`) REFERENCES teams_informations(team_id)
);

CREATE TABLE `top_players`
(
  `id_player` int PRIMARY KEY,
  `name` varchar(40),
  `team` varchar(20),
  `goals` int,
  `first_goals` int,
  `team_id` int,
  FOREIGN KEY (team_id) REFERENCES teams_informations(team_id)
);

