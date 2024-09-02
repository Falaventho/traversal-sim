import random
import matplotlib.pyplot as plt
from datetime import datetime


class NumberLine:

    def __init__(self, start=0, end=2, starting_position=1):
        self.start = start
        self.end = end
        self.points = []

        if start <= starting_position <= end:
            self.starting_position = starting_position
        else:
            raise ValueError("Starting position" +
                             f"{starting_position} is out of bounds [{start}, {end}]")

    def add_point(self, p):
        if self.start <= p <= self.end:
            self.points.append(p)
        else:
            raise ValueError(
                f"Point {p} is out of bounds [{self.start}, {self.end}]")

    def generate_random_points(self, n) -> list[float]:
        return [random.uniform(self.start, self.end) for _ in range(n)]

    def generate_and_add_random_points(self, n):
        points = self.generate_random_points(n)
        for point in points:
            self.add_point(point)

    def find_max_point(self):
        return max(self.points)

    def find_min_point(self):
        return min(self.points)

    def find_best_path(self) -> float:
        max_point = max(self.points)
        min_point = min(self.points)

        dist_to_max = abs(self.starting_position - max_point)
        dist_to_min = abs(self.starting_position - min_point)

        first_traversal = min(dist_to_max, dist_to_min)
        second_traversal = abs(max_point - min_point)

        return first_traversal + second_traversal

    def display(self):
        print(f"Number line segment: [{self.start}, {self.end}]")
        print(f"Points on the line segment: {sorted(self.points)}")
        print(f"Optimal path from starting position " +
              f"{self.starting_position} requires a traversal of {self.find_best_path()} to contact all points.")

    def visualize(self, label=False):
        fig, ax = plt.subplots()

        # Draw the number line
        ax.plot([self.start, self.end], [0, 0], 'k-', lw=2)  # Solid black line

        # Mark the start_position
        ax.plot(self.starting_position, 0, 'bo')
        ax.text(self.starting_position, -0.02,
                'Start', ha='center', fontsize=10)

        # Plot each point
        for point in self.points:
            ax.plot(point, 0, 'ro')  # Red circle for each point
            # Label the point with its value
            if label:
                ax.text(point, 0.02, f'{point:.2f}', ha='center', fontsize=10)

        # Set the limits and remove y-axis for clarity
        ax.set_xlim(self.start - 0.1, self.end + 0.1)
        ax.get_yaxis().set_visible(False)

        # Add labels and title
        ax.set_xlabel('Number Line')
        ax.set_title('Number Line with Points')

        plt.show()


class Dataset:

    def __init__(self, start=0, end=2, starting_position=1, number_of_points=1, iterations=1):
        self.start = 0
        self.end = 2
        self.starting_position = starting_position
        self.best_paths = []
        self.min_points = []
        self.max_points = []
        self.number_of_points = number_of_points
        self.iterations = iterations

    def gather(self):
        for i in range(self.iterations):
            number_line = NumberLine(
                self.start, self.end, self.starting_position)
            number_line.generate_and_add_random_points(self.number_of_points)
            self.best_paths.append(number_line.find_best_path())
            self.min_points.append(number_line.find_min_point())
            self.max_points.append(number_line.find_max_point())

    def display(self):
        print(f"Starting position: {self.starting_position}")
        print(f"Number of points: {len(self.best_paths)}")
        print(f"Average traversal: {self.get_mean_path()}")
        print(f"Average max: {self.get_mean_max()}")
        print(f"Average min: {self.get_mean_min()}")

    def visualize(self):

        visualization_line = NumberLine(
            self.start, self.end, self.starting_position)
        avg_max = self.get_mean_max
        avg_min = self.get_mean_min
        visualization_line.add_point(avg_max)
        visualization_line.add_point(avg_min)

        visualization_line.visualize(label=True)

    def get_mean_path(self):
        return sum(self.best_paths) / len(self.best_paths)

    def get_mean_max(self):
        return sum(self.max_points) / len(self.max_points)

    def get_mean_min(self):
        return sum(self.min_points) / len(self.min_points)

    def dump_to_file():

        with open(f"dataset-{self.start}-{self.end}-{self.start_position}-{self.number_of_points}-{self.iterations}-{datetime.now()}") as f:
            f.write(f"Starting position: {self.starting_position}")
            f.write(f"Number of points: {len(self.best_paths)}")
            f.write(f"Average traversal: {self.get_mean_path()}")
            f.write(f"Average max: {self.get_mean_max()}")
            f.write(f"Average min: {self.get_mean_min()}")
