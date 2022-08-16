import pygame

pygame.init()
SCREEN_X = 800
SCREEN_Y = 600
screen = pygame.display.set_mode([SCREEN_X, SCREEN_Y])
input_box = pygame.Rect(SCREEN_X/2-150, SCREEN_Y/2-40, SCREEN_X/2-50, 32)
clock = pygame.time.Clock()
input_active = False
text = ""
font = pygame.font.Font(None, 32)
x_inputbox = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    text = ""
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    txt_surface = font.render(text, True, (255, 255, 255))
    width_box = max(250, txt_surface.get_width() + 10)
    input_box.w = width_box
    screen.fill((0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.draw.rect(screen, (255, 0, 0), input_box, 1)
    pygame.display.flip()
    clock.tick(30)