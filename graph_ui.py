import pygame
import math
from settings import WIDTH, HEIGHT, SIDEBAR_WIDTH, GRAPH_FONT, GRAPH_AXIS_FONT, COLOUR_BACKGROUND, COLOUR_GRAPH_SEPARATOR, COLOUR_AXIS

def drawGraphArea(screen, derivative_order=1, dual_view=False, variable="x", font=[GRAPH_FONT, GRAPH_AXIS_FONT], scale=40, use_degrees=False, trig=False):
    """
    Draws the graph background and axes with numbering in degrees if needed
    Single or dual view
    """
    axis_color = COLOUR_AXIS
    grid_color = COLOUR_GRAPH_SEPARATOR

    def draw_axes(center_x, center_y, left, top, width, height, bottom_graph=False,
                  clip_bottom=None, scale=40, font=[GRAPH_FONT, GRAPH_AXIS_FONT], use_degrees=False, trig=False):
        """
        Draws X and Y axes
        """
        y_axis_bottom = top + height if clip_bottom is None else clip_bottom

        # Draw main X and Y axes
        pygame.draw.line(screen, axis_color, (center_x, top), (center_x, y_axis_bottom), 2)
        pygame.draw.line(screen, axis_color, (left, center_y), (left + width, center_y), 2)

        # Y-axis label with derivative notation
        if bottom_graph:
            # For the bottom graph show the derivative order
            y_label_text = f"f{'\'' * derivative_order}({variable})"
        else:
            # For the top graph show one order lower
            y_label_text = f"f{'\'' * (derivative_order - 1)}({variable})"

        x_label_surface = font[1].render(variable, True, axis_color)
        y_label_surface = font[1].render(y_label_text, True, axis_color)

        # Position axis labels
        x_label_rect = x_label_surface.get_rect(topleft=(left + width - x_label_surface.get_width() - 10, center_y))
        y_label_rect = y_label_surface.get_rect(topleft=(center_x + 8, top + 5))
        screen.blit(x_label_surface, x_label_rect.topleft)
        screen.blit(y_label_surface, y_label_rect.topleft)

        # Draw X-axis numbers
        if trig:
            # Draw the degrees axis
            # Converts from radians as the same is done on the graphing end, the actual graph is in radians
            step_radians = math.pi / 2
            num_steps = (width // scale) // 2
            for index in range(-num_steps, num_steps - 4):
                # Dont draw 0s to avoid axis overlap
                if index in [0, -num_steps, num_steps, num_steps]:
                    continue

                # Convert the index to a radian value then convert to a pixel position            
                rad_value = index * step_radians
                px = center_x + rad_value * scale

                # Dont draw the label if its pixel position is off the graph
                if px < left + 5 or px > left + width - 5:
                    continue

                if use_degrees:
                    # Degree labels
                    label  = f"{int(math.degrees(rad_value))}°"
                else:
                    # π fraction labels step π/2
                    numerator = index
                    denominator = 2

                    # Simplify if numerator divisible by denominator
                    if numerator % denominator == 0:
                        label = f"{numerator // denominator}π"
                    else:
                        if numerator == 1:
                            label = "π/2"
                        elif numerator == -1:
                            label = "-π/2"
                        else:
                            label = f"{numerator}π/2"

                    # Make negatives look better
                    if label == "1π":
                        label = "π"
                    elif label == "-1π":
                        label = "-π"
                # Then convert to degrees and render the label slightly below the axis
                text_surface = font[0].render(str(label), True, axis_color)
                text_rect = text_surface.get_rect(center=(px, center_y + 8 + text_surface.get_height()//2))
                screen.blit(text_surface, text_rect.topleft)

        else:
            # Draw X-axis numbers when no trig
            num_x_numbers = width // scale
            for index in range(-num_x_numbers//2, num_x_numbers//2 + 1):

                # Dont draw 0s or edge numbers to avoid overlap
                if index in [0, -num_x_numbers//2, num_x_numbers//2]:
                    continue

                # Convert the number index to pixel position and render
                px = center_x + index * scale
                text_surface = font[0].render(str(index), True, axis_color)
                text_rect = text_surface.get_rect(center=(px, center_y + 8 + text_surface.get_height()//2))
                if not text_rect.colliderect(x_label_rect):
                    screen.blit(text_surface, text_rect.topleft)

        # Draw Y-axis numbers 
        num_y_numbers = height // scale
        for index in range(-num_y_numbers//2, num_y_numbers//2 + 1):
            # Dont draw 0s to avoid overlap
            if index == 0:
                continue

            # Convert the number index to pixel position and render
            py = center_y - index * scale
            text_surface = font[0].render(str(index), True, axis_color)
            text_rect = text_surface.get_rect(center=(center_x + 8 + text_surface.get_width()//2, py))
            if not text_rect.colliderect(y_label_rect):
                screen.blit(text_surface, text_rect.topleft)


    # Single view
    if not dual_view:
        graph_rect = pygame.Rect(SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEIGHT)
        pygame.draw.rect(screen, COLOUR_BACKGROUND, graph_rect)
        center_x = SIDEBAR_WIDTH + (WIDTH - SIDEBAR_WIDTH)//2
        center_y = HEIGHT//2
        draw_axes(center_x, center_y, SIDEBAR_WIDTH, 0, WIDTH - SIDEBAR_WIDTH, HEIGHT, scale=scale, font=font, use_degrees=use_degrees, trig=trig)

    # Dual view 
    else:
        graph_left = SIDEBAR_WIDTH
        graph_width = WIDTH - SIDEBAR_WIDTH
        graph_height = HEIGHT // 2
        separator_gap = 4

        # Top graph
        top_center_x = graph_left + graph_width // 2
        top_center_y = graph_height // 2
        pygame.draw.rect(screen, COLOUR_BACKGROUND, (graph_left, 0, graph_width, graph_height))
        draw_axes(top_center_x, top_center_y, graph_left, 0, graph_width, graph_height,
                  clip_bottom=graph_height - separator_gap, scale=scale, font=font, use_degrees=False, trig=trig)

        # Bottom graph
        bottom_center_x = graph_left + graph_width // 2
        bottom_center_y = graph_height + graph_height // 2
        pygame.draw.rect(screen, COLOUR_BACKGROUND, (graph_left, graph_height, graph_width, graph_height))
        draw_axes(bottom_center_x, bottom_center_y, graph_left, graph_height + separator_gap,
                  graph_width, graph_height, bottom_graph=True, clip_bottom=HEIGHT, scale=scale, font=font, use_degrees=False, trig=trig )

        # Draw separator lines
        pygame.draw.line(screen, grid_color, (graph_left, graph_height - separator_gap), (WIDTH, graph_height - separator_gap), 1)
        pygame.draw.line(screen, grid_color, (graph_left, graph_height + separator_gap), (WIDTH, graph_height + separator_gap), 1)
