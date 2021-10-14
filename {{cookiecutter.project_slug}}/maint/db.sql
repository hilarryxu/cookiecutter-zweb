--
-- Database: {{cookiecutter.pkg_name}}
--


-- CREATE DATABASE `db_{{cookiecutter.pkg_name}}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci ;


-- User
CREATE TABLE `{{cookiecutter.pkg_name}}_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `phone` varchar(20) NOT NULL DEFAULT '',
  `nickname` varchar(200) NOT NULL DEFAULT '',
  `avatar_url` varchar(255) NOT NULL DEFAULT '',
  `props` longtext,
  `created_at` bigint(20) NOT NULL DEFAULT 0,
  `updated_at` bigint(20) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;
