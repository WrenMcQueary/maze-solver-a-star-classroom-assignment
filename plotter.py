"""Visualization of the directions given by the student, to see if they make a sensible path through the maze"""


from maze import Maze
import tkinter
import numpy as np
import ctypes
windows_scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100


def plot_directions(maze, directions: list) -> None:
    """Show the user's directions on a plot of the maze."""
    # Handle errors
    # maze not a Maze object
    if not isinstance(maze, Maze):
        raise TypeError("maze must be a Maze object")
    # directions not a list
    if not isinstance(directions, list):
        raise TypeError("directions must be a list")
    # directions contains non-string element
    for element in directions:
        if not isinstance(element, str):
            raise TypeError("directions contains non-string element")
    # directions contains an element that is not u/d/l/r
    for element in directions:
        if element not in ["u", "d", "l", "r"]:
            raise ValueError("directions contains an element that is not 'u', 'd', 'l', or 'r'")

    window = tkinter.Tk()
    window.title("Directions through maze")
    window.geometry(f"{int(800/windows_scale_factor)}x{int(830/windows_scale_factor)}")
    window["background"] = "#2B2B2B"
    canvas = tkinter.Canvas(window, width=int(800/windows_scale_factor), height=int(800/windows_scale_factor), background="#CCCCCC")    # #A33DB8 is also nice
    canvas.grid(row=0, column=0)
    window.after(500, lambda: draw(maze, directions, canvas))
    window.mainloop()


def draw(maze, directions: list, canvas) -> None:
    """Draw to the canvas.  This function is called by plot_directions()"""
    def physics_coords_to_tkinter_coords(physics_coords):
        """Converts from the physics coordinate system to the tkinter canvas coordinate system.
        physics_coords is a list of 2 floats.
        """
        return [int(physics_coords[1]/windows_scale_factor), int((800 - physics_coords[0])/windows_scale_factor)]

    def numpy_coords_to_tkinter_coords(numpy_coords: list) -> list:
        """Converts from numpy cell coordinates to the tkinter canvas coordinate system, pointing at the center of a
        cell"""
        r, c = numpy_coords[0], numpy_coords[1]
        return [int((40*c + 20)/windows_scale_factor), int((40*r + 20)/windows_scale_factor)]

    # Handle errors
    # maze not a Maze object
    if not isinstance(maze, Maze):
        raise TypeError("maze must be a Maze object")
    # directions not a list
    if not isinstance(directions, list):
        raise TypeError("directions must be a list")
    # directions contains non-string element
    for element in directions:
        if not isinstance(element, str):
            raise TypeError("directions contains non-string element")
    # directions contains an element that is not u/d/l/r
    for element in directions:
        if element not in ["u", "d", "l", "r"]:
            raise ValueError("directions contains an element that is not 'u', 'd', 'l', or 'r'")
    # canvas not a Canvas object
    if not isinstance(canvas, tkinter.Canvas):
        raise TypeError("canvas must be a tkinter.Canvas object")

    wall_color = "#2B2B2B"

    # Wipe old contents of canvas.
    canvas.delete("all")

    # Draw the walls of the maze to the canvas.
    for wall in maze._walls:
        this_ctl_in_tk_coords = physics_coords_to_tkinter_coords(wall.ctl)
        this_cbr_in_tk_coords = physics_coords_to_tkinter_coords(wall.cbr)
        canvas.create_rectangle(this_ctl_in_tk_coords[0], this_ctl_in_tk_coords[1], this_cbr_in_tk_coords[0],
                                     this_cbr_in_tk_coords[1], outline=wall_color, fill=wall_color)

    # Draw the goal of the maze to the canvas.
    goal_ctl_in_tk_coords = physics_coords_to_tkinter_coords(maze._goal.ctl)
    goal_cbr_in_tk_coords = physics_coords_to_tkinter_coords(maze._goal.cbr)
    canvas.create_rectangle(goal_ctl_in_tk_coords[0], goal_ctl_in_tk_coords[1], goal_cbr_in_tk_coords[0],
                                 goal_cbr_in_tk_coords[1], fill="green")

    # Draw a dot at starting position
    current_cell_coords = [np.shape(maze.grid)[0] - 1, 0]  # numpy coordinates
    dot_center = numpy_coords_to_tkinter_coords(current_cell_coords)
    dot_radius = 8/windows_scale_factor  # pixels
    canvas.create_oval(dot_center[0] - dot_radius, dot_center[1] - dot_radius, dot_center[0] + dot_radius, dot_center[1] + dot_radius, fill="cyan")

    # Draw the user's path
    for step in directions:
        # Draw a dot at new position
        dot_center = numpy_coords_to_tkinter_coords(current_cell_coords)
        dot_radius = 8/windows_scale_factor  # pixels
        canvas.create_oval(dot_center[0] - dot_radius, dot_center[1] - dot_radius, dot_center[0] + dot_radius, dot_center[1] + dot_radius, fill="cyan")
        # Draw a line to next position
        if step == "u":
            new_cell_coords = [current_cell_coords[0]-1, current_cell_coords[1]]
        elif step == "d":
            new_cell_coords = [current_cell_coords[0]+1, current_cell_coords[1]]
        elif step == "l":
            new_cell_coords = [current_cell_coords[0], current_cell_coords[1]-1]
        else:   # step == "r"
            new_cell_coords = [current_cell_coords[0], current_cell_coords[1]+1]
        line_start = dot_center.copy()
        line_end = numpy_coords_to_tkinter_coords(new_cell_coords)
        canvas.create_line(line_start[0], line_start[1], line_end[0], line_end[1], fill="cyan")
        # Draw a dot at new position
        dot_center = numpy_coords_to_tkinter_coords(new_cell_coords)
        dot_radius = 8/windows_scale_factor  # pixels
        canvas.create_oval(dot_center[0] - dot_radius, dot_center[1] - dot_radius, dot_center[0] + dot_radius, dot_center[1] + dot_radius, fill="cyan")
        # Update current_cell_coords
        current_cell_coords = new_cell_coords.copy()

    # Update the canvas.
    canvas.update()
