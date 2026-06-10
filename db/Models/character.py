TABLE_NAME = "character"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    class VARCHAR(50),
    race VARCHAR(50),
    level INTEGER DEFAULT 1,
    background TEXT,
    alignment VARCHAR(50),
    
    strength INTEGER DEFAULT 10,
    dexterity INTEGER DEFAULT 10,
    constitution INTEGER DEFAULT 10,
    intelligence INTEGER DEFAULT 10,
    wisdom INTEGER DEFAULT 10,
    charisma INTEGER DEFAULT 10,
    
    hit_points_max INTEGER DEFAULT 10,
    hit_points_current INTEGER DEFAULT 10,
    armor_class INTEGER DEFAULT 10,
    speed INTEGER DEFAULT 30,
    proficiency_bonus INTEGER DEFAULT 2,
    
    ability_scores JSON,
    skills JSON,
    saving_throws JSON,
    features JSON,
    traits JSON,
    equipment JSON,
    spells JSON,
    inventory JSON,
    backstory TEXT,
    
    is_active BOOLEAN DEFAULT 1,
    is_alive BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (player_id) REFERENCES player(player_id) ON DELETE CASCADE,
    FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE CASCADE
);
"""