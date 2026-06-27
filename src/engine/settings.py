import pygame

# Screen Configurations
VIRTUAL_WIDTH = 1280
VIRTUAL_HEIGHT = 720
TARGET_FPS = 60
GAME_TITLE = "LearnScape"

# Database & Save Config
DB_PATH = "data/saves/save_game.db"
QUESTIONS_DIR = "data/questions"

# Themes and Colors
COLOR_BLACK = (10, 10, 15)
COLOR_WHITE = (245, 245, 250)
COLOR_GOLD = (230, 185, 55)
COLOR_GOLD_DARK = (165, 120, 25)
COLOR_GOLD_GLOW = (255, 215, 0)
COLOR_GRAY = (100, 100, 110)
COLOR_GRAY_DARK = (40, 40, 45)
COLOR_RED = (210, 50, 50)
COLOR_GREEN = (50, 200, 80)
COLOR_BLUE = (40, 120, 230)
COLOR_MANA = (40, 180, 240)
COLOR_XP = (180, 70, 230)

# Colors for Dialogues and Custom UI Borders
UI_BG_COLOR = (24, 24, 32)
UI_BORDER_COLOR = (60, 50, 40)
UI_BORDER_GLOW = (230, 185, 55)

# Subject Theme Styling
SUBJECT_THEMES = {
    "mathematics": {
        "color_primary": (30, 80, 200),
        "color_accent": (70, 150, 255),
        "bg_color": (15, 30, 60),
        "title": "Mathematics Kingdom",
        "desc": "Solve math formulas, equations, and logic puzzles.",
        "icon": "plus_minus"
    },
    "science": {
        "color_primary": (0, 150, 160),
        "color_accent": (50, 220, 200),
        "bg_color": (10, 45, 45),
        "title": "Science Kingdom",
        "desc": "Explore general science concepts and theories.",
        "icon": "flask"
    },
    "biology": {
        "color_primary": (30, 140, 60),
        "color_accent": (80, 220, 110),
        "bg_color": (10, 45, 20),
        "title": "Biology Forest",
        "desc": "Learn about ecosystems, anatomy, and plant biology.",
        "icon": "leaf"
    },
    "chemistry": {
        "color_primary": (210, 70, 20),
        "color_accent": (255, 140, 40),
        "bg_color": (50, 20, 10),
        "title": "Chemistry Volcano",
        "desc": "Master elements, chemical equations, and reactions.",
        "icon": "beaker"
    },
    "physics": {
        "color_primary": (130, 30, 180),
        "color_accent": (200, 80, 255),
        "bg_color": (30, 10, 45),
        "title": "Physics Laboratory",
        "desc": "Calculate forces, motion, energy, and electromagnetism.",
        "icon": "atom"
    },
    "english": {
        "color_primary": (180, 140, 20),
        "color_accent": (240, 210, 80),
        "bg_color": (40, 35, 15),
        "title": "English Castle",
        "desc": "Conquer grammar, spelling, vocabulary, and literature.",
        "icon": "book"
    },
    "history": {
        "color_primary": (150, 90, 40),
        "color_accent": (210, 150, 90),
        "bg_color": (35, 25, 15),
        "title": "History Museum",
        "desc": "Travel back to ancient civilizations and historic events.",
        "icon": "pillar"
    },
    "geography": {
        "color_primary": (20, 150, 180),
        "color_accent": (80, 220, 240),
        "bg_color": (15, 40, 50),
        "title": "Geography Island",
        "desc": "Chart continents, oceans, landmarks, and world maps.",
        "icon": "globe"
    },
    "computer_science": {
        "color_primary": (10, 180, 90),
        "color_accent": (30, 240, 160),
        "bg_color": (10, 40, 25),
        "title": "Computer Science City",
        "desc": "Decode programming, algorithms, networks, and binary logic.",
        "icon": "terminal"
    }
}

# Keyboard Bindings (Pygame Key Constants)
KEYS = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "interact": pygame.K_e,
    "inventory": pygame.K_i,
    "pause": pygame.K_ESCAPE,
    "run": pygame.K_LSHIFT,
}

# Human readable names for keyboard remapping
KEY_NAMES = {
    pygame.K_w: "W",
    pygame.K_s: "S",
    pygame.K_a: "A",
    pygame.K_d: "D",
    pygame.K_e: "E",
    pygame.K_i: "I",
    pygame.K_ESCAPE: "ESC",
    pygame.K_LSHIFT: "LSHIFT",
    pygame.K_UP: "UP ARROW",
    pygame.K_DOWN: "DOWN ARROW",
    pygame.K_LEFT: "LEFT ARROW",
    pygame.K_RIGHT: "RIGHT ARROW",
    pygame.K_SPACE: "SPACE",
    pygame.K_RETURN: "ENTER",
}
