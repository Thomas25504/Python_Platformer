# Configuration constants 

TILE_SIZE = 40
GRAVITY = 0.6
MOVE_SPEED = 5
JUMP_SPEED = 12

SCREEN_W = 1000
SCREEN_H = 700

# Color palette
COLOR_BG = (12, 16, 28)
COLOR_PANEL = (44, 68, 108)
COLOR_PANEL_DARK = (34, 52, 86)
COLOR_TEXT = (248, 252, 255)
COLOR_TEXT_MUTED = (214, 226, 240)
COLOR_TEXT_WARM = (255, 248, 224)
COLOR_HEADER = (224, 236, 252)
COLOR_SOLID = (190, 210, 236)
COLOR_KEY = (220, 237, 28)
COLOR_EXIT_UNLOCKED = (72, 255, 72)
COLOR_EXIT_LOCKED = (255, 72, 72)
COLOR_PLAYER = (126, 214, 255)
COLOR_UI_ACCENT = (24, 140, 153)
COLOR_PANEL_HOVER = (64, 92, 140)
COLOR_PANEL_DARK_HOVER = (54, 72, 116)

LEVEL_FILES = {
    1: "level1.txt",
    2: "level2.txt",
    3: "level3.txt",
    4: "level4.txt",
    5: "level5.txt",
    6: "level6.txt",
    7: "level7.txt",
    8: "level8.txt",
    9: "level9.txt",
    10: "level10.txt",
}

# Game States
STATE_MENU = "menu"
STATE_LEVEL_SELECT = "level_select"
STATE_PLAYING = "playing"
STATE_LEVEL_COMPLETE = "level_complete"