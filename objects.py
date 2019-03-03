import pygame
import math
from random import random, randint
from constants import *

pygame.mixer.init(44100, -16, 2, 512)

# 이미지 로드
IMAGE_PLAYER_PHOENIX = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_PLAYER_PHOENIX) if PATH_PLAYER_PHOENIX else None
IMAGE_PHOENIX_SATCK_P1 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_PHOENIX_STACK_P1) if PATH_PHOENIX_STACK_P1 else None
IMAGE_PHOENIX_SATCK_P2 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_PHOENIX_STACK_P2) if PATH_PHOENIX_STACK_P2 else None
IMAGE_PHOENIX_SATCK_P3 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_PHOENIX_STACK_P3) if PATH_PHOENIX_STACK_P3 else None
IMAGE_PHOENIX_SATCK_P4 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_PHOENIX_STACK_P4) if PATH_PHOENIX_STACK_P4 else None
IMAGE_PHOENIX_SATCK_P5 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_PHOENIX_STACK_P5) if PATH_PHOENIX_STACK_P5 else None
IMAGE_BULLET_PHOENIX_P1 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_BULLET_PHOENIX_P1) if PATH_BULLET_PHOENIX_P1 else None
IMAGE_BULLET_PHOENIX_P2 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_BULLET_PHOENIX_P2) if PATH_BULLET_PHOENIX_P2 else None
IMAGE_BULLET_PHOENIX_P3 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_BULLET_PHOENIX_P3) if PATH_BULLET_PHOENIX_P3 else None
IMAGE_BULLET_PHOENIX_P4 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_BULLET_PHOENIX_P4) if PATH_BULLET_PHOENIX_P4 else None
IMAGE_BULLET_PHOENIX_P5 = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_BULLET_PHOENIX_P5) if PATH_BULLET_PHOENIX_P5 else None
IMAGE_ENEMY_W = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_ENEMY_W) if PATH_ENEMY_W else None
IMAGE_ENEMY_S = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_ENEMY_S) if PATH_ENEMY_S else None
IMAGE_ENEMY_F = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_ENEMY_F) if PATH_ENEMY_F else None
IMAGE_ITEM_BBONGDDA = pygame.image.load(RELATIVE_PATH_IMAGES + PATH_ITEM_BBONGDDA) if PATH_ITEM_BBONGDDA else None
# 사운드 로드
SOUND_PHOENIX_ATTACK = pygame.mixer.Sound(RELATIVE_PATH_SOUNDS + PATH_PHOENIX_ATTACK) if PATH_PHOENIX_ATTACK else None
SOUND_PHOENIX_ATTACK.set_volume(0.1) if SOUND_PHOENIX_ATTACK else None


