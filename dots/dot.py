import math
import random
from .point import Point


class Dot(Point):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 0)

        self.last_pos = None

        self.board_ranges = (range(int(-1 * (self.RESOLUTION[0] / 2)), int((self.RESOLUTION[0] / 2) + 1)),
                             range(int(-1 * (self.RESOLUTION[1] / 2)), int((self.RESOLUTION[1] / 2) + 1)))

    def get_new_pos(self, direction: tuple):
        """ Generates new position using direction """
        return self.pos[0] + direction[0], self.pos[1] + direction[1]

    def move(self, positions: list, bad_points: list, good_points: list):
        """ Makes dot move """
        direction = self.get_direction(positions + bad_points, good_points)
        new_pos = self.get_new_pos(direction)

        self.last_pos = self.pos
        self.pos = new_pos

    def is_dead(self):
        """ Checks if dot is dead """
        if self.pos[0] in self.board_ranges[0] and self.pos[1] in self.board_ranges[1]:
            return False
        return True

    def get_direction(self, bad_points: list, good_points: list):
        """ Sends the best possible direction """
        directions = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1)]

        if self.last_pos:
            direction_to_last = (self.last_pos[0] - self.pos[0], self.last_pos[1] - self.pos[1])
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

    def analise_bad_points(self, bad_points: list, directions: list):
        """ Analyses bad points """
        # Find the closest bad point
        points_lst = [(bad_point, math.dist(self.pos, bad_point.pos)) for bad_point in bad_points]
        point, distance = sorted(points_lst, key=lambda l: l[1])[0]

        # Find the worst and the best directions
        data = [(d, math.dist(self.get_new_pos(d), point.pos)) for d in directions]
        sorted_data = sorted(data, key=lambda l: l[1])

        if distance == 0:
            return random.choice(sorted_data[:4]), random.choice(sorted_data[4:])

        # First one is the worst direction
        # Second one is the best direction
        return sorted_data[0], sorted_data[-1]

    def analise_good_points(self, good_points: list, directions: list):
        """ Analyses good points """
        if not good_points:
            return False, False

        good_points = [(good_point.pos[0], good_point.pos[1]) for good_point in good_points]

        # Find the closest good point
        points_lst = [(good_point, math.dist(self.pos, good_point)) for good_point in good_points]
        point, distance = sorted(points_lst, key=lambda l: l[1])[0]

        # Find the worst and the best directions
        data = [(d, math.dist(self.get_new_pos(d), point)) for d in directions]
        sorted_data = sorted(data, key=lambda l: l[1], reverse=True)

        if distance == 0:
            return random.choice(sorted_data[:4]), random.choice(sorted_data[4:])

        # First one is the worst direction
        # Second one is the best direction
        return sorted_data[0], sorted_data[-1]
