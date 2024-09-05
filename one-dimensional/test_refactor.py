import pytest
from refactor import RandomPointGenerator
import random


class TestPointGenerator:
    def test_random_point_generator(self):
        pg = RandomPointGenerator()
        n = random.randint(0, 1000)
        points = pg.generate_points(0, 2, n)
        assert len(points) == n
