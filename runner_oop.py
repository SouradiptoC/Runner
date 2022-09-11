import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_surfs = [player_walk_1, player_walk_2]
        self.player_ind = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.6)

        self.image = self.player_surfs[self.player_ind]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_grav(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_ind += 0.1
            self.image = self.player_surfs[int(self.player_ind) % 2]

    def update(self) -> None:
        self.player_input()
        self.apply_grav()
        self.animation_state()


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, _type):
        super().__init__()
        if _type == 'fly':
            fly_1_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2_surf = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.surfs = [fly_1_surf, fly_2_surf]
            y_pos = 200
        else:
            snail_1_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2_surf = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.surfs = [snail_1_surf, snail_2_surf]
            y_pos = 300
        self.animation_ind = 0
        self.image = self.surfs[self.animation_ind]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_ind += 0.1
        self.image = self.surfs[int(self.animation_ind) % 2]

    def destroy(self):
        if self.rect.x < -50:
            self.kill()

    def update(self) -> None:
        self.animation_state()
        self.rect.x -= 6


def display_score():
    current_time = (pygame.time.get_ticks() // 1000) - start_time
    score_surf = score_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(topright=(800, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        obstacle.empty()
        return False
    return True


pygame.init()
game_active = False
start_time = 0
score = 0
bgm = pygame.mixer.Sound('audio/music.wav')
bgm.set_volume(0.4)
bgm.play(loops=-1)

# creating display surface
width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Runner')

# creating font
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
score_color = (64, 64, 64)
score_bg_color = '#c0e8ec'

# creating regular surface
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# obstacle surface
obstacle = pygame.sprite.Group()

# player surface
player = pygame.sprite.GroupSingle()
player.add(Player())

# Intro Screen
player_stand_surf = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(center=(400, 200))
game_name_surf = score_font.render('Runner', False, (111, 196, 169))
game_name_rect = game_name_surf.get_rect(center=(400, 80))
intro_msg_surf = score_font.render('Press SPACE to start', False, (111, 196, 169))
intro_msg_rect = intro_msg_surf.get_rect(center=(400, 330))

# Game Over
game_over_msg_surf = score_font.render('Press SPACE to replay', False, (111, 196, 169))
game_over_msg_rect = game_over_msg_surf.get_rect(center=(400, 370))

# timer
#   obstacle generation
obstacle_time = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_time, 1200)

# controlling fps
clock = pygame.time.Clock()

# event loop
while True:
    for event in pygame.event.get():
        # closing the game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            # generation of obstacles
            if event.type == obstacle_time:
                obstacle.add(Obstacles(choice(['fly', 'snail', 'fly', 'snail', 'snail'])))
        else:
            # restarting the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks() // 1000

    if game_active:
        # displaying the const surfaces
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        #     score surface
        score = display_score()

        # obstacle animation
        obstacle.draw(screen)
        obstacle.update()

        # player animation
        player.draw(screen)
        player.update()

        # collision
        game_active = collisions()
    else:
        # intro or finishing screen msgs
        screen.fill((94, 129, 162))
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(game_name_surf, game_name_rect)
        # score msg
        score_msg_surf = score_font.render(f'Your Score: {score}', False, (111, 196, 169))
        score_msg_rect = score_msg_surf.get_rect(center=(400, 330))
        if not score:
            screen.blit(intro_msg_surf, intro_msg_rect)
        else:
            screen.blit(score_msg_surf, score_msg_rect)
            screen.blit(game_over_msg_surf, game_over_msg_rect)

    pygame.display.update()
    clock.tick(60)  # creating celling