class Player(pygame.sprite.Sprite):
    color = COLOR_DARK_GREEN
    color_shield = COLOR_LIGHT_BLUE
    color_stack = COLOR_GREEN
    color_warning1 = COLOR_ORANGE
    color_warning2 = COLOR_RED

    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        self.center = [center_x, center_y]
        if self.image:
            self.width = self.image.get_size()[0]
            self.height = self.image.get_size()[1]
            self.image_rotate = self.image
            self.image_width = self.image.get_size()[0]
            self.image_height = self.image.get_size()[1]
        self.synchronize_position()
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.weapon_numbers = 1
        self.weapon_number_max = 8
        self.power = 1
        self.power_max = 5
        self.penetrate = 1
        self.penetrate_max = 5
        self.ult_stack = 0
        self.ult_stack_max = 10
        self.shield = 3
        self.shield_stack = 0
        self.state = 'live'

    def synchronize_position(self):
        self.left = self.center[0] - self.radius
        self.right = self.center[0] + self.radius
        self.top = self.center[1] - self.radius
        self.bottom = self.center[1] + self.radius
        if self.image:
            self.image_left = self.center[0] - self.image_width / 2
            self.image_top = self.center[1] - self.image_height / 2
            self.image_rect = pygame.Rect(self.image_left, self.image_top, self.image_width, self.image_height)

    def move(self, FRICTION, GRAVITY):
        self.calc_friction(FRICTION)
        self.calc_gravity(GRAVITY)
        self.crashed_wall()

        self.center[0] += self.velocity[0]
        self.center[1] += self.velocity[1]
        self.synchronize_position()

    def rotate(self, destination):
        x_diff = self.center[0] - destination[0]
        y_diff = self.center[1] - destination[1]
        arctan = math.atan2(x_diff, y_diff)
        self.angle = arctan if arctan > 0 else arctan + 2 * math.pi

        if self.image:
            angle_degree = self.angle * 180 / math.pi
            self.image_width = (self.width * abs(math.cos(self.angle)) + self.height * abs(math.sin(self.angle)))
            self.image_height = (self.width * abs(math.sin(self.angle)) + self.height * abs(math.cos(self.angle)))
            self.image_rotate = pygame.transform.rotate(self.image, angle_degree)

    def key_move(self):
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
            self.acceleration[0] -= 1
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.acceleration[0] += 1
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
            self.acceleration[1] -= 1
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            self.acceleration[1] += 1

        if self.acceleration[0] == 0 and self.acceleration[1] == 0:
            pass
        else:
            self.velocity[0] += self.speed * self.acceleration[0] / math.hypot(*self.acceleration)
            self.velocity[1] += self.speed * self.acceleration[1] / math.hypot(*self.acceleration)

        self.acceleration = [0, 0]

    def calc_gravity(self, GRAVITY):
        self.velocity[1] += GRAVITY

    def calc_friction(self, FRICTION):
        v_diagonal = math.hypot(self.velocity[0], self.velocity[1])
        if v_diagonal > FRICTION:
            self.velocity[0] = self.velocity[0] * (1 - FRICTION / v_diagonal)
            self.velocity[1] = self.velocity[1] * (1 - FRICTION / v_diagonal)
        elif v_diagonal <= FRICTION:
            self.velocity = [0, 0]

    def crashed_wall(self):
        if self.left < 0:
            self.center[0] = self.radius
            self.synchronize_position()
            self.velocity[0] = 0 if self.velocity[0] < 0 else self.velocity[0]
        elif self.right > DISPLAY_SIZE[0]:
            self.center[0] = DISPLAY_SIZE[0] - self.radius
            self.synchronize_position()
            self.velocity[0] = 0 if self.velocity[0] > 0 else self.velocity[0]
        elif self.top < 0:
            self.center[1] = self.radius
            self.synchronize_position()
            self.velocity[1] = 0 if self.velocity[1] < 0 else self.velocity[1]
        elif self.bottom > DISPLAY_SIZE[1]:
            self.center[1] = DISPLAY_SIZE[1] - self.radius
            self.synchronize_position()
            self.velocity[1] = 0 if self.velocity[1] > 0 else self.velocity[1]

    def draw(self, screen):
        center_int = int(self.center[0]), int(self.center[1])
        radius_int = int(self.radius)
        left_int, right_int = int(self.left), int(self.top)
        width_int, height_int = int(self.radius) * 2, int(self.radius) * 2
        rect = pygame.Rect(left_int, right_int, width_int, height_int)
        angle_start = math.pi / 2
        angle_end = math.pi / 2 + math.pi * 2 * self.ult_stack / self.ult_stack_max

        if self.state == 'live':
            pygame.draw.circle(screen, self.color, center_int, radius_int, 2)
        elif self.state[:8] == 'collided':
            if int(self.state[8:]) <= 20:
                pygame.draw.circle(screen, self.color_warning1, center_int, radius_int, 2)
            elif int(self.state[8:]) <= 40:
                pygame.draw.circle(screen, self.color_warning2, center_int, radius_int, 2)
        elif self.state == 'dead':
            pygame.draw.circle(screen, self.color_warning2, center_int, radius_int, 2)

        # 쉴드
        for shield in range(self.shield):
            pygame.draw.circle(screen, self.color_shield, center_int, radius_int + 2 * (shield + 1), 1)
        # 궁극기 스택
        pygame.draw.arc(screen, self.color_stack, rect, angle_start, angle_end, 2)
        # 파워관통 스택
        image_power = eval('self.image_stack_p' + str(self.power))
        image_penetrate = eval('self.image_stack_p' + str(self.penetrate))
        if image_power:
            screen.blit(image_power, (self.center[0] - self.radius - image_power.get_size()[0], self.center[1] - image_power.get_size()[1] / 2))
        if image_penetrate:
            screen.blit(image_penetrate, (self.center[0] + self.radius, self.center[1] - image_penetrate.get_size()[1] / 2))

        # 이미지
        if self.image:
            screen.blit(self.image_rotate, self.image_rect)


