from rich import box
from rich.console import Console
from simulation import (
    Strategy,
    get_random_strategy,
    Result,
    simulate_with_strategy,
)
from rich.live import Live
from rich.table import Table
from rich.align import Align, AlignMethod
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

    def get_total_iterations(self):
        return self.keep_wins + self.keep_losses + self.change_wins + self.change_losses

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
    table = Table(title="Monty Hall Simulation", box=box.ROUNDED)
    
    table.add_column("", style="bold red")
    table.add_column("Keep", style="cyan")
    table.add_column("Change", style="green")

    table.add_row(
        "Win rate",
        "{:.2f}%".format(data.get_keep_win_rate() * 100, 2),
        "{:.2f}%".format(data.get_change_win_rate() * 100, 2),
    )
    table.add_row(
        "Lose rate",
        "{:.2f}%".format(data.get_keep_lose_rate() * 100, 2),
        "{:.2f}%".format(data.get_change_lose_rate() * 100, 2),
    )
    table.add_row(
        "Iterations",
        str(data.keep_wins + data.keep_losses),
        str(data.change_wins + data.change_losses),
    )

    return Align(table, "center")


def main():
    console = Console()
    data = TableData()

    console.clear()
    with Live(generate_table(data), refresh_per_second=30, console=console) as live:
        for _ in range(100000):
            strategy = get_random_strategy()
            result = simulate_with_strategy(strategy)

            data.update(strategy, result)
            live.update(generate_table(data))

    console.print(f"[red bold]Total iterations:[/] {data.get_total_iterations()}")


if __name__ == "__main__":
    main()
