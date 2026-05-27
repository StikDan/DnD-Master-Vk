TABLE_NAME = "npc"

CREATE_TABLE = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Основная информация
    name VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(50) DEFAULT 'Жив',
    race VARCHAR(50) NOT NULL,
    age VARCHAR(50) NOT NULL,
    role TEXT NOT NULL,
    description TEXT NOT NULL,
    appearance TEXT NOT NULL,
    
    -- Характеристики D&D в JSON
    ability_scores JSON NOT NULL,
    hit_points INTEGER DEFAULT 15,
    armor_class INTEGER NOT NULL,
    speed INTEGER DEFAULT 30,
    
    -- Сложные данные в JSON
    personality JSON,
    skills JSON,
    actions JSON,
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

    -- Метаданные
    is_active BOOLEAN DEFAULT 1
);"""