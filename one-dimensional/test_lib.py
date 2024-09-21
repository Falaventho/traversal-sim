import pytest
from lib import Simulation, UserInterface, ProgramTimer, ProgressBar
from placement_optimization_sim import NumberLine
import tkinter as tk
import statistics
import os
import json
import time
import uuid
import tempfile


class TestSimulation:
    def test_run(self):
        number_line = NumberLine(0, 2, 1, 3)
        simulation = Simulation(number_line, 1, 1, 1)
        simulation.run()
        assert len(simulation.optimal_p_values) == 1

    def test_gather(self):
        number_line = NumberLine(0, 2, 1, 3)
        simulation = Simulation(number_line, 1, 1, 1)
        traversal = simulation._Simulation__gather()
        assert 0 <= traversal <= 3

    def test_find_optimal_p(self):
        number_line = NumberLine(0, 2, 1, 3)
        simulation = Simulation(number_line, 1, 1, 1)
        traversal_distances = [0, 1, 2, 3, 4]
        tested_p_values = [0, 1, 2, 3, 4]
        assert simulation._Simulation__find_optimal_p(
            traversal_distances, tested_p_values) == 0

    def test_funnel_to_p_value(self):
        number_line = NumberLine(0, 2, 1, 3)
        simulation = Simulation(number_line, 1, 1, 1)
        assert (simulation._Simulation__funnel_to_p_value() *
                1) % 10 >= 1


class TestUserInterface:
    @pytest.fixture
    def ui(self):
        root = tk.Tk()
        timer = ProgramTimer()
        return UserInterface(root, timer)

    def test_validate_entry_data(self, ui):
        ui.n_left_bound.set(1)
        ui.n_right_bound.set(2)
        assert ui._UserInterface__validate_entry_data() == []

    def test_calculate_stats_for_superset(self, ui):
        ui.optimal_distance_from_center_superset = [[1, 2, 3], [4, 5, 6]]
        ui._UserInterface__calculate_stats_for_superset()
        assert len(ui.optimal_distance_from_center_superset) == 2

    def test_try_run_simulation_with_single_plot(self, ui):
        ui._UserInterface__try_run_simulation_with_single_plot()
        assert True

    def test_lock_metadata(self, ui):
        ui._UserInterface__lock_metadata()
        assert 'n_left_bound' in ui.metadata

    def test_run_simulation_with_single_plot(self, ui):
        ui._UserInterface__run_simulation_with_single_plot()
        assert True

    def test_plot_optimal_distances(self, ui):
        ui._UserInterface__plot_optimal_distances()
        assert True

    def test_export_data(self, ui):
        with tempfile.TemporaryDirectory() as temp_dir:
            ui._UserInterface__export_data(temp_dir)
            exported_files = os.listdir(temp_dir)
            assert len(exported_files) > 0  # Ensure files are exported

    def test_import_data(self, ui):
        test_file_path = os.path.join(
            tempfile.gettempdir(), 'test_import.json')
        with open(test_file_path, 'w') as f:
            json.dump({}, f)
        ui._UserInterface__import_data(test_file_path)
        assert True
        os.remove(test_file_path)  # Clean up after test

    def test_synchronize_panel_with_metadata(self, ui):
        ui._UserInterface__synchronize_panel_with_metadata()
        assert True

    def test_run_simulation_across_n_values(self, ui):
        ui._UserInterface__run_simulation_across_n_values()
        assert True

    def test_run_simulation_for_n(self, ui):
        ui._UserInterface__run_simulation_for_n(1)
        assert True

    def test_quit_app(self, ui):
        ui.quit_app()
        assert True


class TestProgramTimer:
    def test_start(self):
        timer = ProgramTimer()
        timer.start()
        assert True

    def test_get_time_since_start(self):
        timer = ProgramTimer()
        timer.start()
        assert timer.get_time_since_start() >= 0

    def test_get_time_since_init(self):
        timer = ProgramTimer()
        assert timer.get_time_since_init() >= 0

    def test_get_counter_time(self):
        timer = ProgramTimer()
        assert timer.get_counter_time() >= 0

    def test_reset_counter(self):
        timer = ProgramTimer()
        timer.reset_counter()
        assert True

    def test_report_step(self):
        timer = ProgramTimer()
        timer.report_step("Test")
        assert True


class TestProgressBar:
    @pytest.fixture
    def progress_bar(self):
        root = tk.Tk()
        return ProgressBar(root)

    def test_update_progress(self, progress_bar):
        progress_bar.update_progress()
        assert True

    def test_increment_progress(self, progress_bar):
        progress_bar.increment_progress()
        assert True

    def test_clear_progress(self, progress_bar):
        progress_bar.clear_progress()
        assert True
