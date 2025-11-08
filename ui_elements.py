import pygame
from settings import UI_FONT, UI_FONT_SMALL, COLOUR_BUTTON, COLOUR_BOX, COLOUR_TEXT, SUPERSCRIPT_MAP, IGNORE_KEYS, COLOUR_SIDEBAR


class InputBox:
    def __init__(self, x, y, w, h, font=UI_FONT, text='', center_text=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.border_colour = COLOUR_BOX
        self.text_colour = COLOUR_TEXT
        self.border_width = 2
        self.text = text  
        self.display_text = text  
        self.font = font
        self.center_text = center_text
        self.txt_surface = self.font.render(self.display_text, True, self.text_colour)
        self.active = False
        self.superscript_mode = False
        self.allow_get = True
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_interval = 250  
        self.cursor_width = 1

    def handleEvent(self, event):
        """
        Handles interaction in the form of pygame events
        """
        # Check for a mouse click to activate or deactivate the box
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.border_width = 3 if self.active else 2
            self.cursor_visible = True
            self.cursor_timer = 0

        # Handling keyboard inputs
        elif event.type == pygame.KEYDOWN and self.active:
            # Disable superscript if navigation key entered
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_HOME, pygame.K_END]:
                self.superscript_mode = False

            # Event of backspace pressed
            elif event.key == pygame.K_BACKSPACE:
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_CTRL:
                    # Delete all text if CTRL pressed also
                    self.text = ""
                    self.display_text = ""
                    self.superscript_mode = False
                else:
                    if not self.text:
                        return
                    # Remove last character from text
                    removed_char = self.text[-1]
                    self.text = self.text[:-1]

                    # Remove last character from display_text
                    if removed_char == "^":
                        # Removed ^ does not appear in display_text
                        self.superscript_mode = False
                    elif self.superscript_mode:
                        self.display_text = self.display_text[:-1]
                    else:
                        self.display_text = self.display_text[:-1]

            # If the key is one that should be added to the input field
            elif event.key not in IGNORE_KEYS:
                char = event.unicode

                if char == "^":
                    # Add ^ to the text if valid but not display text
                    if self.text and (self.text[-1].isalnum() or self.text[-1] == ")"):
                        self.text += char
                        self.superscript_mode = True
                else:
                    # Adds other characters to display_text and text
                    self.text += char
                    if self.superscript_mode:
                        self.display_text += SUPERSCRIPT_MAP.get(char, char)
                    else:
                        self.display_text += char

            # Update the rendered surface
            self.txt_surface = self.font.render(self.display_text, True, self.text_colour)

            # Reset cursor blink after typing
            self.cursor_visible = True
            self.cursor_timer = 0

    def update(self, change_in_time):
        """
        Updates cursor blink timer
        """
        if self.active:
            self.cursor_timer += change_in_time
            if self.cursor_timer >= self.cursor_interval:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = False

    def draw(self, screen):
        """
        Draws the input box, text and border on screen
        """
        full_surface = self.font.render(self.display_text, True, self.text_colour)

        # Clip text if wider than the box
        if full_surface.get_width() > self.rect.width - 10:
            clip_rectangle = pygame.Rect(
                full_surface.get_width() - (self.rect.width - 10),
                0,
                self.rect.width - 10,
                full_surface.get_height()
            )
            visible_surface = full_surface.subsurface(clip_rectangle)
        else:
            visible_surface = full_surface

        # Draw centered or left
        if self.center_text:
            text_rect = visible_surface.get_rect(center=self.rect.center)
            screen.blit(visible_surface, text_rect.topleft)
            cursor_x = text_rect.right
            cursor_y = text_rect.y
        else:
            text_pos = (self.rect.x + 5, self.rect.y + 5)
            screen.blit(visible_surface, text_pos)
            cursor_x = text_pos[0] + visible_surface.get_width()
            cursor_y = text_pos[1]

        # Draw border
        pygame.draw.rect(screen, self.border_colour, self.rect, self.border_width)

        # Draw cursor if active
        if self.active and self.cursor_visible:
            if self.superscript_mode:
                # Smaller superscript cursor
                cursor_height = self.font.get_height() // 2 
                cursor_rect = pygame.Rect(cursor_x + 2, cursor_y, self.cursor_width, cursor_height)
            else:
                cursor_rect = pygame.Rect(cursor_x + 2, cursor_y, self.cursor_width, self.font.get_height())
            pygame.draw.rect(screen, self.text_colour, cursor_rect)

    def getText(self):
        """
        Returns the current text in the input box
        """
        return self.text

    def setError(self, error=True):
        """
        Turns the border red if error, otherwise resets it
        """
        if error:
            self.border_colour = (255, 0, 0)  
        else:
            self.border_colour = COLOUR_BOX


