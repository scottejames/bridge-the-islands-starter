"""Demo runner — runs count_reachable_queries on one example case and prints the result."""

import os

from bridge_islands import count_reachable_queries
from test_data import TEST_DATA_DIR, load_case


def main() -> None:
    path = os.path.join(TEST_DATA_DIR, "medium", "01_long_chain_trap.txt")
    case = load_case(path)

    print(f"Case: {case.name}")
    print(f"Islands: {case.n}")
    print("Events:")
    for event in case.events:
        print(" ", event)

    result = count_reachable_queries(case.n, case.events)
    print(f"Queries answered yes: {result}")


if __name__ == "__main__":
    main()
