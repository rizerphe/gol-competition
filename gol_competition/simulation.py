import cv2
import matplotlib.pyplot as plt
import numpy as np


def simulate_against(
    grid1: np.ndarray[np.bool_] | None = None,
    grid2: np.ndarray[np.bool_] | None = None,
    display_frequency: int = 100,
    plot_path: str | None = None,
) -> tuple[int, int]:
    # Initialize a 300x300 grid and a corresponding is_red array
    grid = np.zeros((300, 300), dtype=np.uint8)
    is_red = np.zeros((300, 300), dtype=np.bool_)

    # Place two 100x250 grids
    grid[25:275, 25:125] = (
        np.random.randint(0, 2, (250, 100)) if grid1 is None else grid1
    )
    grid[25:275, 175:275] = (
        np.random.randint(0, 2, (250, 100)) if grid2 is None else grid2
    )

    # Initialize colors for existing cells
    is_red[25:275, 25:125] = True
    is_red[25:275, 175:275] = False

    # Initialize stats tracking
    step = 0
    stats = []

    while True:
        # Sum up the neighbors of each cell using toroidal geometry
        neighbors = np.zeros_like(grid)
        red_neighbors = np.zeros_like(grid)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                rolled = np.roll(np.roll(grid, i, axis=0), j, axis=1)
                neighbors += rolled
                red_neighbors += rolled * np.roll(np.roll(is_red, i, axis=0), j, axis=1)

        # Apply the Game of Life rules
        new_born = (grid == 0) & (neighbors == 3)
        survivors = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
        grid = (survivors | new_born).astype(np.uint8)

        # Update colors for newly born cells
        is_red[new_born] = red_neighbors[new_born] > (neighbors[new_born] / 2)

        # Increment step counter
        step += 1

        if display_frequency and not step % display_frequency:
            # Create RGB image for a single 300x300 grid
            rgb_image = np.concatenate(
                [
                    np.zeros((300, 300, 1), dtype=np.uint8),
                    np.full(
                        (300, 300, 1),
                        255 * (1 - is_red).reshape(300, 300, 1),
                        dtype=np.uint8,
                    ),
                    np.full(
                        (300, 300, 1), 255 * is_red.reshape(300, 300, 1), dtype=np.uint8
                    ),
                ],
                axis=2,
            )
            rgb_image = rgb_image * grid.reshape(300, 300, 1)

            # Create a 600x600 grid with 4 copies of the field
            large_rgb_image = np.zeros((600, 600, 3), dtype=np.uint8)
            large_rgb_image[:300, :300] = rgb_image
            large_rgb_image[:300, 300:] = rgb_image
            large_rgb_image[300:, :300] = rgb_image
            large_rgb_image[300:, 300:] = rgb_image

            # Display the 600x600 grid
            cv2.imshow("Game of Life - Toroidal Display", large_rgb_image)

        # Print stats every 100 steps
        if step % 100 == 0:
            red_count = np.sum(grid * is_red)
            green_count = np.sum(grid * (1 - is_red))
            print(f"Step: {step}, Red: {red_count}, Green: {green_count}")
            stats.append((step, red_count, green_count))

        if display_frequency:
            # Break if the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord("q") or step > 5000:
                break

    # Determine the winner
    red_count = np.sum(grid * is_red)
    green_count = np.sum(grid * (1 - is_red))

    # Plot stats
    steps, red_counts, green_counts = zip(*stats)
    plt.figure(figsize=(10, 6))
    plt.plot(steps, red_counts, "r-", label="Red")
    plt.plot(steps, green_counts, "g-", label="Green")
    plt.xlabel("Steps")
    plt.ylabel("Cell Count")
    plt.title("Cell Population over Time")
    plt.legend()
    plt.grid(True)

    if plot_path:
        plt.savefig(plot_path)
    else:
        plt.show()
    return (red_count, green_count)


if __name__ == "__main__":
    simulate_against()
