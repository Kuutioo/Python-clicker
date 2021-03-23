import pygame
import random
import sys
import time
from pygame.locals import *

# Initialize game
pygame.init()

# FPS
FPS = 60

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


class Button():
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
            font = pygame.font.SysFont(None, 40)
            text = font.render(self.text, True, (WHITE))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class Inventory():
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


class DrawItemDisplay():
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



class InventoryButton():
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


class Gold():
    def __init__(self, color, x, y, width, height, gold_x, gold_y, gold_amount = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gold_x = gold_x
        self.gold_y = gold_y
        self.gold_amount = gold_amount

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height),0)

    def draw_text(self, screen, _gold_amount = ""):
        font = pygame.font.SysFont(None, 50)
        text = font.render(_gold_amount, True, (WHITE))
        screen.blit(text, (self.gold_x, self.gold_y))


class QuestTimerBox():
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height),0)


def main():
    # Fill screen
    screen.fill((BLACK))

    item_inventory_display.draw(screen, (CYAN))

    # Set a caption
    pygame.display.set_caption("Quest Master")

    while True:
        run_game()


def draw_texts_to_item_display(item_name = "", item_price = ""):
    # Button
    global sell_button

    # Inventory
    global item_inventory
    global item_inventory_display

    # Draw stuff
    item_inventory_display.draw(screen, (CYAN))
    item_inventory_display.draw_item_display_text(screen, item_name, item_price)
    sell_button.draw(screen, (CYAN))


# Declare stuff here for global variables
# Items and amounts
debug_item_amount = items["Debug item"][0]
debug_item_price = items["Debug item"][1]
wood_item_amount = items["Wood"][0]
wood_item_price = items["Wood"][1]
stone_item_amount = items["Stone"][0]
stone_item_price = items["Stone"][1]
iron_item_amount = items["Iron"][0]
iron_item_price = items["Iron"][1]


# Gold
gold_amount = 0
gold_display = Gold((BLACK), 748, 600, 250, 115, 752, 637, "")

# Inventory
item_inventory = Inventory((BLACK), 1000, 2, 278, 490, "Inventory")
item_inventory_display = DrawItemDisplay((BLACK), 1000, 495, 278, 220, 1005, 505, 1005, 565, ".", ".")

quest_timer_box = QuestTimerBox((BLACK), 748, 494, 250, 103)

# Buttons
quest_button = Button((BLACK), 10, 10, 250, 100, "CHOP WOOD")
quest_button_2 = Button((BLACK), 270, 10, 250, 100, "GO MINING")

sell_button = Button((BLACK), 1014, 600, 250, 100, "SELL")

# Inventory buttons
debug_item_button = InventoryButton((BLACK), 1000, 2, 278, 20, 1002, 4, 1150, 4, f'Debug Item: {debug_item_amount}', f'Price: {debug_item_price}')
wood_item_button = InventoryButton((BLACK), 1000, 22, 278, 20, 1002, 24, 1150, 24, f'Wood: {wood_item_amount}', f'Price: {wood_item_price}')
stone_item_button = InventoryButton((BLACK), 1000, 42, 278, 20, 1002, 44, 1150, 44, f'Stone: {stone_item_amount}', f'Price: {stone_item_price}')
iron_item_button = InventoryButton((BLACK), 1000, 62, 278, 20, 1002, 64, 1150, 64, f'Iron: {iron_item_amount}', f'Price: {iron_item_price}')

clock = pygame.time.Clock()

# Custom quest events
TIMER = pygame.USEREVENT + 1

QUEST_1 = pygame.USEREVENT + 2
QUEST_2 = pygame.USEREVENT + 3


