COLORS: dict = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (180, 0, 0),
    "rose": (230, 105, 180),
    "missed": (255, 0, 255),
    "gray": (200, 200, 200),
    "blue": (83,141,180),
}

STATUSES: dict = {
    "0":"idle",
    "1":"animation",
    "2":"hold",
    "3":"in_progress",
    "4":"killed",
}


TEXT_OFFSET = 6
WINSIZE = [480, 320]

TEMPLATE_MASS = 10.
TEMPLATE_SIZE = 56
TEMPLATE_STR = "non-init-value"
TEMPLATE_FOV = 20000.
TEMPLATE_COL = COLORS["rose"]
TEMPLATE_SPEED = 5.
TEMPLATE_DRAG = 0.9
TEMPLATE_HUNG = 400

OVERLAP_DIST = 5
OVERLAP_SAFE_DIST = 5

CONST_G = 6.7
FPS = 60

RANDOM_RANGE = 100

FONT = "Consolas"
FONT_SIZE = 16