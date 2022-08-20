from json import load
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
font_loading_info = pygame.font.Font("font.otf", 40)
font_option_difficulty = pygame.font.Font("font.otf", 30)
font_box_difficulty = pygame.font.Font("font.otf", 25)
x_inputbox = 300
button_retry = pygame.image.load("button-retry.png")
rect_button = button_retry.get_rect(center=(SCREEN_X/2, SCREEN_Y/2 + 90))
#window_lose = pygame.Rect(SCREEN_X/2 - 200, SCREEN_Y/2 - 100, 400, 200)
window_lose = pygame.image.load("lose-window.png")
window_lose_rect = window_lose.get_rect(center=(SCREEN_X / 2 , SCREEN_Y / 2))
bg_start = pygame.image.load("background.png")
bg_start = pygame.transform.scale(bg_start, (SCREEN_X, SCREEN_Y))
bg_start1 = pygame.image.load("background.png")
bg_start1 = pygame.transform.scale(bg_start1, (SCREEN_X, SCREEN_Y))
bg_transition = pygame.image.load("bg-transition.png")
bg_transition1 = pygame.image.load("bg.png")
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
option_window = pygame.image.load("options-window.png")
option_window_rect = option_window.get_rect(center=(SCREEN_X/2, SCREEN_Y/2))
exit_option_window = pygame.image.load("exit-window-option.png")
exit_option_window_rect = exit_option_window.get_rect(center=(option_window_rect.x + 100, option_window_rect.y + 60))
option_button_box = pygame.image.load("box-transparent.png")
option_button_box_easy = pygame.transform.scale(option_button_box, (40, 40))
option_button_box_medium = pygame.transform.scale(option_button_box, (40, 40))
option_button_box_hard = pygame.transform.scale(option_button_box, (40, 40))
option_button_box_easy_rect = option_button_box_easy.get_rect(center=(window_lose_rect.x + 254, window_lose_rect.y + 97))
option_button_box_medium_rect = option_button_box_medium.get_rect(center=(window_lose_rect.x + 380, window_lose_rect.y + 97))
option_button_box_hard_rect = option_button_box_hard.get_rect(center=(window_lose_rect.x + 480, window_lose_rect.y + 97))
bg_loading = pygame.image.load("bg-loading.png")
bg_loading = pygame.transform.scale(bg_loading, (SCREEN_X, SCREEN_Y))
bg_loading1 = pygame.image.load("bg-loading.png")
bg_loading1 = pygame.transform.scale(bg_loading, (SCREEN_X, SCREEN_Y))
word = None
option_state = False
game_run = False
difficulty = "easy"
time = 0
dec_time = 0
time_to_same = 10
difficulty_time = {"easy": 10, "medium":5, "hard":4}
pos = []
pos_n = 0
loading = False
list_words_same = []
list_dec_time = []
y_bg1 = 0
y_bg2 = 0
y_bg3 = 0
points = 0
x_points, y_points = 32, 50
dir_p_x = 0.16
dir_p_y = 0.4
time_loading = 0
txt_loading_info_str = ""

def difficulty_set(collid=False):
    global option_button_box_easy, option_button_box_medium, option_button_box_hard, difficulty, time_to_same

    if collid:
        if option_button_box_easy_rect.collidepoint(event.pos):
            difficulty = "easy"
            time_to_same = difficulty_time[difficulty]
            option_button_box_easy = pygame.image.load("mark-box.png")
            option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
            #clear others boxs
            option_button_box_medium = pygame.image.load("box-transparent.png")
            option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
            option_button_box_hard = pygame.image.load("box-transparent.png")
            option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40,40))
        if option_button_box_medium_rect.collidepoint(event.pos):
            difficulty = "medium"
            time_to_same = difficulty_time[difficulty]
            option_button_box_medium = pygame.image.load("mark-box.png")
            option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
            #clear others boxs
            option_button_box_easy = pygame.image.load("box-transparent.png")
            option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
            option_button_box_hard = pygame.image.load("box-transparent.png")
            option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40,40))
        if option_button_box_hard_rect.collidepoint(event.pos):
            difficulty = "hard"
            time_to_same = difficulty_time[difficulty]
            option_button_box_hard = pygame.image.load("mark-box.png")
            option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40,40))
            #clear others boxs
            option_button_box_medium = pygame.image.load("box-transparent.png")
            option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
            option_button_box_easy = pygame.image.load("box-transparent.png")
            option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
        return

    if difficulty == "easy":
        option_button_box_easy = pygame.image.load("easy-box-marked.png")
        option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
    if difficulty == "medium":
        option_button_box_medium = pygame.image.load("medium-box-marked.png")
        option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
    if difficulty == "hard":
        option_button_box_hard = pygame.image.load("hard-box-marked.png")
        option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40, 40))

