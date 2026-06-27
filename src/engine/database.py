import sqlite3
import os
import json
from src.engine.settings import DB_PATH

class DatabaseManager:
    def __init__(self):
        # Create saves directory if it doesn't exist
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = None
        self.init_db()

    def get_connection(self):
        if not self.conn:
            try:
                self.conn = sqlite3.connect(DB_PATH)
            except Exception as e:
                print(f"Database connection error: {e}")
        return self.conn

    def init_db(self):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()

        # Create Profile Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profile (
                id INTEGER PRIMARY KEY DEFAULT 1,
                name TEXT DEFAULT 'Hero',
                avatar TEXT DEFAULT 'adventurer',
                level INTEGER DEFAULT 1,
                xp INTEGER DEFAULT 0,
                coins INTEGER DEFAULT 100,
                hp INTEGER DEFAULT 100,
                max_hp INTEGER DEFAULT 100,
                mana INTEGER DEFAULT 50,
                max_mana INTEGER DEFAULT 50,
                hair_color TEXT DEFAULT '(200, 50, 50)',
                outfit_color TEXT DEFAULT '(50, 80, 200)'
            )
        """)

        # Create Inventory Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                item_id TEXT PRIMARY KEY,
                item_type TEXT,
                quantity INTEGER DEFAULT 1,
                equipped INTEGER DEFAULT 0
            )
        """)

        # Create Kingdom Progress Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS progress (
                kingdom_id TEXT PRIMARY KEY,
                unlocked INTEGER DEFAULT 0,
                completed INTEGER DEFAULT 0,
                boss_defeated INTEGER DEFAULT 0,
                quests_done TEXT DEFAULT '[]'
            )
        """)

        # Create Achievements Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_id TEXT PRIMARY KEY,
                unlocked INTEGER DEFAULT 0,
                unlocked_at TEXT
            )
        """)

        # Create Learning Metrics Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY DEFAULT 1,
                total_study_time REAL DEFAULT 0.0,
                total_questions INTEGER DEFAULT 0,
                correct_questions INTEGER DEFAULT 0,
                monsters_defeated INTEGER DEFAULT 0,
                bosses_defeated INTEGER DEFAULT 0
            )
        """)

        # Create App Settings Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_settings (
                id INTEGER PRIMARY KEY DEFAULT 1,
                music_volume REAL DEFAULT 0.5,
                sfx_volume REAL DEFAULT 0.5,
                fullscreen INTEGER DEFAULT 0,
                keybindings TEXT DEFAULT ''
            )
        """)

        conn.commit()

        # Insert single-row defaults if they don't exist
        cursor.execute("SELECT COUNT(*) FROM profile")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO profile (id) VALUES (1)")
        
        cursor.execute("SELECT COUNT(*) FROM metrics")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO metrics (id) VALUES (1)")

        cursor.execute("SELECT COUNT(*) FROM game_settings")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO game_settings (id) VALUES (1)")

        conn.commit()

    def has_save(self):
        """Returns True if there is a customized/existing profile (e.g. level > 1 or non-default name or coins != 100)"""
        conn = self.get_connection()
        if not conn:
            return False
        cursor = conn.cursor()
        cursor.execute("SELECT name, level, coins FROM profile WHERE id = 1")
        row = cursor.fetchone()
        if row:
            name, level, coins = row
            if name != 'Hero' or level > 1 or coins != 100:
                return True
        return False

    def load_profile(self):
        conn = self.get_connection()
        if not conn:
            return {}
        cursor = conn.cursor()
        cursor.execute("SELECT name, avatar, level, xp, coins, hp, max_hp, mana, max_mana, hair_color, outfit_color FROM profile WHERE id = 1")
        row = cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "avatar": row[1],
                "level": row[2],
                "xp": row[3],
                "coins": row[4],
                "hp": row[5],
                "max_hp": row[6],
                "mana": row[7],
                "max_mana": row[8],
                "hair_color": eval(row[9]),
                "outfit_color": eval(row[10])
            }
        return {}

    def save_profile(self, p):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE profile SET 
                name = ?, avatar = ?, level = ?, xp = ?, coins = ?,
                hp = ?, max_hp = ?, mana = ?, max_mana = ?,
                hair_color = ?, outfit_color = ?
            WHERE id = 1
        """, (
            p["name"], p["avatar"], p["level"], p["xp"], p["coins"],
            p["hp"], p["max_hp"], p["mana"], p["max_mana"],
            str(p["hair_color"]), str(p["outfit_color"])
        ))
        conn.commit()

    def load_inventory(self):
        conn = self.get_connection()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT item_id, item_type, quantity, equipped FROM inventory")
        rows = cursor.fetchall()
        return [{"id": r[0], "type": r[1], "quantity": r[2], "equipped": bool(r[3])} for r in rows]

    def save_inventory(self, items):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory")
        for item in items:
            cursor.execute("""
                INSERT INTO inventory (item_id, item_type, quantity, equipped)
                VALUES (?, ?, ?, ?)
            """, (item["id"], item["type"], item["quantity"], 1 if item["equipped"] else 0))
        conn.commit()

    def load_progress(self):
        conn = self.get_connection()
        if not conn:
            return {}
        cursor = conn.cursor()
        cursor.execute("SELECT kingdom_id, unlocked, completed, boss_defeated, quests_done FROM progress")
        rows = cursor.fetchall()
        progress = {}
        for r in rows:
            progress[r[0]] = {
                "unlocked": bool(r[1]),
                "completed": bool(r[2]),
                "boss_defeated": bool(r[3]),
                "quests_done": json.loads(r[4])
            }
        return progress

    def save_progress(self, progress_dict):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        for k_id, data in progress_dict.items():
            cursor.execute("""
                INSERT OR REPLACE INTO progress (kingdom_id, unlocked, completed, boss_defeated, quests_done)
                VALUES (?, ?, ?, ?, ?)
            """, (
                k_id,
                1 if data["unlocked"] else 0,
                1 if data["completed"] else 0,
                1 if data["boss_defeated"] else 0,
                json.dumps(data["quests_done"])
            ))
        conn.commit()

    def load_achievements(self):
        conn = self.get_connection()
        if not conn:
            return {}
        cursor = conn.cursor()
        cursor.execute("SELECT achievement_id, unlocked, unlocked_at FROM achievements")
        rows = cursor.fetchall()
        return {r[0]: {"unlocked": bool(r[1]), "unlocked_at": r[2]} for r in rows}

    def save_achievements(self, achievements_dict):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        for ach_id, data in achievements_dict.items():
            cursor.execute("""
                INSERT OR REPLACE INTO achievements (achievement_id, unlocked, unlocked_at)
                VALUES (?, ?, ?)
            """, (ach_id, 1 if data["unlocked"] else 0, data["unlocked_at"]))
        conn.commit()

    def load_metrics(self):
        conn = self.get_connection()
        if not conn:
            return {}
        cursor = conn.cursor()
        cursor.execute("SELECT total_study_time, total_questions, correct_questions, monsters_defeated, bosses_defeated FROM metrics WHERE id = 1")
        row = cursor.fetchone()
        if row:
            return {
                "total_study_time": row[0],
                "total_questions": row[1],
                "correct_questions": row[2],
                "monsters_defeated": row[3],
                "bosses_defeated": row[4]
            }
        return {}

    def save_metrics(self, m):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE metrics SET 
                total_study_time = ?, total_questions = ?, 
                correct_questions = ?, monsters_defeated = ?, bosses_defeated = ?
            WHERE id = 1
        """, (
            m["total_study_time"], m["total_questions"],
            m["correct_questions"], m["monsters_defeated"], m["bosses_defeated"]
        ))
        conn.commit()

    def load_settings(self):
        conn = self.get_connection()
        if not conn:
            return {}
        cursor = conn.cursor()
        cursor.execute("SELECT music_volume, sfx_volume, fullscreen, keybindings FROM game_settings WHERE id = 1")
        row = cursor.fetchone()
        if row:
            return {
                "music_volume": row[0],
                "sfx_volume": row[1],
                "fullscreen": bool(row[2]),
                "keybindings": json.loads(row[3]) if row[3] else None
            }
        return {}

    def save_settings(self, s):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        keybindings_json = json.dumps(s["keybindings"]) if s.get("keybindings") else ""
        cursor.execute("""
            UPDATE game_settings SET 
                music_volume = ?, sfx_volume = ?, fullscreen = ?, keybindings = ?
            WHERE id = 1
        """, (s["music_volume"], s["sfx_volume"], 1 if s["fullscreen"] else 0, keybindings_json))
        conn.commit()

    def reset_save(self):
        conn = self.get_connection()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM profile")
        cursor.execute("DELETE FROM inventory")
        cursor.execute("DELETE FROM progress")
        cursor.execute("DELETE FROM achievements")
        cursor.execute("DELETE FROM metrics")
        
        cursor.execute("INSERT INTO profile (id) VALUES (1)")
        cursor.execute("INSERT INTO metrics (id) VALUES (1)")
        
        conn.commit()

    def close(self):
        if self.conn:
            try:
                self.conn.close()
            except:
                pass
            self.conn = None
