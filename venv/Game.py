import pygame
import random
import sys
from pygame.locals import *

pygame.init()

FPS = 30

# Constants for screen width and height
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Constants for basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Items
items = {
    "Debug item" : [0, 0],
    "Wood" : [0, 0],
    "Stone" : [0, 0],
    "Iron" : [0, 0]
}


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


class inventory():
    def __init__(self, color, box_x, box_y, box_width, box_height, inventory_text = ""):
        self.color = color
        self.box_x = box_x
        self.box_y = box_y
        self.box_width = box_width
        self.box_height = box_height
        self.inventory_text = inventory_text

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.box_x - 2, self.box_y - 2, self.box_width + 4, self.box_height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.box_x, self.box_y, self.box_width, self.box_height), 0)


class draw_item_display():
    def __init__(self, color, x, y, width, height, item_name_x, item_name_y, item_price_x, item_price_y, item_name = "", item_price = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item_name_x = item_name_x
        self.item_name_y = item_name_y
        self.item_price_x = item_price_x
        self.item_price_y = item_price_y
        self.item_name = item_name
        self.item_price = item_price

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height),0)

    def draw_item_display_text(self, screen, _itemname = "", _itemprice = ""):
        if self.item_name != "":
            item_name_font = pygame.font.SysFont(None, 50)
            item_name_text = item_name_font.render(_itemname, True, (WHITE))
            screen.blit(item_name_text, (self.item_name_x, self.item_name_y))

        if self.item_price != "":
            item_price_font = pygame.font.SysFont(None, 25)
            item_price_text = item_price_font.render(_itemprice, True, (WHITE))
            screen.blit(item_price_text, (self.item_price_x, self.item_price_y))



class inventory_button():
    def __init__(self, color, x, y, width, height, item_name_x, item_name_y, item_price_x, item_price_y, item_name = "", item_price = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item_name_x = item_name_x
        self.item_name_y = item_name_y
        self.item_price_x = item_price_x
        self.item_price_y = item_price_y
        self.item_name = item_name
        self.item_price = item_price

    def draw(self, screen, outline = None):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

    def draw_inventory_text(self, screen, _itemname = "", _itemprice = ""):
        item_name_font = pygame.font.SysFont(None, 25)
        item_name_text = item_name_font.render(_itemname, True, (WHITE))
        screen.blit(item_name_text, (self.item_name_x, self.item_name_y))

        item_price_font = pygame.font.SysFont(None, 25)
        item_price_text = item_price_font.render(_itemprice, True, (WHITE))
        screen.blit(item_price_text, (self.item_price_x, self.item_price_y))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


def main():
    # Make screen
    screen.fill((BLACK))

    # Set a caption
    pygame.display.set_caption("Quest Master")

    while True:
        run_game()


def draw_texts_to_item_display(item_name = "", item_price = ""):
    # Button
    global test_sell_button

    # Inventory
    global item_inventory
    global item_inventory_display

    # Draw stuff
    item_inventory_display.draw(screen, (CYAN))
    item_inventory_display.draw_item_display_text(screen, item_name, item_price)
    test_sell_button.draw(screen, (CYAN))


# Declare stuff here for global variables
# Items and amounts
debug_item_amount = items["Debug item"][0]
debug_item_price = items["Debug item"][1]
wood_item_amount = items["Wood"][0]
wood_item_price = items["Wood"][1]

# Inventory
item_inventory = inventory((BLACK), 1000, 2, 278, 400, "Inventory")
item_inventory_display = draw_item_display((BLACK), 1000, 400, 278, 315, 1005, 415, 1005, 475, ".", ".")

# Test buttons
test_quest_button = button((GREEN), 2, 2, 250, 100)
test_sell_button = button((RED), 1014, 600, 250, 100, "SELL")

# Inventory buttons
debug_item_button = inventory_button((BLACK), 1000, 2, 278, 20, 1000, 4, 1150, 4, f'Debug Item: {debug_item_amount}', f'Price: {debug_item_price}')
wood_item_button = inventory_button((BLACK), 1000, 22, 278, 20, 1000, 24, 1150, 24, f'Wood Item: {wood_item_amount}', f'Price: {wood_item_price}')


def run_game():
    # Items and amounts
    global debug_item_amount
    global debug_item_price
    global wood_item_amount
    global wood_item_price

    # Test buttons
    global test_quest_button

    # Inventory buttons
    global debug_item_button
    global wood_item_button

    # Variable for game loop
    running = True

    # Boolean to items to sell
    sell_debug_item = False
    sell_wood = False

    # clock to tick
    clock = pygame.time.Clock()

    while running:
        # Mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check for events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    terminate()
            elif event.type == QUIT:
                running == False
                terminate()

            # If mousebutton down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if test_quest_button.is_over(mouse_pos):
                    debug_item_amount += random.randint(1, 6)
                    debug_item_price += debug_item_amount * 10

                    wood_item_amount += random.randint(1, 3)
                    wood_item_price += wood_item_amount * 4

                    screen.fill((BLACK))
                elif test_sell_button.is_over(mouse_pos):
                    if sell_debug_item == True:
                        debug_item_amount -= debug_item_amount
                        debug_item_price -= debug_item_price
                        sell_debug_item = False
                    elif sell_wood == True:
                        wood_item_amount -= wood_item_amount
                        wood_item_price -= wood_item_price
                        sell_wood = False

                    screen.fill((BLACK))
                elif debug_item_button.is_over(mouse_pos) and debug_item_amount >= 1:
                    draw_texts_to_item_display("Debug item", f'Price: {debug_item_price}')
                    sell_debug_item = True
                elif wood_item_button.is_over(mouse_pos) and wood_item_amount >= 1:
                    draw_texts_to_item_display("Wood", f'Price: {wood_item_price}')
                    sell_wood = True


        test_quest_button.draw(screen, (CYAN))

        item_inventory.draw(screen,(CYAN))

        debug_item_button.draw(screen, (BLACK))
        wood_item_button.draw(screen, (BLACK))

        if debug_item_amount >= 1:
            debug_item_button.draw_inventory_text(screen, f'Debug Item: {debug_item_amount}', f'Price: {debug_item_price}')
        if wood_item_amount >= 1:
            wood_item_button.draw_inventory_text(screen, f'Wood: {wood_item_amount}', f'Price: {wood_item_price}')

        pygame.display.update()

        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
