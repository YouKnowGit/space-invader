import os
import pygame
import time
import random

from models.ship import Player, Enemy
from utils.collide import collide
from .controls import audio_cfg, display_cfg, controls
from .background import bg_obj

from constants import GAME_MUSIC_PATH, \
    WIDTH, \
    HEIGHT, \
    CANVAS, \
    heartImage, \
    score_list, \
    framespersec, \
    FPS, \
    FONT_PATH, \
    stage_1, stage_2, stage_3, \
    game_over_1, game_over_2, game_over_3, game_over_4

"""
설정 창 넣기
stage 1, 6, 11 => 스토리 설명 
어디서 게임 끝나는지에 따라 다른 gameover창 띄움(총4개)

TODO text/image 기입, 리펙토링 하기
TODO stage넘김 : 시간 =>  key, mouse event로 변경
"""

def game(isMouse=False):
    lives = 3
    level = 0
    laser_vel = 15

    main_font = pygame.font.Font(os.path.join(FONT_PATH, "edit_undo.ttf"), 50)
    sub_font = pygame.font.Font(os.path.join(FONT_PATH, "neue.ttf"), 40)
    sub_small_font = pygame.font.Font(os.path.join(FONT_PATH, "neue.ttf"), 35)
    lost_font = pygame.font.Font(os.path.join(FONT_PATH, "edit_undo.ttf"), 55)
    win_font = pygame.font.Font(os.path.join(FONT_PATH, "edit_undo.ttf"), 55)

    # load and play ingame music
    audio_cfg.play_music(GAME_MUSIC_PATH)

    enemies = []  #몹들
    wave_length = 0 #몹cnt
    enemy_vel = 1

    player = Player(300, 585, mouse_movement=isMouse)
    pygame.mouse.set_visible(False)

    # 종료화면
    lost = [False, False, False, False]
    lost_img = [game_over_1, game_over_2, game_over_3, game_over_4]

    # story설명
    story = [True, True, True, True]
    story_img = [stage_1, stage_2, stage_3]

    # boss등장
    boss = [True, True, True, True]

    pause = False #일시정지
    setting = False #설정창

    def redraw_window(pause=False): # 렌더링
        if not pause:
            bg_obj.update()
        bg_obj.render(CANVAS)

        window_width = CANVAS.get_width()
        background_width = bg_obj.rectBGimg.width
        screen_rect = CANVAS.get_rect()
        center_x = screen_rect.centerx
        starting_x = center_x - background_width//2
        ending_x = center_x + background_width//2

        # Draw Text
        level_label = sub_small_font.render(f'STAGE: {level if level <= 15 else 15} / 15', 1, (0, 255, 255))
        score_label = sub_font.render(f'{player.get_score()}', 1, (0, 255, 0))
        setting_btn = sub_font.render(f'set[c]', 1, (255, 0, 0))

        player.draw(CANVAS)

        for enemyShip in enemies:
            enemyShip.draw(CANVAS)

        # blit player stats after enemyShips to prevent the later
        # from being drawn over the stats

        # Header
        for index in range(1, lives + 1):# Lives
            CANVAS.blit(heartImage, (starting_x + 37 * index - 10, 17))

        CANVAS.blit(level_label, ((ending_x - level_label.get_width()) / 2 - 20, 15))# stage 위치
        CANVAS.blit(score_label, (ending_x - score_label.get_width() - 130, 10))# 점수 위치
        CANVAS.blit(setting_btn, (ending_x - setting_btn.get_width() - 10, 10))

        # 종료화면
        if lost[int(level/5)]:
            score_list.append(player.get_score()) #점수체크
            # `game_over_{int(level/5)}`
            CANVAS.blit(lost_img[int(level/5)], (window_width // 2 - lost_img[int(level/5)].get_width() // 2, 150))


        # 스토리 설명 + 보스몹 출현
        if level <= 15 and level % 5 == 1 and story[level // 5]: # story1
            CANVAS.blit(story_img[int(level / 5)], (window_width // 2 - lost_img[int(level / 5)].get_width() // 2, 150))


        elif level <= 15 and level % 5 == 0 and boss[level // 5]: # boss1
            last_label = lost_font.render(f'BOSS {level // 5}', 1, (255, 0, 0))
            CANVAS.blit(last_label, (window_width//2 -
                        last_label.get_width()//2, 350))

        # 일시중지 스크린
        if pause:
            pause_label = main_font.render('Game Paused', 1, (0, 255, 255))
            CANVAS.blit(pause_label, (window_width//2 -
                        pause_label.get_width()//2, 350))

            key_msg = sub_font.render('Press [p] to unpause', 1, (0, 0, 255))
            CANVAS.blit(key_msg, (window_width//2 -
                        key_msg.get_width()//2, 400))

        if setting: #설정창
            setting_label = main_font.render('setting', 1, (0, 255, 255))
            CANVAS.blit(setting_label, (window_width//2 -
                        setting_label.get_width()//2, 100))

        audio_cfg.display_volume(CANVAS)
        pygame.display.update()
        framespersec.tick(FPS)

    # 게임 시작
    while player.run:
        redraw_window()

        if lives > 0:
            if player.health <= 0:
                lives -= 1
                player.health = 100
        # game over
        else:
            if level < 5:
                lost[0] = True
            elif level < 10:
                lost[1] = True
            elif level < 15:
                lost[2] = True
            redraw_window()
            time.sleep(3)
            player.run = False
            pygame.mouse.set_visible(True)


        if level < 15 and level % 5 == 1 and story[int(level / 5)]: # story
            # redraw_window()
            story[int(level / 5)] = False
            time.sleep(1)
            redraw_window()

        elif level <= 15 and level > 1 and level % 5 == 0 and boss[int(level / 5)]: # boss
            time.sleep(0.5)
            boss[int(level / 5)] = False
            redraw_window()

        if level > 15:
            lost[3] = True
            redraw_window()
            time.sleep(3)
            player.run = False

        if len(enemies) == 0:
            level += 1
            wave_length += 1


            # stage 5, 10, 15때 보스몹 1마리 나옴
            for i in range(wave_length if (level != 5 and level != 10 and level != 15) else 1):
                enemies.append(Enemy(
                    random.randrange(50, WIDTH - 100),
                    random.randrange(-1200, -100),
                    random.choice(['easy', 'medium', 'hard']) if (level != 5 and level != 10 and level != 15) else 'boss')
                )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    pygame.mouse.set_visible(True)
                    pause = True
                if event.key == pygame.K_m:
                    audio_cfg.toggle_mute()
                if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    audio_cfg.inc_volume(5)
                if event.key == pygame.K_MINUS:
                    audio_cfg.dec_volume(5)
                if event.key == pygame.K_f:
                    display_cfg.toggle_full_screen()
                # 설정창
                if event.key == pygame.K_c:
                    pygame.mouse.set_visible(True)
                    setting= True

        # 일시정지, 설정창
        while pause or setting:
            # create a fresh screen
            redraw_window(pause)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_m:
                        audio_cfg.toggle_mute()
                    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                        audio_cfg.inc_volume(5)
                    if event.key == pygame.K_MINUS:
                        audio_cfg.dec_volume(5)
                    if event.key == pygame.K_p:
                        pygame.mouse.set_visible(False)
                        pause = False
                        break
                    if event.key == pygame.K_c:
                        pygame.mouse.set_visible(False)
                        setting = False
                        break

        player.move()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            if collide(enemy, player): # 충돌시 (몹-총알, 몹-유저)
                player.SCORE += 50
                if enemy.ship_type == 'boss':
                    if enemy.boss_max_health - 5 <= 0:
                        enemies.remove(enemy)
                        enemy.boss_max_health = 100
                        player.health -= 100
                    else:
                        enemy.boss_max_health -= 5
                        player.health -= 100
                else:
                    player.health -= 10
                    enemies.remove(enemy)
            elif enemy.y + enemy.get_height()/2 > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)
