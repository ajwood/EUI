/* Dummy database used for development, this will pretty quickly
be ripped out and replaced with the real backend data.
*/
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

DROP TABLE IF EXISTS user;
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

DROP TABLE IF EXISTS resource;
CREATE TABLE resource (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE NOT NULL,
  effort FLOAT NOT NULL -- amount of effort to generate
);

DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  owner_id INTEGER NOT NULL,
  resource_id INTEGER NOT NULL,
  obtained TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (owner_id) REFERENCES user (id),
  FOREIGN KEY (resource_id) REFERENCES resource (id)
);