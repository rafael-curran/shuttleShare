----
-- phpLiteAdmin database dump (https://www.phpliteadmin.org/)
-- phpLiteAdmin version: 1.9.9-dev
-- Exported: 5:59pm on December 1, 2022 (UTC)
-- database file: /workspaces/105811115/final/shuttle.db
----
BEGIN TRANSACTION;

----
-- Table structure for rides
----
CREATE TABLE 'rides' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'owner_id' INTEGER NOT NULL, 'start_location_id' INTEGER NOT NULL, 'end_location_id' INTEGER NOT NULL, 'depart_date_time' DATETIME NOT NULL, 'capacity' INTEGER);

----
-- Data dump for rides, a total of 0 rows
----

----
-- Table structure for user-rides
----
CREATE TABLE 'user-rides' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'user_id' INTEGER NOT NULL, 'ride_id' INTEGER NOT NULL);

----
-- Data dump for user-rides, a total of 0 rows
----

----
-- Table structure for locations
----
CREATE TABLE 'locations' ('id' INTEGER NOT NULL, 'name' TEXT NOT NULL);

----
-- Data dump for locations, a total of 0 rows
----

----
-- Table structure for users
----
CREATE TABLE 'users' (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL, 'email_address' TEXT, 'phone_number' INTEGER);

----
-- Data dump for users, a total of 2 rows
----
INSERT INTO "users" ("id","username","hash","email_address","phone_number") VALUES ('1','rafaelcurran','pbkdf2:sha256:260000$NSxY0Sv21MLA1pjp$c244b1b9b5cf49cf4eff2918ae4b1661ee760853e29766974906431382eaa7a2',NULL,NULL);
INSERT INTO "users" ("id","username","hash","email_address","phone_number") VALUES ('2','raf','pbkdf2:sha256:260000$kthUljRXLGNoiL3K$8f52e0efc621b2a9db99f01c22c2650620eaf5e546dac515beda1125532aaa31',NULL,NULL);

----
-- structure for index username on table users
----
CREATE UNIQUE INDEX username ON users (username);
COMMIT;
