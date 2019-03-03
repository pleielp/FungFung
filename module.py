import sys
import pygame
from math import hypot, sqrt
from objects import Phoenix, WeakEnemy, StrongEnemy, FastEnemy, Bbongdda
from random import random
from constants import *

# pygame 초기화
pygame.mixer.pre_init(44100, -16, 2, 512)  # 사운드 미리 초기화
pygame.init()

screen = pygame.display.set_mode(DISPLAY_SIZE, DISPLAY_MODE)
pygame.display.set_caption('FungFung')

# 키보드 키 상수
QUIT = pygame.QUIT
K_ESCAPE = pygame.K_ESCAPE
K_F10 = pygame.K_F10
K_F11 = pygame.K_F11
K_SPACE = pygame.K_SPACE
KEYDOWN = pygame.KEYDOWN

# 이미지 로드
IMAGE_BACKGROUND = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_BG_IMAGE) if PATH_BG_IMAGE else None
# 사운드 로드
SOUND_EXPLOSION = pygame.mixer.Sound(RELATIVE_PATH_SOUNDS + PATH_EXPLOSION_SOUND) if PATH_EXPLOSION_SOUND else None
SOUND_EXPLOSION.set_volume(0.2) if SOUND_EXPLOSION else None
SOUND_GET_BBONGDDA = pygame.mixer.Sound(RELATIVE_PATH_SOUNDS + PATH_GET_BBONGDDA) if PATH_GET_BBONGDDA else None
# 음악 로드
pygame.mixer.music.load(RELATIVE_PATH_SOUNDS + PATH_BG_MUSIC) if PATH_BG_MUSIC else None
pygame.mixer.music.set_volume(0.1)


