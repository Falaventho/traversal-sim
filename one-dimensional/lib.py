import random
import matplotlib.pyplot as plt
import time
import tkinter as tk
from tkinter import ttk, messagebox
import statistics
import placement_optimization_sim as aposrs


class NumberLine:
    def __init__(self, start=0, end=2, starting_position=1, number_of_points=1):
        self.start = start
        self.end = end
        self.starting_position = starting_position
        self.number_of_points = number_of_points

        self.regenerate_data()

    def regenerate_data(self):
        self.traversal_distance = aposrs.generate_traversal(
            self.start, self.end, self.number_of_points, self.starting_position)

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
    def __init__(self, number_line, iterations=1, repetitions=1, significant_figures=1, progress_callback=None):
        self.number_line = number_line
        self.iterations = iterations
        self.repetitions = repetitions
        self.significant_figures = significant_figures
        self.optimal_p_values = []
        self.progress_callback = progress_callback

    def run(self):
        for _ in range(self.repetitions):
            p_val = self.__funnel_to_p_value()
            self.optimal_p_values.append(p_val)
            self.progress_callback()

    def __gather(self):
        dataset = []
        for _ in range(self.iterations):
            self.number_line.regenerate_data()
            dataset.append(self.number_line.traversal_distance)
        return statistics.mean(dataset)

    # ! Definite Bottleneck
    def __funnel_to_p_value(self):
        left_bound = float(self.number_line.starting_position)
        right_bound = float(self.number_line.end)
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
                traversal = self.__gather()
                traversal_distances.append(traversal)
                tested_p_values.append(j)
                j += float(step)

            optimal_p_val = self.__find_optimal_p(
                traversal_distances, tested_p_values)
            left_bound = min(optimal_p_val - step, self.number_line.end)
            right_bound = min(optimal_p_val + step, self.number_line.end)

        return self.__find_optimal_p(traversal_distances, tested_p_values)

    def __find_optimal_p(self, traversal_distances, tested_p_values):
        minimum_traversal = min(traversal_distances)
        idx = traversal_distances.index(minimum_traversal)
        return tested_p_values[idx]


class UserInterface:
    def __init__(self, root, simulation_factory, program_timer):
        self.root = root
        self.root.title("Simulation Control Panel")
        self.simulation_factory = simulation_factory
        self.program_timer = program_timer

        self.n_left_bound = tk.IntVar(value=1)
        self.n_right_bound = tk.IntVar(value=1)
        self.sig_fig_var = tk.IntVar(value=3)
        self.iteration_var = tk.IntVar(value=1000)
        self.repetitions_var = tk.IntVar(value=3)
        self.mean_decimal_places = tk.IntVar(value=2)
        self.stdev_decimal_places = tk.IntVar(value=2)

        self.__setup_ui()
        self.program_timer.reset_counter("UI Init")

    def __setup_ui(self):

        # Frames
        self.stats_frame = ttk.LabelFrame(self.root, text="Statistics")
        self.stats_frame.grid(row=7, column=0, columnspan=4,
                              padx=10, pady=10, sticky='ew')

        # Labels and entries
        self.__create_label_and_entry(
            "n-values from:", self.n_left_bound, 0, 0)
        self.__create_label_and_entry("to", self.n_right_bound, 0, 2)
        self.__create_label_and_entry(
            "Significant Figures", self.sig_fig_var, 2, 0, 10)
        self.__create_label_and_entry(
            "Iteration Count", self.iteration_var, 3, 0, 1000000)
        self.__create_label_and_entry(
            "Repetitions Count", self.repetitions_var, 4, 0, 100)
        self.__create_label_and_entry(
            "Round final stats mean to places: ", self.mean_decimal_places, 0, 0, master=self.stats_frame, width=2)
        self.__create_label_and_entry(
            "Round final stats stdev to places: ", self.stdev_decimal_places, 1, 0, master=self.stats_frame, width=2)

        # Buttons and progress
        self.run_button = ttk.Button(
            self.root, text="Run", command=self.__try_run_simulation_with_single_plot)
        self.run_button.grid(row=5, column=1, padx=10, pady=10)

        self.quit_button = ttk.Button(
            self.root, text="Quit", command=self.quit_app)
        self.quit_button.grid(row=5, column=2, padx=10, pady=10)

        self.progress_bar = ProgressBar(self.root, bar_row=6, label_row=6)

        self.program_timer.report_step("UI Setup")

    def __create_label_and_entry(self, text, variable, row, col, scale_to=None, master=None, width=None):
        m = master or self.root
        w = width or 20

        label = ttk.Label(m, text=text)
        label.grid(row=row, column=col, padx=10, pady=5)
        entry = ttk.Entry(m, textvariable=variable, width=w)
        entry.grid(row=row, column=col + 1, padx=10, pady=5)
        if scale_to:
            slider = ttk.Scale(m, from_=1, to=scale_to, orient='horizontal',
                               variable=variable, command=lambda val: variable.set(int(float(val))))
            slider.grid(row=row, column=col + 2, padx=10, pady=5)

    def __validate_entry_data(self) -> list[str]:
        err_msg_list = []
        left_bound = self.n_left_bound.get()
        right_bound = self.n_right_bound.get()
        if left_bound > right_bound:
            err_msg_list.append(
                "n-value error: left bound greater than right bound")

        return err_msg_list

    def __try_run_simulation_with_single_plot(self):
        err_msg_list = self.__validate_entry_data()
        self.program_timer.start()
        if len(err_msg_list) == 0:
            self.__run_simulation_with_single_plot()
        else:
            messagebox.showwarning(title="Input data error", message=f"Error messages:\n\n" +
                                   f"{'\n'.join(err_msg_list)}\n\nResolve input errors and press run.")

    def __run_simulation_with_single_plot(self):
        optimal_distance_from_center_superset = self.__run_simulation_across_n_values()
        self.program_timer.report_step("Simulation Complete")
        fig, ax = plt.subplots()
        left_bound = self.n_left_bound.get()
        mean_decimal_places = self.mean_decimal_places.get()
        stdev_decimal_places = self.stdev_decimal_places.get()
        for i, subset in enumerate(optimal_distance_from_center_superset):
            n_value = left_bound + i
            x_values = [n_value] * len(subset)
            ax.scatter(x_values, subset, label=f'n={n_value}')

            # Calculate statistics
            mean = statistics.mean(subset)
            stdev = statistics.stdev(subset)

            # Round statistics to user-specified precision
            mean = round(mean, mean_decimal_places)
            stdev = round(stdev, stdev_decimal_places)

            # Create labels for each n value
            n_label = tk.Label(self.stats_frame, text=f"n={n_value} ")
            n_label.grid(row=i+2, column=0, padx=10, pady=5)

            mean_label = tk.Label(self.stats_frame,
                                  text=f"Mean: {mean}")
            mean_label.grid(row=i+2, column=1, padx=10, pady=5)

            stdev_label = tk.Label(self.stats_frame,
                                   text=f"Std Dev: {stdev}")
            stdev_label.grid(row=i+2, column=2, padx=10, pady=5)

        ax.set_xlabel('n value')
        ax.set_ylabel('Optimal distance from center')
        ax.set_title('Optimal Distances from Center for Different n Values')
        ax.legend()
        plt.show()

    def __run_simulation_across_n_values(self):
        optimal_distance_from_center_superset = []
        left_bound = self.n_left_bound.get()
        right_bound = self.n_right_bound.get() + 1

        repetitions = self.repetitions_var.get()
        max_progress_count = (right_bound - left_bound) * repetitions
        self.progress_bar.update_progress(max_count=max_progress_count)
        self.progress_bar.clear_progress()

        for n_value in range(left_bound, right_bound):
            self.program_timer.reset_counter(f"sim n={n_value}")
            optimal_dist = self.__run_simulation_for_n(n_value)
            optimal_distance_from_center_superset.append(optimal_dist)
            self.program_timer.report_step(f"sim n={n_value}")

        return optimal_distance_from_center_superset

    def __run_simulation_for_n(self, n_value):
        sig_fig = self.sig_fig_var.get()
        iteration_count = self.iteration_var.get()
        repetitions_count = self.repetitions_var.get()
        number_line = NumberLine(
            start=0, end=2, starting_position=1, number_of_points=n_value)
        simulation = self.simulation_factory.create_simulation(
            number_line, iteration_count, repetitions_count, sig_fig, self.progress_bar.increment_progress)
        simulation.run()
        distances_from_center = [abs(x - 1)
                                 for x in simulation.optimal_p_values]
        return distances_from_center

    def quit_app(self):
        self.root.quit()


