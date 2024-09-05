import pytest
from refactor import RandomPointGenerator, NumberLine
import random


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
