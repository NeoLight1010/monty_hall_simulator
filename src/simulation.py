from enum import Enum
import random


class Strategy(Enum):
    CHANGE = 0
    KEEP = 1


class Result(Enum):
    LOSE = 0
    WIN = 1


def get_random_strategy() -> Strategy:
    return random.choice(list(Strategy))


def simulate_with_strategy(strategy: Strategy) -> Result:
    closed_doors = {0, 1, 2}

    win_door = random.choice(list(closed_doors))
    chosen_door = random.choice(list(closed_doors))

    # Choose door to open.
    open_door = closed_doors - {win_door} - {chosen_door}
    if len(open_door) == 2:
        open_door = open_door - {random.choice(list(open_door))}
    open_door = list(open_door)[0]

    # Open door.
    closed_doors = closed_doors - {open_door}

    # Apply strategy
    if strategy == Strategy.KEEP:
        pass

    if strategy == Strategy.CHANGE:
        chosen_door = list(closed_doors - {chosen_door})[0]  # Switch chosen door.

    if win_door == chosen_door:
        return Result.WIN
    return Result.LOSE


def simulate_with_random_strategy() -> Result:
    strategy = get_random_strategy()
    return simulate_with_strategy(strategy)
