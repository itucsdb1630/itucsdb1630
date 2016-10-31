DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id           SERIAL PRIMARY KEY,
  username     VARCHAR(50) UNIQUE,
  password     VARCHAR(150),
  email        VARCHAR(100) UNIQUE,
  name         VARCHAR(200),
  confirmed_at timestamp DEFAULT NULL,
  deleted      BOOLEAN   DEFAULT FALSE,
  is_staff     BOOLEAN   DEFAULT FALSE
);
INSERT INTO users (
  username, email, name, is_staff
) VALUES (
  'admin', 'info@lightmdb.org', 'LightMdb Admin', TRUE
);

DROP TABLE IF EXISTS user_messages;
CREATE TABLE user_messages (
  id          SERIAL PRIMARY KEY,
  pk_sender   INT,
  pk_receiver INT,
  time_stamp  timestamp DEFAULT CURRENT_TIMESTAMP,
  message     VARCHAR(200)
);
INSERT INTO user_messages (
  pk_sender, pk_receiver, message
) VALUES (
  1, 2, 'Are you even exist ? Please do not tell anybody but I believe I am not.'
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
