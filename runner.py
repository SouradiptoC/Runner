import pygame
from sys import exit
from random import randint


def display_score():
    current_time = (pygame.time.get_ticks() // 1000) - start_time
    score_surf = score_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(topright=(800, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_animation(obstacle_lst: list):
    if obstacle_lst:
        for obstacle_rect in obstacle_lst:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_lst = [obstacle for obstacle in obstacle_lst if obstacle.x > -50]
        return obstacle_lst
    else:
        return []


def player_animation():
    global player_ind, player_surf
    if player_rect.bottom < 300:
        # jump
        player_surf = player_jump
    else:
        # walk
        player_ind += 0.1
        player_surf = player_surfs[int(player_ind) % 2]


def collisions(player: pygame.Rect, obstacles: list):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


pygame.init()
game_active = False
start_time = 0
score = 0
jump_sound = pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.3)
bgm = pygame.mixer.Sound('audio/music.wav')
bgm.set_volume(0.3)
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
#   snail
snail_1_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_2_surf = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_surfs = [snail_1_surf, snail_2_surf]
snail_ind = 0
snail_surf = snail_surfs[snail_ind]
#   fly
fly_1_surf = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_2_surf = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_surfs = [fly_1_surf, fly_2_surf]
fly_ind = 0
fly_surf = fly_surfs[fly_ind]
obstacle_rect_lst = list()

# player surface
player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_ind = 0
player_surfs = [player_walk_1, player_walk_2]
player_surf = player_surfs[player_ind]
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_grav = 0

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
pygame.time.set_timer(obstacle_time, 1500)
#   snail animation
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)
#   fly animation
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
            #     jump
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom == 300:
                    player_grav = -20
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    jump_sound.play()
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks() // 1000
        if game_active:
            # generation of obstacles
            if event.type == obstacle_time:
                if randint(0, 2):
                    obstacle_rect_lst.append(snail_surf.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_lst.append(fly_surf.get_rect(bottomright=(randint(900, 1100), 200)))
            # snail animation
            if event.type == snail_animation_timer:
                if snail_ind:
                    snail_ind = 0
                else:
                    snail_ind = 1
                snail_surf = snail_surfs[snail_ind]
            # fly animation
            if event.type == fly_animation_timer:
                if fly_ind:
                    fly_ind = 0
                else:
                    fly_ind = 1
                fly_surf = fly_surfs[fly_ind]
    if game_active:
        # displaying the const surfaces
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        #     score surface
        score = display_score()

        # obstacle animation
        obstacle_rect_lst = obstacle_animation(obstacle_rect_lst)

        # player animation
        player_grav += 1
        player_rect.y += player_grav
        if player_rect.bottom > 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # collision
        game_active = collisions(player_rect, obstacle_rect_lst)
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

        # initialising elements
        obstacle_rect_lst.clear()
        player_rect.midbottom = (80, 300)
        player_grav = 0

    pygame.display.update()
    clock.tick(60)  # creating celling
