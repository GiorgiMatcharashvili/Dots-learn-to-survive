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
        # Find all occupied good points
        occupied_points = []
        for good_point in self.good_points:
            for obj in self.objs:
                dist = math.dist(good_point.pos, obj.pos)
                if dist < 5:
                    occupied_points.append(good_point)
                    break

        # Move all the dots
        for obj in self.objs:
            positions = []
            for diff_obj in self.objs:
                if obj != diff_obj:
                    positions.append(Point(*diff_obj.pos, 1))
            obj.move(positions, self.bad_points, list(set(self.good_points) - set(occupied_points)))

        self.check()

    def check(self):
        # Check if they are alive
        for obj in self.objs:
            if obj.is_dead():
                self.bad_points.append(Point(*obj.pos, -1))
                self.objs.remove(obj)
                self.death_time = dt.now()

        population = len(self.objs)

        # show population
        self.board.show_text("Population: " + str(population),
                             (-1 * self.RESOLUTION[0] / 2, self.RESOLUTION[0] / 2))

        # Check if they should regenerate
        time_limit = 20 if population == self.POPULATION else 10

        if self.death_time:
            time_dilation = dt.now() - self.death_time
            if float(time_dilation.total_seconds()) > time_limit:
                self.regeneration()

    def regeneration(self):
        self.save_data()
        self.objs = [Dot(*self.start_pos) for _ in range(self.POPULATION)]

        self.death_time = dt.now()

    def calculate_good_points(self):
        current_population = len(self.objs)

        good_points_amount = int(current_population / 10)

        good_points = sorted(self.objs, key=self.sort_key_func)[:good_points_amount]
        for good_point in good_points:
            self.good_points.append(Point(*good_point.pos, 1))

    def sort_key_func(self, element):
        for good_point in self.good_points:
            if math.dist(good_point.pos, element.pos) < 25:
                if element.dist_to_border <= good_point.dist_to_border:
                    self.good_points.remove(good_point)
                    return element.dist_to_border
                return 1000

        return element.dist_to_border

    def save_data(self):
        with open("./data.json", "r+") as f:
            data = json.load(f)

            try:
                # Add bad points
                data[str(self.POPULATION)]["bad_points"] = list({bad_point.pos for bad_point in self.bad_points})

                # Add good points
                self.calculate_good_points()
                data[str(self.POPULATION)]["good_points"] = list({good_point.pos for good_point in self.good_points})

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
