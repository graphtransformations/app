import pygame
import os
import sys 

pygame.init()

# Screen
WIDTH, HEIGHT = 1280, 720
SIDEBAR_WIDTH = 350

# Superscripts
SUPERSCRIPT_MAP = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³",
    "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷",
    "8": "⁸", "9": "⁹",
    "+": "⁺", "-": "⁻", "=": "⁼",
    "(": "⁽", ")": "⁾",
    "h": "ʰ", "i": "ⁱ", "j": "ʲ", "l": "ˡ",
    "n": "ⁿ", "r": "ʳ", "s": "ˢ",
    "w": "ʷ", "x": "ˣ", "y": "ʸ"
}

# Colours
COLOUR_INACTIVE = pygame.Color('black')
COLOUR_BUTTON = pygame.Color('gray60')
COLOUR_BOX = pygame.Color('black')
COLOUR_TEXT = pygame.Color('black')
COLOUR_FAIL = pygame.Color('red')

FUNCTION_COLOURS = [
    pygame.Color('red'), pygame.Color('orange'), pygame.Color('gold'),
    pygame.Color('green'), pygame.Color('deepskyblue'), pygame.Color('blue'),
    pygame.Color('purple'), pygame.Color('magenta'), pygame.Color('brown'),
    pygame.Color('teal'), pygame.Color('navy'), pygame.Color('darkgreen'),
]

COLOUR_AXIS = pygame.Color(50, 50, 50)
COLOUR_GRAPH_SEPARATOR = pygame.Color(200, 200, 200)
COLOUR_BACKGROUND = (255, 255, 255)
COLOUR_SIDEBAR = (230, 230, 230)

# Frame rate
FPS = 60

# Base dir
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Icon
icon_path = os.path.join(BASE_DIR, "assets", "icon.png")  
icon_surface = pygame.image.load(icon_path)
pygame.display.set_icon(icon_surface)
pygame.display.set_caption("Transformation Animator")

# Fonts
font_path = os.path.join(BASE_DIR, "assets", "STIXTwoText-Italic.otf")
MATHS_FONT = pygame.font.Font(font_path, 50)
GRAPH_AXIS_FONT = pygame.font.Font(font_path, 20)

UI_FONT = pygame.font.SysFont("Arial", 20)
UI_FONT_SMALL = pygame.font.SysFont("Arial", 15)
GRAPH_FONT = pygame.font.SysFont("Arial", 10)

# Load assets
def load_assets():
    arrow_path = os.path.join(BASE_DIR, "assets", "arrow.svg")
    arrow_img = pygame.image.load(arrow_path).convert_alpha()
    arrow_img = pygame.transform.scale(arrow_img, (20, 20))

    tick_path = os.path.join(BASE_DIR, "assets", "tick.svg")
    tick_img = pygame.image.load(tick_path).convert_alpha()
    tick_img = pygame.transform.scale(tick_img, (20, 20))

    return arrow_img, tick_img

# Ignore keys
IGNORE_KEYS = [
    pygame.K_RETURN, pygame.K_DELETE, pygame.K_ESCAPE, pygame.K_TAB,
    pygame.K_CAPSLOCK, pygame.K_NUMLOCK, pygame.K_SCROLLLOCK,
    pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_LCTRL, pygame.K_RCTRL,
    pygame.K_LALT, pygame.K_RALT, pygame.K_LGUI, pygame.K_RGUI,
    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
    pygame.K_PAGEUP, pygame.K_PAGEDOWN, pygame.K_HOME, pygame.K_END,
    pygame.K_INSERT,
    pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4, pygame.K_F5,
    pygame.K_F6, pygame.K_F7, pygame.K_F8, pygame.K_F9, pygame.K_F10,
    pygame.K_F11, pygame.K_F12,
]

# Graphing
LINE_THICKNESS = 3
GRAPH_SCALE = 40
