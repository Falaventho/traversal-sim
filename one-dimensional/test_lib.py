import pytest
from onedimoptlib import NumberLine


class TestNumberLine:

    def test_create_number_line(self):
        number_line = NumberLine()
        assert [number_line.start, number_line.end,
                number_line.starting_position, number_line.points] == [0, 2, 1, []]

    def test_add_point(self):

        number_line = NumberLine(0, 2, 1)

        number_line.add_point(0)
        number_line.add_point(1)
        number_line.add_point(2)

        assert number_line.points == [0, 1, 2]

    def test_add_point_outside_bounds(self):

        number_line = NumberLine(0, 2, 1)
        with pytest.raises(ValueError):
            number_line.add_point(3)

    def test_generate_random_points(self):
        number_line = NumberLine(0, 2, 1)
        random_points = number_line.generate_random_points(3)

        assert len(random_points) == 3

        for point in random_points:
            assert 0 <= point <= 2

    def test_find_best_path(self):

        number_line = NumberLine(0, 2, 1)
        number_line.add_point(0)
        number_line.add_point(1)
        number_line.add_point(2)

        assert number_line.find_best_path() == 3
