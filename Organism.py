import math
import time
import random
import pygame as pg

pg.init()
font = pg.font.SysFont(None, 24)


class Organism:
    def __init__(self, pos, color, speed, gen=0, max_age=random.randint(5, 9)) -> None:
        self.COLOR = color
        self.gen = gen
        self.gen_render = font.render(str(self.gen), True, (255, 255, 255))
        self.speed = speed
        self.age = 0
        self.born = time.time()
        # age of death
        self.max_age = max_age

        self.food_eaten = 0
        # amount of food eaten before reproducing
        self.reproduce_food = random.randint(3, 5)
        self.target_food = None

        self.pos = pg.Rect(0, 0, 25, 25)
        self.pos.center = pos

    def summon(self, screen):
        self.age = time.time()
        pg.draw.rect(screen, self.COLOR, self.pos)
        screen.blit(
            self.gen_render,
            (
                self.pos.centerx - self.gen_render.get_width() / 2,
                self.pos.centery - self.gen_render.get_height() / 2,
            ),
        )

    def move(self, foods):
        if self.target_food not in foods:
            self.target_food = None
            return
        dx = self.target_food.pos.centerx - self.pos.centerx
        dy = self.target_food.pos.centery - self.pos.centery
        d = math.hypot(dx, dy)

        if not self.pos.colliderect(self.target_food.pos):
            self.pos.centery += dy / d * self.speed
            self.pos.centerx += dx / d * self.speed
        else:
            self.eat(self.target_food)

    def eat(self, food):
        self.target_food.eaten = True
        self.target_food = None
        self.food_eaten += 1

    def reproduce(self):
        return Organism(
            self.pos.center,
            self.COLOR,
            random.uniform(self.speed - 0.1, self.speed + 0.1),
            gen=self.gen + 1,
            max_age=random.randint(self.max_age - 2, self.max_age+ 2),
        )

    def find_dist(self, food):
        dx = abs(food.pos.centerx - self.pos.centerx)
        dy = abs(food.pos.centery - self.pos.centery)
        return math.sqrt(dx**2 + dy**2)

    def target(self, foods):
        closest_food = None
        food_dist = None
        for food in foods:
            if closest_food is None:
                closest_food = food
                food_dist = self.find_dist(food)
                continue
            d = self.find_dist(food)
            if d <= food_dist:
                closest_food = food
                food_dist = d
        self.target_food = closest_food
