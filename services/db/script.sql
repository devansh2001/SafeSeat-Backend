CREATE DATABASE gtemhack;

CREATE TABLE user (
    name varchar(64),
    email varchar(128) PRIMARY KEY,
    password varchar(32),
    role varchar(16)
);
