import pytest

from lib import NumberLine, Simulation
from time import sleep


class TestNumberLine:

    def test_create_number_line(self):

        number_line = NumberLine()
        number_line.points.clear()

        assert (number_line.start, number_line.end,

                number_line.starting_position, number_line.points) == (0, 2, 1, [])

    def test_add_point(self):

        number_line = NumberLine(0, 2, 1)

        number_line.points.clear()

        number_line._NumberLine__add_point(0)
        number_line._NumberLine__add_point(1)
        number_line._NumberLine__add_point(2)

        assert number_line.points == [0, 1, 2]

    def test_add_point_outside_bounds(self):

        number_line = NumberLine(0, 2, 1)

        with pytest.raises(ValueError):
            number_line._NumberLine__add_point(3)

    def test_generate_random_points(self):

        number_line = NumberLine(0, 2, 1)

        random_points = number_line._NumberLine__generate_random_points(3)

        assert len(random_points) == 3

        for point in random_points:

            assert 0 <= point <= 2

    def test_find_best_path(self):

        number_line = NumberLine(0, 2, 1)
        number_line.points.clear()
        number_line._NumberLine__add_point(0)
        number_line._NumberLine__add_point(1)
        number_line._NumberLine__add_point(2)
        number_line._NumberLine__update_attributes()

        assert number_line._NumberLine__find_best_path() == 3

    def test_display(self, capsys):

        number_line = NumberLine()
        number_line.points.clear()
        number_line._NumberLine__add_point(0)
        number_line._NumberLine__add_point(1)
        number_line._NumberLine__add_point(2)
        number_line._NumberLine__update_attributes()

        number_line.display()

        captured = capsys.readouterr()

        assert captured.out == "Number line segment: [0, 2]\nPoints on the line segment: [0, 1, 2]\nOptimal path from starting position 1 requires a traversal of 3 to contact all points.\n"

    def test_visualize(self):

        number_line = NumberLine()
        number_line.points.clear()
        number_line._NumberLine__add_point(0.5)
        number_line._NumberLine__add_point(1.5)
        number_line._NumberLine__update_attributes()

        number_line.visualize()

        # required for cleanup, stops interference with other visualizing tests

        sleep(1)

        assert True

    def test_visualize_random(self):

        number_line = NumberLine(0, 2, 1, 10)

        number_line.visualize()

        # required for cleanup, stops interference with other visualizing tests

        sleep(1)

        assert True


class TestSimulation:

    def test_create_simulation(self):

        sim = Simulation(0, 2, 1, 1, 1, 1)

        assert sim.start == 0
        assert sim.end == 2
        assert sim.number_of_points == sim.iterations == sim.repetitions == sim.significant_figures == 1
        assert len(sim.optimal_p_values) == 0

    def test_run_sim(self):

        sim = Simulation(0, 2, 1, 1, 1, 1)
        sim.run()
        assert len(sim.optimal_p_values) == 1

    def test_n_1(self):
        start = 0
        end = 2
        number_of_points = 1
        iterations = 100000
        repetitions = 1
        significant_figures = 1

        sim = Simulation(start, end, number_of_points,
                         iterations, repetitions, significant_figures)
        sim.run()
        assert sim.optimal_p_values[0] == 1.0

    def test_repetitions(self):
        start = 0
        end = 2
        number_of_points = 1
        iterations = 1
        repetitions = 5
        significant_figures = 1

        sim = Simulation(start, end, number_of_points,
                         iterations, repetitions, significant_figures)
        sim.run()

        assert len(sim.optimal_p_values) == repetitions
