TABLE_NAME = "location"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(100),
    parent_location_id INTEGER,
    
    name VARCHAR(200) NOT NULL,
    location_type VARCHAR(50),
    description TEXT,
    atmosphere TEXT,
    dangers TEXT,
    points_of_interest JSON,
    npcs JSON,
    encounters JSON,
    loot JSON,
    exits JSON,
    
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE SET NULL,
    FOREIGN KEY (parent_location_id) REFERENCES location(id) ON DELETE SET NULL
);
"""