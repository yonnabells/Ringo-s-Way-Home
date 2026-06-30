import pygame
import sys
import random
from pygame import mixer
pygame.init()

# SCREEN SIZE
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ringo's Way Home: A Jump Through Space Junk!")

# BACKGROUND
space = pygame.image.load('SKY BG.png').convert()
title = pygame.image.load('TITLE.png').convert()

# MUSIC
mixer.music.load('MAIN BG MUSIC.mp3')
mixer.music.play(-1)
meow = mixer.Sound('CATMEOW.mp3')

# CHARACTERS
ringo_left = pygame.image.load('ringostarr.png').convert_alpha()
ringo_left = pygame.transform.smoothscale(ringo_left, (150, 78))
ringo_right = pygame.transform.flip(ringo_left, True, False)
current_ringo = ringo_left
character_rect = ringo_left.get_rect()
character_rect.center = (width // 2, height - 100)

# INTRO
intro_1 = pygame.image.load('intro_1.png').convert_alpha()
intro_2 = pygame.image.load('intro_2.png').convert_alpha()
intro_3 = pygame.image.load('intro_3.png').convert_alpha()
intro_4 = pygame.image.load('intro_4.png').convert_alpha()
intro_5 = pygame.image.load('intro_5.png').convert_alpha()
intro_6 = pygame.image.load('intro_6.png').convert_alpha()
intro_7 = pygame.image.load('intro_7.png').convert_alpha()
intro_8 = pygame.image.load('intro_8.png').convert_alpha()
intro_9 = pygame.image.load('intro_9.png').convert_alpha()
objectives = pygame.image.load('objectives.png').convert_alpha()

# AFTER GAME SCREENS
game_over = pygame.image.load('game over.png').convert_alpha()
saved = pygame.image.load('saved_ringo.png').convert_alpha()

# ENDING
ending_1 = pygame.image.load('ending_1.png').convert_alpha()
ending_2 = pygame.image.load('ending_2.png').convert_alpha()
ending_3 = pygame.image.load('ending_3.png').convert_alpha()
thankyou = pygame.image.load('thankyou.png').convert_alpha()

intro_screens = [
    intro_1, intro_2, intro_3, intro_4, intro_5,
    intro_6, intro_7, intro_8, intro_9
]
current_intro_index = 0

ending_screens = [
    ending_2, ending_3, thankyou
]
current_ending_index = 0

# SPACE JUNK
junk_images = [
    pygame.image.load('spacejunk1.png').convert_alpha(),
    pygame.image.load('spacejunk2.png').convert_alpha(),
    pygame.image.load('spacejunk3.PNG').convert_alpha(),
    pygame.image.load('spacejunk4.PNG').convert_alpha(),
    pygame.image.load('spacejunk5.PNG').convert_alpha()
]

# Resize junk
resized_junk = []
for img in junk_images:
    w = 80
    h = int(img.get_height() * (w / img.get_width()))
    resized_junk.append(pygame.transform.smoothscale(img, (w, h)))

junk_list = []
for img in resized_junk:
    rect = img.get_rect()
    rect.x = random.randint(0, width - rect.width)
    rect.y = random.randint(-600, -50)
    speed = random.randint(2, 4)
    junk_list.append({'image': img, 'rect': rect, 'speed': speed})

# Clock and speed
clock = pygame.time.Clock()
movement_speed = 5
lives = 9
total_time = 90  # seconds to survive
font = pygame.font.SysFont(None, 36)
game_state = "start_menu"


def draw_start_menu():
    screen.blit(title, (0, 0))
    pygame.display.flip()

# START START START START START START START START START START START START START START START START START START START START START START
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # KEYSSESESESESES
        elif event.type == pygame.KEYDOWN:
            if game_state == "start_menu" and event.key == pygame.K_SPACE:
                game_state = "intro"
                current_intro_index = 0
            elif game_state == "intro" and event.key == pygame.K_SPACE:
                current_intro_index += 1
                if current_intro_index >= len(intro_screens):
                    game_state = "objectives"
            elif game_state == "objectives" and event.key == pygame.K_RETURN:
                game_state = "game"
                start_ticks = pygame.time.get_ticks()
                lives = 9
                character_rect.center = (width // 2, height - 100)
                for junk in junk_list:
                    junk['rect'].y = random.randint(-600, -50)
                    junk['rect'].x = random.randint(0, width - junk['rect'].width)
            elif game_state == "game_over" and event.key == pygame.K_h:
                game_state = "start_menu"

            elif game_state == "saved" and event.key == pygame.K_SPACE:
                game_state = "ending1"
                current_ending_index = 0
            elif game_state == "ending1" and event.key == pygame.K_SPACE:
                game_state = "endingf"
                current_ending_index += 0
            elif game_state == "endingf" and event.key == pygame.K_SPACE:
                current_ending_index += 1
                if current_ending_index >= len(ending_screens):
                    game_state = "close"

    # erm flow
    if game_state == "start_menu":
        draw_start_menu()

    elif game_state == "intro":
        screen.blit(intro_screens[current_intro_index], (0, 0))
        pygame.display.flip()

    elif game_state == "objectives":
        screen.blit(objectives, (0, 0))
        pygame.display.flip()

    elif game_state == "game":
        clock.tick(60)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            character_rect.x -= movement_speed
            current_ringo = ringo_left
        elif keys[pygame.K_RIGHT]:
            character_rect.x += movement_speed
            current_ringo = ringo_right
        if keys[pygame.K_UP]:
            character_rect.y -= movement_speed
        if keys[pygame.K_DOWN]:
            character_rect.y += movement_speed

        # ringo inside screen
        character_rect.left = max(0, character_rect.left)
        character_rect.right = min(width, character_rect.right)
        character_rect.top = max(0, character_rect.top)
        character_rect.bottom = min(height, character_rect.bottom)

        # Move junk
        for junk in junk_list:
            junk['rect'].y += junk['speed']
            if junk['rect'].y > height:
                junk['rect'].y = random.randint(-100, -50)
                junk['rect'].x = random.randint(0, width - junk['rect'].width)
            if character_rect.colliderect(junk['rect'].inflate(-20, -20)):
                meow.play()
                lives -= 1
                junk['rect'].y = random.randint(-100, -50)
                junk['rect'].x = random.randint(0, width - junk['rect'].width)

        # Timer
        seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
        time_left = max(0, int(total_time - seconds_passed))

        # junknknknknknkn
        screen.blit(space, (0, 0))
        for junk in junk_list:
            screen.blit(junk['image'], junk['rect'])
        screen.blit(current_ringo, character_rect)

        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))
        timer_text = font.render(f"Time: {time_left}", True, (255, 255, 0))
        screen.blit(timer_text, (width - 150, 10))

        # Check win/lose
        if lives <= 0:
            game_state = "game_over"
        elif time_left <= 0:
            game_state = "saved"

        pygame.display.flip()

    elif game_state == "game_over":
        screen.blit(game_over, (0, 0))
        pygame.display.flip()

    elif game_state == "saved":
        screen.blit(saved, (0, 0))
        pygame.display.flip()

    elif game_state == "ending1":
        screen.blit(ending_1, (0, 0))
        pygame.display.flip()

    elif game_state == "endingf":
        screen.blit(ending_screens[current_ending_index], (0, 0))
        pygame.display.flip()

    elif game_state == "close":
        pygame.quit()
        sys.exit()
