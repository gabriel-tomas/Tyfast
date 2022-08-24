from threading import Thread
import pygame
from time import sleep
from english_words import english_words_set
from random import choice
import sys
from update import update
from saveload import save, load, save_score


pygame.init()
display_info = pygame.display.Info()
if "display" in load():
    SCREEN_X, SCREEN_Y, fullscreen = load()["display"]
    if fullscreen:
        screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y], pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
else:
    SCREEN_X, SCREEN_Y = display_info.current_w, display_info.current_h
    screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])

if "difficulty" in load():
    difficulty = load()["difficulty"]
else:
    difficulty = "easy"

if "easy" in load("score.json"):
    last_max_points = load("score.json")
else:
    last_max_points = {"easy":0, "medium":0, "hard":0}

clock = pygame.time.Clock()
input_active = False
text = ""
font = pygame.font.Font(None, 32)
font_timer = pygame.font.Font("assets/font/font.otf", 200)
font_heading = pygame.font.Font("assets/font/font.otf", 110, bold=True)
font_point = pygame.font.Font("assets/font/font.otf", 80)
font_lose = pygame.font.Font("assets/font/font.otf", 80)
font_last_points = pygame.font.Font("assets/font/font.otf", 40)
font_loading_info = pygame.font.Font("assets/font/font.otf", 40)
font_options = pygame.font.Font("assets/font/font.otf", 30)
font_box_choice = pygame.font.Font("assets/font/font.otf", 25)
font_last_max_points = pygame.font.Font("assets/font/font.otf", 30)
font_about_window = pygame.font.Font("assets/font/font.otf", 25)
input_box, input_box_rect, info_box_word, info_box_word_rect, button_retry, rect_button, window_lose, window_lose_rect, bg_start, bg_start1, bg1, bg2, start_menu, rect_start_menu, options_menu, rect_options_menu, about_menu, rect_about_menu, option_window, option_window_rect,exit_option_window, exit_option_window_rect, option_button_box, option_button_box_easy, option_button_box_medium, option_button_box_hard, option_button_res_800, option_button_res_1280, option_button_res_1920, option_button_res_800_rect, option_button_res_1280_rect, option_button_res_1920_rect, option_button_box_easy_rect, option_button_box_medium_rect, option_button_box_hard_rect, bg_loading, bg_loading1, button_exit, button_exit_rect, option_box_fullscreen, option_box_fullscreen_rect, about_window, about_window_rect = update(SCREEN_X, SCREEN_Y)
word = None
option_state = False
about_state = False
game_run = False
time = 0
dec_time = 0
difficulty_time = {"easy": 10, "medium":5, "hard":4}
time_to_same = difficulty_time[difficulty]
pos = []
pos_n = 0
loading = False
list_words_same = []
list_dec_time = []
y_bg1 = 0
y_bg2 = 0
points = 0
x_points, y_points = 32, 50
dir_p_x = 0.16
dir_p_y = 0.4
time_loading = 0
txt_loading_info_str = ""
program_run = True
dict_save = {}


def max_score(difficulty):
    last_max_points[difficulty] = points
    #print(last_max_points)
    list = save_score(last_max_points, difficulty)
    return list


def res_set(width=None, height=None, fullscreen=False):
    dict_save["display"] = [width, height, fullscreen]
    save(dict_save, "config.json")
    if fullscreen:
        option_1920 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_fullscreen = pygame.image.load("assets/buttons/button-windows-options/res-box-marked.png")
        return pygame.display.set_mode([width, height], pygame.FULLSCREEN), width, height, pygame.transform.scale(option_fullscreen, (40, 40)), pygame.transform.scale(option_1920, (40, 40))
    marked, transparent = pygame.image.load("assets/buttons/button-windows-options/res-box-marked.png"), pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
    return pygame.display.set_mode([width, height]), width, height, pygame.transform.scale(marked, (40, 40)), pygame.transform.scale(transparent, (40, 40))



def resolution_set(collid=False):
    global input_box, input_box_rect, info_box_word, info_box_word_rect, button_retry, rect_button, window_lose, window_lose_rect, bg_start, bg_start1, bg1, bg2, start_menu, rect_start_menu, options_menu, rect_options_menu, about_menu, rect_about_menu, option_window, option_window_rect,exit_option_window, exit_option_window_rect, option_button_box, option_button_box_easy, option_button_box_medium, option_button_box_hard, option_button_res_800, option_button_res_1280, option_button_res_1920, option_button_res_800_rect, option_button_res_1280_rect, option_button_res_1920_rect, option_button_box_easy_rect, option_button_box_medium_rect, option_button_box_hard_rect, bg_loading, bg_loading1, button_exit, button_exit_rect, option_box_fullscreen, option_box_fullscreen_rect, screen, SCREEN_X, SCREEN_Y, about_window, about_window_rect
    

    if collid:
        if option_box_fullscreen_rect.collidepoint(event.pos):
            screen, SCREEN_X, SCREEN_Y, option_box_fullscreen, option_button_res_1920= res_set(display_info.current_w, display_info.current_h, fullscreen=True)
            input_box, input_box_rect, info_box_word, info_box_word_rect, button_retry, rect_button, window_lose, window_lose_rect, bg_start, bg_start1, bg1, bg2, start_menu, rect_start_menu, options_menu, rect_options_menu, about_menu, rect_about_menu, option_window, option_window_rect, exit_option_window, exit_option_window_rect, option_button_box, option_button_box_easy, option_button_box_medium, option_button_box_hard, option_button_res_800, option_button_res_1280, option_button_res_192, option_button_res_800_rect, option_button_res_1280_rect, option_button_res_1920_rect, option_button_box_easy_rect, option_button_box_medium_rect, option_button_box_hard_rect, bg_loading, bg_loading1, button_exit, button_exit_rect, option_box_fullscree, option_box_fullscreen_rect, about_window, about_window_rect = update(SCREEN_X, SCREEN_Y)
        if option_button_res_800_rect.collidepoint(event.pos):
            screen, SCREEN_X, SCREEN_Y, option_button_res_800, option_button_res_1280 = res_set(width=800, height=600)
            input_box, input_box_rect, info_box_word, info_box_word_rect, button_retry, rect_button, window_lose, window_lose_rect, bg_start, bg_start1, bg1, bg2, start_menu, rect_start_menu, options_menu, rect_options_menu, about_menu, rect_about_menu, option_window, option_window_rect, exit_option_window, exit_option_window_rect, option_button_box, option_button_box_easy, option_button_box_medium, option_button_box_hard, res_chang, option_button_res_1280, option_button_res_1920, option_button_res_800_rect, option_button_res_1280_rect, option_button_res_1920_rect, option_button_box_easy_rect, option_button_box_medium_rect, option_button_box_hard_rect, bg_loading, bg_loading1, button_exit, button_exit_rect, option_box_fullscreen, option_box_fullscreen_rect, about_window, about_window_rect = update(SCREEN_X, SCREEN_Y)
            option_button_res_1920 = option_button_res_1280
        elif option_button_res_1280_rect.collidepoint(event.pos):
            screen, SCREEN_X, SCREEN_Y, option_button_res_1280, option_button_res_800 = res_set(width=1280, height=720)
            input_box, input_box_rect, info_box_word, info_box_word_rect, button_retry, rect_button, window_lose, window_lose_rect, bg_start, bg_start1, bg1, bg2, start_menu, rect_start_menu, options_menu, rect_options_menu, about_menu, rect_about_menu, option_window, option_window_rect, exit_option_window, exit_option_window_rect, option_button_box, option_button_box_easy, option_button_box_medium, option_button_box_hard, option_button_res_800, res_change, option_button_res_1920, option_button_res_800_rect, option_button_res_1280_rect, option_button_res_1920_rect, option_button_box_easy_rect, option_button_box_medium_rect, option_button_box_hard_rect, bg_loading, bg_loading1, button_exit, button_exit_rect, option_box_fullscreen, option_box_fullscreen_rect, about_window, about_window_rect = update(SCREEN_X, SCREEN_Y)
            option_button_res_1920 = option_button_res_800
        elif option_button_res_1920_rect.collidepoint(event.pos):
            screen, SCREEN_X, SCREEN_Y, option_button_res_1920, option_button_res_1280 = res_set(width=1920, height=1080)
            input_box, input_box_rect, info_box_word, info_box_word_rect, button_retry, rect_button, window_lose, window_lose_rect, bg_start, bg_start1, bg1, bg2, start_menu, rect_start_menu, options_menu, rect_options_menu, about_menu, rect_about_menu, option_window, option_window_rect, exit_option_window, exit_option_window_rect, option_button_box, option_button_box_easy, option_button_box_medium, option_button_box_hard, option_button_res_800, option_button_res_1280, res_chang, option_button_res_800_rect, option_button_res_1280_rect, option_button_res_1920_rect, option_button_box_easy_rect, option_button_box_medium_rect, option_button_box_hard_rect, bg_loading, bg_loading1, button_exit, button_exit_rect, option_box_fullscreen, option_box_fullscreen_rect, about_window, about_window_rect = update(SCREEN_X, SCREEN_Y)
            option_button_res_800 = option_button_res_1280
        return
    if SCREEN_X == 800:
        option_button_res_800 = pygame.image.load("assets/buttons/button-windows-options/res-box-marked.png")
        option_button_res_800 = pygame.transform.scale(option_button_res_800, (40, 40))
        #clear others
        option_button_res_1280 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_1280 = pygame.transform.scale(option_button_res_1280, (40, 40))
        option_button_res_1920 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_1920 = pygame.transform.scale(option_button_res_1920, (40, 40))
    elif SCREEN_X == 1280:
        option_button_res_1280 = pygame.image.load("assets/buttons/button-windows-options/res-box-marked.png")
        option_button_res_1280 = pygame.transform.scale(option_button_res_1280, (40, 40))
        #clear others
        option_button_res_800 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_800 = pygame.transform.scale(option_button_res_800, (40, 40))
        option_button_res_1920 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_1920 = pygame.transform.scale(option_button_res_1920, (40, 40))
    elif SCREEN_X == 1920:
        option_button_res_1920 = pygame.image.load("assets/buttons/button-windows-options/res-box-marked.png")
        option_button_res_1920 = pygame.transform.scale(option_button_res_1920, (40, 40))
        #clear others
        option_button_res_800 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_800 = pygame.transform.scale(option_button_res_800, (40, 40))
        option_button_res_1280 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_1280 = pygame.transform.scale(option_button_res_1280, (40, 40))
    elif fullscreen:
        option_box_fullscreen = pygame.image.load("assets/buttons/button-windows-options/res-box-marked.png")
        option_box_fullscreen = pygame.transform.scale(option_box_fullscreen, (40, 40))
        option_button_res_800 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_800 = pygame.transform.scale(option_button_res_800, (40, 40))
        option_button_res_1280 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_1280 = pygame.transform.scale(option_button_res_1280, (40, 40))
        option_button_res_1920 = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
        option_button_res_1920 = pygame.transform.scale(option_button_res_1920, (40, 40))


def difficulty_set(collid=False):
    global option_button_box_easy, option_button_box_medium, option_button_box_hard, difficulty, time_to_same

    if collid:
        if option_button_box_easy_rect.collidepoint(event.pos):
            difficulty = "easy"
            time_to_same = difficulty_time[difficulty]
            option_button_box_easy = pygame.image.load("assets/buttons/button-windows-options/mark-box.png")
            option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
            #clear others boxs
            option_button_box_medium = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
            option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
            option_button_box_hard = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
            option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40,40))
        if option_button_box_medium_rect.collidepoint(event.pos):
            difficulty = "medium"
            time_to_same = difficulty_time[difficulty]
            option_button_box_medium = pygame.image.load("assets/buttons/button-windows-options/mark-box.png")
            option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
            #clear others boxs
            option_button_box_easy = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
            option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
            option_button_box_hard = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
            option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40,40))
        if option_button_box_hard_rect.collidepoint(event.pos):
            difficulty = "hard"
            time_to_same = difficulty_time[difficulty]
            option_button_box_hard = pygame.image.load("assets/buttons/button-windows-options/mark-box.png")
            option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40,40))
            #clear others boxs
            option_button_box_medium = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
            option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
            option_button_box_easy = pygame.image.load("assets/buttons/button-windows-options/box-transparent.png")
            option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
        dict_save["difficulty"] = difficulty
        dict_save["timesame"] = time_to_same
        save(dict_save, "config.json")
        return
    if difficulty == "easy":
        option_button_box_easy = pygame.image.load("assets/buttons/button-windows-options/easy-box-marked.png")
        option_button_box_easy = pygame.transform.scale(option_button_box_easy, (40, 40))
    if difficulty == "medium":
        option_button_box_medium = pygame.image.load("assets/buttons/button-windows-options/medium-box-marked.png")
        option_button_box_medium = pygame.transform.scale(option_button_box_medium, (40, 40))
    if difficulty == "hard":
        option_button_box_hard = pygame.image.load("assets/buttons/button-windows-options/hard-box-marked.png")
        option_button_box_hard = pygame.transform.scale(option_button_box_hard, (40, 40))
    

def loading_time():
    global time_loading, game_run, loading, word, input_active

    for i in range(1, 4):
        time_loading = i
        sleep(1.3)
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
    global y_bg1, y_bg2

    while True:
        if not program_run:
            break
        if game_run:
            y_bg1 += 1
            sleep(0.01)
            if y_bg1 == SCREEN_Y:
                y_bg1 = 0
        elif game_run == False and loading == False:
            y_bg2 += 1
            sleep(0.01)
            if y_bg2 >= SCREEN_Y:
                y_bg2 = 0

Thread(target=move_bg).start()


#hit word info
def txt_info_see():
    list_words = list_words_same[::-1]
    list_dec = list_dec_time[::-1]
    for i, word in enumerate(list_words):
        info = font.render(f"{word}    -{list_dec[i]}s", True, (255, 255, 255))
        screen.blit(info, (SCREEN_X / 2- 100, SCREEN_Y / 2 + 50 + pos[i]))

    
#time to hit te word
def time_run():
    global time, dec_time

    while True:
        if not program_run:
            break
        if game_run:
            time += 1
            sleep(1)
            if dec_time:
                time += -dec_time
                dec_time = False
            if time == time_to_same:
                break
        else:
            break
        
#run game
while True:
    if game_run == False and loading == False:
        screen.fill((0,0,0))
        screen.blit(bg_start, (0,y_bg2))
        screen.blit(bg_start1, (0,y_bg2 - SCREEN_Y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_start_menu.collidepoint(event.pos) and option_state == False and about_state == False:
                    loading = True
                    Thread(target=loading_time).start()
                    Thread(target=txt_str_loading).start()
                if rect_options_menu.collidepoint(event.pos):
                    option_state = True
                if exit_option_window_rect.collidepoint(event.pos):
                    option_state = False
                    about_state = False
                if rect_about_menu.collidepoint(event.pos) and option_state == False:
                    about_state = True
                if option_state and about_state == False:
                    difficulty_set(True)
                    resolution_set(True)

        txt_heading = font_heading.render("Tyfast", True, (82, 39, 39))
        screen.blit(start_menu, rect_start_menu)
        screen.blit(options_menu, rect_options_menu)
        screen.blit(about_menu, rect_about_menu)
        screen.blit(txt_heading, (SCREEN_X /2 - int(txt_heading.get_rect()[2]) + 130, SCREEN_Y / 2 - 250))
        if option_state:
            txt_dificulty = font_options.render("Difficulty", True, (255, 255, 255))
            txt_easy = font_box_choice.render("Easy", True, (0, 255, 0))
            txt_medium = font_box_choice.render("Medium", True, (226, 247, 18))
            txt_hard = font_box_choice.render("Hard", True, (255, 0, 0))
            txt_resolution = font_options.render("Resolution", True, (255, 255, 255))
            txt_800 = font_box_choice.render("800x600", True, (200, 200, 200))
            txt_1280 = font_box_choice.render("1280x720", True, (200, 200, 200))
            txt_1920 = font_box_choice.render("1920x1080", True, (200, 200, 200))
            txt_fullscreen = font_box_choice.render("Fullscreen", True, (200, 200, 200))
            screen.blit(option_window, option_window_rect)
            screen.blit(exit_option_window, (option_window_rect.x + 35, option_window_rect.y + 30))
            screen.blit(txt_dificulty, (window_lose_rect.x - 5, window_lose_rect.y + 80))
            screen.blit(txt_hard, (window_lose_rect.x + 416, window_lose_rect.y + 82))
            screen.blit(option_button_box_hard, option_button_box_hard_rect)
            screen.blit(txt_medium, (window_lose_rect.x + 288, window_lose_rect.y + 82))
            screen.blit(option_button_box_medium, option_button_box_medium_rect)
            screen.blit(txt_easy, (window_lose_rect.x + 187, window_lose_rect.y + 82))
            screen.blit(option_button_box_easy, option_button_box_easy_rect)
            screen.blit(txt_resolution, (window_lose_rect.x - 5, window_lose_rect.y + 150))
            screen.blit(txt_800, (window_lose_rect.x + 130, window_lose_rect.y + 152))
            screen.blit(option_button_res_800, option_button_res_800_rect)
            screen.blit(txt_1280, (window_lose_rect.x + 248, window_lose_rect.y + 152))
            screen.blit(option_button_res_1280, option_button_res_1280_rect)
            screen.blit(txt_1920, (window_lose_rect.x + 372, window_lose_rect.y + 152))
            screen.blit(option_button_res_1920, option_button_res_1920_rect)
            screen.blit(txt_fullscreen, (window_lose_rect.x + 130, window_lose_rect.y + 202))
            screen.blit(option_box_fullscreen, option_box_fullscreen_rect)
            difficulty_set()
            resolution_set()
        if about_state:
            txt_about_game = font_about_window.render("In this game you have to get the word right before it ", True, (255, 255, 255))
            txt_about_game1 = font_about_window.render("reaches the selected time.", True, (255, 255, 255))
            txt_about_me = font_about_window.render("See more about me:", True, (255, 255, 255))
            # https://github.com/ratohg
            txt_about_github = font_about_window.render("GitHub: https://github.com/ratohg", True, (51, 51, 51))
            txt_about_replit = font_about_window.render("Replit: https://replit.com/@ratohg", True, (43, 50, 69))
            screen.blit(about_window, about_window_rect)
            screen.blit(exit_option_window, (about_window_rect.x + 35, about_window_rect.y + 30))
            screen.blit(txt_about_game, (about_window_rect.x + 50, about_window_rect.y + 100))
            screen.blit(txt_about_game1, (about_window_rect.x + 50, about_window_rect.y + 123))
            screen.blit(txt_about_me, (about_window_rect.x + 50, about_window_rect.y + 250))
            screen.blit(txt_about_github, (about_window_rect.x + 50, about_window_rect.y + 273))
            screen.blit(txt_about_replit, (about_window_rect.x + 50, about_window_rect.y + 293))

        pygame.display.flip()
        clock.tick(75)
    #in game
    elif game_run:
        screen.fill((0,0,0))
        screen.blit(bg1, (0, y_bg1))
        screen.blit(bg1, (0, y_bg1 - SCREEN_Y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_run = False
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
                if button_exit_rect.collidepoint(event.pos):
                    time = 0
                    points = 0
                    text = ""
                    list_words_same.clear()
                    list_dec_time.clear()
                    game_run = False
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
                            last_max_points = max_score(difficulty)
                            print(last_max_points)
                            word = choice(list(english_words_set))
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode.strip()
        txt_surface = font.render(text, True, (255, 255, 255))
        txt_word = font.render(word, True, (255, 255, 255))
        txt_lose = font_lose.render("YOU'RE LOSE", True, (255, 255, 255))
        txt_last_points = font_last_points.render(f"Points: {points} in {difficulty}", True, (255, 255, 255))
        txt_time = font_timer.render(str(time), True, (48, 48, 48))
        txt_points = font_point.render(str(points), True, (48, 48, 48))
        txt_last_max_points = font_last_max_points.render(f"Max points in Easy:{last_max_points['easy']} Medium:{last_max_points['medium']} Hard:{last_max_points['hard']}", True, (255, 255, 255))
        width_box = max(450, txt_surface.get_width() + 10)
        input_box_rect.w = width_box
        screen.blit(input_box, input_box_rect)
        screen.blit(txt_surface, (input_box_rect.x + 5, input_box_rect.y + 10))
        screen.blit(txt_time, (SCREEN_X/2 - int(txt_time.get_rect()[2]) + 45, SCREEN_Y/2 - 350))
        screen.blit(info_box_word, info_box_word_rect)
        screen.blit(txt_word, (int(info_box_word_rect[0])+70, int(info_box_word_rect[1])+45))
        txt_points = pygame.transform.scale(txt_points, (x_points, y_points))
        screen.blit(txt_points, (SCREEN_X - 100, 5))
        screen.blit(button_exit, button_exit_rect)
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
            screen.blit(txt_last_points, (SCREEN_X/2 - 115, SCREEN_Y/2 - 30))
            screen.blit(txt_last_max_points, (SCREEN_X/2 - 205, SCREEN_Y/2 + 20))
            #print(window_lose_rect.x, window_lose_rect.y)  
        pygame.display.flip()
        clock.tick(75)
    elif loading:
        screen.fill((0,0,0))
        screen.blit(bg_loading, (0, 0))
        txt_loading = font_timer.render(str(time_loading), True, (255, 255, 255))
        txt_loading_info = font_loading_info.render(f"Starting game in{txt_loading_info_str}", True, (255, 255, 255))
        screen.blit(txt_loading, (SCREEN_X/2 - 40, SCREEN_Y/2 - 130))
        screen.blit(txt_loading_info, (SCREEN_X/2 - 120, SCREEN_Y/2 - 160))
        pygame.display.flip()
        clock.tick(75)