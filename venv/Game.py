import pygame
import random
import sys
from pygame.locals import *

pygame.init()

# Constants for screen width and height
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class button():
    def __init__(self, color, x, y, width, height, text = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.text, True, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


def main():
    # Make screen
    screen.fill((255, 255, 255))

    # Set a caption
    pygame.display.set_caption("Clicker")

    while True:
        run_game()


def run_game():

    # Test button
    green_button = button((0, 255, 0), 150, 225, 250, 100, "Click me!")

    # Variable for game loop
    running = True

    # clock to tick
    clock = pygame.time.Clock()

    while running:

        # Mouse position
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    terminate()
            elif event.type == QUIT:
                running == False
                terminate()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if green_button.is_over(mouse_pos):
                    print("Button clicked")

            if event.type == MOUSEMOTION:
                if green_button.is_over(mouse_pos):
                    green_button.color = (255, 0, 0)
                else:
                    green_button.color = (0, 255, 0)

        green_button.draw(screen, (0, 0, 0))

        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
