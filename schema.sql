
DROP DATABASE IF EXISTS postgres;
CREATE DATABASE postgres;
\c postgres;


DROP TABLE IF EXISTS exhibition CASCADE;
DROP TABLE IF EXISTS museum_department CASCADE;
DROP TABLE IF EXISTS museum_floor CASCADE;
DROP TABLE IF EXISTS assistance_interaction CASCADE;
DROP TABLE IF EXISTS emergency_interaction CASCADE;
DROP TABLE IF EXISTS rating_interaction CASCADE;
DROP TABLE IF EXISTS rating_type CASCADE;


CREATE TABLE IF NOT EXISTS museum_floor (
    floor_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    floor_name VARCHAR(100) NOT NULL,
    UNIQUE (floor_name)
);

CREATE TABLE IF NOT EXISTS museum_department (
    department_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    UNIQUE (department_name)
);

CREATE TABLE IF NOT EXISTS exhibition (
    exhibit_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibit_code INT NOT NULL,
    exhibit_name VARCHAR(100) NOT NULL,
    exhibit_start_date TIMESTAMPTZ NOT NULL,
    exhibit_description text NOT NULL,
    floor_name VARCHAR(100) NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (floor_name) REFERENCES museum_floor(floor_name) ON DELETE CASCADE,
    FOREIGN KEY (department_name) REFERENCES museum_department(department_name) ON DELETE CASCADE,
    UNIQUE (exhibit_code)
);

CREATE TABLE IF NOT EXISTS assistance_interaction (
    assistance_interaction_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assistance_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exhibit_code smallint NOT NULL,
    FOREIGN KEY (exhibit_code) REFERENCES exhibition(exhibit_code) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS emergency_interaction (
    emergency_interaction_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    emergency_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exhibit_code smallint NOT NULL,
    FOREIGN KEY (exhibit_code) REFERENCES exhibition(exhibit_code) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS rating_type (
    rating_type_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rating_value smallint NOT NULL,
    rating_description text NOT NULL,
    UNIQUE (rating_value)
);

CREATE TABLE IF NOT EXISTS rating_interaction (
    rating_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rating_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    exhibit_code smallint NOT NULL,
    rating_value smallint NOT NULL,
    FOREIGN KEY (exhibit_code) REFERENCES exhibition(exhibit_code) ON DELETE CASCADE,
    FOREIGN KEY (rating_value) REFERENCES rating_type(rating_value) ON DELETE CASCADE
);

INSERT INTO rating_type (rating_value, rating_description) VALUES 
    ('0', 'Terrible'),
    ('1', 'Bad'),
    ('2', 'Neutral'),
    ('3', 'Good'),
    ('4', 'Amazing');

INSERT INTO museum_floor (floor_name) VALUES 
    ('Vault'),
    ('1'),
    ('2'),
    ('3');

INSERT INTO museum_department (department_name) VALUES 
    ('Entomology'),
    ('Geology'),
    ('Paleontology'),
    ('Zoology'),
    ('Ecology');


INSERT INTO exhibition (exhibit_name, exhibit_code, floor_name, department_name, exhibit_start_date, exhibit_description)
    VALUES 
    ('Cetacean Sensations', 3, '1', 'Zoology', '2019-07-01', 'Whales: from ancient myth to critically endangered.'),
    ('The Crenshaw Collection', 2, '2', 'Zoology', '2021-03-03', 'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.'),
    ('Thunder Lizards', 5, '1', 'Paleontology', '2023-02-01', 'How new research is making scientists rethink what dinosaurs really looked like.'),
    ('Adaptation', 1, 'Vault', 'Entomology', '2019-07-01', 'How insect evolution has kept pace with an industrialised world'),
    ('Measureless to Man', 0, '1', 'Geology', '2021-08-23', 'An immersive 3D experience: delve deep into a previously-inaccessible cave system.'),
    ('Our Polluted World', 4, '3', 'Ecology', '2021-05-12', 'A hard-hitting exploration of humanitys impact on the environment.');