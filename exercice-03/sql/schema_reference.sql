-- Structure de référence attendue.

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(100) NOT NULL
);

CREATE TABLE observations (
    id SERIAL PRIMARY KEY,
    indicator VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL,
    year INTEGER NOT NULL,
    value DOUBLE PRECISION NOT NULL,
    unit VARCHAR(30) NOT NULL
);
