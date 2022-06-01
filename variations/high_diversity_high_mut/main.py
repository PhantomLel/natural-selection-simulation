import time
import random
import pygame as pg
from Food import Food
from Organism import Organism, font
from extras import gather_data, produce_graph


def start_sim(food_amount=100):
    """Create some starting organisms and food"""
    organisms = [
        Organism(
            (random.randint(100, 900), random.randint(100, 650)),
            color,
            round(random.uniform(3.5, 6), 3),
        )
        for color in [(128, 128, 128) for _ in range(1)]
    ]
    foods = [
        Food((random.randint(20, 40), random.randint(20, 40)))
        for _ in range(food_amount)
    ]
    return organisms, foods


BLACK = (0, 0, 0)

# initialize pg
pg.init()
screen_size = (900, 700)

# create a window
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("pg Test")

# clock is used to set a max fps
clock = pg.time.Clock()

# dict to keep track of all stats and data
data = {
    "start_time": time.time(),
    "frames": [],
    "vals": {
        "population": [],
        "avg_gen": [],
        "avg_mut": [],
        "food_available": [],
        "highest_gen": [],
        "avg_speed": [],
        "avg_max_age": [],
        "avg_litter_size": [],
    },
}

running = True
paused = False
frame_rate = 60
frames_passed = 0

organisms, foods = start_sim()


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            # restart the simulation
            if event.key == pg.K_r:
                organisms, foods = start_sim()
            # pause the simulation
            if event.key == pg.K_p:
                paused = not paused
            # arrows control framerate
            if event.key == pg.K_RIGHT:
                frame_rate += 15
            if event.key == pg.K_LEFT:
                if frame_rate > 15:
                    frame_rate -= 15

    if not paused:
        frames_passed += 1
        if frames_passed % 100 == 0:
            gather_data(data, frames_passed, organisms, foods)
        screen.fill(BLACK)
        # renders for population and framerate
        organism_render = font.render(
            f"# Organisms: {len(organisms)}", True, (255, 255, 255)
        )
        frame_rate_render = font.render(
            f"FPS: {round(clock.get_fps())}/{frame_rate}", True, (255, 255, 255)
        )
        screen.blit(organism_render, (10, 10))
        screen.blit(frame_rate_render, (10, 30))

        # organisms have all gone extinct
        if len(organisms) == 0:
            running = False

        if random.randint(1, 6) == 2:
            for _ in range(random.randint(1, 4)):
                foods.append(Food((random.randint(10, 20), random.randint(10, 20))))

        for food in foods:
            if food.eaten:
                foods.remove(food)
                continue
            food.summon(screen)

        for organism in reversed(organisms):

            if organism.age > organism.max_age:
                organisms.remove(organism)
                continue
            # if the organsim has no target food, target the closest food
            if organism.target_food is None:
                organism.target(foods)
            organism.move(foods)
            organism.summon(screen)
            # check if organism has eaten enough to reproduce
            if (
                organism.food_eaten >= organism.reproduce_food
                and len(organisms) < 10000
            ):
                for i in range(random.randint(0, organism.litter_size)):
                    # reproduce
                    organisms.append(organism.reproduce())
                    
                organism.food_eaten = 0
            organism.age += 1

    pg.display.flip()
    clock.tick(frame_rate)

produce_graph(data)

pg.quit()
