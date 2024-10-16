import itertools
import random
import math
from typing import List, Tuple, Dict


class Point:
    def __init__(self, x: float, y: float, id_num: int):
        self.x = x
        self.y = y
        self.id_num = id_num


class PointGenerator:
    @staticmethod
    def generate_points(starting_point: Point, num_points: int) -> List[Point]:
        points = [starting_point]
        for i in range(num_points):
            rand_x = random.uniform(0, 1)
            rand_y = random.uniform(0, 1)
            new_point = Point(rand_x, rand_y, i)
            points.append(new_point)
        return points

    @staticmethod
    def generate_start_set() -> List[Point]:
        points = []
        for y_offset in range(6):
            y_offset = float(y_offset) / 10
            gen_y = 0.5 + y_offset
            for x_offset in range(6):
                x_offset = float(x_offset) / 10
                gen_x = 0.5 + x_offset
                new_point = Point(gen_x, gen_y, 0)
                points.append(new_point)
        return points


class DistanceCalculator:
    @staticmethod
    def calc_dist(a: Point, b: Point) -> float:
        x_delta = abs(a.x - b.x)
        y_delta = abs(a.y - b.y)
        return math.sqrt((x_delta ** 2) + (y_delta ** 2))


class PathMapGenerator:
    @staticmethod
    def generate_path_map(points: List[Point]) -> Dict[Tuple[Point, Point], float]:
        path_map = {}
        for i in range(len(points)):
            for p in points[i+1:]:
                dist = DistanceCalculator.calc_dist(points[i], p)
                path_map[(points[i], p)] = dist
                path_map[(p, points[i])] = dist
        return path_map


class HamiltonianPathFinder:
    @staticmethod
    def find_all_hamiltonian_path_lengths(points: List[Point], path_map: Dict[Tuple[Point, Point], float]) -> Tuple[List[Tuple[Point, ...]], List[float]]:
        starting_point = points[0]
        working_points = points[1:]
        permutations = list(itertools.permutations(working_points))
        distances = []

        for perm in permutations:
            dist = path_map[(starting_point, perm[0])]
            for i in range(len(perm) - 1):
                dist += path_map[(perm[i], perm[i+1])]
            distances.append(dist)

        return permutations, distances


class PathPrinter:
    @staticmethod
    def print_path(perm: Tuple[Point, ...]) -> str:
        return f"({', '.join([str(p.id_num) for p in perm])})"


class Gatherer:
    @staticmethod
    def gather(starting_point: Point, num_points: int) -> Tuple[float, Tuple[Point, ...]]:
        points = PointGenerator.generate_points(starting_point, num_points)
        path_map = PathMapGenerator.generate_path_map(points)
        permutations, dists = HamiltonianPathFinder.find_all_hamiltonian_path_lengths(
            points, path_map)
        min_dist = min(dists)
        min_perm = permutations[dists.index(min_dist)]
        return min_dist, min_perm


class MainApp:
    @staticmethod
    def main():
        starting_point_set = PointGenerator.generate_start_set()
        left = int(input("Enter left bound of n-values: "))
        right = int(input("Enter right bound of n-values: ")) + 1
        point_range = range(left, right)
        iterations = int(input("How many iterations: "))

        for num_points in point_range:
            min_distances = []
            min_permutations = []
            min_start = []

            for starting_point in starting_point_set:
                distances = []
                permutations = []

                for _ in range(iterations):
                    dist, perm = Gatherer.gather(starting_point, num_points)
                    distances.append(dist)
                    permutations.append(perm)

                min_distance = min(distances)
                min_permutation = permutations[distances.index(min_distance)]
                min_distances.append(min_distance)
                min_permutations.append(min_permutation)
                min_start.append(starting_point)

            true_min_distance = min(min_distances)
            true_min_index = min_distances.index(true_min_distance)
            true_min_start = min_start[true_min_index]
            print(f"True minimum distance for n=" +
                  f"{num_points}: {true_min_distance}")
            print(f"True minimum starting point for n=" +
                  f"{num_points}: ({true_min_start.x}, {true_min_start.y})")
            print(f"Average minimum distance for n={num_points}: " +
                  f"{sum(min_distances) / len(min_distances)}")


if __name__ == "__main__":
    MainApp.main()