def run_game():
    # Items and amounts
    global debug_item_amount
    global debug_item_price
    global wood_item_amount
    global wood_item_price
    global stone_item_amount
    global stone_item_price
    global iron_item_amount
    global iron_item_price

    # Test buttons
    global quest_button
    global quest_button_2

    # Gold
    global gold_amount
    global gold_text

    # Inventory buttons
    global debug_item_button
    global wood_item_button
    global stone_item_button
    global iron_item_button

    # Variable for game loop
    running = True

    # Quest timers
    timer_font = pygame.font.Font(None, 38)
    timer_box_font = pygame.font.Font(None, 50)
    current_timer = None
    current_timer_text = None

    quest_1_timer = 10
    quest_1_timer_text = timer_font.render("00:10", True, (WHITE))

    quest_2_timer = 30
    quest_2_timer_text = timer_font.render("00:30", True, (WHITE))

    # Boolean to items to sell
    sell_debug_item = False
    sell_wood = False
    sell_stone = False
    sell_iron = False

    # Boolean to check if button is clicked
    clicked = False
    
    # clock to tick
    global clock

    while running:
        # Mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check for events
        for event in pygame.event.get():
            # User pressed a key?
            if event.type == KEYDOWN:
                # If the key is escape
                if event.key == K_ESCAPE:
                    # Shutdown the program
                    running = False
                    terminate()
            # User hit the cross in top right corner
            elif event.type == QUIT:
                # Shutdown the program
                running == False
                terminate()


            if event.type == TIMER:
                if current_timer > 0:
                    current_timer -= 1
                    current_timer_text = timer_box_font.render("00:%02d" % current_timer, True, (WHITE))
                else:
                    pygame.time.set_timer(TIMER, 0)
                    current_timer = None
                    current_timer_text = None
                    screen.fill((BLACK))
                    item_inventory_display.draw(screen, (CYAN))


            if event.type == QUEST_1:
                wood_item_amount += random.randint(1, 3)
                wood_item_price += wood_item_amount * 4

                pygame.time.set_timer(QUEST_1, 0)

                clicked = False


            elif event.type == QUEST_2:
                stone_item_amount += random.randint(2, 5)
                stone_item_price += stone_item_amount * 2

                iron_item_amount += random.randint(1, 2)
                iron_item_price += iron_item_amount * 8

                pygame.time.set_timer(QUEST_2, 0)

                clicked = False


            # If mousebutton down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quest_button.is_over(mouse_pos) and clicked == False:
                    clicked = True

                    quest_1_timer_text = timer_font.render("00:10", True, (WHITE))
                    current_timer = quest_1_timer
                    current_timer_text = quest_1_timer_text

                    pygame.time.set_timer(QUEST_1, 10000)
                    pygame.time.set_timer(TIMER, 1000)

                elif quest_button_2.is_over(mouse_pos) and clicked == False:
                    clicked = True

                    quest_2_timer_text = timer_font.render("00:30", True, (WHITE))
                    current_timer = quest_2_timer
                    current_timer_text = quest_2_timer_text

                    pygame.time.set_timer(QUEST_2, 30000)
                    pygame.time.set_timer(TIMER, 1000)


                # Check if player pressed the sell button
                # Make this into a function later... FUCKKKKKKKKKKKKK
                if sell_button.is_over(mouse_pos):
                    if sell_debug_item == True:
                        gold_amount += debug_item_price
                        gold_display.draw_text(screen, f'Gold: {gold_amount}')
                        debug_item_amount -= debug_item_amount
                        debug_item_price -= debug_item_price
                        sell_debug_item = False
                    elif sell_wood == True:
                        gold_amount += wood_item_price
                        gold_display.draw_text(screen, f'Gold: {gold_amount}')
                        wood_item_amount -= wood_item_amount
                        wood_item_price -= wood_item_price
                        sell_wood = False
                    elif sell_stone == True:
                        gold_amount += stone_item_price
                        gold_display.draw_text(screen, f'Gold: {gold_amount}')
                        stone_item_amount -= stone_item_amount
                        stone_item_price -= stone_item_price
                        sell_stone = False
                    elif sell_iron == True:
                        gold_amount += iron_item_price
                        gold_display.draw_text(screen, f'Gold: {gold_amount}')
                        iron_item_amount -= iron_item_amount
                        iron_item_price -= iron_item_price
                        sell_iron = False
                    item_inventory_display.draw(screen, (CYAN))


                # Check if player pressed a button/text in the inventory
                if debug_item_button.is_over(mouse_pos) and debug_item_amount >= 1:
                    draw_texts_to_item_display("Debug item", f'Price: {debug_item_price}')
                    sell_debug_item = True
                elif wood_item_button.is_over(mouse_pos) and wood_item_amount >= 1:
                    draw_texts_to_item_display("Wood", f'Price: {wood_item_price}')
                    sell_wood = True
                elif stone_item_button.is_over(mouse_pos) and stone_item_amount >= 1:
                    draw_texts_to_item_display("Stone", f'Price: {stone_item_price}')
                    sell_stone = True
                elif iron_item_button.is_over(mouse_pos) and iron_item_amount >= 1:
                    draw_texts_to_item_display("Iron", f'Price: {iron_item_price}')
                    sell_iron = True

        # Draw buttons
        quest_button.draw(screen, (CYAN))
        quest_button_2.draw(screen, (CYAN))

        # Draw inventory
        item_inventory.draw(screen,(CYAN))

        # Draw gold
        gold_display.draw(screen, (CYAN))
        gold_display.draw_text(screen, f'Gold: {gold_amount}')

        quest_timer_box.draw(screen, (CYAN))

        # Draw inventory buttons
        debug_item_button.draw(screen, (BLACK))
        wood_item_button.draw(screen, (BLACK))
        stone_item_button.draw(screen, (BLACK))
        iron_item_button.draw(screen, (BLACK))



        # Draw timers to butons
        if current_timer_text == None:
            screen.blit(quest_1_timer_text, (100, 15))
            screen.blit(quest_2_timer_text, (360, 15))
        else:
            screen.blit(current_timer_text, (825, 525))

        # Draw texts to inventory
        if debug_item_amount >= 1:
            debug_item_button.draw_inventory_text(screen, f'Debug Item: {debug_item_amount}', f'Price: {debug_item_price}')
        if wood_item_amount >= 1:
            wood_item_button.draw_inventory_text(screen, f'Wood: {wood_item_amount}', f'Price: {wood_item_price}')
        if stone_item_amount >= 1:
            stone_item_button.draw_inventory_text(screen, f'Stone: {stone_item_amount}', f'Price: {stone_item_price}')
        if iron_item_amount >= 1:
            iron_item_button.draw_inventory_text(screen, f'Iron: {iron_item_amount}', f'Price: {iron_item_price}')

        # Update the display
        pygame.display.update()

        clock.tick(FPS)


# Function to shutdown the program
def terminate():
    pygame.quit()
    sys.exit()

# Go to the main function
if __name__ == "__main__":
    main()
