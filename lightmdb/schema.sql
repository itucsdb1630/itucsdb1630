DROP TABLE if exists users;
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username varchar(50) UNIQUE,
  password varchar(150),
  email varchar(100) UNIQUE,
  name varchar(200),
  confirmed_at timestamp DEFAULT NULL,
  deleted boolean DEFAULT false,
  is_staff boolean DEFAULT false
);
INSERT INTO users (
  username, email, name, is_staff
) VALUES (
  'admin', 'info@lightmdb.org', 'LightMdb Admin', true
);
