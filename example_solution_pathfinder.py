"""Example solution to the pathfinder file."""


from util import MinPriorityQueue


#
# CLASSES
#
class PositionAndPath:
    """Class for containing a position coordinate pair and a series of directions to reach it.
    Also automatically calculates f(s) for this position.
    """

    def __init__(self, coords: list, path: list, maze):
        """
        :param coords:      list of 2 integers: [row, column]
        :param path:        list of directions 'u', 'd', 'l', 'r' to get from the start to this point
        :param maze:        the problem Maze object
        """
        # Handle errors
        # coords not a list
        if not isinstance(coords, list):
            raise TypeError("coords must be a list")
        # coords does not have length 2
        if len(coords) != 2:
            raise ValueError("coords must have exactly 2 elements")
        # coords contains non-integer element
        for element in coords:
            if not isinstance(element, int):
                raise TypeError("all elements of coords must be ints")
        # path not a list
        if not isinstance(path, list):
            raise TypeError("path must be a list")
        # path contains non-string element
        for element in path:
            if not isinstance(element, str):
                raise TypeError("all elements of path must be strings")
        # path contains an element that is not 'u', 'd', 'l', or 'r'
        for element in path:
            if element not in ["u", "d", "l", "r"]:
                raise ValueError("all elements of path must be either 'u', 'd', 'l', or 'r'")

        self.coords = coords
        self.path = path
        self.maze = maze
        self.f = self.calculate_f()

    def calculate_f(self) -> int:
        """Calculate the f(s) value for this point.
        f(s) = g(s) + h(s)
        """
        # Calculate g
        g = len(self.path)

        # Calculate h using Manhattan distance
        winning_position = self.maze.winning_position
        distance_row = abs(winning_position[0] - self.coords[0])
        distance_col = abs(winning_position[1] - self.coords[1])
        h = distance_row + distance_col

        # Sum and return
        f = g + h
        return f


#
# HELPER FUNCTIONS
#
def get_directions(maze) -> list:
    """Given a Maze object, return a list of directions to perform in order to get from the bottom-left corner
    (marked 3) to the exit (marked 2).  Use the A* search algorithm.
    Each element of the list returned should be "u", "d", "l", or "r".
    Useful note: maze.grid is the numpy grid representation of the maze.  Also, maze has several functions that might
    be useful.  Feel free to use of its methods or attributes, except the ones that
    start with underscores.  Also, util.MinPriorityQueue is a useful class for enqueueing the nodes you discover.
    """
    # Get starting position and goal position
    starting_position = [19, 0]     # r, c
    goal_position = maze.winning_position

    # Set up a fringe, initially with just the starting point
    fringe = MinPriorityQueue()  # Contains PositionAndPath object
    initial_state = PositionAndPath(starting_position, [], maze)
    fringe.enqueue(initial_state, initial_state.f)

    # Keep track of visited states
    visited_coords = [[19, 0]]    # List of coordinate sublists, each of which is formatted [r, c]

    # Run A*
    while True:
        # Pop a position from the priority queue
        to_explore = fringe.dequeue()

        # Get list of neighbors that aren't in visited_coords
        moves = maze.get_legal_moves(to_explore.coords[0], to_explore.coords[1])
        can_visit = []  # List of sublists, where each sublist is a coordinate subsublist, followed by the direction to reach it
        for move in moves:
            result = maze.get_next_space(to_explore.coords[0], to_explore.coords[1], move)
            if result not in visited_coords:
                can_visit.append([result, move])

        # For each neighbor, check if it's the winning position.  If not, add to visited_coords and enqueue into fringe
        for neighbor in can_visit:
            neighbor_coords = neighbor[0]
            neighbor_direction = neighbor[1]
            if maze.is_winning_position(neighbor_coords[0], neighbor_coords[1]):
                return to_explore.path + [neighbor_direction]
            else:
                visited_coords.append(neighbor_coords)
                new_state = PositionAndPath(neighbor_coords, to_explore.path+[neighbor_direction], maze)
                fringe.enqueue(new_state, new_state.f)
