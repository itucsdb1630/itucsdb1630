DROP TABLE IF EXISTS users CASCADE;
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
CREATE INDEX user_username_index ON users USING btree (username);
CREATE INDEX user_email_index ON users USING btree (email);
INSERT INTO users (
  username, email, name, is_staff
) VALUES
  ('admin', 'info@lightmdb.org', 'LightMdb Admin', TRUE),
  ('tonystark', 'tonystark@lightmdb.org', 'Tony Stark', FALSE),
  ('elonmusk', 'elonmusk@lightmdb.org', 'Elon Musk', FALSE),
  ('thor', 'thorodinson@lightmdb.org', 'Thor Odinson', FALSE);

DROP TABLE IF EXISTS user_followers CASCADE;
CREATE TABLE user_followers (
  id            SERIAL PRIMARY KEY,
  follower_id   INT NOT NULL,
  following_id  INT NOT NULL
);
-- ALTER TABLE ONLY user_followers
--     ADD CONSTRAINT user_followers_follower_id_uniq UNIQUE (follower_id, following_id);
CREATE INDEX user_followers_follower_index ON user_followers USING btree (follower_id);
CREATE INDEX user_followers_following_index ON user_followers USING btree (following_id);
ALTER TABLE ONLY user_followers
    ADD CONSTRAINT user_followers_fk_follower_id FOREIGN KEY (follower_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY user_followers
    ADD CONSTRAINT user_followers_fk_following_id FOREIGN KEY (following_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;

--INSERT INTO user_followers (follower_id, following_id) VALUES (2, 3), (3, 2);
--@TODO handle it in init code, as serial id fails when using id to add users.

DROP TABLE IF EXISTS user_messages CASCADE;
CREATE TABLE user_messages (
  id          SERIAL PRIMARY KEY,
  sender_pk   INT,
  receiver_pk INT,
  time_stamp  timestamp DEFAULT CURRENT_TIMESTAMP,
  message     VARCHAR(200)
);
INSERT INTO user_messages (
  sender_pk, receiver_pk, message
) VALUES (  3, 2, 'Are you even exist ? Please do not tell anybody but I believe I am not.'),
( 3, 1, 'Hey you!'),
(2 ,3 , 'Sshhh! It is between us.' ),
  (1,3,'Yo yo...');

DROP TABLE IF EXISTS movies;
CREATE TABLE movies(
  id SERIAL PRIMARY KEY,
  title varchar(200) UNIQUE NOT NULL,
  synopsis varchar(254) NOT NULL,
  plot TEXT,
  year INT,
  runtime INT,
  votes INT,
  score FLOAT,
  rewatchability_count INT,
  rewatchability FLOAT,
  cover TEXT,
  trailer TEXT,
  certification varchar(20),
  imdb_pk varchar(20),
  imdb_score FLOAT
);



DROP TABLE IF EXISTS contactUs CASCADE;
DROP TYPE IF EXISTS contactStatus;
CREATE TYPE contactStatus AS ENUM ('new', 'replied', 'waiting', 'spam', 'closed');
CREATE TABLE contactUs (
  id       SERIAL PRIMARY KEY,
  title    VARCHAR(100) NOT NULL,
  content  VARCHAR(255) NOT NULL,
  email    VARCHAR(50)  NOT NULL,
  phone    VARCHAR(50)  NOT NULL,
  status   contactStatus DEFAULT 'new',
  sendTime timestamp     DEFAULT CURRENT_TIMESTAMP,
  deleted  BOOLEAN       DEFAULT FALSE
);

INSERT INTO contactUs (title, content, email, phone)
VALUES ('Want to ask', 'How can I change my password', 'user@example.com', '555111222333');

DROP TABLE IF EXISTS contactComments CASCADE;
CREATE TABLE contactComments(
  id SERIAL PRIMARY KEY,
  pk_contact INT NOT NULL,
  comment varchar(255) NOT NULL,
  sendMail boolean NOT NULL ,
  sendTime timestamp DEFAULT CURRENT_TIMESTAMP,
  deleted boolean DEFAULT false
);

-- ALTER TABLE ONLY contactComments
--     ADD CONSTRAINT contact_id_uniq UNIQUE (pk_contact);
CREATE INDEX contact_id ON contactComments USING btree (pk_contact);
ALTER TABLE ONLY contactComments
    ADD CONSTRAINT comment_fk_for_contact_id FOREIGN KEY (pk_contact) REFERENCES contactUs(id) DEFERRABLE INITIALLY DEFERRED;
