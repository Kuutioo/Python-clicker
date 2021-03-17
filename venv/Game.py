import pygame
import random
import sys
from pygame.locals import *

pygame.init()

# Constants for screen width and height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Items
items = {
    "Debug item" : [0, 0]
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class button():
    def __init__(self, color, x, y, width, height, item_price_x, item_price_y, text = "", item_price = "", ):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.item_price = item_price
        self.item_price_x = item_price_x
        self.item_price_y = item_price_y

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            font = pygame.font.SysFont(None, 60)
            text = font.render(self.text, True, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

        if self.item_price != "":
            price_font = pygame.font.SysFont("calibri", 30)
            price_text = price_font.render(self.item_price, True, (0, 0, 0))
            screen.blit(price_text, (self.item_price_x, self.item_price_y))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class inventory():
    def __init__(self, color, box_x, box_y, box_width, box_height, item_name_x, item_name_y, item_price_x, item_price_y, inventory_text = "", item_name = "", item_price = ""):
        self.color = color
        self.box_x = box_x
        self.box_y = box_y
        self.box_width = box_width
        self.box_height = box_height
        self.item_name_x = item_name_x
        self.item_name_y = item_name_y
        self.item_price_x = item_price_x
        self.item_price_y = item_price_y
        self.inventory_text = inventory_text
        self.item_name = item_name
        self.item_price = item_price

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.box_x - 2, self.box_y - 2, self.box_width + 4, self.box_height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.box_x, self.box_y, self.box_width, self.box_height), 0)

    def draw_inventory_text(self, screen, _itemname = "", _itemprice = ""):
        if self.item_name != "":
            item_name_font = pygame.font.SysFont(None, 25)
            item_name_text = item_name_font.render(_itemname, True, (WHITE))
            screen.blit(item_name_text, (self.item_name_x, self.item_name_y))

        if self.item_price != "":
            item_price_font = pygame.font.SysFont(None, 25)
            item_price_text = item_price_font.render(_itemprice, True, (WHITE))
            screen.blit(item_price_text, (self.item_price_x, self.item_price_y))



def main():
    # Make screen
    screen.fill((BLACK))

    # Set a caption
    pygame.display.set_caption("Clicker")

    while True:
        run_game()


def run_game():
    amount = items["Debug item"][0]
    price = items["Debug item"][1]

    # Test button
    green_button = button((0, 255, 0), 2, 2, 250, 100, 500, 110)

    # Inventory
    item_inventory = inventory((0, 0, 0), 1000, 2, 278, 716, 1000, 4, 1150, 4, "Inventory", f'Debug Item: {amount}', f'Price: {price}')

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
                    screen.fill((BLACK))
                    item_inventory.draw_inventory_text(screen, f'Debug item: {amount}', f'Price: {price}')
                    # green_button = button((0, 255, 0), 2, 2, 250, 100, 35, 110, f'Clicks: {amount}', f'Price: {price}')

        green_button.draw(screen, (0, 0, 0))
        item_inventory.draw(screen,(0, 255, 255))

        if amount >= 1:
            item_inventory.draw_inventory_text(screen, f'Debug item: {amount}', f'Price: {price}')

        pygame.display.update()

def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
