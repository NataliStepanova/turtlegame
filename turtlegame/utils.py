import random


def take_random_coordinate(screen, edge_lenght, cherepashka_position):
    random_coord = random.randint(-screen/2, screen/2 - edge_lenght)
    cherepashka_min = cherepashka_position - 80
    cherepashka_max = cherepashka_position + 80
    if random_coord < cherepashka_min or random_coord > cherepashka_max:
        return random_coord
    else:
        return take_random_coordinate(screen, edge_lenght, cherepashka_position)
