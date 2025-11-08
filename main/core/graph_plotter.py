import pygame
import math
from settings import WIDTH, HEIGHT
from core.ast import evaluateAST   
from settings import SIDEBAR_WIDTH, LINE_THICKNESS, GRAPH_SCALE

def drawLine(screen, colour, points, thickness=4):
    """
    Draw a thick anti-aliased line
    Required as pygame has either line thickness or anti-aliasing but not both
    """

    # Needs at least two points to draw a line
    if len(points) < 2:
        return

    # Prepare offsets for a thick line
    offsets = []
    half = thickness // 2
    for dx in range(-half, half + 1):
        for dy in range(-half, half + 1):
            offsets.append((dx, dy))

    # Draw line segments for each offset
    for dx, dy in offsets:
        offset_points = [(x + dx, y + dy) for x, y in points]

        # Draw the segment with anti-aliasing
        for i in range(1, len(offset_points)):
            pygame.draw.aaline(screen, colour, offset_points[i-1], offset_points[i])


class GraphPlotter:
    def __init__(self):
        self.functions = [] 
        self.dual_view = False

    def getBaseFunction(self):
        """
        Returns the first function added which is the base function
        """
        return self.functions[0]

    def plotFunction(self, function_object):
        """
        Clears old graph and plots only the new user function
        """
        self.functions = [function_object]

    def plotSubsequent(self, function_object):
        """
        Adds a new transformed function without clearning any previous
        """
        self.functions.append(function_object)

    def drawAll(self, screen, dual_view=False, top_function=None, bottom_function=None, use_degrees=False):
        """
        Draws either a single graph or a dual-view graph
        """
        if not dual_view:
            # Normal mode draw functions on a single graph
            for function in self.functions:
                self.drawFunction(screen, function)
        else:
            graph_height = HEIGHT // 2  # Each graph is half height

            # Top draws top function
            if top_function:
                self.drawFunction(
                    screen, top_function,
                    y_offset=0, 
                    graph_height=graph_height,
                    use_degrees=use_degrees
                )

            # Bottom draws bottom function
            if bottom_function:
                self.drawFunction(
                    screen, bottom_function,
                    y_offset=graph_height, 
                    graph_height=graph_height,
                    use_degrees=use_degrees
                )

    def drawFunction(self, screen, function_object, color_override=None, y_offset=0, graph_height=None, use_degrees=False):
        """
        Draws a given function
        Takes colour override, y offset and graph height if required
        """

        try:
            # If not altered default to full height
            if graph_height is None:
                graph_height = HEIGHT 

            # Get the tree, variable and colour from the function arguement
            function_tree = function_object.getFunction()
            if function_tree is None:
                return
            variable = function_object.getFunctionVar()
            # Override to gray if needed
            colour = color_override or function_object.getColour()

            # Define graph drawing area and scale        
            graph_left = SIDEBAR_WIDTH
            graph_width = WIDTH - SIDEBAR_WIDTH
            center_x = graph_left + graph_width // 2
            center_y = y_offset + graph_height // 2
            scale = GRAPH_SCALE

            prev_py = None
            segment = []

            min_y = y_offset
            # Removed 5 from the graph height to ensure the plotted function does not go over the dual graph boundaries
            max_y = y_offset + graph_height - 5

            # Iterate over pixels along the graphs length
            for px in range(graph_left, WIDTH):
                # For each x value,
                x_val = (px - center_x) / scale
                # The y value is the function evaluated at that x value
                y_val = evaluateAST(function_tree, x_val, variable, use_degrees=use_degrees)

                # Handles discontinuous functions
                if y_val is None or math.isnan(y_val) or math.isinf(y_val):
                    # Draws the current segment and resets
                    if len(segment) > 1:
                        drawLine(screen, colour, segment, thickness=LINE_THICKNESS)
                    segment = []
                    prev_py = None
                    continue

                # Map y values to screen pixels
                py = center_y - int(y_val * scale)

                # If in bounds or just one graph just draw the line
                if min_y <= py <= max_y or graph_height>500:
                    if prev_py is not None and abs(py - prev_py) > graph_height / 2:
                        if len(segment) > 1:
                            drawLine(screen, colour, segment, thickness=LINE_THICKNESS)
                        segment = []
                    segment.append((px, py))
                    prev_py = py

                # If out of bounds needs to clip to boundary (for asymptotes)
                else:
                    if py < min_y:
                        clipped_py = min_y
                    elif py > max_y - 10:
                        clipped_py = max_y

                    if len(segment) > 0:
                        # Extend to the boundary
                        segment.append((px, clipped_py))
                        drawLine(screen, colour, segment, thickness=LINE_THICKNESS)

                    # Reset segment for the next branch
                    segment = []
                    prev_py = None

            # Ensure there are no segments left undrawn
            if len(segment) > 1:
                drawLine(screen, colour, segment, thickness=LINE_THICKNESS)
        except:
            print ("An error occured in graphing")