--install database model in sqllight


CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    email TEXT
);

CREATE TABLE sections (
    id INTEGER PRIMARY KEY,
    type TEXT,
    title TEXT,
    author TEXT,
    date TEXT,
    content TEXT,
    icon TEXT,
    link TEXT
);

CREATE TABLE site_settings (
    id INTEGER PRIMARY KEY,
    logo TEXT,
    footer TEXT
);
