import pytest
from lib import NumberLine
from time import sleep


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

    def test_display(self, capsys):

        number_line = NumberLine()

        number_line.add_point(0)
        number_line.add_point(1)
        number_line.add_point(2)

        number_line.display()

        captured = capsys.readouterr()
        assert captured.out == "Number line segment: [0, 2]\nPoints on the line segment: [0, 1, 2]\nOptimal path from starting position 1 requires a traversal of 3 to contact all points.\n"

    def test_visualize(self):

        number_line = NumberLine()

        number_line.add_point(0.5)
        number_line.add_point(1.5)

        number_line.visualize()

        # required for cleanup, stops interference with other visualizing tests
        sleep(1)

        assert True

    def test_visualize_random(self):

        number_line = NumberLine()

        random_points = number_line.generate_random_points(10)

        for point in random_points:
            number_line.add_point(point)

        assert len(number_line.points) == 10

        number_line.visualize()
        # required for cleanup, stops interference with other visualizing tests
        sleep(1)

        assert True
