CREATE DATABASE gtemhack;
USE gtemhack;
CREATE TABLE user (
    name varchar(64) NOT NULL,
    email varchar(128) PRIMARY KEY,
    password varchar(32) NOT NULL,
    role varchar(16) NOT NULL
);

CREATE TABLE takes (
    email varchar(128) NOT NULL,
    class varchar(16) NOT NULL
);

CREATE TABLE room (
    room_id varchar(64) NOT NULL,
    length integer NOT NULL,
    breadth integer NOT NULL
);

CREATE TABLE config (
    room_id varchar(64) NOT NULL,
    seat_id integer NOT NULL,
    status varchar(16) NOT NULL,
    taken_by varchar(128)
);


DROP DATABASE gtemhack;