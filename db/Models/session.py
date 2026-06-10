TABLE_NAME = "session"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS session (
    session_id VARCHAR(400) PRIMARY KEY,
    peer_id INTEGER UNIQUE,
    session_name VARCHAR(80),
    state VARCHAR(50) DEFAULT 'NONE',
    current_location_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active INTEGER DEFAULT 1
);
"""