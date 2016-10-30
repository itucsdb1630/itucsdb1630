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


DROP TABLE IF EXISTS contactUs;
DROP TYPE IF EXISTS contactStatus;
CREATE TYPE contactStatus AS ENUM ('new','replied','waiting','spam','closed');
CREATE TABLE contactUs(
  id SERIAL PRIMARY KEY,
  title varchar(100) NOT NULL,
  content varchar(255) NOT NULL,
  email varchar(50) NOT NULL,
  phone varchar(50) NOT NULL,
  status contactStatus DEFAULT 'new',
  sendTime timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted boolean DEFAULT false
);

INSERT INTO contactUs (title,content,email,phone) 
    VALUES ('Want to ask','How can I change my password','user@example.com','555111222333');
