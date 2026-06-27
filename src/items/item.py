ITEMS_DATABASE = {
    # Weapons
    "rusty_sword": {
        "name": "Rusty Dagger",
        "type": "weapon",
        "cost": 20,
        "power": 3,
        "desc": "A basic, slightly weathered training weapon (+3 Atk)."
    },
    "silver_sword": {
        "name": "Silver Claymore",
        "type": "weapon",
        "cost": 150,
        "power": 8,
        "desc": "A forged iron blade coated in gleaming silver (+8 Atk)."
    },
    "gold_sword": {
        "name": "Gilded Excalibur",
        "type": "weapon",
        "cost": 400,
        "power": 18,
        "desc": "An epic golden broadsword crackling with magic (+18 Atk)."
    },
    
    # Shields
    "wooden_shield": {
        "name": "Wooden Buckler",
        "type": "shield",
        "cost": 15,
        "defense": 2,
        "desc": "A rudimentary circular shield (+2 Def)."
    },
    "iron_shield": {
        "name": "Iron Kite Shield",
        "type": "shield",
        "cost": 120,
        "defense": 5,
        "desc": "A heavy-grade steel shield (+5 Def)."
    },
    "dragon_shield": {
        "name": "Dragon Aegis",
        "type": "shield",
        "cost": 350,
        "defense": 12,
        "desc": "A dragon-scale shield that absorbs major blows (+12 Def)."
    },

    # Armor
    "leather_armor": {
        "name": "Leather Tunic",
        "type": "armor",
        "cost": 30,
        "defense": 3,
        "hp_boost": 10,
        "desc": "Flexible light leather gear (+3 Def, +10 HP)."
    },
    "iron_armor": {
        "name": "Steel Plate Mail",
        "type": "armor",
        "cost": 180,
        "defense": 7,
        "hp_boost": 25,
        "desc": "Heavy steel plates covering vital areas (+7 Def, +25 HP)."
    },
    "obsidian_armor": {
        "name": "Obsidian Armor",
        "type": "armor",
        "cost": 450,
        "defense": 16,
        "hp_boost": 60,
        "desc": "Infused volcanic glass armor plate (+16 Def, +60 HP)."
    },

    # Usables
    "health_potion": {
        "name": "Health Potion",
        "type": "potion",
        "cost": 25,
        "effect": "heal_50",
        "desc": "A red cherry flask. Restores 50 Health points."
    },
    "mana_potion": {
        "name": "Mana Potion",
        "type": "potion",
        "cost": 25,
        "effect": "mana_30",
        "desc": "A blue blueberry flask. Restores 30 Mana points."
    },
    
    # Scrolls and Cards
    "hint_card": {
        "name": "Knowledge Scroll",
        "type": "card",
        "cost": 40,
        "effect": "hint",
        "desc": "Consumable scroll. Instantly eliminates 2 wrong answers!"
    },
    "spellbook_intellect": {
        "name": "Tome of Intellect",
        "type": "book",
        "cost": 250,
        "mana_boost": 20,
        "desc": "Adds +20 maximum Mana and increases spell casting slots."
    }
}

def get_item_details(item_id):
    return ITEMS_DATABASE.get(item_id, {
        "name": "Unknown Artifact",
        "type": "misc",
        "cost": 0,
        "desc": "A mysterious runic artifact."
    })