def loading_time():
    global time_loading, game_run, loading, word, input_active

    for i in range(1, 4):
        time_loading = i
        sleep(2)
    game_run = True
    loading = False
    input_active = True
    word = choice(list(english_words_set))
    Thread(target=time_run).start()

def txt_str_loading():
    global txt_loading_info_str

    str = ""
    while True:
        txt_loading_info_str = str
        str += "."
        sleep(0.1)
        if str == "....":
            str = ""
        if loading == False:
            break

def move_bg():
    global y_bg1, y_bg2, y_bg3

    while True:
        if game_run:
            y_bg1 += 1
            sleep(0.01)
            if y_bg1 == SCREEN_Y:
                y_bg1 = 0
        elif game_run == False and loading == False:
            y_bg2 += 5
            sleep(0.01)
            if y_bg2 >= SCREEN_Y:
                y_bg2 = 0
        elif loading:
            y_bg3 += 4
            sleep(0.01)
            if y_bg3 >= SCREEN_Y:
                y_bg3 = 0
        #else:
        #    y_bg3 += 5
        #    sleep(0.01)
        #    if y_bg3 == SCREEN_Y:
        #        y_bg3 = 0

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
    if game_run == False and loading == False:
        print("menu")
        screen.fill((0,0,0))
        screen.blit(bg_start, (0,y_bg2))
        screen.blit(bg_start1, (0,y_bg2 - SCREEN_Y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_start_menu.collidepoint(event.pos) and option_state == False:
                    loading = True
                    Thread(target=loading_time).start()
                    Thread(target=txt_str_loading).start()
                if rect_options_menu.collidepoint(event.pos):
                    option_state = True
                if exit_option_window_rect.collidepoint(event.pos):
                    option_state = False
                if option_state:
                    difficulty_set(True)
        txt_heading = font_heading.render("Tyfast", True, (82, 39, 39))
        txt_dificulty = font_option_difficulty.render("Difficulty", True, (255, 255, 255))
        txt_easy = font_box_difficulty.render("Easy", True, (0, 255, 0))
        txt_medium = font_box_difficulty.render("Medium", True, (226, 247, 18))
        txt_hard = font_box_difficulty.render("Hard", True, (255, 0, 0))
        screen.blit(start_menu, rect_start_menu)
        screen.blit(options_menu, rect_options_menu)
        screen.blit(about_menu, rect_about_menu)
        screen.blit(txt_heading, (SCREEN_X /2 - int(txt_heading.get_rect()[2]) + 130, SCREEN_Y / 2 - 250))
        if option_state:
            screen.blit(option_window, option_window_rect)
            screen.blit(exit_option_window, (option_window_rect.x + 35, option_window_rect.y + 30))
            screen.blit(txt_dificulty, (window_lose_rect.x - 5, window_lose_rect.y + 80))
            screen.blit(txt_hard, (window_lose_rect.x + 416, window_lose_rect.y + 82))
            screen.blit(option_button_box_hard, option_button_box_hard_rect)
            screen.blit(txt_medium, (window_lose_rect.x + 288, window_lose_rect.y + 82))
            screen.blit(option_button_box_medium, option_button_box_medium_rect)
            screen.blit(txt_easy, (window_lose_rect.x + 187, window_lose_rect.y + 82))
            screen.blit(option_button_box_easy, option_button_box_easy_rect)
            difficulty_set()
        clock.tick(75)
        pygame.display.flip()
    if game_run:
        print("run game")
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
                    input_active = True
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
        txt_points = pygame.transform.scale(txt_points, (x_points, y_points))
        screen.blit(txt_points, (SCREEN_X - 100, 5))
        
        x_points += dir_p_x
        y_points += dir_p_y
        if y_points >= 75:
            dir_p_x = -0.16
            dir_p_y = -0.4
        if y_points <= 60:
            dir_p_x = 0.16
            dir_p_y = 0.4
        if len(list_words_same) >= 1:
            txt_info_see()
        if time == time_to_same:
            screen.blit(window_lose, window_lose_rect)
            screen.blit(button_retry, rect_button)
            screen.blit(txt_lose, (SCREEN_X/2 - 180, SCREEN_Y/2 - 120))
            screen.blit(txt_last_points, (SCREEN_X/2 - 70, SCREEN_Y/2 - 20))
            print(window_lose_rect.x, window_lose_rect.y)
            
        pygame.display.flip()
        clock.tick(75)
    if loading:
        print("loading")
        screen.fill((0,0,0))
        screen.blit(bg_loading, (0, 0))
        txt_loading = font_timer.render(str(time_loading), True, (255, 255, 255))
        txt_loading_info = font_loading_info.render(f"Starting game in{txt_loading_info_str}", True, (255, 255, 255))
        screen.blit(txt_loading, (SCREEN_X/2 - 40, SCREEN_Y/2 - 130))
        screen.blit(txt_loading_info, (SCREEN_X/2 - 120, SCREEN_Y/2 - 160))
        clock.tick(75)
        pygame.display.flip()