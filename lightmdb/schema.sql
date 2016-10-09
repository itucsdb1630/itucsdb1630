DROP TABLE if exists users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username varchar(50) UNIQUE,
  password varchar(150) NOT NULL,
  email varchar(100) UNIQUE,
  is_staff boolean DEFAULT true
);
