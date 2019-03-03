# 게임 기본 상수
FPS = 60
DISPLAY_SIZE = 1920, 1080
DISPLAY_CENTER = DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2
DISPLAY_MODE = -2147483648  # 풀스크린
DEBUG_MODE = 0

# 물리 상수
FRICTION = 3 / FPS
GRAVITY = 6 / FPS

# 적 출현빈도
W_ENEMY_FREQ_INITIAL = 0.5 / FPS                  # 적 출현빈도 초기값
W_ENEMY_FREQ_INCREASE = 0.1 / FPS ** 2      # 적 출현빈도 증가량
S_ENEMY_FREQ_INITIAL = -2.0 / FPS                  # 적 출현빈도 초기값
S_ENEMY_FREQ_INCREASE = 0.02 / FPS ** 2      # 적 출현빈도 증가량
F_ENEMY_FREQ_INITIAL = 0.1 / FPS                  # 적 출현빈도 초기값
F_ENEMY_FREQ_INCREASE = 0.001 / FPS ** 2      # 적 출현빈도 증가량
W_ENEMY_LIMIT = 65
F_ENEMY_LIMIT = 66

# 아이템 및 버프 드랍율
DROPRATE_BBONGDDA = 0.01
INCREASE_PENETRATE = 0.1
INCREASE_POWER = 1 - 0.02

# 색깔 상수
COLOR_BLACK = 0, 0, 0
COLOR_RED = 255, 0, 0
COLOR_ORANGE = 255, 127, 0
COLOR_YELLOW = 255, 255, 0
COLOR_GREEN = 0, 255, 0
COLOR_DARK_GREEN = 0, 127, 0
COLOR_SKY_BLUE = 0, 255, 255
COLOR_LIGHT_BLUE = 0, 127, 255
COLOR_BLUE = 0, 0, 255
COLOR_PURPLE = 255, 0, 255
COLOR_WHITE = 255, 255, 255
# 안티앨리어스
ANTIALIAS = False

# 외부파일 경로설정
RELATIVE_PATH_IMAGES = "images/"
RELATIVE_PATH_SOUNDS = "sounds/"
RELATIVE_PATH_FONTS = "fonts/"

# 사진 파일
PATH_BG_IMAGE = ""
PATH_PLAYER_PHOENIX = "player_phoenix.gif"
PATH_PHOENIX_STACK_P1 = "phoenix_stack_p1.gif"
PATH_PHOENIX_STACK_P2 = "phoenix_stack_p2.gif"
PATH_PHOENIX_STACK_P3 = "phoenix_stack_p3.gif"
PATH_PHOENIX_STACK_P4 = "phoenix_stack_p4.gif"
PATH_PHOENIX_STACK_P5 = "phoenix_stack_p5.gif"
PATH_BULLET_PHOENIX_P1 = "bullet_phoenix_p1.gif"
PATH_BULLET_PHOENIX_P2 = "bullet_phoenix_p2.gif"
PATH_BULLET_PHOENIX_P3 = "bullet_phoenix_p3.gif"
PATH_BULLET_PHOENIX_P4 = "bullet_phoenix_p4.gif"
PATH_BULLET_PHOENIX_P5 = "bullet_phoenix_p5.gif"
PATH_ENEMY_W = ""
PATH_ENEMY_S = ""
PATH_ENEMY_F = ""
PATH_ITEM_BBONGDDA = ""

# 사운드 파일
PATH_PHOENIX_ATTACK = "phoenix_attack.ogg"
PATH_EXPLOSION_SOUND = "explosion.ogg"
PATH_GET_BBONGDDA = "get_bbongdda.ogg"
PATH_BG_MUSIC = "bg_music.ogg"
# 폰트 파일
FONT_FILE = 'Ubuntu-R.ttf'

# 준비 상태 상수
FONT_SIZE_READY = 100
FONT_SIZE_STOP1 = 100
FONT_SIZE_STOP2 = 50

# 온게임 정보 상수
FONT_SIZE_ONGAME = 33
MARGIN_ONGAME = 13

# 일시정지 상태 상수
WIDTH_PAUSE = 15
HEIGHT_PAUSE = 45
PADDING_PAUSE = 30
SIDE_BOX_PAUSE = HEIGHT_PAUSE + PADDING_PAUSE

# 디버그 모드 상수
FONT_SIZE_DEBUG = 20
MARGIN_DEBUG = 10
