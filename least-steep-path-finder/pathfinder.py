# live version: https://repl.it/repls/TerrificIckyCode

import os
import time
import random

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clear_screen()
grid_size = int(input('Enter Grid Size: '))
grid = []

# x = 0
# for i in range(grid_size):
#     grid.append([])
#     for j in range(grid_size):
#         grid[i].append(x)
#         x += 1

for i in range(grid_size):
    grid.append([])
    for j in range(grid_size):
        grid[i].append(random.randint(1, 99))

# grid_size = 8
# grid = [
#     [25, 92, 47, 61, 13, 11, 25, 68],
#     [88, 99, 61, 20, 88, 99, 61, 20],
#     [13, 11, 25, 68, 12, 34, 37, 40],
#     [12, 34, 37, 40, 25, 92, 47, 61],
#     [88, 79, 61, 20, 88, 99, 61, 20],
#     [13, 11, 25, 68, 12, 34, 37, 40],
#     [25, 92, 61, 61, 13, 11, 25, 68],
#     [12, 34, 37, 40, 25, 92, 47, 61],
# ]

clear_screen()
print()
print('GRID')
print()
print("\t", end="")
for i in range(grid_size):
    print(str(i) + "\t", end="")
print()
print("\t", end="")
for i in range(grid_size):
    print("_\t", end="")
for i, v in enumerate(grid):
    print()
    print()
    print(str(i) + "|\t", end="")
    for j, w in enumerate(v):
        print(str(grid[i][j]) + '\t', end="")
print()
print()
print()

print('Starting Point')
input_row = int(input("Enter Row Number: "))
input_col = int(input("Enter Col Number: "))
start = (input_row, input_col, grid[input_row][input_col])
print()
print('Destination Point')
input_row = int(input("Enter Row Number: "))
input_col = int(input("Enter Col Number: "))
destination = (input_row, input_col, grid[input_row][input_col])
current = start
prev_steps = [start]
taken_steps = [start]
iterations = 1
num_of_steps = 1

for row in grid:
    print(row)
while (current[0] != destination[0] 
        or current[1] != destination[1] 
        or current[2] != destination[2]):
    row, column = current[0], current[1]
    directions = {
        'up': (row - 1, column) if row - 1 < grid_size and row - 1 >= 0 else None,
        'down': (row + 1, column) if row + 1 < grid_size and row + 1 >= 0 else None,
        'left': (row, column - 1) if column - 1 < grid_size and column - 1 >= 0 else None,
        'right': (row, column + 1) if column + 1 < grid_size and column + 1 >= 0 else None,
    }
    for direction in directions:
        if directions[direction] is not None:
            directions[direction] = (
                directions[direction][0], 
                directions[direction][1], 
                grid[directions[direction][0]][directions[direction][1]],
            )
            
            if directions[direction] in prev_steps:
                directions[direction] = None
            
    if directions['up'] is None\
        and directions['down'] is None\
        and directions['left'] is None\
        and directions['right'] is None\
        and len(prev_steps) > 2:
            current = start
            prev_steps = prev_steps[
                -iterations if iterations < len(prev_steps) else -1 * random.randint(0, len(prev_steps))
                ::]
            # prev_steps = prev_steps[-iterations::]
            taken_steps = []
            num_of_steps = 0
            iterations += 1
            
            clear_screen()
            print()
            print('GRID')
            print()
            print("\t", end="")
            for i in range(grid_size):
                print(str(i) + "\t", end="")
            print()
            print("\t", end="")
            for i in range(grid_size):
                print("_\t", end="")
            for i, v in enumerate(grid):
                print()
                print()
                print(str(i) + "|\t", end="")
                for j, w in enumerate(v):
                    temp_tuple = (i, j, w)
                    if temp_tuple in taken_steps:
                        print(str(grid[i][j]) + "^\t", end="")
                    else:
                        if temp_tuple in prev_steps:
                            print("_\t", end="")
                        else:
                            print(str(grid[i][j]) + '\t', end="")
            print()
            print()
            print()
            print('Trapped! If this does not go away in 2 seconds, then Press Ctrl+C to Quit!')
            time.sleep(0.5)
            
            # continue

    next_step = False
    pref_steps = []

    if current[2] < destination[2]:
        for direction in directions:
            if directions[direction] is not None and directions[direction][2] >= current[2]:
                pref_steps.append(directions[direction])
        
        if len(pref_steps) > 1:
            for direction in pref_steps:
                for direction_ in pref_steps:
                    if direction_[2] <= direction[2]:
                        next_step = direction_
        elif len(pref_steps) == 1:
            next_step = pref_steps[0]
        else:
            pref_steps = []
            for direction in directions:
                if directions[direction] is not None and directions[direction][2] <= current[2]:
                    pref_steps.append(directions[direction])
            if len(pref_steps) > 1:
                for direction in pref_steps:
                    for direction_ in pref_steps:
                        if direction_[2] >= direction[2]:
                            next_step = direction_
            elif len(pref_steps) == 1:
                next_step = pref_steps[0]
        
        if next_step is not False:
            current = next_step

    elif current[2] >= destination[2]:
        for direction in directions:
            if directions[direction] is not None and directions[direction][2] <= current[2]:
                pref_steps.append(directions[direction])

        if len(pref_steps) > 1:
            for direction in pref_steps:
                for direction_ in pref_steps:
                    if direction_[2] >= direction[2]:
                        next_step = direction_
        elif len(pref_steps) == 1:
            next_step = pref_steps[0]
        else:
            pref_steps = []
            for direction in directions:
                if directions[direction] is not None and directions[direction][2] >= current[2]:
                    pref_steps.append(directions[direction])
            if len(pref_steps) > 1:
                for direction in pref_steps:
                    for direction_ in pref_steps:
                        if direction_[2] <= direction[2]:
                            next_step = direction_
            elif len(pref_steps) == 1:
                next_step = pref_steps[0]
            
        if next_step is not False:
            current = next_step

    taken_steps.append(current)
    if current not in prev_steps:
        prev_steps.append(current)
    
    clear_screen()
    print()
    print('GRID')
    print()
    print("\t", end="")
    for i in range(grid_size):
        print(str(i) + "\t", end="")
    print()
    print("\t", end="")
    for i in range(grid_size):
        print("_\t", end="")
    for i, v in enumerate(grid):
        print()
        print()
        print(str(i) + "|\t", end="")
        for j, w in enumerate(v):
            temp_tuple = (i, j, w)
            if temp_tuple in taken_steps:
                print(str(grid[i][j]) + "^\t", end="")
            else:
                if temp_tuple in prev_steps:
                    print("_\t", end="")
                else:
                    print(str(grid[i][j]) + '\t', end="")
    print()
    print()
    num_of_steps += 1
    time.sleep(0.2)

clear_screen()
print()
print('FINAL GRID')
print()
print("\t", end="")
for i in range(grid_size):
    print(str(i) + "\t", end="")
print()
print("\t", end="")
for i in range(grid_size):
    print("_\t", end="")
for i, v in enumerate(grid):
    print()
    print()
    print(str(i) + "|\t", end="")
    for j, w in enumerate(v):
        temp_tuple = (i, j, w)
        if temp_tuple in taken_steps:
            print(str(grid[i][j]) + "^" + str(taken_steps.index(temp_tuple)) + "\t", end="")
        else:
            print(str(grid[i][j]) + '\t', end="")
print()
print()
print()
print('Taken Steps: ', taken_steps)
print('Iterations: ' + str(iterations))
print('Num of steps: ', num_of_steps)
