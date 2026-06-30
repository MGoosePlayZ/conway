#!/usr/bin/env -S uv run

import copy
import random
from time import sleep

# CONFIG
cols, rows = 100, 100
sleeptime = 0.02

game_of_life_defaults = {
    "rulestring": [[3], [2,3]],
    
    "checked": [[-1, -1], [-1, 0], [-1, 1], 
                [0, -1],           [0, 1], 
                [1, -1],  [1, 0],  [1, 1]],
    "loopover": True
}

def weighted_grid(rows, cols, alive_chance=0.2):
    weights = [1 - alive_chance, alive_chance]
    
    grid = [
        [random.choices([0, 1], weights=weights)[0] for _ in range(cols)] 
        for _ in range(rows)
    ]
    return grid

def random_grid(rows, cols):
    return [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    
def pattern(rows, cols, pattern, start_row, start_col):
    """
    Creates a blank grid (all 0s) and places a specific pattern at the target position.
    """
    
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    pattern_rows = len(pattern)
    pattern_cols = len(pattern[0]) if pattern_rows > 0 else 0
    
    for r in range(pattern_rows):
        for c in range(pattern_cols):
            grid_r = start_row + r
            grid_c = start_col + c
            grid[grid_r][grid_c] = pattern[r][c]
                
    return grid

def game_of_life(grid,
    rulestring = game_of_life_defaults["rulestring"],
    checked = game_of_life_defaults["checked"],
    loopover = game_of_life_defaults["loopover"]) -> list[list[int]]:

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    output = copy.deepcopy(grid)
    
    for r in range(rows):
        for c in range(cols):
            neighbors = 0
            
            for dr, dc in checked:
                nr, nc = r + dr, c + dc
                
                if loopover:
                    nr %= rows
                    nc %= cols
                    neighbors += grid[nr][nc]
                else:
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbors += grid[nr][nc]
            
            if grid[r][c] == 0:  # Dead cell
                if neighbors in rulestring[0]:  # Birth
                    output[r][c] = 1
            else:  # Alive cell
                if neighbors in rulestring[1]:  # Survival
                    pass 
                else:  # Death
                    output[r][c] = 0

    return output

def print_grid(matrix: list[list[int]]):

    for row in matrix:
        line = "".join("██" if cell == 1 else "  " for cell in row)
        print(line)   

def main():
    #grid = random_grid(rows, cols)
    grid = weighted_grid(rows, cols, 0.1)
    #grid = pattern(rows, cols, [[0,1,0],[0,0,1],[1,1,1]], rows//2, cols//2)
    
    while True:
        print_grid(grid)
        grid = game_of_life(grid)
        sleep(sleeptime)

if __name__ == "__main__":
    main()