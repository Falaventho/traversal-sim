import json
import os
import uuid
import random
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import time
import tkinter as tk
from tkinter import ttk, messagebox
import statistics
from placement_optimization_sim import NumberLine


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
            dataset.append(self.number_line.regenerate_data())
        return statistics.mean(dataset)

    # ! Definite Bottleneck
    def __funnel_to_p_value(self):
        left_bound = float(self.number_line.get_starting_position())
        right_bound = float(self.number_line.get_end())
        step = 1
        # ! Space for data structure improvement here, lists are not the best
        traversal_distances = []
        tested_p_values = []

        for _ in range(self.significant_figures):
            traversal_distances.clear()
            tested_p_values.clear()
            step /= 10
            j = left_bound
            while j <= right_bound:
                self.number_line.set_starting_position(j)
                traversal = self.__gather()
                traversal_distances.append(traversal)
                tested_p_values.append(j)
                j += float(step)

            optimal_p_val = self.__find_optimal_p(
                traversal_distances, tested_p_values)
            end = self.number_line.get_end()
            left_bound = min(optimal_p_val - step, end)
            right_bound = min(optimal_p_val + step, end)

        return self.__find_optimal_p(traversal_distances, tested_p_values)

    def __find_optimal_p(self, traversal_distances, tested_p_values):
        minimum_traversal = min(traversal_distances)
        idx = traversal_distances.index(minimum_traversal)
        return tested_p_values[idx]


