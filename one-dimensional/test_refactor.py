import pytest
from refactor import RandomPointGenerator, NumberLine, Simulation
import random
from time import sleep


class TestPointGenerator:
    def test_generate_points(self):
        pg = RandomPointGenerator()
        n = random.randint(0, 1000)
        points = pg.generate_points(0, 2, n)
        assert len(points) == n


class TestNumberLine:
    def test_display(self, capsys):
        n = random.randint(0, 100)
        number_line = NumberLine(0, 2, 1, n)
        number_line.display()
        captured = capsys.readouterr()
        assert captured.out[:20] == "Number line segment:"

    def test_visualize(self):
        n = random.randint(0, 100)
        number_line = NumberLine(0, 2, 1, n)
        number_line.visualize()
        # required for cleanup, stops interference with other visualizing tests
        sleep(1)
        assert True

    def test_regenerate_data(self):
        n = random.randint(0, 100)
        number_line = NumberLine(0, 2, 1, n)
        points = number_line.points
        number_line.regenerate_data()
        assert points != number_line.points

    def test_find_best_path(self):
        number_line = NumberLine(0, 2, 1, 1)
        number_line.max_point = 1.5
        number_line.min_point = 0.5
        distance = number_line._NumberLine__find_best_path()
        assert distance == 1.5


class TestSimulation:
    def test_run(self):
        r = random.randint(0, 100)
        number_line = NumberLine(0, 2, 1, 3)
        simulation = Simulation(number_line, 1, r, 1)
        simulation.run()
        assert len(simulation.optimal_p_values) == r

    def test_gather(self):
        pass

    def test_funnel_to_p_value(self):
        pass

    def test_find_optimal_p(self):
        pass
