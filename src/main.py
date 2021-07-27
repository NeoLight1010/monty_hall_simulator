from simulation import (
    Strategy,
    get_random_strategy,
    simulate_with_random_strategy,
    Result,
    simulate_with_strategy,
)
from rich.live import Live
from rich.table import Table
from dataclasses import dataclass


@dataclass
class TableData:
    keep_wins: int = 0
    keep_losses: int = 0
    change_wins: int = 0
    change_losses: int = 0

    def update(self, strategy: Strategy, result: Result):
        if strategy == Strategy.KEEP:
            if result == Result.WIN:
                self.keep_wins += 1
            elif result == Result.LOSE:
                self.keep_losses += 1

        if strategy == Strategy.CHANGE:
            if result == Result.WIN:
                self.change_wins += 1
            elif result == Result.LOSE:
                self.change_losses += 1

    def get_keep_win_rate(self):
        try:
            return self.keep_wins / (self.keep_wins + self.keep_losses)
        except ZeroDivisionError:
            return 0

    def get_keep_lose_rate(self):
        try:
            return self.keep_losses / (self.keep_wins + self.keep_losses)
        except ZeroDivisionError:
            return 0

    def get_change_win_rate(self):
        try:
            return self.change_wins / (self.change_wins + self.change_losses)
        except ZeroDivisionError:
            return 0

    def get_change_lose_rate(self):
        try:
            return self.change_losses / (self.change_wins + self.change_losses)
        except ZeroDivisionError:
            return 0


def generate_table(data: TableData):
    table = Table("", "Keep", "Change", title="Monty Hall Simulation")

    table.add_row(
        "Win rate",
        str(round(data.get_keep_win_rate() * 100, 2)) + "%",
        str(round(data.get_change_win_rate() * 100, 2)) + "%",
    )
    table.add_row(
        "Lose rate",
        str(round(data.get_keep_lose_rate() * 100, 2)) + "%",
        str(round(data.get_change_lose_rate() * 100, 2)) + "%",
    )
    table.add_row(
        "Iterations",
        str(data.keep_wins + data.keep_losses),
        str(data.change_wins + data.change_losses),
    )

    return table


def main():
    data = TableData()

    with Live(generate_table(data), refresh_per_second=4) as live:
        for _ in range(1000):
            strategy = get_random_strategy()
            result = simulate_with_strategy(strategy)

            data.update(strategy, result)
            live.update(generate_table(data))


if __name__ == "__main__":
    main()
