CREATE TABLE people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    gender REFERENCES gender(id),
    city TEXT,
    state TEXT,
    diagnosis_type REFERENCES diagnoses,
    description TEXT,
    years_of_no_treatment INTEGER
);
insert into people (first_name, last_name, description) values ('Nelson', 'Smith', 'Enjoys a good root beer');
insert into people (first_name, last_name, description) values ('Andrew', 'Polican', 'Wonders about computers');

CREATE TABLE friendships (
    person1_id REFERENCES people(id),
    person2_id REFERENCES people(id)
);
insert into friendships (person1_id, person2_id) values (1,2);

CREATE TABLE interests(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE person_interests(
    interest_id REFERENCES interests(id),
    person_id REFERENCES people(id)
);

CREATE TABLE gender(
    id INTEGER PRIMARY KEY,
    name TEXT
);
INSERT INTO gender (id, name) values (0, 'Male');
INSERT INTO gender (id, name) values (1, 'Female');
INSERT INTO gender (id, name) values (2, 'Other');

CREATE TABLE communities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    city TEXT,
    state TEXT
);

CREATE TABLE community_members (
    community_id REFERENCES community(id),
    community_member_id REFERENCES people(id)
);

CREATE TABLE diagnoses (
    name TEXT
);
INSERT INTO diagnoses (name) values ('Lukemia');
INSERT INTO diagnoses (name) values ('Melanoma');

CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    start_time TEXT    --use ISO 8601 strings
);

CREATE TABLE event_members (
    event_id REFERENCES events(id),
    person_id REFERENCES people(id)
);

CREATE TABLE non_community_conversations (
    first_person_id REFERENCES people(id),
    second_person_id REFERENCES people(id),
    conversation_id REFERENCES conversations(id)
);

CREATE TABLE community_conversations (
    community_id REFERENCES comunities(id),
    conversation_id REFERENCES conversations(id)
);

CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    datetime TEXT      --use ISO 8601 strings
);

CREATE TABLE messages (
    conversation_id REFERENCES conversations(id),
    message TEXT,
    datetime TEXT,
    person_id REFERENCES people(id)
);