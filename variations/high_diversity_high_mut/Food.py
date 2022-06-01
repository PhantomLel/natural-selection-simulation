import pygame as pg
import random


class Food:
    def __init__(self, size) -> None:
        self.size = size
        self.pos = pg.Rect(0, 0, *size)
        self.pos.center = (random.randint(50, 850), random.randint(50, 600))
        self.eaten = False

    def summon(self, screen):
        pg.draw.rect(screen, (90, 200, 150), self.pos)
