import random
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import statistics


class NumberLine:

    def __init__(self, start=0, end=2, starting_position=1, number_of_points=1):
        self.start = start
        self.end = end
        self.points = []
        self.number_of_points = number_of_points

        if start <= starting_position <= end:
            self.starting_position = starting_position
        else:
            raise ValueError("Starting position" +
                             f"{starting_position} is out of bounds [{start}, {end}]")

        self.__generate_and_add_random_points(number_of_points)
        self.max_point = self.__find_max_point()
        self.min_point = self.__find_min_point()
        self.traversal_distance = self.__find_best_path()

    def set_number_of_points(self, n: int):
        self.number_of_points = n

    def set_starting_position(self, p: float):
        self.starting_position = p

    def regenerate_data(self):
        self.points.clear()
        self.__generate_and_add_random_points(self.number_of_points)
        self.__update_attributes()

    def __update_attributes(self):
        self.max_point = self.__find_max_point()
        self.min_point = self.__find_min_point()
        self.traversal_distance = self.__find_best_path()

    def __add_point(self, p):
        if self.start <= p <= self.end:
            self.points.append(p)
        else:
            raise ValueError(
                f"Point {p} is out of bounds [{self.start}, {self.end}]")

    def __generate_random_points(self, n) -> list[float]:
        return [random.uniform(self.start, self.end) for _ in range(n)]

    def __generate_and_add_random_points(self, n):
        points = self.__generate_random_points(n)
        for point in points:
            self.__add_point(point)

    def __find_max_point(self):
        return max(self.points)

    def __find_min_point(self):
        return min(self.points)

    def __find_best_path(self) -> float:

        dist_to_max = abs(self.starting_position - self.max_point)
        dist_to_min = abs(self.starting_position - self.min_point)

        first_traversal = min(dist_to_max, dist_to_min)
        second_traversal = abs(self.max_point - self.min_point)

        return first_traversal + second_traversal

    def display(self):
        print(f"Number line segment: [{self.start}, {self.end}]")
        print(f"Points on the line segment: {sorted(self.points)}")
        print(f"Optimal path from starting position " +
              f"{self.starting_position} requires a traversal of {self.traversal_distance} to contact all points.")

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


class Simulation:

    def __init__(self, start=0, end=2, number_of_points=1, iterations=1, repetitions=1, significant_figures=1):
        self.start = 0
        self.end = 2
        self.starting_position = (self.end - self.start) / 2
        self.optimal_p_values = []
        self.number_of_points = number_of_points
        self.iterations = iterations
        self.repetitions = repetitions
        self.significant_figures = significant_figures
        self.number_line = NumberLine(
            start, end, self.starting_position, number_of_points)

    def __gather(self, p: float) -> float:
        dataset = []
        for i in range(self.iterations):
            self.number_line.regenerate_data()
            dataset.append(self.number_line.traversal_distance)

        return statistics.mean(dataset)

    def run(self):

        for i in range(self.repetitions):
            p_val = self.__funnel_to_p_value()
            self.optimal_p_values.append(p_val)

    def __funnel_to_p_value(self) -> float:

        left_bound = self.starting_position
        right_bound = self.end
        step = 1
        traversal_distances = []
        tested_p_values = []

        for i in range(self.significant_figures):

            traversal_distances.clear()
            tested_p_values.clear()
            step = step / 10
            j = left_bound
            while j <= right_bound:

                self.number_line.set_starting_position(j)
                traversal = self.__gather(j)
                traversal_distances.append(traversal)
                tested_p_values.append(j)
                j += step

            optimal_p_val = self.__find_optimal_p(
                traversal_distances, tested_p_values)

            left_bound = optimal_p_val - step
            right_bound = optimal_p_val + step

        return self.__find_optimal_p(traversal_distances, tested_p_values)

    def __find_optimal_p(self, traversal_distances: list[float], tested_p_values: list[float]) -> float:

        minimum_traversal = min(traversal_distances)
        idx = traversal_distances.index(minimum_traversal)
        return tested_p_values[idx]


class UserInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulation Control Panel")

        # Variables for storing slider values
        self.n_var = tk.IntVar(value=1)
        self.sig_fig_var = tk.IntVar(value=3)
        self.iteration_var = tk.IntVar(value=1000)
        self.repetitions_var = tk.IntVar(value=3)

        # n-value controls
        self.n_label = ttk.Label(root, text="n-value")
        self.n_label.grid(row=0, column=0, padx=10, pady=5)
        self.n_entry = ttk.Entry(root, textvariable=self.n_var)
        self.n_entry.grid(row=0, column=1, padx=10, pady=5)
        self.n_slider = ttk.Scale(root, from_=1, to=1000, orient='horizontal',
                                  variable=self.n_var, command=lambda val: self.n_var.set(int(float(val))))
        self.n_slider.grid(row=0, column=2, padx=10, pady=5)

        # Sig Fig controls
        self.sig_fig_label = ttk.Label(root, text="Significant Figures")
        self.sig_fig_label.grid(row=1, column=0, padx=10, pady=5)
        self.sig_fig_entry = ttk.Entry(root, textvariable=self.sig_fig_var)
        self.sig_fig_entry.grid(row=1, column=1, padx=10, pady=5)
        self.sig_fig_slider = ttk.Scale(root, from_=1, to=10, orient='horizontal',
                                        variable=self.sig_fig_var, command=lambda val: self.sig_fig_var.set(int(float(val))))
        self.sig_fig_slider.grid(row=1, column=2, padx=10, pady=5)

        # Iteration count controls
        self.iteration_label = ttk.Label(root, text="Iteration Count")
        self.iteration_label.grid(row=2, column=0, padx=10, pady=5)
        self.iteration_entry = ttk.Entry(root, textvariable=self.iteration_var)
        self.iteration_entry.grid(row=2, column=1, padx=10, pady=5)
        self.iteration_slider = ttk.Scale(root, from_=1, to=1000000, orient='horizontal',
                                          variable=self.iteration_var, command=lambda val: self.iteration_var.set(int(float(val))))
        self.iteration_slider.grid(row=2, column=2, padx=10, pady=5)

        # Repetitions count controls
        self.repetitions_label = ttk.Label(root, text="Repetitions Count")
        self.repetitions_label.grid(row=3, column=0, padx=10, pady=5)
        self.repetitions_entry = ttk.Entry(
            root, textvariable=self.repetitions_var)
        self.repetitions_entry.grid(row=3, column=1, padx=10, pady=5)
        self.repetitions_slider = ttk.Scale(root, from_=1, to=100, orient='horizontal',
                                            variable=self.repetitions_var, command=lambda val: self.repetitions_var.set(int(float(val))))
        self.repetitions_slider.grid(row=3, column=2, padx=10, pady=5)

        # Run button
        self.run_button = ttk.Button(
            root, text="Run", command=self.run_simulation)
        self.run_button.grid(row=4, column=1, padx=10, pady=10)

        # Quit button
        self.quit_button = ttk.Button(root, text="Quit", command=self.quit_app)
        self.quit_button.grid(row=4, column=2, padx=10, pady=10)

    def run_simulation(self):
        """This method is called when the 'Run' button is clicked."""
        n_value = self.n_var.get()
        sig_fig = self.sig_fig_var.get()
        iteration_count = self.iteration_var.get()
        repetitions_count = self.repetitions_var.get()

        print(f"Running simulation with parameters:")
        print(f"n-value: {n_value}")
        print(f"Significant figures: {sig_fig}")
        print(f"Iteration count: {iteration_count}")
        print(f"Repetitions count: {repetitions_count}")

    def quit_app(self):
        """This method quits the application."""
        self.root.quit()


# Running the interface
if __name__ == "__main__":
    root = tk.Tk()
    app = UserInterface(root)
    root.mainloop()
