import pytest
from refactor import RandomPointGenerator, NumberLine
import random
from time import sleep


class TestPointGenerator:
    def test_random_point_generator(self):
        pg = RandomPointGenerator()
        n = random.randint(0, 1000)
        points = pg.generate_points(0, 2, n)
        assert len(points) == n


class TestNumberLine:
    def test_number_line_display(self, capsys):
        n = random.randint(0, 100)
        number_line = NumberLine(0, 2, 1, n)
        number_line.display()
        captured = capsys.readouterr()
        assert captured.out[:20] == "Number line segment:"

    def test_number_line_visualize(self):
        n = random.randint(0, 100)
        number_line = NumberLine(0, 2, 1, n)
        number_line.visualize()
        # required for cleanup, stops interference with other visualizing tests
        sleep(1)
        assert True

    def test_number_line_regenerate_data(self):
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
