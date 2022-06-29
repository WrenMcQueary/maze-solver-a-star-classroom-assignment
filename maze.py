"""Definition of the maze itself"""


import numpy as np
import random


class Maze:
    """Fully defines a maze for the rover to explore."""

    def __init__(self):
        """self._walls is a list of Zone objects.
        self._goal is a Zone object.
        self.grid is the underlying numpy grid for the maze
        """
        (self._walls, self._goal, self.grid) = self._generate_walls_and_goal()
        self.winning_position = self._get_winning_position()

    def _generate_walls_and_goal(self):
        """Randomly generates _walls and the goal for this maze.
        Uses Prim's Algorithm: https://en.wikipedia.org/wiki/Prim%27s_algorithm
        """

        def _remove_duplicates_from_list(input_list):
            """Returns a version of input_list such that redundant elements are removed."""
            output_list = []
            for item in input_list:
                if item not in output_list:
                    output_list.append(item)
            return output_list

        def _get_all_1_neighbors_of_0s(input_array):
            """Returns a list of all indices for neighbors of 0s which are not themselves 0s.
            input_array is an ndarray containing 0s.
            """
            input_height = np.shape(input_array)[0]
            input_width = np.shape(input_array)[1]
            neighbor_indices = []
            for rr in range(input_height):
                for cc in range(input_width):
                    if input_array[rr, cc] == 0:
                        # Check all neighbors.  Add the indices of neighboring non-0s to neighbor_indices.
                        # Upper neighbor
                        if rr - 1 in range(input_height):
                            if input_array[rr - 1, cc] != 0:
                                neighbor_indices.append([rr - 1, cc])
                        # Lower neighbor
                        if rr + 1 in range(input_height):
                            if input_array[rr + 1, cc] != 0:
                                neighbor_indices.append([rr + 1, cc])
                        # Left neighbor
                        if cc - 1 in range(input_width):
                            if input_array[rr, cc - 1] != 0:
                                neighbor_indices.append([rr, cc - 1])
                        # Right neighbor
                        if cc + 1 in range(input_width):
                            if input_array[rr, cc + 1] != 0:
                                neighbor_indices.append([rr, cc + 1])
            neighbor_indices = _remove_duplicates_from_list(neighbor_indices)
            return neighbor_indices

        def _does_it_have_3_or_more_0_neighbors(query_index, array):
            """Returns True if the cell at query_index has 2 or more neighbors of 0 in any direction
            (not just crosswise).  Else returns False.
            query_index is a list of 2 integers.
            array is an ndarray
            """
            neighbor_counter = 0
            input_height = np.shape(array)[0]
            input_width = np.shape(array)[1]
            r = query_index[0]
            c = query_index[1]
            # Check upper
            if r - 1 in range(input_height):
                if array[r - 1, c] == 0:
                    neighbor_counter += 1
                # Check upper-left
                if c - 1 in range(input_width):
                    if array[r - 1, c - 1] == 0:
                        neighbor_counter += 1
                # Check upper-right
                if c + 1 in range(input_width):
                    if array[r - 1, c + 1] == 0:
                        neighbor_counter += 1
            # Check lower
            if r + 1 in range(input_height):
                if array[r + 1, c] == 0:
                    neighbor_counter += 1
                # Check lower-left
                if c - 1 in range(input_width):
                    if array[r + 1, c - 1] == 0:
                        neighbor_counter += 1
                # Check lower-right
                if c + 1 in range(input_width):
                    if array[r + 1, c + 1] == 0:
                        neighbor_counter += 1
            # Check left
            if c - 1 in range(input_width):
                if array[r, c - 1] == 0:
                    neighbor_counter += 1
            # Check right
            if c + 1 in range(input_width):
                if array[r, c + 1] == 0:
                    neighbor_counter += 1

            # Return based on neighbor_counter.
            if neighbor_counter >= 3:
                return True
            else:
                return False

        def _euclidean_dist(pos0, pos1):
            """Returns the distance between pos0 and pos1.
            pos0 is a list of 2 floats, representing a coordinate pair.
            pos1 is a list of 2 floats, representing a coordinate pair.
            Returns a float.
            """
            x0 = pos0[0]
            y0 = pos0[1]
            x1 = pos1[0]
            y1 = pos1[1]
            return ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5

        def _tkinter_coords_to_physics_coords(tkinter_coords):
            """Converts from the tkinter canvas coordinate system to the physics coordinate system.
            tkinter_coords is a list of 2 floats.
            """
            return [800 - tkinter_coords[0], tkinter_coords[1]]

        maze_length = 800   # pixels; the maze is assumed square.  maze_length must be divisible by cell_length.
        cell_length = 40    # pixels; each cell is assumed square.  cell_length must divide maze_length.
        prims_array_length = int(maze_length / cell_length)     # nodes in an array.

        # Create an nxn array, where n = prims_array_length.  Randomly weight each cell.
        weight_array = np.array([[random.random() for _ in range(prims_array_length)] for _ in range(prims_array_length)])

        # Create an nxn array of 0s (halls) and 1s (walls).  At first, have it all be walls.
        halls_and_walls_array = np.array([[1 for _ in range(prims_array_length)] for _ in range(prims_array_length)])   # Initially everything is a wall.
        # Mark the bottom-left spot as a hall.  This will be the starting point.
        halls_and_walls_array[prims_array_length - 1, 0] = 0

        # Generate the rest of the maze.
        are_walls_done = False
        while not are_walls_done:     # Each cycle of this loop creates exactly one new hall cell.
            neighbors = _get_all_1_neighbors_of_0s(halls_and_walls_array)    # Get the indices of all walls that are neighbors of a hall.
            # Of the wall cells neighboring a hall cell in halls_and_walls_array, make the one with lowest weight in weight_array a hall.  But if that wall is adjacent to 2 or more hall tiles, try the next-lowest-weight neighboring wall instead.  If you find no such walls, break; the maze is complete.
            while True:
                # Find the index with the lowest weight in neighbors.
                lowest_index = neighbors[0]
                lowest_weight = weight_array[lowest_index[0], lowest_index[1]]
                for index in neighbors:
                    this_weight = weight_array[index[0], index[1]]
                    if this_weight < lowest_weight:
                        lowest_weight = this_weight
                        lowest_index = index
                # If this wall is not adjacent to another hall, turn it into a wall and break, because it's time to make a new hall cell!
                if not _does_it_have_3_or_more_0_neighbors(lowest_index, halls_and_walls_array):
                    halls_and_walls_array[lowest_index[0], lowest_index[1]] = 0
                    break
                else:   # Else remove this wall from neighbors and try again, unless neighbors is empty, in which case the maze is complete!
                    neighbors.remove(lowest_index)
                    if len(neighbors) == 0:
                        are_walls_done = True
                        break

        # Put a goal marker at a point of the maze farthest from the bottom-left spot!
        # Find a hall spot with the greatest distance from the bottom-left tile.
        greatest_index = [prims_array_length - 1, 0]
        greatest_distance = 0
        for rr in range(prims_array_length):
            for cc in range(prims_array_length):
                if halls_and_walls_array[rr, cc] == 0:
                    this_distance = _euclidean_dist([prims_array_length - 1, 0], [rr, cc])
                    if this_distance > greatest_distance:
                        greatest_index = [rr, cc]
                        greatest_distance = this_distance
        # Change the 0 of that hall to a 2, to represent a goal.
        halls_and_walls_array[greatest_index[0], greatest_index[1]] = 2

        # Change the bottom-left corner to a start (3)
        halls_and_walls_array[-1, 0] = 3

        # Use halls_and_walls_array to generate a list of Wall objects which use pixel coordinates.
        output_walls = []
        output_goal = None
        for rr in range(prims_array_length):
            for cc in range(prims_array_length):
                if halls_and_walls_array[rr, cc] == 1:
                    output_walls.append(Zone(ctl=_tkinter_coords_to_physics_coords([(rr+1)*cell_length - 1, (cc+1)*cell_length - 1]), cbr=_tkinter_coords_to_physics_coords([rr*cell_length, cc*cell_length])))
                elif halls_and_walls_array[rr, cc] == 2:
                    output_goal = Zone(ctl=_tkinter_coords_to_physics_coords([(rr+1)*cell_length - 1, (cc+1)*cell_length - 1]), cbr=_tkinter_coords_to_physics_coords([rr*cell_length, cc*cell_length]))

        # Return!
        return output_walls, output_goal, halls_and_walls_array

    def get_legal_moves(self, r: int, c: int) -> list:
        """Given row and column coordinates to a position on self.grid, return a list of legal moves 'u', 'd', 'l', or
        'r' that can be made from that position.
        """
        # Handle errors
        # r not int
        if not isinstance(r, int):
            raise TypeError("r must be an int")
        # c not int
        if not isinstance(c, int):
            raise TypeError("c must be an int")
        # r out of bounds
        if not (0 <= r < np.shape(self.grid)[0]):
            raise IndexError("r is out of bounds")
        # c out of bounds
        if not (0 <= c < np.shape(self.grid)[0]):
            raise IndexError("c is out of bounds")
        # r, c points to a wall
        if self.grid[r, c] == 1:
            raise ValueError("coordinate pair (r, c) points to a wall. No moves possible")

        output_moves = []

        # Check for 'u'
        if 0 <= r-1 < np.shape(self.grid)[0]:   # If in bounds:
            if np.grid[r-1, c] != 1:    # If not a wall:
                output_moves.append("u")
        # Check for 'd'
        if 0 <= r+1 < np.shape(self.grid)[0]:   # If in bounds:
            if np.grid[r+1, c] != 1:    # If not a wall:
                output_moves.append("d")
        # Check for 'l'
        if 0 <= c-1 < np.shape(self.grid)[0]:   # If in bounds:
            if np.grid[r, c-1] != 1:    # If not a wall:
                output_moves.append("l")
        # Check for 'r'
        if 0 <= c+1 < np.shape(self.grid)[0]:   # If in bounds:
            if np.grid[r, c+1] != 1:    # If not a wall:
                output_moves.append("r")

        return output_moves

    def get_next_space(self, r: int, c: int, direction: str) -> tuple:
        """Given direction 'u', 'd', 'l', or 'r', return the coordinates of the next space.
        If the move is illegal, raise an error instead.
        """
        # Handle errors
        # r not int
        if not isinstance(r, int):
            raise TypeError("r must be an int")
        # c not int
        if not isinstance(c, int):
            raise TypeError("c must be an int")
        # r out of bounds
        if not (0 <= r < np.shape(self.grid)[0]):
            raise IndexError("r is out of bounds")
        # c out of bounds
        if not (0 <= c < np.shape(self.grid)[0]):
            raise IndexError("c is out of bounds")
        # r, c points to a wall
        if self.grid[r, c] == 1:
            raise ValueError("coordinate pair (r, c) points to a wall. No moves possible")
        # direction not a string
        if not isinstance(direction, str):
            raise TypeError("direction must be a string")
        # direction not a valid character
        if direction not in ["u", "d", "l", "r"]:
            raise ValueError("direction must be 'u', 'd', 'l', or 'r'")
        # direction not a valid move from r, c
        if direction not in self.get_legal_moves(r, c):
            raise ValueError("direction not a legal move from (r, c)")

        if direction == "u":
            return r-1, c
        elif direction == "d":
            return r+1, c
        elif direction == "l":
            return r, c-1
        else:   # direction must equal "r"
            return r, c+1

    def is_winning_position(self, r: int, c: int) -> bool:
        """Given row and column coordinates to a position on self.grid, return whether it's a winning position.
        """
        # Handle errors
        # r not int
        if not isinstance(r, int):
            raise TypeError("r must be an int")
        # c not int
        if not isinstance(c, int):
            raise TypeError("c must be an int")
        # r out of bounds
        if not (0 <= r < np.shape(self.grid)[0]):
            raise IndexError("r is out of bounds")
        # c out of bounds
        if not (0 <= c < np.shape(self.grid)[0]):
            raise IndexError("c is out of bounds")

        return self.grid[r, c] == 2

    def _get_winning_position(self) -> tuple:
        """Return the numpy coordinates of the winning position in the maze."""
        for rr in range(np.shape(self.grid)[0]):
            for cc in range(np.shape(self.grid)[1]):
                if self.grid[rr, cc] == 2:
                    return rr, cc


class Zone:
    """Coordinates defining a zone (ie wall or goal) in a maze.  These use physics coordinates."""

    def __init__(self, ctl, cbr):
        """ctl is short for "corner top left", and is a list of 2 floats, in pixel coordinates.
        cbr is short for "corner bottom right", and is a list of 2 floats, in pixel coordinates.
        """
        self.ctl = ctl
        self.cbr = cbr
