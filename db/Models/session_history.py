TABLE_NAME = "session_history"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS session_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(400) NOT NULL,
    role VARCHAR(45) NOT NULL,
    content TEXT NOT NULL
);"""