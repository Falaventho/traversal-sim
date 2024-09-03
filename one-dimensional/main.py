from lib import Dataset


def main():

    running = True
    print("1D Travel Optimization Simulation -- Alterable Point\n")

    while running:
        running = menu()


def menu() -> bool:
    start = float(input("Left bound: "))
    end = float(input("Right bound: "))
    starting_position = float(input("Starting position A: "))
    right_position_bound = float(input("Starting position B: "))
    step = float(input("Step amount: "))
    number_of_points = int(input("Number of points: "))
    iterations = int(input("Iterations per step: "))

    superset = []

    while starting_position <= right_position_bound:
        dataset = Dataset(start, end, starting_position,
                          number_of_points, iterations)
        dataset.gather()
        stats = bundle_stats(dataset)
        superset.append(stats)

        starting_position += step

    print_superset(superset)

    print_best(superset)

    return input("Run again? y/n") == 'y'


def bundle_stats(dataset: Dataset) -> object:

    stats = {
        "avg_path": dataset.get_mean_path(),
        "avg_min": dataset.get_mean_min(),
        "avg_max": dataset.get_mean_max(),
        "start": dataset.start,
        "end": dataset.end,
        "starting_position": dataset.starting_position,
        "number_of_points": dataset.number_of_points,
        "iterations": dataset.iterations
    }

    return stats


def find_best_starting_position_and_traversal(superset: list[object]) -> dict:
    best_val = superset[0]["avg_path"]
    best_position = superset[0]["starting_position"]

    for stats in superset:
        if stats["avg_path"] < best_val:
            best_val = stats["avg_path"]
            best_position = stats["starting_position"]

    return {
        "best_val": best_val,
        "best_position": best_position
    }


def print_superset(superset: list[object]):
    for idx, stats in enumerate(superset):
        print(f"Dataset {idx+1}")
        print(f"For P={stats["starting_position"]}" +
              f", n={stats["number_of_points"]}. {stats["iterations"]} iterations.")
        print(f"Average traversal length: {stats["avg_path"]}")
        print(f"Average minimum: {stats["avg_min"]}")
        print(f"Average maximum: {stats["avg_max"]}\n")


def print_best(superset: list[object]):
    start = superset[0]["start"]
    end = superset[0]["end"]
    best_data = find_best_starting_position_and_traversal(superset)
    number_of_points = superset[0]["number_of_points"]
    best_starting_position = best_data["best_position"]
    best_traversal_length = best_data["best_val"]

    print(f"Best starting position for n={number_of_points} in range ({start},{end}) is found at " +
          f"P={best_starting_position} with average traversal of {best_traversal_length}.")


if __name__ == '__main__':
    main()
