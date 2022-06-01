import time
import matplotlib.pyplot as plt
from Organism import Organism


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


def produce_graph(data):

    for category, val in data["vals"].items():
        plt.plot(data["frames"], val, label=category)
    plt.xlabel("Frames (100's)")
    plt.legend()
    plt.show()
