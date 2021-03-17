import pygame
import random
import sys
from pygame.locals import *

pygame.init()

# Constants for screen width and height
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Items
items = {
    "Debug item" : [0, 0]
}



class button():
    def __init__(self, color, x, y, width, height, text = "", item_price = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.item_price = item_price

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.text, True, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.item_price != "":
            price_font = pygame.font.SysFont(None, 60)
            price_text = price_font.render(self.item_price, True, (0, 0, 0))
            screen.blit(price_text, (self.x + (self.width / 4 - price_text.get_width() / 4), self.y + (self.height / 4 - price_text.get_height() / 4)))

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
    amount = items["Debug item"][0]
    price = items["Debug item"][1]

    # Test button
    green_button = button((0, 255, 0), 150, 225, 250, 100, f'Clicks: {amount}', f'Price: {price}')

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
                    amount += 1
                    price += 10
                    print(amount)
                    green_button = button((0, 255, 0), 150, 225, 250, 100, f'Clicks: {amount}' , f'Price: {price}')

        green_button.draw(screen, (0, 0, 0))

        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
