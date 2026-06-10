TABLE_NAME = "npc"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id VARCHAR(100),
    
    name VARCHAR(100) NOT NULL,
    title VARCHAR(200),
    race VARCHAR(50),
    gender VARCHAR(20),
    age VARCHAR(50),
    role TEXT,
    description TEXT,
    appearance TEXT,
    
    cr VARCHAR(20),
    ability_scores JSON,
    hit_points INTEGER DEFAULT 15,
    armor_class INTEGER DEFAULT 10,
    speed INTEGER DEFAULT 30,
    
    personality JSON,
    skills JSON,
    actions JSON,
    reactions JSON,
    legendary_actions JSON,
    racial_traits JSON,
    combat_tactics JSON,
    equipment JSON,
    companions JSON,
    relationships JSON,
    plot_roles JSON,
    possible_fates JSON,
    phrases JSON,
    loot JSON,
    gm_notes JSON,

    is_active BOOLEAN DEFAULT 1,
    is_alive BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES session(session_id) ON DELETE SET NULL
);
"""