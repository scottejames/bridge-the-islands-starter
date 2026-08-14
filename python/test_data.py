"""
Loads Bridge the Islands test cases from ../test_data/{simple,medium,hard}/*.txt.

File format:

    name=<case name>
    n=<int>
    expected=<int>
    events=
    <event 0>
    <event 1>
    ...
"""

import os
from dataclasses import dataclass
from typing import List

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "test_data")


@dataclass
class TestCase:
    name: str
    n: int
    events: List[str]
    expected: int


def load_case(path: str) -> TestCase:
    with open(path) as f:
        lines = f.read().splitlines()

    name = None
    n = None
    expected = None
    events_start = None

    for i, line in enumerate(lines):
        if line == "events=":
            events_start = i + 1
            break
        key, _, value = line.partition("=")
        if key == "name":
            name = value
        elif key == "n":
            n = int(value)
        elif key == "expected":
            expected = int(value)

    events = lines[events_start:]
    return TestCase(name=name, n=n, events=events, expected=expected)


def load_tier(tier: str) -> List[TestCase]:
    tier_dir = os.path.join(TEST_DATA_DIR, tier)
    cases = []
    for filename in sorted(os.listdir(tier_dir)):
        if filename.endswith(".txt"):
            cases.append(load_case(os.path.join(tier_dir, filename)))
    return cases
