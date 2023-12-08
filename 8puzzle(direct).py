import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def get_manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_row, goal_col = divmod(value - 1, 3)
                distance += abs(i - goal_row) + abs(j - goal_col)
    return distance

def get_neighbors(node):
    neighbors = []
    zero_row, zero_col = next((i, j) for i, row in enumerate(node.state) for j, val in enumerate(row) if val == 0)
    
    for action in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_row, new_col = zero_row + action[0], zero_col + action[1]
        
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = [list(row) for row in node.state]
            new_state[zero_row][zero_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[zero_row][zero_col]
            neighbors.append(PuzzleNode(new_state, node, action, node.cost + 1, get_manhattan_distance(new_state)))
    
    return neighbors

def a_star(initial_state):
    initial_node = PuzzleNode(initial_state, None, None, 0, get_manhattan_distance(initial_state))
    heap = [initial_node]
    visited_states = set()

    while heap:
        current_node = heapq.heappop(heap)

        if current_node.state == goal_state:
            return get_solution_path(current_node)

        visited_states.add(tuple(map(tuple, current_node.state)))

        for neighbor in get_neighbors(current_node):
            if tuple(map(tuple, neighbor.state)) not in visited_states:
                heapq.heappush(heap, neighbor)

def get_solution_path(node):
    path = []
    while node:
        path.append((node.state, node.action))
        node = node.parent
    return path[::-1]

def print_puzzle(puzzle):
    for row in puzzle:
        print(row)
    print()

# Example usage:
initial_state = [[1, 2, 3], [0, 4, 6], [7, 5, 8]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

solution_path = a_star(initial_state)

for state, action in solution_path:
    print_puzzle(state)
    print(f"Action: {action}")
