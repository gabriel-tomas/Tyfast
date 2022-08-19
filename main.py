from threading import Thread
import pygame
from time import sleep
from english_words import english_words_set
from random import choice
import sys


pygame.init()
SCREEN_X = 1280
SCREEN_Y = 720
screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
input_box = pygame.image.load("input-box.png")
input_box_rect = input_box.get_rect(center=(SCREEN_X/2, SCREEN_Y/2))
info_box_word = pygame.image.load("info-word.png")
info_box_word_rect = info_box_word.get_rect(center=(SCREEN_X/2 , SCREEN_Y/2- 100))
clock = pygame.time.Clock()
input_active = False
text = ""
font = pygame.font.Font(None, 32)
font_timer = pygame.font.Font("font.otf", 200)
font_heading = pygame.font.Font("font.otf", 110, bold=True)
font_point = pygame.font.Font("font.otf", 80)
font_lose = pygame.font.Font("font.otf", 80)
font_last_points = pygame.font.Font("font.otf", 40)
x_inputbox = 300
button_retry = pygame.image.load("button-retry.png")
rect_button = button_retry.get_rect(center=(SCREEN_X/2, SCREEN_Y/2 + 90))
#window_lose = pygame.Rect(SCREEN_X/2 - 200, SCREEN_Y/2 - 100, 400, 200)
window_lose = pygame.image.load("lose-window.png")
window_lose_rect = window_lose.get_rect(center=(SCREEN_X / 2 , SCREEN_Y / 2))
background_start = pygame.image.load("background.png")
background_start = pygame.transform.scale(background_start, (SCREEN_X, SCREEN_Y))
background_start1 = pygame.image.load("background.png")
background_start1 = pygame.transform.scale(background_start1, (SCREEN_X, SCREEN_Y))
bg1 = pygame.image.load("bg.png")
bg1 = pygame.transform.scale(bg1, (SCREEN_X, SCREEN_Y))
bg2 = pygame.image.load("bg.png")
bg2 = pygame.transform.scale(bg2, (SCREEN_X, SCREEN_Y))
start_menu = pygame.image.load("button-start.png")
rect_start_menu = start_menu.get_rect(center=(SCREEN_X/2 - int(start_menu.get_rect()[2]) + 100, SCREEN_Y/2 - 30))
options_menu = pygame.image.load("button-options.png")
rect_options_menu = options_menu.get_rect(center=(SCREEN_X/2 - int(start_menu.get_rect()[2]) + 100, SCREEN_Y/2 + 20))
about_menu = pygame.image.load("button-about.png")
rect_about_menu = about_menu.get_rect(center=(SCREEN_X/2 - int(start_menu.get_rect()[2]) + 100, SCREEN_Y/2 + 70))
word = None
time = 0
dec_time = 0
time_to_same = 10
pos = []
pos_n = 0
list_words_same = []
list_dec_time = []
game_run = False
y_bg1 = 0
y_bg2 = 0
points = 0


def move_bg():
    global y_bg1, y_bg2

    while True:
        print(y_bg1)
        if game_run:
            y_bg1 += 1
            sleep(0.01)
            if y_bg1 == SCREEN_Y:
                y_bg1 = 0
        elif not game_run:
            y_bg2 += 1
            sleep(0.01)
            if y_bg2 == SCREEN_Y:
                y_bg2 = 0
                
Thread(target=move_bg).start()


#hit word info
def txt_info_see():
    list_words = list_words_same[::-1]
    list_dec = list_dec_time[::-1]
    print(list_words)
    for i, word in enumerate(list_words):
        info = font.render(f"{word}    -{list_dec[i]}s", True, (255, 255, 255))
        screen.blit(info, (SCREEN_X / 2- 100, SCREEN_Y / 2 + 50 + pos[i]))

    
#time to hit te word
def time_run():
    global time, dec_time

    while True:
        time += 1
        print(time)
        sleep(1)
        if dec_time:
            time += -dec_time
            dec_time = False
        if time == time_to_same:
            break
        
#run game
while True:
    if not game_run:
        screen.fill((0,0,0))
        screen.blit(background_start, (0,y_bg2))
        screen.blit(background_start1, (0,y_bg2 - SCREEN_Y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_start_menu.collidepoint(event.pos):
                    game_run = True
                    word = choice(list(english_words_set))
                    Thread(target=time_run).start()
        #txt_start_game = font.render("Start", True, (255, 255, 255))
        #txt_about = font.render("About", True, (255, 255, 255))
        txt_heading = font_heading.render("Tyfast", True, (82, 39, 39))
        screen.blit(start_menu, rect_start_menu)
        screen.blit(options_menu, rect_options_menu)
        screen.blit(about_menu, rect_about_menu)
        screen.blit(txt_heading, (SCREEN_X /2 - int(txt_heading.get_rect()[2]) + 130, SCREEN_Y / 2 - 250))
        pygame.display.flip()
    elif game_run:
        screen.fill((0,0,0))
        screen.blit(bg1, (0, y_bg1))
        screen.blit(bg1, (0, y_bg1 - SCREEN_Y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #verify mouse click and pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                #input box mouse click check
                if input_box_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                #button start mouse click check
                if rect_button.collidepoint(event.pos) and time == time_to_same:
                    time = 0
                    points = 0
                    text = ""
                    list_words_same.clear()
                    list_dec_time.clear()
                    word = choice(list(english_words_set))
                    Thread(target=time_run).start()
            #verify keyboard click
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        if text.strip() == word and time != time_to_same:
                            list_words_same.append(word)
                            pos.append(pos_n)
                            pos_n += 20
                            if len(word) >= 9:
                                dec_time = 3
                            elif len(word) >= 7:
                                dec_time = 2
                            else:
                                dec_time = 1
                            list_dec_time.append(dec_time)
                            text = ""
                            points += 1
                            word = choice(list(english_words_set))
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode.strip()
        txt_surface = font.render(text, True, (255, 255, 255))
        #txt_start = font.render("Start", True, (255, 255, 255))
        txt_word = font.render(word, True, (255, 255, 255))
        txt_lose = font_lose.render("YOU'RE LOSE", True, (255, 255, 255))
        txt_last_points = font_last_points.render(f"Points: {points}", True, (255, 255, 255))
        txt_time = font_timer.render(str(time), True, (48, 48, 48))
        txt_points = font_point.render(str(points), True, (48, 48, 48))
        width_box = max(450, txt_surface.get_width() + 10)
        input_box_rect.w = width_box
        screen.blit(input_box, input_box_rect)
        screen.blit(txt_surface, (input_box_rect.x + 5, input_box_rect.y + 10))
        #screen.blit(loading_bar, rect_bar)
        screen.blit(txt_time, (SCREEN_X/2 - int(txt_time.get_rect()[2]) + 45, SCREEN_Y/2 - 350))
        #screen.blit(txt_start, (710, 550))
        screen.blit(info_box_word, info_box_word_rect)
        screen.blit(txt_word, (int(info_box_word_rect[0])+70, int(info_box_word_rect[1])+45))
        screen.blit(txt_points, (SCREEN_X - 100, 5))
        if len(list_words_same) >= 1:
            txt_info_see()
        if time == time_to_same:
            screen.blit(window_lose, window_lose_rect)
            screen.blit(button_retry, rect_button)
            screen.blit(txt_lose, (SCREEN_X/2 - 180, SCREEN_Y/2 - 120))
            screen.blit(txt_last_points, (SCREEN_X/2 - 70, SCREEN_Y/2 - 20))
        pygame.display.flip()
        clock.tick(60)
    #pygame.display.flip()