class Phoenix(Player):
    radius = 40
    name = 'Phoenix'
    image = IMAGE_PLAYER_PHOENIX
    image_stack_p1 = IMAGE_PHOENIX_SATCK_P1
    image_stack_p2 = IMAGE_PHOENIX_SATCK_P2
    image_stack_p3 = IMAGE_PHOENIX_SATCK_P3
    image_stack_p4 = IMAGE_PHOENIX_SATCK_P4
    image_stack_p5 = IMAGE_PHOENIX_SATCK_P5
    image_bullet_p1 = IMAGE_BULLET_PHOENIX_P1
    image_bullet_p2 = IMAGE_BULLET_PHOENIX_P2
    image_bullet_p3 = IMAGE_BULLET_PHOENIX_P3
    image_bullet_p4 = IMAGE_BULLET_PHOENIX_P4
    image_bullet_p5 = IMAGE_BULLET_PHOENIX_P5
    sound = SOUND_PHOENIX_ATTACK

    def __init__(self, center_x, center_y, FPS):
        super(Phoenix, self).__init__(center_x, center_y)
        self.speed = 18 / FPS
        self.weapon = IonCannon

    def fire_weapon(self, FPS, destination):
        weapon_center = [0, 0]
        bullets = []
        for i in range(1, self.weapon_numbers + 1):
            weapon_center[0] = self.center[0] + math.cos(self.angle) * (-57 + 114 * i / (self.weapon_numbers + 1))
            weapon_center[1] = self.center[1] + math.sin(self.angle) * (57 - 114 * i / (self.weapon_numbers + 1))
            bullets.append(self.weapon(*weapon_center, FPS, self.angle, self.power, self.penetrate))
        if self.sound:
            pygame.mixer.Sound.play(self.sound)

        return bullets

    def use_ult(self, enemy_group):
        enemy_group.empty()

    def __str__(self):
        return "shield {} power {} penetrate {}".format(self.shield, self.power, self.penetrate)


class Weapon(pygame.sprite.Sprite):
    color = COLOR_SKY_BLUE

    def __init__(self, center_x, center_y, angle, power, penetrate):
        pygame.sprite.Sprite.__init__(self)
        self.center = [center_x, center_y]
        if self.image:
            self.image_width = self.image.get_size()[0]
            self.image_height = self.image.get_size()[1]
        self.synchronize_position()
        self.angle = angle
        self.velocity = [0, 0]
        self.velocity[0] = -self.speed * math.sin(self.angle)
        self.velocity[1] = -self.speed * math.cos(self.angle)
        self.power = power
        self.penetrate = penetrate
        self.state = 'live'

    def synchronize_position(self):
        self.left = self.center[0] - self.radius
        self.right = self.center[0] + self.radius
        self.top = self.center[1] - self.radius
        self.bottom = self.center[1] + self.radius
        if self.image:
            self.image_left = self.center[0] - self.image_width / 2
            self.image_top = self.center[1] - self.image_height / 2
            self.image_rect = pygame.Rect(self.image_left, self.image_top, self.image_width, self.image_height)

    def move(self):
        self.center[0] += self.velocity[0]
        self.center[1] += self.velocity[1]
        self.synchronize_position()

        if self.left < 0 or self.top < 0 or self.right > DISPLAY_SIZE[0] or self.bottom > DISPLAY_SIZE[1]:
            self.state = 'to far'

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.image_rect)
        else:
            center_int = int(self.center[0]), int(self.center[1])
            radius_int = int(self.radius)
            pygame.draw.circle(screen, self.color, center_int, radius_int, 2)

    def update(self, *args):
        if args[0] == 'move':
            self.move(*args[1:])
        elif args[0] == 'draw':
            self.draw(*args[1:])


