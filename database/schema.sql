CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY,
    web_name TEXT NOT NULL,
    total_points INTEGER NOT NULL,
    minutes INTEGER NOT NULL
);