class SimulationFactory:
    def create_simulation(self, number_line, iterations, repetitions, significant_figures, progress_callback):
        return Simulation(number_line, iterations, repetitions, significant_figures, progress_callback)


class ProgramTimer:
    def __init__(self):
        self.init_time = time.time()
        self.counter = time.time()
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def get_time_since_start(self):
        return time.time() - self.start_time

    def get_time_since_init(self):
        return time.time() - self.init_time

    def get_counter_time(self):
        return time.tim() - self.counter

    def reset_counter(self, step=None):
        print(f"Counter reset on {step}")
        self.counter = time.time()

    def report_step(self, step):
        now_time = time.time()
        i_time = now_time - self.init_time
        s_time = now_time - (self.start_time or now_time)
        c_time = now_time - self.counter
        print(f"Step {step} report:")
        print(f"Time since init: {i_time:.2f}")
        print(f"Time since start: {s_time:.2f}")
        print(f"Time since counter reset: {c_time:.2f}")


class ProgressBar:
    def __init__(self, master, max_count=100, current_count=0, bar_row=0, label_row=0, bar_col=0, label_col=3):
        self.max_count = max_count
        self.current_count = current_count
        self.master = master

        self.progress_bar = ttk.Progressbar(
            master, orient='horizontal', mode='determinate')
        self.progress_bar.grid(row=bar_row, column=bar_col, columnspan=3,
                               padx=10, pady=10, sticky='ew')

        percentage = self.__get_current_percent()
        self.progress_label = tk.Label(
            master, text=f'{percentage}%')
        self.progress_label.grid(
            row=label_row, column=label_col, padx=10, pady=10, sticky='w')

        self.__update()

    def __get_current_percent(self):
        return int((self.current_count / self.max_count) * 100)

    def update_progress(self, count=None, max_count=None):
        if max_count:
            self.max_count = max_count
        if count:
            self.current_count = count
        self.__update()

    def increment_progress(self):
        self.current_count += 1
        self.__update()

    def clear_progress(self):
        self.current_count = 0
        self.__update()

    def __update(self):
        percent = self.__get_current_percent()
        self.progress_bar['maximum'] = self.max_count
        self.progress_bar['value'] = self.current_count
        self.progress_label.config(text=f'{percent}%')
        self.master.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    simulation_factory = SimulationFactory()
    timer = ProgramTimer()
    app = UserInterface(root, simulation_factory, timer)
    root.mainloop()
