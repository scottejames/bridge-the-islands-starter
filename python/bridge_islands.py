"""
Bridge the Islands.

Implement count_reachable_queries below. See ../README.md for the full
problem statement, constraints, and worked examples.

The helper functions are optional scaffolding — use them, change their
signatures, or delete them and structure your solution however you like.
"""

from typing import List, Tuple


def parse_event(event: str) -> Tuple[str, int, int]:
    """Split an event string like "U 3 5" into ("U", 3, 5)."""
    # TODO: implement
    raise NotImplementedError


def is_valid_island(island: int, n: int) -> bool:
    """Return True if island is a valid index for n islands (0 to n-1)."""
    # TODO: implement
    raise NotImplementedError


def count_reachable_queries(n: int, events: List[str]) -> int:
    """
    Process events in order. Each event is either "U u v" (build a bridge
    between islands u and v, permanently) or "Q u v" (query: can you
    currently travel from u to v using any sequence of built bridges?).

    Return how many of the Q events were answered "yes".
    """
    # TODO: implement
    raise NotImplementedError
