import csv
import glob
import json

import click
import cv2
import numpy as np

from .simulation import simulate_against


@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False))
@click.argument("output", type=click.Path(exists=False, file_okay=False, writable=True))
def main(path, output):
    files = glob.glob(f"{path}/*.json")
    results = [[(0, 0) for _ in files] for _ in files]
    results_reversed = [[(0, 0) for _ in files] for _ in files]

    for player1_id, player1 in enumerate(files):
        for player2_id, player2 in enumerate(files):
            if player1 == player2:
                continue

            # Get player names
            player1_name = player1.split("/")[-1].split(".")[0]
            player2_name = player2.split("/")[-1].split(".")[0]

            print()
            print("#" * 80)
            print(f"Simulating {player1} against {player2}")
            print("#" * 80)

            grid1 = np.bool(np.array(json.load(open(player1))))
            if grid1.shape != (250, 100):
                raise ValueError(
                    f"Invalid shape for {player1}: {grid1.shape}; expected (250, 100)"
                )

            grid2 = np.bool(np.array(json.load(open(player2))))
            if grid2.shape != (250, 100):
                raise ValueError(
                    f"Invalid shape for {player2}: {grid2.shape}; expected (250, 100)"
                )

            # Rotate 180 degrees (flip along both axes)
            grid2_reversed = np.flip(np.flip(grid2, axis=0), axis=1)

            player1_stats, player2_stats = simulate_against(
                grid1,
                grid2,
                display_frequency=100,
                plot_path=f"{output}/{player1_name}_vs_{player2_name}.png",
            )

            player1_stats_reversed, player2_stats_reversed = simulate_against(
                grid1,
                grid2_reversed,
                display_frequency=100,
                plot_path=f"{output}/{player1_name}_vs_{player2_name}_reversed.png",
            )

            print(f"{player1_name} stats: {player1_stats}")
            print(f"{player2_name} stats: {player2_stats}")
            print(f"{player1_name} stats (reversed): {player1_stats_reversed}")
            print(f"{player2_name} stats (reversed): {player2_stats_reversed}")

            results[player1_id][player2_id] = (
                player1_stats,
                player2_stats,
            )
            results_reversed[player1_id][player2_id] = (
                player1_stats_reversed,
                player2_stats_reversed,
            )

    # Save the table as csv (true if row won)
    with open(f"{output}/results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow([""] + [f.split("/")[-1].split(".")[0] for f in files])
        for i, raw_results in enumerate(results):
            bool_results = [
                int(raw_results[j][0] > raw_results[j][1]) for j in range(len(files))
            ]
            bool_results[i] = ""
            writer.writerow([files[i].split("/")[-1].split(".")[0]] + bool_results)

    # Save the table as csv (scores)
    with open(f"{output}/scores.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow([""] + [f.split("/")[-1].split(".")[0] for f in files])
        for i, raw_results in enumerate(results):
            scores = [
                f"{raw_results[j][0]}-{raw_results[j][1]}" for j in range(len(files))
            ]
            writer.writerow([files[i].split("/")[-1].split(".")[0]] + scores)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
