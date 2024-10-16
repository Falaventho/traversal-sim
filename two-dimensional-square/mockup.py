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


def gather(starting_point, num_points):
    points = generate_points(starting_point, num_points)
    path_map = generate_path_map(points)
    permutations, dists = find_all_hamiltonian_path_lengths(points, path_map)
    min_dist = min(dists)
    min_perm = permutations[dists.index(min_dist)]
    return (min_dist, min_perm)


def generate_start_set():
    gen_x = 0.5
    gen_y = 0.5

    points = [Point(gen_x, gen_y, 0)]

    for y_offset in range(6):
        y_offset = float(y_offset) / 10
        gen_y = 0.5 + y_offset

        for x_offset in range(6):
            x_offset = float(x_offset) / 10
            if x_offset > y_offset:
                break
            gen_x = 0.5 + x_offset
            new_point = Point(gen_x, gen_y, 0)
            points.append(new_point)

    return points


def main():
    starting_point_set = generate_start_set()
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

            for i in range(iterations):
                dist, perm = gather(starting_point, num_points)
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
        print(f"True minimum distance for n={num_points}: {true_min_distance}")
        print(f"True minimum starting point for n={num_points}: (" +
              f"{true_min_start.x}, {true_min_start.y})")
        print(f"Average minimum distance for n={num_points}: " +
              f"{sum(min_distances) / len(min_distances)}")


if __name__ == "__main__":
    main()
