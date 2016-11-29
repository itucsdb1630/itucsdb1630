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
) VALUES (
  'admin', 'info@lightmdb.org', 'LightMdb Admin', TRUE
);

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

DROP TABLE IF EXISTS movies;
CREATE TABLE movies(
  id SERIAL PRIMARY KEY,
  title varchar(200) UNIQUE NOT NULL,
  synopsis varchar(254) NOT NULL,
  year INT,
  votes INT,
  score FLOAT,
  rewatchability_count INT,
  rewatchability FLOAT
);

DROP TABLE IF EXISTS playlists;
CREATE TABLE playlists(
  id SERIAL PRIMARY KEY,
  name varchar(200) UNIQUE NOT NULL,
  is_public boolean,
  user_id INT --this is the user who created the playlist
);

DROP TABLE IF EXISTS playlist_movies CASCADE;
CREATE TABLE playlist_movies(
  id SERIAL PRIMARY KEY,
  playlist_id INT,
  movie_id INT,
  ordering INT --order is a reserved keyword
);


CREATE INDEX playlist_movies_movies_index ON playlist_movies USING btree (movie_id);
CREATE INDEX playlist_movies_playlists_index ON playlist_movies USING btree (playlist_id);
CREATE INDEX playlists_user_index ON playlists USING btree (user_id);
ALTER TABLE ONLY playlists
    ADD CONSTRAINT playlists_user_id FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY playlist_movies
    ADD CONSTRAINT playlist_movies_playlist_id FOREIGN KEY (playlist_id) REFERENCES playlists(id) DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE ONLY playlist_movies
    ADD CONSTRAINT playlist_movies_movie_id FOREIGN KEY (movie_id) REFERENCES movies(id) DEFERRABLE INITIALLY DEFERRED;

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

