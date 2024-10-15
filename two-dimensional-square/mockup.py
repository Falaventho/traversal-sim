import itertools
import random
import math


class Point:

    def __init__(self, x: float, y: float, id_num: int):
        self.x = x
        self.y = y
        self.id_num = id_num


def generate_points(starting_point: Point, num_points: int) -> list[Point]:
    points = [starting_point]
    for i in range(num_points):
        rand_x = random.uniform(0, 1)
        rand_y = random.uniform(0, 1)
        new_point = Point(rand_x, rand_y, i)
        points.append(new_point)
    return points


def calc_dist(a: Point, b: Point):
    x_delta = abs(a.x - b.x)
    y_delta = abs(a.y - b.y)
    return math.sqrt((x_delta ** 2) + (y_delta ** 2))


def generate_path_map(points: list[Point]) -> dict:
    path_map = {}
    for i in range(len(points)):
        for p in points[i+1:]:
            dist = calc_dist(points[i], p)
            path_map[(points[i], p)] = dist
            path_map[(p, points[i])] = dist

    return path_map


def find_all_hamiltonian_path_lengths(points, path_map):
    starting_point = points[0]
    working_points = points[1:]
    permutations = list(itertools.permutations(working_points))
    distances = []

    for perm in permutations:
        dist = path_map[(starting_point, perm[0])]
        for i in range(len(perm) - 1):
            dist += path_map[(perm[i], perm[i+1])]
        distances.append(dist)

    return (permutations, distances)


def print_path(perm):
    return f"({', '.join([str(p.id_num) for p in perm])})"


def main():
    starting_point = Point(0.5, 0.5, 0)
    num_points = 4
    points = generate_points(starting_point, num_points)
    path_map = generate_path_map(points)
    perms, dists = find_all_hamiltonian_path_lengths(points, path_map)
    min_dist = min(dists)
    min_perm = perms[dists.index(min_dist)]
    print(f"Minimum distance: {min_dist}")
    print(f"Minimum path: {print_path(min_perm)}")


if __name__ == "__main__":
    main()
