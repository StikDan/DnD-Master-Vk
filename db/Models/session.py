TABLE_NAME = "session"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS session (
    session_id VARCHAR(400) PRIMARY KEY,
    session_name VARCHAR(80),
    active INTEGER DEFAULT 1
);
"""