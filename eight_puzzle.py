import copy
import random

def is_goal(maze, state):
    """This function is used to check if the current state is the goal state.

    Args:
        maze (list): A 2D list of characters.
        state (tuple): A tuple representing the current state.

    Returns:
        bool: True if the current state is the goal state, False otherwise."""
    return maze[state[0]][state[1]] == 'c' # check if the current state is the goal state (c)

def next_states(maze, state):
    """This function is used to get the next states from the current state.

    Args:
        maze (list): A 2D list of characters.
        state (tuple): A tuple representing the current state.

    Returns:
        list: A list of tuples representing the next states."""
    return get_neighbors(maze, state) # get the neighbors of the current state

def print_maze_with_path(maze, path):
    """Prints the maze with a path drawn through it.
    
    Args:
        maze (list): A 2D list of characters.
        path (list): A list of tuples representing the path.
    """
    
    # mark the path with '*'
    for position in path:
        maze[position[0]][position[1]] = '*'
    
    # print the maze
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if (maze[i][j] == 'u') or (maze[i][j].isdigit()):
                print(str(maze[i][j]), end="")
            elif (maze[i][j] == 'c'):
                print(" ", end="")
            elif (maze[i][j] == '*'):  # added this condition to print the path
                print("*", end="")
            else:
                print("\u2587", end="")
        print()

def get_neighbors(maze, state):
    """Returns the neighbors of a given state in the maze.
    
    Args:
        maze (list): A 2D list of characters.
        state (tuple): A tuple representing the current state. 
        
    Returns:
        list: A list of tuples representing the neighbors of the current state."""

    # get the x and y coordinates of the current state
    x, y = state
    # get the neighbors of the current state
    # here we are only considering the neighbors that are not walls ('w')
    # and are within the bounds of the maze
    # the neighbors are the states that can be reached from the current state by moving up, down, left, or right
    # the neighbors are represented as tuples (x, y)
    neighbors = [(nx, ny) for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                 if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != 'w']
    return neighbors # list of tuples eg. [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (2, 4), (1, 4), (1, 3)]

def calculate_cost(maze, state, neighbor):
    """Returns the cost of moving from a state to a neighbor.
    
    Args:
        maze (list): A 2D list of characters.
        state (tuple): A tuple representing the current state.
        neighbor (tuple): A tuple representing the neighbor state.
        
    Returns:
        int: The cost of moving from the current state to the neighbor."""

    # setup cost based on numbers present in the maze
    # the cost of moving from one state to another is based on the number present in the maze
    # eg, for number 1, the cost is 1, for number 2, the cost is 2, and so on
    # if the state or neighbor is a space (' '), the cost is 1
    # default cost is 1 if the number is not present in the cost_map
    cost_map = {'1': 1, '2': 2, '3': 3, '4': 4, ' ': 1}
    base_cost = cost_map.get(maze[neighbor[0]][neighbor[1]], 1)

    # add extra cost for diagonal moves
    # eg, if the current state is (1, 1) and the neighbor is (2, 2) and is has a cost of 1
    # then the cost of moving from (1, 1) to (2, 2) is 1.5
    # this is because the neighbor is a diagonal move from the current state
    if state[0] != neighbor[0] and state[1] != neighbor[1]:
        base_cost += 0.5

    return base_cost

def heuristic(goal, neighbor):
    """Returns the Manhattan distance from a neighbor to the goal.    
    This function calculates the Manhattan distance from a neighbor state to the goal state.
    The Manhattan distance is the sum of the absolute differences in the x and y coordinates.
    For example, the Manhattan distance from (1, 1) to (3, 3) is 4.

    This is a good heuristic because it never overestimates the distance to the goal 
    because in a grid you can't get closer to the goal without moving at least the Manhattan distance,
    If a heuristic overestimates the distance to the goal, A* might not find the shortest path, 
    but since this heuristic doesn't, A* is guaranteed to find the shortest path when using it.
    It's also efficient to compute, as it's just addition and absolute value.

    Args:
        goal (tuple): The goal state.
        neighbor (tuple): The neighbor state.

    Returns:
        int: The Manhattan distance from the neighbor to the goal."""
    return abs(goal[0] - neighbor[0]) + abs(goal[1] - neighbor[1])

def swap(board, loc1, loc2):
    """Returns a new board that is a deep copy
    of 'board', but with the tiles at 'loc1' and
    'loc2' switched. board is a 3x3 array, loc1
    and loc2 are 2-tuples of locations.
    
    Args:
        board (list): A 3x3 array.
        loc1 (tuple): A 2-tuple of locations.
        loc2 (tuple): A 2-tuple of locations.
        
    Returns:
        list: A new board that is a deep copy of 'board', but with the tiles at 'loc1' and 'loc2' switched."""

    # make a deep copy of the board
    new_board = copy.deepcopy(board)

    # swap loc1 and loc2
    temp = new_board[loc1[0]][loc1[1]]
    new_board[loc1[0]][loc1[1]] = new_board[loc2[0]][loc2[1]]
    new_board[loc2[0]][loc2[1]] = temp

    # return the result
    return new_board

def get_start_state(maze):
    """Returns the goal state in the maze, which is the last 'c' in the last row.
    
    Args:
        maze (list): A 2D list of characters.
        
    Returns:
        tuple: The goal state in the maze."""
    first_row = maze[0]
    for j in range(len(first_row)):
        if first_row[j] == 'c':
            return (0, j)
    return None

def get_goal_state(maze):
    """Returns the goal state in the maze, which is the last 'c' in the last row.
    
    Args:
        maze (list): A 2D list of characters.
        
    Returns:
        tuple: The goal state in the maze."""
    last_row = maze[-1]
    for j in reversed(range(len(last_row))):
        if last_row[j] == 'c':
            return (len(maze)-1, j)
    return None

def print_maze_raw(maze):
    """Prints the maze.
    
    Args:
        maze (list): A 2D list of characters.
        
    Returns:
        None."""

    # print the maze row by row 
    # the expected output will look like this:
    # wwww
    # wccw
    # wwww
    for row in maze:
        print(''.join(row))
    print()