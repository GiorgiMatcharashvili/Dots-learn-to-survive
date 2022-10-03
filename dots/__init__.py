import json
import math
from datetime import datetime as dt
from .dot import Dot
from board import Base
from .point import Point


class Dots(Base):
    def __init__(self, board):
        self.start_pos = (0, 0)

        self.bad_points = []
        self.good_points = []
        self.death_time = None

        self.board = board

        self.load_data()

        self.objs = [Dot(*self.start_pos) for _ in range(self.POPULATION)]

    def move(self):
        # Move all the dots
        for obj in self.objs:
            positions = []
            for obj1 in self.objs:
                if obj != obj1:
                    positions.append(Point(*obj1.pos, 1))
            obj.move(positions, self.bad_points, self.good_points)

        self.check()

    def check(self):
        # Check if they are alive
        for obj in self.objs:
            if obj.is_dead():
                self.bad_points.append(Point(*obj.pos, -1))
                self.objs.remove(obj)
                self.death_time = dt.now()

        # show population
        self.board.show_text("Population: " + str(len(self.objs)), (-1 * self.RESOLUTION[0]/2, self.RESOLUTION[0]/2))

        # Check if they should regenerate
        if self.death_time:
            time_dilation = dt.now() - self.death_time
            if float(time_dilation.total_seconds()) > 10:
                self.regeneration()

    def regeneration(self):
        self.save_data()
        self.objs = [Dot(*self.start_pos) for _ in range(self.POPULATION)]

        self.death_time = dt.now()

    def calculate_good_points(self):
        good_points = []
        current_population = len(self.objs)

        good_points_amount = int(current_population / 10)

        for obj in self.objs:
            pos = obj.pos

            border_points = [(self.RESOLUTION[0], pos[1]), (pos[0], self.RESOLUTION[1]),
                             (self.RESOLUTION[0], pos[1]), (pos[1], self.RESOLUTION[1])]
            closest_to_border = min([math.dist(pos, each) for each in border_points])

            if len(good_points) < good_points_amount:
                good_points.append(Point(*pos, 1))
                continue

            for each in sorted(good_points, key=lambda l: l.dist_to_border, reverse=True):
                if closest_to_border < each.dist_to_border:
                    good_points.remove(each)
                    good_points.append(Point(*pos, 1))
                    break

        self.good_points += good_points

    def save_data(self):
        with open("./data.json", "r+") as f:
            data = json.load(f)

            try:
                # Add bad points
                data[str(self.POPULATION)]["bad_points"] = list(set([bad_point.pos for bad_point in self.bad_points]))

                # Add good points
                self.calculate_good_points()
                data[str(self.POPULATION)]["good_points"] = list(set([good_point.pos for good_point in self.good_points]))

            except KeyError:
                # Add good points
                self.calculate_good_points()
                data[self.POPULATION] = {"bad_points": [bad_point.pos for bad_point in self.bad_points],
                                         "good_points": [good_point.pos for good_point in self.good_points]}

            f.seek(0)

            json.dump(data, f, indent=4)

    def load_data(self):
        with open("./data.json", "r+") as f:
            data = json.load(f)
            try:
                self.bad_points = data[str(self.POPULATION)]["bad_points"]
                self.bad_points = [Point(*bad_point, -1) for bad_point in self.bad_points]

                self.good_points = data[str(self.POPULATION)]["good_points"]
                self.good_points = [Point(*good_point, 1) for good_point in self.good_points]

            except KeyError:
                pass
