import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the window
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("RGB Ball Generation and Random Movement")

# Set up font
font = pygame.font.Font(None, 36)

# Define input box and initial settings
input_box = pygame.Rect(200, 300, 200, 50)  # Input box position and size
color = pygame.Color('black')  # Input box border color
user_text = ""  # Store user input
input_active = False  # Track if input box is active

# Store all generated balls and their information
balls = []

class Ball:
    """Class to store ball properties and movement logic"""
    def __init__(self, color):
        self.color = color
        self.radius = 20
        self.x = random.randint(self.radius, 600 - self.radius)
        self.y = random.randint(self.radius, 400 - self.radius)
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-2, 2])

    def move(self):
        """Move the ball and detect collisions with screen edges"""
        self.x += self.speed_x
        self.y += self.speed_y

        # Bounce when hitting the screen edges
        if self.x - self.radius < 0 or self.x + self.radius > 600:
            self.speed_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > 400:
            self.speed_y *= -1

    def draw(self, screen):
        """Draw the ball on screen"""
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

def render_text(text, x, y):
    """Render text on the screen"""
    txt_surface = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, (x, y))

def get_rgb_from_text(text):
    """Convert user input string to RGB color tuple"""
    try:
        r, g, b = map(int, text.split(","))
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            return (r, g, b)
    except ValueError:
        pass
    return None  # Return None if the input is invalid

def main():
    global user_text, input_active

    running = True
    clock = pygame.time.Clock()  # Control frame rate

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Activate input box if clicked
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

            elif event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    # Generate a new ball with the input color when Enter is pressed
                    new_color = get_rgb_from_text(user_text)
                    if new_color:
                        balls.append(Ball(new_color))
                    user_text = ""  # Clear the input box
                elif event.key == pygame.K_BACKSPACE:
                    # Delete the last character
                    user_text = user_text[:-1]
                else:
                    # Add the new character to the input box
                    user_text += event.unicode

        # Update all ball positions
        for ball in balls:
            ball.move()

        # Fill the background with white
        screen.fill((255, 255, 255))

        # Draw the input box
        pygame.draw.rect(screen, color, input_box, 2)
        render_text(user_text, input_box.x + 5, input_box.y + 10)

        # Draw all the balls
        for ball in balls:
            ball.draw(screen)

        # Update the display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(60)

if __name__ == "__main__":
    main()
