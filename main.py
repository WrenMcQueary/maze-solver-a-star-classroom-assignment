"""Run this file to check your answer."""


from maze import Maze
from pathfinder import get_directions
from plotter import plot_directions


#
# MAIN SCRIPT
#
# Create a maze
problem = Maze()

# Give student maze and request response
direction_list = get_directions(problem)

# Plot maze with the user's directions
plot_directions(problem, direction_list)
