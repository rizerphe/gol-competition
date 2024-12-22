# GOL-competition

A tiny helper tool to run a pairwise competition between multiple players in a toroidal 300x300 colored Game of Life setup.

## Installation

```bash
pipx install git+https://github.com/rizerphe/gol-competition
```

## Usage

```bash
gol-competition path/to/folder/containing/json/files path/to/output/folder
```

## How to read the results

`scores.csv` - corresponds to the actual scores of each game. First the score of the row, then the score of the column. As in, for this table `player_b` won.

```
,player_a,player_b
player_a,0-0,0-4
player_b,4-0,0-0
```

`results.csv` - is 1 if the row player won, 0 if the column player won. As in, for this table `player_b` won.

```
,player_a,player_b
player_a,,0
player_b,1,
```

In the plots, the first player mentioned by name is red, the second one is green. As in, for `player_a_vs_player_b.png`, `player_a` is red and `player_b` is green.

`results_reversed.csv` and `scores_reversed.csv` are exactly the same as above. The tables are not reversed, ontly one of the players turned upside down. These are all possible competition configurations, as long as the players cannot be, for example, flipped.
