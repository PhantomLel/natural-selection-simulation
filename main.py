import random
import pygame as pg
from Food import Food
from Organism import Organism


def start_sim(food_amount=300):
    organisms = [
        Organism(
            (random.randint(100, 900), random.randint(100, 650)),
            color,
            round(random.uniform(3, 4), 3),
        )
        for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    ]
    foods = [Food((random.randint(20, 40), random.randint(20, 40))) for _ in range(food_amount)]
    return organisms, foods


BLACK = (0, 0, 0)

# initialize pg
pg.init()
screen_size = (1000, 700)

# create a window
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("pg Test")

# clock is used to set a max fps
clock = pg.time.Clock()

running = True
paused = False

organisms, foods = start_sim()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_r:
                organisms, foods = start_sim()
            if event.key == pg.K_p:
                paused = not paused

    if not paused:
        screen.fill(BLACK)

        if random.randint(1, 30) == 2:
            foods.append(Food((random.randint(20, 40), random.randint(20, 40))))

        for food in foods:
            if food.eaten:
                foods.remove(food)
            food.summon(screen)

        for organism in organisms:
            if organism.age - organism.born > organism.max_age:
                organisms.remove(organism)

            if organism.target_food is None:
                organism.target(foods)
            else:
                organism.move(foods)
            organism.summon(screen)
            if organism.food_eaten >= organism.reproduce_food:
                organisms.append(organism.reproduce())
                organism.food_eaten = 0

    # flip() updates the screen to make our changes visible
    pg.display.flip()

    # how many updates per second
    clock.tick(60)

pg.quit()
