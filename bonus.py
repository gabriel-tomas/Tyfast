import random, pygame, time
from threading import Thread

class Decrease_time:
    def __init__(self, screenx, screeny):
        self.x = 0
        self.y = -40
        self.run_move = False
        self.width = screenx
        self.height = screeny
        self.run = False
    def set_psimg(self):
        self.time = random.randint(1, 4)
        self.img = pygame.image.load(f"assets/bonus/decrease-{self.time}.png")
        self.x = random.randint(10, self.width)
        print(self.x, self.y)
        self.rect = self.img.get_rect(center=(self.x, self.y))
    def chance_set_bns(self):
        self.chance = random.randint(1, 15)
        print(self.chance)
        if self.chance == 1 and self.run_move == False:
            self.run = True
            self.set_psimg()
            Thread(target=self.move).start()
    def move(self):
        self.run_move = True
        vel = random.randint(2, 3)
        while True:
            self.rect.y += vel
            time.sleep(0.01)
            if self.rect.y >= self.height:
                self.rect.y = -60
                self.run_move = False
                self.run = False
                print("Stoping and breaking loop")
                break
    def blt_img(self, screen):
        screen.blit(self.img, self.rect)
        