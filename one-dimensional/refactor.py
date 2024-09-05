import random
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import statistics
from abc import ABC, abstractmethod


class PointGenerator(ABC):
    @abstractmethod
    def generate_points(self, start, end, n):
        pass


class RandomPointGenerator(PointGenerator):
    def generate_points(self, start, end, n):
        return [random.uniform(start, end) for _ in range(n)]


class NumberLine:
    def __init__(self, start=0, end=2, starting_position=1, number_of_points=1, point_generator=None):
        self.start = start
        self.end = end
        self.starting_position = starting_position
        self.number_of_points = number_of_points
        self.points = []
        self.point_generator = point_generator or RandomPointGenerator()
        self.regenerate_data()

    def regenerate_data(self):
        self.points = self.point_generator.generate_points(
            self.start, self.end, self.number_of_points)
        self.max_point = max(self.points)
        self.min_point = min(self.points)
        self.traversal_distance = self.__find_best_path()

    def __find_best_path(self):
        dist_to_max = abs(self.starting_position - self.max_point)
        dist_to_min = abs(self.starting_position - self.min_point)
        first_traversal = min(dist_to_max, dist_to_min)
        second_traversal = abs(self.max_point - self.min_point)
        return first_traversal + second_traversal

    def display(self):
        print(f"Number line segment: [{self.start}, {self.end}]")
        print(f"Points on the line segment: {sorted(self.points)}")
        print(f"Optimal path from starting position {self.starting_position} requires a traversal of" +
              f"{self.traversal_distance} to contact all points.")

    def visualize(self, label=False):
        fig, ax = plt.subplots()
        ax.plot([self.start, self.end], [0, 0], 'k-', lw=2)
        ax.plot(self.starting_position, 0, 'bo')
        ax.text(self.starting_position, -0.02,
                'Start', ha='center', fontsize=10)
        for point in self.points:
            ax.plot(point, 0, 'ro')
            if label:
                ax.text(point, 0.02, f'{point:.2f}', ha='center', fontsize=10)
        ax.set_xlim(self.start - 0.1, self.end + 0.1)
        ax.get_yaxis().set_visible(False)
        ax.set_xlabel('Number Line')
        ax.set_title('Number Line with Points')
        plt.show()


class Simulation:
    def __init__(self, number_line, iterations=1, repetitions=1, significant_figures=1):
        self.number_line = number_line
        self.iterations = iterations
        self.repetitions = repetitions
        self.significant_figures = significant_figures
        self.optimal_p_values = []

    def run(self):
        for _ in range(self.repetitions):
            p_val = self.__funnel_to_p_value()
            self.optimal_p_values.append(p_val)

    def __gather(self, p):
        dataset = []
        for _ in range(self.iterations):
            self.number_line.regenerate_data()
            dataset.append(self.number_line.traversal_distance)
        return statistics.mean(dataset)

    def __funnel_to_p_value(self):
        left_bound = self.number_line.starting_position
        right_bound = self.number_line.end
        step = 1
        traversal_distances = []
        tested_p_values = []

        for _ in range(self.significant_figures):
            traversal_distances.clear()
            tested_p_values.clear()
            step /= 10
            j = left_bound
            while j <= right_bound:
                self.number_line.starting_position = j
                traversal = self.__gather(j)
                traversal_distances.append(traversal)
                tested_p_values.append(j)
                j += step

            optimal_p_val = self.__find_optimal_p(
                traversal_distances, tested_p_values)
            left_bound = optimal_p_val - step
            right_bound = optimal_p_val + step

        return self.__find_optimal_p(traversal_distances, tested_p_values)

    def __find_optimal_p(self, traversal_distances, tested_p_values):
        minimum_traversal = min(traversal_distances)
        idx = traversal_distances.index(minimum_traversal)
        return tested_p_values[idx]


class UserInterface:
    def __init__(self, root, simulation_factory):
        self.root = root
        self.root.title("Simulation Control Panel")
        self.simulation_factory = simulation_factory

        self.n_left_bound = tk.IntVar(value=1)
        self.n_right_bound = tk.IntVar(value=1)
        self.sig_fig_var = tk.IntVar(value=3)
        self.iteration_var = tk.IntVar(value=1000)
        self.repetitions_var = tk.IntVar(value=3)

        self.__setup_ui()

    def __setup_ui(self):
        self.__create_label_and_entry(
            "n-values from:", self.n_left_bound, 0, 0)
        self.__create_label_and_entry("to", self.n_right_bound, 0, 2)
        self.__create_label_and_entry(
            "Significant Figures", self.sig_fig_var, 2, 0, 10)
        self.__create_label_and_entry(
            "Iteration Count", self.iteration_var, 3, 0, 1000000)
        self.__create_label_and_entry(
            "Repetitions Count", self.repetitions_var, 4, 0, 100)

        self.run_button = ttk.Button(
            self.root, text="Run", command=self.__run_simulation_with_single_plot)
        self.run_button.grid(row=5, column=1, padx=10, pady=10)

        self.quit_button = ttk.Button(
            self.root, text="Quit", command=self.quit_app)
        self.quit_button.grid(row=5, column=2, padx=10, pady=10)

    def __create_label_and_entry(self, text, variable, row, col, scale_to=None):
        label = ttk.Label(self.root, text=text)
        label.grid(row=row, column=col, padx=10, pady=5)
        entry = ttk.Entry(self.root, textvariable=variable)
        entry.grid(row=row, column=col + 1, padx=10, pady=5)
        if scale_to:
            slider = ttk.Scale(self.root, from_=1, to=scale_to, orient='horizontal',
                               variable=variable, command=lambda val: variable.set(int(float(val))))
            slider.grid(row=row, column=col + 2, padx=10, pady=5)

    def __run_simulation_with_single_plot(self):
        optimal_distance_from_center_superset = self.__run_simulation_across_n_values()
        fig, ax = plt.subplots()
        left_bound = self.n_left_bound.get()
        for i, subset in enumerate(optimal_distance_from_center_superset):
            n_value = left_bound + i
            x_values = [n_value] * len(subset)
            ax.scatter(x_values, subset, label=f'n={n_value}')
        ax.set_xlabel('n value')
        ax.set_ylabel('Optimal distances from center')
        ax.set_title('Optimal Distances from Center for Different n Values')
        ax.legend()
        plt.show()

    def __run_simulation_across_n_values(self):
        optimal_distance_from_center_superset = []
        left_bound = self.n_left_bound.get()
        right_bound = self.n_right_bound.get() + 1
        for n_value in range(left_bound, right_bound):
            optimal_dist = self.__run_simulation_for_n(n_value)
            optimal_distance_from_center_superset.append(optimal_dist)
        return optimal_distance_from_center_superset

    def __run_simulation_for_n(self, n_value):
        sig_fig = self.sig_fig_var.get()
        iteration_count = self.iteration_var.get()
        repetitions_count = self.repetitions_var.get()
        number_line = NumberLine(
            start=0, end=2, starting_position=1, number_of_points=n_value)
        simulation = self.simulation_factory.create_simulation(
            number_line, iteration_count, repetitions_count, sig_fig)
        simulation.run()
        distances_from_center = [abs(x - 1)
                                 for x in simulation.optimal_p_values]
        return distances_from_center

    def quit_app(self):
        self.root.quit()


class SimulationFactory:
    def create_simulation(self, number_line, iterations, repetitions, significant_figures):
        return Simulation(number_line, iterations, repetitions, significant_figures)


if __name__ == "__main__":
    root = tk.Tk()
    simulation_factory = SimulationFactory()
    app = UserInterface(root, simulation_factory)
    root.mainloop()
