import os
import time

import pygame
import argparse

from screens.game import game
from screens.controls import audio_cfg, display_cfg, controls
from screens.score_board import score_board
from screens.background import slow_bg_obj

from constants import MENU_MUSIC_PATH, TITLE,\
    WIDTH,\
    BOSS_SHIP,\
    PLAYER_SPACE_SHIP,\
    PLAYER_LASER,\
    startImage,\
    controlImage,\
    trophyImage,\
    CANVAS, \
    framespersec, \
    FPS, \
    FONT_PATH

# parsing arguments
ag = argparse.ArgumentParser()
ag.add_argument("--mute", help="disable all sounds", action="store_true")
args = vars(ag.parse_args())

if args["mute"]:
    audio_cfg.toggle_mute()

pygame.font.init()

pygame.display.set_caption(TITLE)

def main():
    title_font = pygame.font.Font(os.path.join(FONT_PATH, 'edit_undo.ttf'), 60)
    sub_title_font = pygame.font.Font(os.path.join(FONT_PATH, 'neue.ttf'), 30)

    audio_cfg.play_music(MENU_MUSIC_PATH)
    run = True
    index = 0
    while run:
        slow_bg_obj.update()
        slow_bg_obj.render(CANVAS)

        window_width = CANVAS.get_width()
        background_width = slow_bg_obj.rectBGimg.width
        screen_rect = CANVAS.get_rect()
        center_x = screen_rect.centerx
        starting_x = center_x - background_width//2


        # 메인 view 구성
        # Ships
        CANVAS.blit(BOSS_SHIP, (starting_x + 255, 75))
        CANVAS.blit(PLAYER_SPACE_SHIP, (window_width//2 - 50, 575))

        # text
        title_label = title_font.render('debugingjing the Game', 1, (0, 209, 0)) # 띄울 내용 (text, antialias, color, bg)
        CANVAS.blit(title_label, (window_width//2 - title_label.get_width()//2 - 15, 350)) # 띄울 위치(text, x좌표,y좌표)
        CHOICE_COLOR = (249, 166, 2)
        UNCHOICE_COLOR = (255, 255, 255)
        sub_title = [
            {
                'text': 'PLAY [ENTER]'
            },
            {
                'text': 'SCORES [S]'
            },
            {
                'text': 'SUMMARY [L]'
            },
            {
                'text': 'SETTING [C]'
            }
        ]

        CANVAS.blit(startImage, (window_width//2 + title_label.get_width()//2, 353))
        for idx, element in enumerate(sub_title):
            if idx == index:
                label = sub_title_font.render(element['text'], 1, CHOICE_COLOR)
            else:
                label = sub_title_font.render(element['text'], 1, UNCHOICE_COLOR)
            position = (window_width//2 - label.get_width()//2, 410 + idx*40)
            CANVAS.blit(label, position)

        audio_cfg.display_volume(CANVAS)
        pygame.display.update()
        framespersec.tick(FPS) # capping frame rate to 60
        
        # 한 번씩만 체크된
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    audio_cfg.toggle_mute()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_cfg.inc_volume(5)
                if event.key == pygame.K_MINUS:
                    audio_cfg.dec_volume(5)
                if event.key == pygame.K_f:
                    display_cfg.toggle_full_screen()
                # key up, down가능
                if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                    if index == len(sub_title)-1:
                        index = 0
                    else:
                        index += 1
                    print(index)
                if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                    if index == 0:
                        index = len(sub_title)-1
                    else:
                        index -= 1
                    print(index)

        keys = pygame.key.get_pressed() 
        button = pygame.mouse.get_pressed()

        # 계속 체크됨
        if keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            run = False

        if keys[pygame.K_c]:
            controls()

        if keys[pygame.K_s]:
            score_board()

        if keys[pygame.K_RETURN]:
            game()

        if button[0]:
            game(True)

    pygame.quit()

main()
