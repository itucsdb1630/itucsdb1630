DROP TABLE if exists users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username varchar(50) UNIQUE,
  password varchar(150) NOT NULL,
  email varchar(100) UNIQUE,
  name varchar(200),
  active boolean DEFAULT false,
  confirmed_at timestamp DEFAULT NULL,
  is_staff boolean DEFAULT true
);
