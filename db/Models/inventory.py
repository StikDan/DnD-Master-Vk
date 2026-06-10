TABLE_NAME = "inventory"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER NOT NULL,
    owner_type VARCHAR(20) NOT NULL,
    
    item_name VARCHAR(200) NOT NULL,
    item_type VARCHAR(50),
    description TEXT,
    quantity INTEGER DEFAULT 1,
    weight DECIMAL(10,2) DEFAULT 0,
    value_gold INTEGER DEFAULT 0,
    
    properties JSON,
    is_equipped BOOLEAN DEFAULT 0,
    is_cursed BOOLEAN DEFAULT 0,
    is_identified BOOLEAN DEFAULT 1
);
"""