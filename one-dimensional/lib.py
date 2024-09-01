import random
import matplotlib.pyplot as plt


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
