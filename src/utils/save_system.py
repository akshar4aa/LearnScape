import json
import os

SAVE_PATH = "save_game.json"

DEFAULT_DATA = {
    "hero_name": "New Hero",
    "char_type": "Scholar",
    "xp": 0,
    "coins": 0,
    "level": 1,
    "unlocked_planets": ["Earth"],  # Earth is unlocked by default
    "completed_lessons": [],
    "achievements": []
}

class SaveSystem:
    @staticmethod
    def save(data):
        try:
            with open(SAVE_PATH, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game data: {e}")
            return False

    @staticmethod
    def load():
        if not os.path.exists(SAVE_PATH):
            return DEFAULT_DATA.copy()
        
        try:
            with open(SAVE_PATH, "r") as f:
                data = json.load(f)
            
            # Validate fields, add defaults if missing
            validated_data = DEFAULT_DATA.copy()
            for key in validated_data:
                if key in data:
                    validated_data[key] = data[key]
            
            return validated_data
        except Exception as e:
            print(f"Error loading game data (using default values): {e}")
            return DEFAULT_DATA.copy()

    @staticmethod
    def has_save():
        return os.path.exists(SAVE_PATH)

    @staticmethod
    def reset():
        if os.path.exists(SAVE_PATH):
            try:
                os.remove(SAVE_PATH)
                return True
            except Exception as e:
                print(f"Error removing save file: {e}")
        return False
