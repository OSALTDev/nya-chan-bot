-- Adminer 4.3.1 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP TABLE IF EXISTS `custom_commands`;
CREATE TABLE `custom_commands` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_server` varchar(20) NOT NULL,
  `command` varchar(30) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_server` varchar(20) NOT NULL,
  `id_stream` int(10) unsigned NOT NULL,
  `author` varchar(50) NOT NULL,
  `datetime` datetime NOT NULL,
  `question` text NOT NULL,
  `timestamp` char(8) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_stream` (`id_stream`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`id_stream`) REFERENCES `streams` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `statistics_global`;
CREATE TABLE `statistics_global` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_server` varchar(20) NOT NULL,
  `id_user` varchar(20) NOT NULL,
  `id_channel` varchar(20) NOT NULL,
  `msg_count` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_user` (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `streams`;
CREATE TABLE `streams` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_server` varchar(20) NOT NULL,
  `date` datetime NOT NULL,
  `title` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `welcomes`;
CREATE TABLE `welcomes` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_server` varchar(20) NOT NULL,
  `message` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_server` (`id_server`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- 2017-07-04 21:22:11
