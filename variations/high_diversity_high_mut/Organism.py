import math
import random
import pygame as pg
import numpy as np

pg.init()
font = pg.font.SysFont(None, 24)


class Organism:
    def __init__(
        self,
        pos,
        color,
        speed,
        gen=0,
        color_weights=[random.randint(0, 5) for _ in range(3)],
        max_age=random.randint(100, 400),
        litter_size=random.randint(2, 4),
        size=(20, 20),
    ) -> None:
        self.COLOR = color
        self.gen = gen
        # the render that is put on the middle of the organism
        self.gen_render = font.render(str(self.gen), True, (255, 255, 255))

        self.speed = speed
        # number of frames that the organism has been alive
        self.age = 0
        # age of death
        self.max_age = max_age if max_age < 1200 else random.randint(200, 300)

        self.food_eaten = 0
        # amount of food eaten before reproducing
        self.reproduce_food = random.randint(2, 4)
        # max amount of children on reproduction
        self.litter_size = litter_size
        self.target_food = None
        # weights for color change on reproduction between 2 and 15
        self.color_weights = color_weights

        self.pos = pg.Rect(0, 0, *size)
        self.pos.center = pos
        self.regulate_stats()

    def regulate_stats(self):
        pass

    def summon(self, screen):
        pg.draw.rect(screen, self.COLOR, self.pos)
        screen.blit(
            self.gen_render,
            (
                self.pos.centerx - self.gen_render.get_width() / 2,
                self.pos.centery - self.gen_render.get_height() / 2,
            ),
        )

    def move(self, foods):
        if self.target_food not in foods or self.target_food.eaten:
            self.target_food = None
            return
        dx = self.target_food.pos.centerx - self.pos.centerx
        dy = self.target_food.pos.centery - self.pos.centery
        d = math.hypot(dx, dy)

        # check if the organism is close enough to eat
        if not self.pos.collidepoint(self.target_food.pos.center):
            self.pos.centery += dy / d * self.speed
            self.pos.centerx += dx / d * self.speed

        else:
            self.eat()

    def eat(self):
        self.target_food.eaten = True
        self.target_food = None
        self.food_eaten += 1

    def reproduce(self):

        # create the new organism's color based on the parent's color plus a random number generated from the color_weights
        color = [
            i + random.randint(-cw, cw) for i, cw in zip(self.COLOR, self.color_weights)
        ]
        color = np.clip(color, 0, 255)
        # create new color weights based on parent's color weights plus a random number
        color_weights = [
            abs(random.randint(cw - 1, cw + 1)) for cw in self.color_weights
        ]
        # clip color weights to be between 0 and 16
        color_weights = np.clip(color_weights, 0, 16)

        # generate new litter size based on parents litter size plus a random number 
        litter_size = abs(random.randint(self.litter_size - 1, self.litter_size + 1))
        litter_size = np.clip(litter_size, 0, 11)


        return Organism(
            self.pos.topleft,
            color=color,
            color_weights=color_weights,
            speed=round(random.uniform(self.speed - 7, self.speed + 7), 3),
            gen=self.gen + 1,
            max_age=random.randint(self.max_age - 100, self.max_age + 100),
            litter_size=litter_size
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