class Checkbox:
    def __init__(self, x, y, w, h, label="", tick_img=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.checked = False
        self.tick_img = tick_img

    def draw(self, screen):
        """
        Draws the checkbox and tick if checked
        """
        pygame.draw.rect(screen, COLOUR_BOX, self.rect, 2)
        if self.checked and self.tick_img:
            tick_pos = (self.rect.centerx - self.tick_img.get_width() // 2, self.rect.centery - self.tick_img.get_height() // 2)
            screen.blit(self.tick_img, tick_pos)

    def handleEvent(self, event):
        """
        Toggles the checkbox if mouse clicked within the box
        """
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.checked = not self.checked

    def getValue(self):
        """
        Returns whether the checkbox is checked
        """
        return self.checked

class Button:
    def __init__(self, x, y, w, h, text="", small=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.scale = 1.0
        self.hover_scale = 1.05  
        self.small = small

    def update(self, mouse_pos):
        """
        Changes the button scale if mouse is hovering
        """
        if self.rect.collidepoint(mouse_pos):
            self.scale = self.hover_scale
        else:
            self.scale = 1.0

    def draw(self, screen):
        """
        Draws the button rectangle and text
        """
        scaled_rect = self.rect.copy()
        scaled_rect.width = int(self.rect.width * self.scale)
        scaled_rect.height = int(self.rect.height * self.scale)
        scaled_rect.center = self.rect.center  

        pygame.draw.rect(screen, COLOUR_BUTTON, scaled_rect)
        if self.small:
            txt_surf = UI_FONT_SMALL.render(self.text, True, (0, 0, 0))
        else:
            txt_surf = UI_FONT.render(self.text, True, (0, 0, 0))
        text_rect = txt_surf.get_rect(center=scaled_rect.center)
        screen.blit(txt_surf, text_rect.topleft)

    def isClicked(self, event):
        """
        Returns whether the button was clicked
        """
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class Text:
    def __init__(self, x, y, text, colour=(0, 0, 0), font=UI_FONT):
        self.x = x
        self.y = y
        self.text = text
        self.colour = colour
        self.font = font

    def draw(self, screen):
        """
        Renders the text on the screen
        """
        txt_surface = self.font.render(self.text, True, self.colour)
        screen.blit(txt_surface, (self.x, self.y))

    def setText(self, new_text):
        """
        Updates the text to be rendered
        """
        self.text = new_text

class PlayPauseButton(Button):
    def __init__(self, x, y, w, h):
        # Call parent constructor 
        super().__init__(x, y, w, h, text="")
        self.toggled = True

    def draw(self, screen):
        """
        Override draw to use play/pause symbol instead of text
        """
        scaled_rect = self.rect.copy()
        scaled_rect.width = 70
        scaled_rect.height = 30
        scaled_rect.center = self.rect.center

        pygame.draw.rect(screen, COLOUR_SIDEBAR, scaled_rect)

        # Play or pause icon, using default font to render properly
        symbol = "PLAY" if not self.toggled else "PAUSE"
        txt_surf = UI_FONT.render(symbol, True, (0, 0, 0))
        text_rect = txt_surf.get_rect(center=scaled_rect.center)
        screen.blit(txt_surf, text_rect)

    def handle_event(self, event):
        """
        Toggles play/pause
        """
        if self.isClicked(event):  
            self.toggled = not self.toggled
            return True
        return False

    def setState(self, playing):
        """
        Force state
        """
        self.toggled = playing
