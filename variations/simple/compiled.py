import numpy as np
import pygame as pg
import random, math, time
import matplotlib.pyplot as plt

pg.init()
font = pg.font.SysFont(None, 24)


class Organism:
    def __init__(
        self,
        pos,
        color,
        speed,
        gen=0,
        color_weights=[random.randint(0, 255) for _ in range(3)],
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
            litter_size=litter_size,
        )

    def find_dist(self, food):
        # find dist between food and self
        dx = abs(food.pos.centerx - self.pos.centerx)
        dy = abs(food.pos.centery - self.pos.centery)
        return math.sqrt(dx**2 + dy**2)

    def target(self, foods):
        # find the closest food and target it
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


def gather_data(data: dict, frame: int, organisms: Organism, foods: list) -> list:
    data["frames"].append(frame / 100)  # acts as the x-axis for the graph
    data["vals"]["population"].append(len(organisms))
    generation_lst = [org.gen for org in organisms]
    data["vals"]["avg_gen"].append(sum(generation_lst) / len(organisms))
    data["vals"]["highest_gen"].append(max(generation_lst))
    # the difference between 128 (the starting rgb value) and the current value is the mutation value
    data["vals"]["avg_mut"].append(
        sum([abs(128 - i) for org in organisms for i in org.COLOR]) / len(organisms)
    )
    data["vals"]["food_available"].append(len(foods))
    # the average speed of an organism. multiplied by 10 to make the data easier to read on graph
    data["vals"]["avg_speed"].append(
        sum([org.speed * 10 for org in organisms]) / len(organisms)
    )
    # the average max age of organisms
    data["vals"]["avg_max_age"].append(
        sum([org.max_age for org in organisms]) / len(organisms)
    )
    # the average litter size of all the organisms
    data["vals"]["avg_litter_size"].append(
        sum([org.litter_size for org in organisms]) / len(organisms)
    )
    return data


def produce_graph(data):
    # produce the graph containing all the variables
    for category, val in data["vals"].items():
        plt.plot(data["frames"], val, label=category)
    plt.xlabel("Frames (100's)")
    plt.legend()
    plt.show()


class Food:
    def __init__(self, size) -> None:
        self.size = size
        self.pos = pg.Rect(0, 0, *size)
        self.pos.center = (random.randint(50, 850), random.randint(50, 600))
        self.eaten = False

    def summon(self, screen):
        pg.draw.rect(screen, (90, 200, 150), self.pos)


def start_sim(food_amount=100):
    """Create some starting organisms and food"""
    organisms = [
        Organism(
            (random.randint(100, 900), random.randint(100, 650)),
            color,
            round(random.uniform(1, 6), 3),
        )
        for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
    ]
    foods = [
        Food((random.randint(20, 40), random.randint(20, 40)))
        for _ in range(food_amount)
    ]
    return organisms, foods


BLACK = (0, 0, 0)

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
# spawn rate of food
FOOD_RATE = 2

organisms, foods = start_sim()

instructions = font.render(
    f"'p' to pause\nArrow keys to change FR", True, (255, 255, 255)
)

while running:
    # key handling
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
        # gather data every 100 frames
        if frames_passed % 100 == 0:
            data = gather_data(data, frames_passed, organisms, foods)
        screen.fill(BLACK)
        # renders for population and framerate
        organism_render = font.render(
            f"# Organisms: {len(organisms)}", True, (255, 255, 255)
        )
        frame_rate_render = font.render(
            f"FPS: {round(clock.get_fps())}/{frame_rate}", True, (255, 255, 255)
        )
        screen.blit(instructions, (10, 10))
        screen.blit(organism_render, (10, 30))
        screen.blit(frame_rate_render, (10, 50))

        # organisms have all gone extinct
        if len(organisms) == 0:
            running = False


        if random.randint(1, 6) == FOOD_RATE:
            # create some food
            for _ in range(random.randint(1, 4)):
                foods.append(Food((random.randint(10, 20), random.randint(10, 20))))
        # check if a food has been eaten
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
