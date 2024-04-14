from queue import PriorityQueue
import time
from prim_maze_generator import print_maze, generate_maze
from eight_puzzle import get_start_state, get_goal_state, get_neighbors, calculate_cost, heuristic, print_maze_raw, swap, print_maze_with_path

def dfs(maze, start, goal):
    """Depth-first search of the maze from start to goal. In this search, we visit the nodes in the order they are discovered.
    
    Args:
        maze (list): A 2D list of characters.
        start (tuple): The starting position in the maze.
        goal (tuple): The goal position in the maze.
        
    Returns:
        list: The path from start to goal."""

    # stack to store the nodes to visit
    stack = [(start, [start])]
    visited = set() # set to store the visited nodes

    # while the stack is not empty means we have not visited all the nodes
    while stack:
        # get the node (state) to visit
        (vertex, path) = stack.pop()
        # if the node has not been visited
        if vertex not in visited:
            # check if we have reached the goal
            if vertex == goal:
                return path, len(path) # return the path and cost (length of the path)
            # mark the node as visited
            visited.add(vertex)
            # get the neighbors of the current node eg, [(1,1), (1,2), (2,2), (3,2), (3,3), (3,4), (2,4), (1,4), (1,3)]
            for neighbor in get_neighbors(maze, vertex):
                # add the neighbor to the stack
                stack.append((neighbor, path + [neighbor]))
    return None, 0 # return None if we have not found the goal or the goal is not reachable

def bfs(maze, start, goal):
    """Breadth-first search of the maze from start to goal. In this search, we visit the nodes in the order of their distance from the start.
     eg, we visit the nodes that are closer to the start first.

    Args:
        maze (list): A 2D list of characters.
        start (tuple): The starting position in the maze.
        goal (tuple): The goal position in the maze.

    Returns:
        list: The path from start to goal."""

    # queue to store the nodes to visit
    queue = [(start, [start])]
    # set to store the visited nodes
    visited = set()

    # while the queue is not empty means we have not visited all the nodes
    while queue:
        # get the node (state) to visit
        (vertex, path) = queue.pop(0)
        # check if the node has not been visited
        if vertex not in visited:
            # check if we have reached the goal
            if vertex == goal:
                return path, len(path) # return the path and cost (length of the path)
            # mark the node as visited
            visited.add(vertex)
            # get the neighbors of the current node
            for neighbor in get_neighbors(maze, vertex):
                # add the neighbor to the queue
                queue.append((neighbor, path + [neighbor]))
    return None, 0 # return None if we have not found the goal or the goal is not reachable

def a_star(maze, start, goal):
    """A* search of the maze from start to goal. In this search, we visit the nodes in the order of their cost from the start.
        eg, we visit the nodes that have the lowest cost first.

    Args:
        maze (list): A 2D list of characters.
        start (tuple): The starting position in the maze.
        goal (tuple): The goal position in the maze.
    
    Returns:
        list: The path from start to goal."""

    # priority queue to store the nodes to visit
    # we are using priority queue because we want to visit the nodes with the lowest cost first
    # eg, if we have two nodes with the same cost, we will visit the node that was added first
    queue = PriorityQueue()
    queue.put((0, start, [start]))
    cost_so_far = {start: 0}

    # while the queue is not empty means we have not visited all the nodes
    while not queue.empty():
        # get the node (state) with the lowest cost or priority
        (priority, state, path) = queue.get()
        if state == goal: # return the path if we have reached the goal
            return path, cost_so_far[state] # return the path and cost
        # get the neighbors of the current state eg, [(1,1), (1,2), (2,2), (3,2), (3,3), (3,4), (2,4), (1,4), (1,3)]
        for neighbor in get_neighbors(maze, state):
            # calculate the cost of moving from the current state to the neighbor
            new_cost = cost_so_far[state] + calculate_cost(maze, state, neighbor)
            # if the neighbor has not been visited or the new cost is less than the cost of the neighbor
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                # update the cost of the neighbor   
                cost_so_far[neighbor] = new_cost
                # calculate the priority of the neighbor
                priority = new_cost + heuristic(goal, neighbor)
                # add the neighbor to the queue
                queue.put((priority, neighbor, path + [neighbor]))
    return None, 0 # return None if we have not found the goal or the goal is not reachable

if __name__ == '__main__':
    try: # get the width and height of the maze from the user
        width = input("Enter the width of the maze (default is 10): ")
        width = int(width) if width else 10
        
        height = input("Enter the height of the maze (default is 10): ")
        height = int(height) if height else 10

        difficulty = input("Enter the difficulty of the maze (0.0 - 1.0) (default is 0.5): ")
        difficulty = float(difficulty) if difficulty else 0.5

        # generate a random maze with 50% walls 
        # eg, [['w', 'w', 'w', 'w', 'w'], ['w', ' ', ' ', ' ', 'w'], ['w', ' ', 'w', ' ', 'w'], ['w', ' ', ' ', ' ', 'w'], ['w', 'w', 'w', 'w', 'w']]
        maze = generate_maze(width, height, True, difficulty)

        print("Maze:")
        print_maze(maze)
        print()
        print("Raw Maze:")
        print_maze_raw(maze)
        print(f"Start State: {get_start_state(maze)}")
        print(f"Goal State: {get_goal_state(maze)}")
        print()

        # get the start and goal states
        # the start state is the one where we start the search, it is constant for all the searches i.e. the top left corner of the maze
        # the goal state is the one where we want to reach, it is constant for all the searches i.e. the bottom right corner of the maze
        start = get_start_state(maze) # tuple eg. (1, 1)
        goal = get_goal_state(maze) # tuple eg. (1, 2)

        # perform the depth-first search
        start_time = time.time()
        path, cost = dfs(maze, start, goal) # list of tuples eg. [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (2, 4), (1, 4), (1, 3)]
        print("DFS path length: ", len(path))
        print("DFS cost: ", cost)
        print("DFS time: ", time.time() - start_time)
        # print the maze with the path
        print_maze_with_path(maze, path)
        print()

        # perform the breadth-first search
        start_time = time.time()
        path, cost = bfs(maze, start, goal) # list of tuples eg. [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (2, 4), (1, 4), (1, 3)]
        print("BFS path length: ", len(path))
        print("BFS cost: ", cost)
        print("BFS time: ", time.time() - start_time)
        print_maze_with_path(maze, path)
        print()

        # perform the A* search
        start_time = time.time()
        path, cost = a_star(maze, start, goal) # list of tuples eg. [(1, 1), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (2, 4), (1, 4), (1, 3)]
        print("A* path length: ", len(path))
        print("A* cost: ", cost)
        print("A* time: ", time.time() - start_time)
        print_maze_with_path(maze, path)
    except ValueError: # handle the case where the user enters a non-integer value
        print("Invalid input. Please enter a valid integer.")
    except Exception as e: # handle any other exceptions
        print(f"An error occurred: {e}")