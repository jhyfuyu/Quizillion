CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    tg_id TEXT, 
    username TEXT, 
    balance INTEGER, 
    quiz_key1 VARCHAR,
    quiz_key2 VARCHAR,
    quiz_key3 VARCHAR,
    count INTEGER, 
    income_count INTEGER,
    correct_answer INTEGER,
    exc_flag BOOLEAN,
    ref INTEGER,
    quiz TEXT,
    ch_1 VARCHAR,
    ch_2 VARCHAR,
    ch_3 VARCHAR,
    v_end BOOLEAN
);


CREATE TABLE quiz1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unique_key VARCHAR,
    channel TEXT,
    question TEXT,
    answers TEXT,
    correct SMALLINT 
);
INSERT INTO quiz1 (id, unique_key) VALUES (1, "NULL"), (2, "NULL"), (3, "NULL"), (4, "NULL"), (5, "NULL"), (6, "NULL"), (7, "NULL"), (8, "NULL"), (9, "NULL"), (10, "NULL");


CREATE TABLE quiz2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unique_key VARCHAR,
    channel TEXT,
    question TEXT,
    answers TEXT,
    correct SMALLINT 
);
INSERT INTO quiz2 (id, unique_key) VALUES (1, "NULL"), (2, "NULL"), (3, "NULL"), (4, "NULL"), (5, "NULL"), (6, "NULL"), (7, "NULL"), (8, "NULL"), (9, "NULL"), (10, "NULL");


CREATE TABLE quiz3 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unique_key VARCHAR,
    channel TEXT,
    question TEXT,
    answers TEXT,
    correct SMALLINT 
);
INSERT INTO quiz3 (id, unique_key) VALUES (1, "NULL"), (2, "NULL"), (3, "NULL"), (4, "NULL"), (5, "NULL"), (6, "NULL"), (7, "NULL"), (8, "NULL"), (9, "NULL"), (10, "NULL");