class Game(object):

    def __init__(self):
        self.state = 'Ready'

    def initialize_variables(self):
        self.state = 'Running'
        self.process = 0
        self.score = 0
        self.started = pygame.time.get_ticks()
        self.pause_start = 0
        self.pause_end = 0
        self.pause_time = 0
        self.clock = pygame.time.Clock()

        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.item_group = pygame.sprite.Group()

        PLAYER = [Phoenix][0]  # 플레이 케릭터 선택
        self.player = PLAYER(*DISPLAY_CENTER, FPS)

        self.w_enemy_freq = W_ENEMY_FREQ_INITIAL
        self.s_enemy_freq = S_ENEMY_FREQ_INITIAL
        self.f_enemy_freq = F_ENEMY_FREQ_INITIAL

        pygame.mixer.music.play(-1)

    def event(self):
        for event in pygame.event.get():
            e_type = event.type
            e_dict = event.dict
            # 게임 종료 버튼 or ESC
            if e_type == QUIT or (e_type == KEYDOWN and e_dict['key'] == K_ESCAPE):
                sys.exit()
            # F11 전체화면 토글
            if e_type == KEYDOWN and e_dict['key'] == K_F11:
                pygame.display.toggle_fullscreen()
            # F10 Stop 테스트(변수 초기화)
            if e_type == KEYDOWN and e_dict['key'] == K_F10:
                if self.state == 'Running':
                    self.state = 'Stop'
            # 스페이스 키
            if e_type == KEYDOWN and e_dict['key'] == K_SPACE:
                if self.state == 'Running':
                    pygame.mixer.music.pause()
                    self.pause_start = pygame.time.get_ticks()
                    self.state = 'Pause'
                elif self.state == 'Ready':
                    self.initialize_variables()
                elif self.state == 'Pause':
                    pygame.mixer.music.unpause()
                    self.pause_end = pygame.time.get_ticks()
                    self.state = 'Running'
                elif self.state == 'Stop':
                    pygame.mixer.music.stop()
                    self.initialize_variables()
            # 마우스 좌클릭
            if event.type == pygame.MOUSEBUTTONDOWN and e_dict['button'] == 1:
                if self.state == 'Running':
                    # player 회전
                    destination = e_dict['pos']
                    self.player.rotate(destination)
                    # 발사 및 Bullet 생성
                    self.bullet_group.add(self.player.fire_weapon(FPS, destination))
            # 마우스 우클릭
            if event.type == pygame.MOUSEBUTTONDOWN and e_dict['button'] == 3:
                if self.state == 'Running':
                    # 궁극기 사용
                    if self.player.ult_stack == self.player.ult_stack_max:
                        self.player.use_ult(self.enemy_group)
                        self.player.ult_stack = 0

    def input(self):
        if self.state == 'Running':
            self.player.key_move()

    def create_enemies(self):
        if len(self.enemy_group) <= W_ENEMY_LIMIT:
            if random() < self.w_enemy_freq:
                self.enemy_group.add(WeakEnemy.create(FPS, self.player.center))
        else:
            if random() < self.s_enemy_freq / 20:
                self.enemy_group.add(StrongEnemy.create(FPS, self.player.center))
        if random() < self.s_enemy_freq:
            self.enemy_group.add(StrongEnemy.create(FPS, self.player.center))
        if len(self.enemy_group) <= F_ENEMY_LIMIT:
            if random() < self.f_enemy_freq:
                self.enemy_group.add(FastEnemy.create(FPS, self.player.center))
        else:
            if random() < self.f_enemy_freq * 3:
                self.enemy_group.add(FastEnemy.create(FPS, self.player.center, 1))

    def move(self):
        self.player.move(FRICTION, GRAVITY)
        self.bullet_group.update('move')
        self.enemy_group.update('move', self.player.center)

    def check_collide(self):
        self.check_player_item()
        self.check_bullet_enemy()
        self.check_player_enemy()

    def check_state(self):
        self.bullet_state()
        self.enemy_state()
        self.player_state()
        self.item_state()

    def draw(self):
        screen.blit(IMAGE_BACKGROUND, (0, 0)) if IMAGE_BACKGROUND else screen.fill(COLOR_BLACK)
        self.player.draw(screen)
        self.bullet_group.update('draw', screen)
        self.enemy_group.update('draw', screen)
        self.item_group.update('draw', screen)

        self.show_ongame_info()
        self.show_debug_info() if DEBUG_MODE else None

        pygame.display.flip()

    def wellfare(self):
        if self.player.weapon_numbers <= self.score // 200:
            if self.player.weapon_numbers < self.player.weapon_number_max:
                self.player.weapon_numbers += 1

    def next_process(self):
        self.clock.tick(FPS)
        self.w_enemy_freq += W_ENEMY_FREQ_INCREASE
        self.s_enemy_freq += S_ENEMY_FREQ_INCREASE
        self.f_enemy_freq += F_ENEMY_FREQ_INCREASE
        if self.player.shield_stack + 1 < self.get_game_time() / 10:
            self.player.shield += 1
            self.player.shield_stack += 1

    def bullet_state(self):
        for bullet in self.bullet_group.sprites():
            if bullet.state == 'collided':
                self.bullet_group.remove(bullet)
            if bullet.state == 'to far':
                self.bullet_group.remove(bullet)

    def enemy_state(self):
        for enemy in self.enemy_group.sprites():
            if enemy.state == 'fired':
                pygame.mixer.Sound.play(SOUND_EXPLOSION)
                self.score += 1
                self.enemy_group.remove(enemy)
                if enemy.name == 'weak':
                    if random() < DROPRATE_BBONGDDA:
                        self.item_group.add(Bbongdda(*enemy.center))
                if enemy.name == 'strong':
                    droprate_buff = random()
                    if droprate_buff < INCREASE_PENETRATE:
                        if self.player.penetrate < self.player.penetrate_max:
                            self.player.penetrate += 1
                    elif droprate_buff > INCREASE_POWER:
                        if self.player.power < self.player.power_max:
                            self.player.power += 1
                if enemy.name == 'fast':
                    if self.player.ult_stack < self.player.ult_stack_max:
                        self.player.ult_stack += 1
            if enemy.state == 'collided':
                self.enemy_group.remove(enemy)

    def player_state(self):
        if self.player.state == 'dead':
            pygame.mixer.music.stop()
            print('SCORE: {}'.format(self.score), end='\n\n')
            self.state = 'Stop'
        elif self.player.state[:8] == 'collided':
            warning_collide = int(self.player.state[8:])
            if warning_collide:
                self.player.state = 'collided' + str(warning_collide - 1)
            else:
                self.player.state = 'live'

    def item_state(self):
        for item in self.item_group.sprites():
            if item.state == 'collided':
                pygame.mixer.Sound.play(SOUND_GET_BBONGDDA)
                self.item_group.remove(item)

    def check_player_item(self):
        for item in self.item_group.sprites():
            if self.collide_rect_circle(item.rect, self.player):
                if item.name == 'bbongdda':
                    if self.player.weapon_numbers < self.player.weapon_number_max:
                        self.player.weapon_numbers += 1
                    else:
                        self.player.shield += 1
                    item.state = 'collided'

    def check_bullet_enemy(self):
        for bullet in self.bullet_group.sprites():
            for enemy in self.enemy_group.sprites():
                if self.collide_rect_circle(enemy.rect, bullet):
                    if enemy.life > bullet.power:
                        if enemy.name == 'fast':
                            enemy.life -= 1
                        else:
                            enemy.life -= bullet.power
                        if enemy.name == 'strong' and enemy.life <= enemy.life_anger:
                            enemy.speed = enemy.speed_anger
                        bullet.state = 'collided'
                    else:
                        enemy.state = 'fired'
                        if enemy.name == 'weak' and bullet.penetrate > 2:
                            bullet.penetrate -= 1
                        else:
                            bullet.state = 'collided'

    def check_player_enemy(self):
        for enemy in self.enemy_group.sprites():
            if self.collide_rect_circle(enemy.rect, self.player):
                enemy.state = 'collided'
                if self.player.shield:
                    if enemy.name == 'strong':
                        self.player.shield = self.player.shield - enemy.power if self.player.shield > 3 else 0
                        self.player.state = 'collided40'
                    else:
                        self.player.shield -= enemy.power
                        if enemy.power > 0:
                            self.player.state = 'collided20'
                else:
                    if enemy.power > 0:
                        self.player.state = 'dead'

    def show_ready_scene(self):
        font = pygame.font.Font(RELATIVE_PATH_FONTS + FONT_FILE, FONT_SIZE_READY)

        # 준비대사1
        FontSurface = font.render('PRESS SPACE!', ANTIALIAS, COLOR_BLUE)
        lefttop_FontSurface = (DISPLAY_CENTER[0] - FontSurface.get_size()[0] / 2, DISPLAY_CENTER[1] - FontSurface.get_size()[1])
        screen.blit(FontSurface, lefttop_FontSurface)
        # 준비대사2
        FontSurface = font.render('to start game', ANTIALIAS, COLOR_WHITE)
        lefttop_FontSurface = (DISPLAY_CENTER[0] - FontSurface.get_size()[0] / 2, DISPLAY_CENTER[1])
        screen.blit(FontSurface, lefttop_FontSurface)

        pygame.display.flip()

    def show_pause_scene(self):
        # 일시정지
        rect1 = pygame.Rect(DISPLAY_CENTER[0] - WIDTH_PAUSE * 3, DISPLAY_CENTER[1] - HEIGHT_PAUSE, WIDTH_PAUSE * 2, HEIGHT_PAUSE * 2)
        rect2 = pygame.Rect(DISPLAY_CENTER[0] + WIDTH_PAUSE * 1, DISPLAY_CENTER[1] - HEIGHT_PAUSE, WIDTH_PAUSE * 2, HEIGHT_PAUSE * 2)
        pygame.draw.rect(screen, COLOR_BLUE, rect1, 0)
        pygame.draw.rect(screen, COLOR_BLUE, rect2, 0)
        # 박스
        rect = pygame.Rect(DISPLAY_CENTER[0] - SIDE_BOX_PAUSE, DISPLAY_CENTER[1] - SIDE_BOX_PAUSE, 2 * SIDE_BOX_PAUSE, 2 * SIDE_BOX_PAUSE)
        pygame.draw.rect(screen, COLOR_BLUE, rect, 2)

        pygame.display.flip()

    def show_stop_scene(self):
        font1 = pygame.font.Font(RELATIVE_PATH_FONTS + FONT_FILE, FONT_SIZE_STOP1)
        font2 = pygame.font.Font(RELATIVE_PATH_FONTS + FONT_FILE, FONT_SIZE_STOP2)

        # 점수
        FontSurface = font1.render('SCORE: {}'.format(self.score), ANTIALIAS, COLOR_BLUE)
        lefttop_FontSurface = (DISPLAY_CENTER[0] - FontSurface.get_size()[0] / 2, DISPLAY_CENTER[1] - FontSurface.get_size()[1])
        screen.blit(FontSurface, lefttop_FontSurface)
        # 엔딩대사1
        FontSurface = font2.render('press space', ANTIALIAS, COLOR_WHITE)
        lefttop_FontSurface = (DISPLAY_CENTER[0] - FontSurface.get_size()[0] / 2, DISPLAY_CENTER[1])
        screen.blit(FontSurface, lefttop_FontSurface)
        # 엔딩대사2
        FontSurface = font2.render('to regame', ANTIALIAS, COLOR_WHITE)
        lefttop_FontSurface = (DISPLAY_CENTER[0] - FontSurface.get_size()[0] / 2, DISPLAY_CENTER[1] + FontSurface.get_size()[1])
        screen.blit(FontSurface, lefttop_FontSurface)

        pygame.display.flip()

    def show_ongame_info(self):
        font = pygame.font.Font(RELATIVE_PATH_FONTS + FONT_FILE, FONT_SIZE_ONGAME)

        # 시간
        string = '{:4s}: {:.2f}s'.format('TIME', self.get_game_time())
        FontSurface = font.render(string, ANTIALIAS, COLOR_WHITE)
        screen.blit(FontSurface, (MARGIN_ONGAME, MARGIN_ONGAME))
        # 점수
        string = '{:5s}: {}'.format('SCORE', self.score)
        FontSurface = font.render(string, ANTIALIAS, COLOR_WHITE)
        screen.blit(FontSurface, (DISPLAY_SIZE[0] - FontSurface.get_size()[0] - MARGIN_ONGAME, MARGIN_ONGAME))

    def show_debug_info(self):
        font = pygame.font.Font(RELATIVE_PATH_FONTS + 'Ubuntu-R.ttf', FONT_SIZE_DEBUG)
        offset_debug_info = 1
        DEBUG_INFO_LIST = [('FPS', self.clock.get_fps()),
                           ('w_enemy_freq', self.w_enemy_freq),
                           ('s_enemy_freq', self.s_enemy_freq),
                           ('f_enemy_freq', self.f_enemy_freq),
                           ('Player', self.player),
                           ('bullet_group', self.bullet_group),
                           ('enemy_group', self.enemy_group),
                           ('item_group', self.item_group)]

        for debug_info in DEBUG_INFO_LIST:
            if isinstance(debug_info[1], float):
                string = '{:15}: {:.2f}'.format(*debug_info)
            elif isinstance(debug_info[1], pygame.sprite.Group):
                string = '{:15}: {}'.format(debug_info[0], len(debug_info[1].sprites()))
            else:
                string = '{:15}: {}'.format(*debug_info)
            FontSurface = font.render(string, ANTIALIAS, COLOR_WHITE)
            screen.blit(FontSurface, (MARGIN_DEBUG, DISPLAY_SIZE[1] - FONT_SIZE_DEBUG * offset_debug_info - MARGIN_DEBUG))
            offset_debug_info += 1

    def get_game_time(self):
        if self.pause_end > 0:
            self.pause_time += self.pause_end - self.pause_start
            self.pause_start, self.pause_end = 0, 0

        return (pygame.time.get_ticks() - self.started - self.pause_time) / 1000

    def collide_rect_circle(self, rect, circle, shield=0):
        s = circle.shield * 2 if hasattr(circle, 'shield') else 0

        rleft, rright, rtop, rbottom = rect.left, rect.right, rect.top, rect.bottom
        cleft, cright, ctop, cbottom = circle.left - s, circle.right + s, circle.top - s, circle.bottom + s
        radius, center_x, center_y = circle.radius + s, *circle.center

        if rleft > cright or rright < cleft or rtop > cbottom or rbottom < ctop:
            return False

        for x in (rleft, rright):
            for y in (rtop, rbottom):
                if hypot(x - center_x, y - center_y) <= radius:
                    return True

        if rleft <= center_x <= rright or rtop <= center_y <= rbottom:
            return True

        return False