class UserInterface:
    def __init__(self, root, program_timer):
        self.root = root
        self.root.title("Simulation Control Panel")
        self.program_timer = program_timer
        self.optimal_distance_from_center_superset = []
        self.metadata = {}

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
                              padx=10, pady=10, sticky="ew")

        # HR Seperator
        separator = ttk.Separator(self.stats_frame, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=4, sticky="ew", pady=10)

        # Canvas and Scrollbar
        self.stats_canvas = tk.Canvas(self.stats_frame)
        self.stats_scrollbar = ttk.Scrollbar(
            self.stats_frame, orient="vertical", command=self.stats_canvas.yview)
        self.stats_canvas.configure(yscrollcommand=self.stats_scrollbar.set)

        # Create a frame inside the canvas
        self.stats_inner_frame = ttk.Frame(self.stats_canvas)

        # Add the frame to the canvas
        self.stats_canvas.create_window(
            (0, 0), window=self.stats_inner_frame, anchor="nw")

        # Pack the canvas and scrollbar
        self.stats_canvas.grid(row=4, column=0, sticky="nsew")
        self.stats_scrollbar.grid(row=4, column=3, sticky="ns")

        # Configure the inner frame to expand with the canvas
        self.stats_inner_frame.bind("<Configure>", lambda e: self.stats_canvas.configure(
            scrollregion=self.stats_canvas.bbox("all")))

        # Labels and entries
        self.__create_label_and_entry(
            "n-values from:", self.n_left_bound, 0, 0, focus=True)
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
        self.quit_button.grid(row=5, column=4, padx=10, pady=10)

        self.export_button = ttk.Button(
            self.root, text="Export Run", command=self.try_export)
        self.export_button.grid(row=5, column=2, padx=10, pady=10)

        self.import_button = ttk.Button(
            self.root, text="Import Run", command=self.try_import)
        self.import_button.grid(row=5, column=3, padx=10, pady=10)

        self.progress_bar = ProgressBar(self.root, bar_row=6, label_row=6)

        self.recalculate_stats_button = ttk.Button(
            self.stats_frame, text="Recalculate", command=self.__calculate_stats_for_superset)
        self.recalculate_stats_button.grid(row=2, column=0, padx=10, pady=10)

        self.program_timer.report_step("UI Setup")

        # Bindings
        self.stats_canvas.bind_all("<MouseWheel>", self.__on_mousewheel)

        self.root.bind("<Return>", self.__on_enter_key)

    def __on_mousewheel(self, event):
        self.stats_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def __on_enter_key(self, event):
        self.__try_run_simulation_with_single_plot()

    def try_export(self):
        if self.metadata and self.optimal_distance_from_center_superset:
            self.__export_data(".")
        else:
            messagebox.showwarning(
                title="Export Failed", message="Metadata or dataset missing or corrupted, run or import a simulation before exporting data.")

    def try_import(self):
        pass

    def __create_label_and_entry(self, text, variable, row, col, scale_to=None, master=None, width=None, focus=False):
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

        if focus:
            entry.focus_set()

    def __validate_entry_data(self, err_msg_list=[]) -> list[str]:
        left_bound = self.n_left_bound.get()
        right_bound = self.n_right_bound.get()
        if left_bound > right_bound:
            err_msg_list.append(
                "n-value error: left bound greater than right bound")

        return err_msg_list

    def __calculate_stats_for_superset(self):
        if not self.optimal_distance_from_center_superset:
            messagebox.showwarning(
                title="Recalculate Error", message="No dataset available to run calculations on. Run a simulation first.")
            return
        for idx, subset in enumerate(self.optimal_distance_from_center_superset):
            n = self.left_bound + idx
            self.__calculate_and_display_stats(subset, n, n+2)

    def __calculate_and_display_stats(self, subset, n_value, row_idx):

        mean_decimal_places = self.mean_decimal_places.get()
        stdev_decimal_places = self.stdev_decimal_places.get()

        # Calculate statistics
        mean = statistics.mean(subset)
        stdev = statistics.stdev(subset)

        # Round statistics to user-specified precision
        mean = round(mean, mean_decimal_places)
        stdev = round(stdev, stdev_decimal_places)

        # Create labels for each n value
        n_label = tk.Label(self.stats_inner_frame, text=f"n={n_value} ")
        n_label.grid(row=row_idx, column=0, padx=10, pady=5)

        mean_label = tk.Label(self.stats_inner_frame,
                              text=f"Mean: {mean}")
        mean_label.grid(row=row_idx, column=1, padx=10, pady=5)

        stdev_label = tk.Label(self.stats_inner_frame,
                               text=f"Std Dev: {stdev}")
        stdev_label.grid(row=row_idx, column=2, padx=10, pady=5)

    def __try_run_simulation_with_single_plot(self):
        err_msg_list = self.__validate_entry_data()
        self.program_timer.start()
        if len(err_msg_list) == 0:
            self.__lock_metadata()
            self.__run_simulation_with_single_plot()
        else:
            err_block = '\n'.join(err_msg_list)
            messagebox.showwarning(title="Input data error", message=f"Error messages:\n\n" +
                                   f"{err_block}\n\nResolve input errors and press run.")

    def __lock_metadata(self):
        self.metadata = {
            'n_left_bound': self.n_left_bound.get(),
            'n_right_bound': self.n_right_bound.get(),
            'sig_fig': self.sig_fig_var.get(),
            'iterations': self.iteration_var.get(),
            'repetitions': self.repetitions_var.get(),
            'mean_decimal_places': self.mean_decimal_places.get(),
            'stdev_decimal_places': self.stdev_decimal_places.get(),
            'gmt-timestamp': time.gmtime()
        }

    def __run_simulation_with_single_plot(self):
        self.optimal_distance_from_center_superset = self.__run_simulation_across_n_values()
        self.program_timer.report_step("Simulation Complete")
        self.__plot_optimal_distances()

    def __plot_optimal_distances(self):
        fig, ax = plt.subplots()
        self.left_bound = self.n_left_bound.get()
        for i, subset in enumerate(self.optimal_distance_from_center_superset):
            n_value = self.left_bound + i
            x_values = [n_value] * len(subset)
            ax.scatter(x_values, subset, label=f'n={n_value}')
        self.__calculate_stats_for_superset()

        ax.set_xlabel('n value')
        ax.set_ylabel('Optimal distance from center')
        ax.set_title('Optimal Distances from Center for Different n Values')
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.show()

    def __export_data(self, directory: str):
        # Sanitize and validate the directory path
        if not os.path.isdir(directory):
            raise ValueError("Invalid directory path")

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        unique_id = uuid.uuid4()
        filename = f"export_{timestamp}_{unique_id}.json"
        path = os.path.join(directory, filename)

        data = {
            'meta': self.metadata,
            'dataset': self.optimal_distance_from_center_superset
        }
        json_data = json.dumps(data, indent=4)

        with open(path, 'x') as f:
            f.write(json_data)

    def __import_data(self, path: str):
        with open(path, 'r') as f:
            data = json.load(f)

        self.metadata = data.get('meta', {})
        self.optimal_distance_from_center_superset = data.get('dataset', [])

        self.__synchronize_panel_with_metadata()

    def __synchronize_panel_with_metadata(self):
        self.n_left_bound.set(self.metadata.get('n_left_bound', 1))
        self.n_right_bound.set(self.metadata.get('n_right_bound', 1))
        self.sig_fig_var.set(self.metadata.get('sig_fig', 3))
        self.iteration_var.set(self.metadata.get('iterations', 1000))
        self.repetitions_var.set(self.metadata.get('repetitions', 3))
        self.mean_decimal_places.set(
            self.metadata.get('mean_decimal_places', 2))
        self.stdev_decimal_places.set(
            self.metadata.get('stdev_decimal_places', 2))

    def __run_simulation_across_n_values(self):
        optimal_distance_from_center_superset = []
        left_bound = self.n_left_bound.get()
        right_bound = self.n_right_bound.get() + 1

        repetitions = self.repetitions_var.get()
        max_progress_count = (right_bound - left_bound) * repetitions
        self.progress_bar.update_progress(max_count=max_progress_count)
        self.progress_bar.clear_progress()

        # ! Target for multithreading
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
            start=0.0, end=2.0, starting_position=1.0, number_of_points=n_value)
        simulation = Simulation(
            number_line, iteration_count, repetitions_count, sig_fig, self.progress_bar.increment_progress)
        simulation.run()
        distances_from_center = [abs(x - 1)
                                 for x in simulation.optimal_p_values]
        return distances_from_center

    def quit_app(self):
        self.root.quit()


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
    timer = ProgramTimer()
    app = UserInterface(root, timer)
    root.mainloop()
