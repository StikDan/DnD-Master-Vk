TABLE_NAME = "global_history"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state_type VARCHAR(50) NOT NULL,
    session_id VARCHAR(100),
    actor_id INTEGER,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE SET NULL
);
"""