class IonCannon(Weapon):
    radius = 5

    def __init__(self, center_x, center_y, FPS, angle, power, penetrate):
        self.speed = 900 / FPS
        self.image = eval('IMAGE_BULLET_PHOENIX_P' + str(min(power, penetrate)))
        if self.image:
            self.image = pygame.transform.rotate(self.image, angle * 180 / math.pi)
        super(IonCannon, self).__init__(center_x, center_y, angle, power, penetrate)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, destination):
        pygame.sprite.Sprite.__init__(self)
        self.center = [center_x, center_y]
        self.synchronize_position()
        self.destination = destination
        self.direction = self.get_direction(self.destination)
        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]
        self.state = 'live'

    @classmethod
    def create(cls, FPS, destination, power=0):
        location = {
            1: ((DISPLAY_SIZE[0] - cls.size[0]) * random(), -cls.size[1]),
            2: (-cls.size[0], (DISPLAY_SIZE[1] - cls.size[1]) * random()),
            3: ((DISPLAY_SIZE[0] - cls.size[0]) * random(), DISPLAY_SIZE[1]),
            4: (DISPLAY_SIZE[0], (DISPLAY_SIZE[1] - cls.size[0]) * random()),
        }

        if cls.name == 'fast' and power == 1:
            return cls(FPS, *location[randint(1, 4)], destination, 1)
        else:
            return cls(FPS, *location[randint(1, 4)], destination)

    def get_direction(self, destination):
        x_diff = destination[0] - self.center[0]
        y_diff = destination[1] - self.center[1]
        p_diff = math.hypot(x_diff, y_diff)
        return x_diff / p_diff, y_diff / p_diff

    def move(self, center_player):
        self.direction = self.get_direction(center_player)
        self.velocity = [self.speed * self.direction[0], self.speed * self.direction[1]]

        self.center[0] += self.velocity[0]
        self.center[1] += self.velocity[1]
        self.synchronize_position()

    def synchronize_position(self):
        self.left = self.center[0] - self.width / 2
        self.right = self.center[0] + self.width / 2
        self.top = self.center[1] - self.height / 2
        self.bottom = self.center[1] + self.height / 2
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self, *args):
        if args[0] == 'move':
            self.move(*args[1:])
        elif args[0] == 'draw':
            self.draw(*args[1:])


class WeakEnemy(Enemy):
    image = IMAGE_ENEMY_W
    size = width, height = 50, 50
    name = 'weak'
    color = COLOR_YELLOW

    def __init__(self, FPS, center_x, center_y, destination, power=1):
        self.speed = 180 / FPS
        super(WeakEnemy, self).__init__(center_x, center_y, destination)
        self.life = 1
        self.power = power


class StrongEnemy(Enemy):
    image = IMAGE_ENEMY_S
    size = width, height = 50, 50
    name = 'strong'
    color = COLOR_RED

    def __init__(self, FPS, center_x, center_y, destination, power=3):
        self.speed = 60 / FPS
        self.speed_anger = 60 / FPS * 2
        super(StrongEnemy, self).__init__(center_x, center_y, destination)
        self.life = 25
        self.life_anger = 10
        self.power = power


class FastEnemy(Enemy):
    image = IMAGE_ENEMY_F
    size = width, height = 50, 50
    name = 'fast'
    color = COLOR_ORANGE

    def __init__(self, FPS, center_x, center_y, destination, power=0):
        self.speed = 1080 / FPS
        super(FastEnemy, self).__init__(center_x, center_y, destination)
        self.life = 10
        self.power = power
        if power:
            self.color = COLOR_PURPLE
            self.power = power


class Item(pygame.sprite.Sprite):
    color = COLOR_BLUE

    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        self.center = [center_x, center_y]
        self.synchronize_position()
        self.state = 'live'

    def move(self):
        self.synchronize_position()

    def synchronize_position(self):
        self.left = self.center[0] - self.width / 2
        self.right = self.center[0] + self.width / 2
        self.top = self. center[1] - self.height / 2
        self.bottom = self.center[1] + self.height / 2
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def update(self, *args):
        if args[0] == 'draw':
            self.draw(*args[1:])


class Bbongdda(Item):
    image = IMAGE_ITEM_BBONGDDA
    size = width, height = 40, 40
    name = 'bbongdda'

    def __init__(self, center_x, center_y):
        super(Bbongdda, self).__init__(center_x, center_y)
