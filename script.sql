CREATE TABLE `games` (
  `game_id` int NOT NULL AUTO_INCREMENT,
  `game_name` varchar(50) DEFAULT NULL,
  `game_slug` varchar(50) DEFAULT NULL,
  `launch_date` date DEFAULT NULL,
  PRIMARY KEY (`game_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci