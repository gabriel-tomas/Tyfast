from threading import Thread
from tkinter import SCROLL
import pygame
from time import sleep
from english_words import english_words_set
from random import choice
import sys


pygame.init()
SCREEN_X = 800
SCREEN_Y = 600
screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
input_box = pygame.Rect(SCREEN_X/2-130, SCREEN_Y/2-80, SCREEN_X/2-50, 32)
clock = pygame.time.Clock()
input_active = False
text = ""
font = pygame.font.Font(None, 32)
x_inputbox = 300
loading_bar = pygame.image.load("Tyfast/bar.png")
loading_bar = pygame.transform.scale(loading_bar, (80, 50))
rect_bar = loading_bar.get_rect(center=(60, 560))
button_start = pygame.image.load("Tyfast/button.png")
button_start = pygame.transform.scale(button_start, (80, 50))
rect_button = button_start.get_rect(center=(740, 560))
txt_time = font.render("0", True, (255, 255, 255))
word = None
time = 0
dec_time = 0
time_to_same = 10

def txt_time_see():
    pass

def time_run():
    global txt_time, time, dec_time

    while True:
        txt_time = font.render(str(time + 1), True, (255, 255, 255))
        time += 1
        print(time)
        sleep(1)
        if dec_time:
            time += -dec_time
            dec_time = False
        if time == time_to_same:
            break
        

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
            if rect_button.collidepoint(event.pos):
                time = 0
                word = choice(list(english_words_set))
                #print(word)
                Thread(target=time_run).start()
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    if text.strip() == word and time != time_to_same:
                        if len(word) >= 9:
                            dec_time = 3
                        elif len(word) >= 7:
                            dec_time = 2
                        else:
                            dec_time = 1
                        text = ""
                        word = choice(list(english_words_set))
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    txt_surface = font.render(text, True, (255, 255, 255))
    txt_start = font.render("Start", True, (255, 255, 255))
    txt_word = font.render(word, True, (255, 255, 255))
    txt_lose = font.render("YOU'RE LOSE", True, (255, 0, 0))
    width_box = max(250, txt_surface.get_width() + 10)
    input_box.w = width_box
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    screen.blit(loading_bar, rect_bar)
    screen.blit(txt_time, (60, 560))
    screen.blit(button_start, rect_button)
    screen.blit(txt_start, (710, 550))
    screen.blit(txt_word, (SCREEN_X / 2 - 50, SCREEN_Y / 2 - 150))
    if time == time_to_same:
        screen.blit(txt_lose, (SCREEN_X/2 - 80, SCREEN_Y/2))
    pygame.draw.rect(screen, (255, 0, 0), input_box, 1)
    pygame.display.flip()
    clock.tick(60)