import json
from datetime import datetime as dt
import pygame
import math
import random


class Dot:
    def __init__(self, position, color, surface, resolution):
        self.position = position
        self.color = color
        self.surface = surface
        self.resolution = resolution
        self.radius = 4
        self.last_position = None

        self.draw()

    def move(self, positions, bad_points, good_points):
        direction = self.get_direction(positions + bad_points, good_points)
        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])

        self.last_position = self.position
        self.position = new_position

        self.draw()

    def is_dead(self):
        if self.position[0] not in range(0, 501) or self.position[1] not in range(0, 501):
            return True
        return False

    def draw(self):
        pygame.draw.circle(self.surface, self.color, self.position, self.radius)

    def get_direction(self, bad_points, good_points):
        directions = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1)]

        if self.last_position:
            direction_to_last = (self.last_position[0] - self.position[0], self.last_position[1] - self.position[1])
            directions.remove(direction_to_last)

        worst_bad, best_bad = self.analise_bad_points(bad_points, directions)
        worst_good, best_good = self.analise_good_points(good_points, directions)

        if worst_good and best_good:
            if worst_bad[0] != best_good[0]:
                return best_good[0]
            else:
                if best_good[1] < worst_bad[1]:
                    return best_good[0]
                else:
                    return best_bad[0]
        else:
            return best_bad[0]

    def analise_bad_points(self, bad_points, directions):
        # Find the closest bad point
        points_lst = [(bad_point, math.dist(self.position, bad_point)) for bad_point in bad_points]
        point, distance = sorted(points_lst, key=lambda l: l[1])[0]

        # Find the worst and the best directions
        data = [(d, math.dist((self.position[0] + d[0], self.position[1] + d[1]), point)) for d in directions]
        sorted_data = sorted(data, key=lambda l: l[1])

        if distance == 0:
            return random.choice(sorted_data[:4]), random.choice(sorted_data[4:])

        # First one is the worst direction
        # Second one is the best direction
        return sorted_data[0], sorted_data[-1]

    def analise_good_points(self, good_points, directions):
        if not good_points:
            return False, False

        good_points = [(good_point[0], good_point[1]) for good_point in good_points]

        # Find the closest good point
        points_lst = [(good_point, math.dist(self.position, good_point)) for good_point in good_points]
        point, distance = sorted(points_lst, key=lambda l: l[1])[0]

        # Find the worst and the best directions
        data = [(d, math.dist((self.position[0] + d[0], self.position[1] + d[1]), point)) for d in directions]
        sorted_data = sorted(data, key=lambda l: l[1], reverse=True)

        if distance == 0:
            return random.choice(sorted_data[:4]), random.choice(sorted_data[4:])

        # First one is the worst direction
        # Second one is the best direction
        return sorted_data[0], sorted_data[-1]


class Dots:
    def __init__(self, population, position, color, game):
        self.generation_into = (position, color, game.surface, game.resolution)

        self.default_population = population
        self.game = game

        self.bad_points = []
        self.good_points = []
        self.death_time = None

        self.load_data()

        self.objs = [Dot(*self.generation_into) for _ in range(self.default_population)]

    def move(self):
        # Move all the dots
        for obj in self.objs:
            positions = []
            for obj1 in self.objs:
                if obj != obj1:
                    positions.append(obj1.position)
            obj.move(positions, self.bad_points, self.good_points)

        self.check()

    def check(self):
        # Check if they are alive
        for obj in self.objs:
            if obj.is_dead():
                self.bad_points.append(obj.position)
                self.objs.remove(obj)
                self.death_time = dt.now()

        # show population
        self.game.text("Population: " + str(len(self.objs)))

        # Check if they should regenerate
        if self.death_time:
            time_dilation = dt.now() - self.death_time
            if float(time_dilation.total_seconds()) > 10:
                self.regeneration()

    def regeneration(self):
        self.save_data()
        self.objs = [Dot(*self.generation_into) for _ in range(self.default_population)]

        self.death_time = dt.now()

    def calculate_good_points(self):
        good_points = []
        current_population = len(self.objs)

        good_points_amount = int(current_population / 10)

        for obj in self.objs:
            pos = obj.position

            border_points = [(self.game.resolution[0], pos[1]), (pos[0], self.game.resolution[1]),
                             (self.game.resolution[0], pos[1]), (pos[1], self.game.resolution[1])]
            closest_to_border = min([math.dist(pos, each) for each in border_points])

            if len(good_points) < good_points_amount:
                good_points.append((*pos, closest_to_border))
                continue

            for each in sorted(good_points, key=lambda l: l[1], reverse=True):
                if closest_to_border < each[1]:
                    good_points.remove(each)
                    good_points.append((*pos, closest_to_border))
                    break

        self.good_points += good_points

    def save_data(self):
        with open("data.json", "r+") as f:
            data = json.load(f)

            try:
                # Add bad points
                data[str(self.default_population)]["bad_points"] = list(set(self.bad_points))

                # Add good points
                self.calculate_good_points()
                data[str(self.default_population)]["good_points"] = list(set(self.good_points))
            except KeyError:
                data[self.default_population] = {"bad_points": self.bad_points,
                                                 "good_points": self.calculate_good_points()}

            f.seek(0)

            json.dump(data, f, indent=4)

    def load_data(self):
        with open("data.json", "r+") as f:
            data = json.load(f)
            try:
                self.bad_points = data[str(self.default_population)]["bad_points"]
                self.bad_points = [tuple(point) for point in self.bad_points]

                self.good_points = data[str(self.default_population)]["good_points"]
                self.good_points = [tuple(point) for point in self.good_points]

            except KeyError:
                pass
