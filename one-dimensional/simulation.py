import statistics


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
            p_val = self._funnel_to_p_value()
            self.optimal_p_values.append(p_val)
            if self.progress_callback:
                self.progress_callback()

    def _gather(self):
        dataset = []
        for _ in range(self.iterations):
            dataset.append(self.number_line.regenerate_data())
        return statistics.mean(dataset)

    # ! Definite Bottleneck
    def _funnel_to_p_value(self):
        left_bound = float(self.number_line.get_starting_position())
        right_bound = float(self.number_line.get_end())
        step = 1
        # ! Space for data structure improvement here, lists may not be best
        traversal_distances = []
        tested_p_values = []

        for _ in range(self.significant_figures):
            traversal_distances.clear()
            tested_p_values.clear()
            step /= 10
            j = left_bound
            while j <= right_bound:
                self.number_line.set_starting_position(j)
                traversal = self._gather()
                traversal_distances.append(traversal)
                tested_p_values.append(j)
                j += float(step)

            optimal_p_val = self._find_optimal_p(
                traversal_distances, tested_p_values)
            end = self.number_line.get_end()
            left_bound = min(optimal_p_val - step, end)
            right_bound = min(optimal_p_val + step, end)

        return self._find_optimal_p(traversal_distances, tested_p_values)

    def _find_optimal_p(self, traversal_distances, tested_p_values):
        minimum_traversal = min(traversal_distances)
        idx = traversal_distances.index(minimum_traversal)
        return tested_p_values[idx]
