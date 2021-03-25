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
    "Iron" : [0, 0],
    "Bear flesh" : [0, 0],
    "Bear skin" : [0, 0],
    "Fish" : [0, 0],
    "Woodman's axe" : [0, 0],
    "Miner's pickaxe" : [0, 0],
    "Hunter's bow" : [0, 0],
    "Fighter's sword" : [0, 0],
    "Fisherman's rod" : [0, 0],
    "Jack of all trades" : [0, 0]
}

shop_items = {
    "Woodman's axe" : 70,
    "Miner's pickaxe" : 320,
    "Hunter's bow" : 900,
    "Fighter's sword" : 2500,
    "Fisherman's rod" : 5300,
    "Jack of all trades" : 10000
}


class Button():
    def __init__(self, color, x, y, width, height, font_size, text = "", locked_text = ""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.locked_text = locked_text
        self.font_size = font_size

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

    def draw_text(self, screen):
        if self.text != "":
            font = pygame.font.SysFont(None, self.font_size)
            text = font.render(self.text, True, (WHITE))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def draw_locked_text(self, screen):
        if self.locked_text != "":
            font = pygame.font.SysFont(None, 30)
            text = font.render(self.locked_text, True, (WHITE))
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
            item_name_font = pygame.font.SysFont(None, 40)
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
        if self.item_name != None:
            item_name_font = pygame.font.SysFont(None, 25)
            item_name_text = item_name_font.render(_itemname, True, (WHITE))
            screen.blit(item_name_text, (self.item_name_x, self.item_name_y))
        if self.item_price != None:
            item_price_font = pygame.font.SysFont(None, 25)
            item_price_text = item_price_font.render(_itemprice, True, (WHITE))
            screen.blit(item_price_text, (self.item_price_x, self.item_price_y))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class Gold():
    def __init__(self, color, x, y, width, height, gold_x, gold_y):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.gold_x = gold_x
        self.gold_y = gold_y

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height),0)

    def draw_text(self, screen, _gold_amount = ""):
        font = pygame.font.SysFont(None, 50)
        text = font.render(_gold_amount, True, (WHITE))
        screen.blit(text, (self.gold_x, self.gold_y))


class Level():
    def __init__(self, color, x, y, width, height, level_x, level_y, xp_x, xp_y):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.level_x = level_x
        self.level_y = level_y
        self.xp_x = xp_x
        self.xp_y = xp_y

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

    def draw_level_text(self, screen, _level_amount = ""):
        font = pygame.font.Font(None, 50)
        text = font.render(_level_amount, True, (WHITE))
        screen.blit(text, (self.level_x, self.level_y))

    def draw_xp_text(self, screen, _xp_amount = ""):
        font = pygame.font.Font(None, 30)
        text = font.render(_xp_amount, True, (WHITE))
        screen.blit(text, (self.xp_x, self.xp_y))


class Shop():
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

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
    item_inventory_display.draw(screen, (CYAN))

    # Set a caption
    pygame.display.set_caption("Quest Master")

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
    sell_button.draw_text(screen)


def quest_reward(rand_num, item_amount, item_price, item_price_int, rand_int_1, rand_int_2):
    rand_num += random.randint(rand_int_1, rand_int_2)
    item_price += rand_num * item_price_int
    item_amount += rand_num

    return item_amount, item_price


def sell_item(item_amount, item_price):
    global gold_amount

    gold_amount += item_price
    gold_display.draw_text(screen, f'Gold: {gold_amount}')
    item_amount -= item_amount
    item_price -= item_price

    return item_amount, item_price


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
bear_flesh_item_amount = items["Bear flesh"][0]
bear_flesh_item_price = items["Bear flesh"][1]
bear_skin_item_amount = items["Bear skin"][0]
bear_skin_item_price = items["Bear skin"][1]
fish_item_amount = items["Fish"][0]
fish_item_price = items["Fish"][1]
woodmans_axe_amount = items["Woodman's axe"][0]
woodmans_axe_price = items["Woodman's axe"][1]
miners_pickaxe_amount = items["Miner's pickaxe"][0]
miners_pickaxe_price = items["Miner's pickaxe"][1]
hunters_bow_amount = items["Hunter's bow"][0]
hunters_bow_price = items["Hunter's bow"][1]
fighters_sword_amount = items["Fighter's sword"][0]
fighters_sword_price = items["Fighter's sword"][1]
fishermans_rod_amount = items["Fisherman's rod"][0]
fishermans_rod_price = items["Fisherman's rod"][1]
jack_of_all_trades_amount = items["Jack of all trades"][0]
jack_of_all_trades_price = items["Jack of all trades"][1]

# Shop items
woodmans_axe_cost = shop_items["Woodman's axe"]
miners_pickaxe_cost = shop_items["Miner's pickaxe"]
hunters_bow_cost = shop_items["Hunter's bow"]
fighters_sword_cost = shop_items["Fighter's sword"]
fishermans_rod_cost = shop_items["Fisherman's rod"]
jack_of_all_trades_cost = shop_items["Jack of all trades"]


# Gold
gold_amount = 50000
gold_display = Gold((BLACK), 748, 600, 250, 115, 752, 637)

# Level
level = 100
xp_to_next_level = 100
level_display = Level((BLACK), 495, 600, 250, 115, 498, 610, 498, 670)

# Inventory
item_inventory = Inventory((BLACK), 1000, 2, 278, 490, "Inventory")
item_inventory_display = DrawItemDisplay((BLACK), 1000, 495, 278, 220, 1005, 505, 1005, 565, ".", ".")

quest_timer_box = QuestTimerBox((BLACK), 748, 494, 250, 103)

# Buttons
# Quest buttons
quest_button = Button((BLACK), 10, 10, 250, 100, 40, "CHOP WOOD")
quest_button_2 = Button((BLACK), 375, 10, 250, 100, 40, "MINE ORES", "LEVEL 3 REQUIRED")
quest_button_3 = Button((BLACK), 740, 10, 250, 100, 40, "GO HUNTING", "LEVEL 5 REQUIRED")
quest_button_4 = Button((BLACK), 10, 190, 250, 100, 40, "GO FISHING", "LEVEL 8 REQUIRED")

# Sell button on item display
sell_button = Button((BLACK), 1014, 600, 250, 100, 40, "SELL")

# Shop button
shop_button = Button((BLACK), 2, 600, 490, 115, 60, "SHOP")

# Inventory buttons
# Normal items
debug_item_button = InventoryButton((BLACK), 1000, 2, 278, 20, 1002, 4, 1150, 4, f'Debug Item: {debug_item_amount}', f'Price: {debug_item_price}')
wood_item_button = InventoryButton((BLACK), 1000, 22, 278, 20, 1002, 24, 1150, 24, f'Wood: {wood_item_amount}', f'Price: {wood_item_price}')
stone_item_button = InventoryButton((BLACK), 1000, 42, 278, 20, 1002, 44, 1150, 44, f'Stone: {stone_item_amount}', f'Price: {stone_item_price}')
iron_item_button = InventoryButton((BLACK), 1000, 62, 278, 20, 1002, 64, 1150, 64, f'Iron: {iron_item_amount}', f'Price: {iron_item_price}')
bear_flesh_item_button = InventoryButton((BLACK), 1000, 82, 278, 20, 1002, 84, 1150, 84, f'Bear Flesh: {bear_flesh_item_amount}', f'Price: {bear_flesh_item_price}')
bear_skin_item_button = InventoryButton((BLACK), 1000, 102, 278, 20, 1002, 104, 1150, 104, f'Bear Skin: {bear_skin_item_amount}', f'Price: {bear_skin_item_price}')
fish_item_button = InventoryButton((BLACK), 1000, 122, 278, 20, 1002, 124, 1150, 124, f'Fish: {fish_item_amount}', f'Price: {fish_item_price}')
woodmans_axe_item_button = InventoryButton((BLACK), 1000, 142, 278, 20, 1002, 144, 1160, 144, f"Woodman's Axe: {woodmans_axe_amount}", f"Price: {woodmans_axe_price}")
miners_pickaxe_item_button = InventoryButton((BLACK), 1000, 162, 278, 20, 1002, 164, 1170, 164, f"Miner's Pickaxe: {miners_pickaxe_amount}", f'Price: {miners_pickaxe_price}')
hunters_bow_item_button = InventoryButton((BLACK), 1000, 182, 278, 20, 1002, 184, 1150, 184, f"Hunter's Bow: {hunters_bow_amount}", f'Price: {hunters_bow_price}')
fighters_sword_item_button = InventoryButton((BLACK), 1000, 202, 278, 20, 1002, 204, 1170, 204, f"Fighter's Sword: {fighters_sword_amount}", f'Price: {fighters_sword_price}')
fishermans_rod_item_button = InventoryButton((BLACK), 1000, 222, 278, 20, 1002, 224, 1180, 224, f"Fisherman's Rod: {fishermans_rod_amount}", f'Price: {fishermans_rod_price}')
jack_of_all_trades_item_button = InventoryButton((BLACK), 1000, 242, 278, 20, 1002, 244, 1180, 244, f"Jack Of All Trades: {jack_of_all_trades_amount}", f'Price: {jack_of_all_trades_price}')

clock = pygame.time.Clock()

# Custom quest events
TIMER = pygame.USEREVENT + 1

QUEST_1 = pygame.USEREVENT + 2
QUEST_2 = pygame.USEREVENT + 3
QUEST_3 = pygame.USEREVENT + 4
QUEST_4 = pygame.USEREVENT + 5


def run_game():
    screen.fill((BLACK))
    item_inventory_display.draw(screen, (CYAN))

    # Items and amounts
    global debug_item_amount
    global debug_item_price
    global wood_item_amount
    global wood_item_price
    global stone_item_amount
    global stone_item_price
    global iron_item_amount
    global iron_item_price
    global bear_flesh_item_amount
    global bear_flesh_item_price
    global bear_skin_item_amount
    global bear_skin_item_price
    global fish_item_amount
    global fish_item_price
    global woodmans_axe_amount
    global woodmans_axe_price
    global miners_pickaxe_amount
    global miners_pickaxe_price
    global hunters_bow_amount
    global hunters_bow_price
    global fighters_sword_amount
    global fighters_sword_price
    global fishermans_rod_amount
    global fishermans_rod_price
    global jack_of_all_trades_amount
    global jack_of_all_trades_price

    # Test buttons
    global quest_button
    global quest_button_2

    # Gold
    global gold_amount
    global gold_text

    # Level
    global level
    global xp_to_next_level
    current_xp_to_next_level = xp_to_next_level

    # Inventory buttons
    global debug_item_button
    global wood_item_button
    global stone_item_button
    global iron_item_button
    global bear_flesh_item_button
    global bear_skin_item_button
    global fish_item_button
    global woodmans_axe_item_button
    global miners_pickaxe_item_button
    global hunters_bow_item_button
    global fighters_sword_item_button
    global fishermans_rod_item_button
    global jack_of_all_trades_item_button

    global woodmans_axe_bought
    global miners_pickaxe_bought
    global hunters_bow_bought
    global fighters_sword_bought
    global fishermans_rod_bought
    global jack_of_all_trades_bought

    # Variable for game loop
    running = True

    # Quest timers
    timer_font = pygame.font.Font(None, 38)
    timer_box_font = pygame.font.Font(None, 50)
    current_timer = 0
    current_timer_text = None

    quest_1_timer = 10
    quest_1_timer_text = timer_font.render("00:10", True, (WHITE))

    quest_2_timer = 30
    quest_2_timer_text = timer_font.render("00:30", True, (WHITE))

    quest_3_timer = 60
    quest_3_timer_text = timer_font.render("01:00", True, (WHITE))

    quest_4_timer = 120
    quest_4_timer_text = timer_font.render("02:00", True, (WHITE))

    # Boolean to items to sell
    sell_debug_item = False
    sell_wood = False
    sell_stone = False
    sell_iron = False
    sell_bear_flesh = False
    sell_bear_skin = False
    sell_fish = False
    sell_woodmans_axe = False
    sell_miners_pickaxe = False
    sell_hunters_bow = False
    sell_fighters_sword = False
    sell_fishermans_rod = False
    sell_jack_of_all_trades = False

    # Boolean to check if button is clicked
    clicked = False

    rand_amount = 0
    
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
                    current_timer_text = timer_box_font.render("%02d" % current_timer, True, (WHITE))
                else:
                    pygame.time.set_timer(TIMER, 0)
                    current_timer = 0
                    current_timer_text = None
                    screen.fill((BLACK))
                    item_inventory_display.draw(screen, (CYAN))


            if event.type == QUEST_1:
                if woodmans_axe_bought == True:
                    if jack_of_all_trades_bought == True:
                        wood_item_amount, wood_item_price = quest_reward(rand_amount, wood_item_amount, wood_item_price, 4, 6, 9)
                        rand_amount = 0
                    else:
                        wood_item_amount, wood_item_price = quest_reward(rand_amount, wood_item_amount, wood_item_price, 4, 3, 4)
                        rand_amount = 0
                else:
                    wood_item_amount, wood_item_price = quest_reward(rand_amount, wood_item_amount, wood_item_price, 4, 1, 3)
                    rand_amount = 0

                xp_to_next_level -= random.randint(8, 12)

                pygame.time.set_timer(QUEST_1, 0)

                clicked = False

                quest_1_timer = 10
            elif event.type == QUEST_2:
                if miners_pickaxe_bought == True:
                    if jack_of_all_trades_bought == True:
                        stone_item_amount, stone_item_price = quest_reward(rand_amount, stone_item_amount, stone_item_price, 2, 8, 12)
                        rand_amount = 0
                        iron_item_amount, iron_item_price = quest_reward(rand_amount, iron_item_amount, iron_item_price, 8, 5, 7)
                        rand_amount = 0
                    else:
                        stone_item_amount, stone_item_price = quest_reward(rand_amount, stone_item_amount, stone_item_price, 2, 5, 8)
                        rand_amount = 0
                        iron_item_amount, iron_item_price = quest_reward(rand_amount, iron_item_amount, iron_item_price, 8, 3, 4)
                        rand_amount = 0
                else:
                    stone_item_amount, stone_item_price = quest_reward(rand_amount, stone_item_amount, stone_item_price, 2, 2, 5)
                    rand_amount = 0
                    iron_item_amount, iron_item_price = quest_reward(rand_amount, iron_item_amount, iron_item_price, 8, 1, 2)
                    rand_amount = 0

                xp_to_next_level -= random.randint(16, 23)

                pygame.time.set_timer(QUEST_2, 0)
                clicked = False

                quest_2_timer = 30
            elif event.type == QUEST_3:
                if fighters_sword_bought == True:
                    if jack_of_all_trades_bought == True:
                        bear_flesh_item_amount, bear_flesh_item_price = quest_reward(rand_amount, bear_flesh_item_amount, bear_flesh_item_price, 16, 4, 6)
                        rand_amount = 0
                        bear_skin_item_amount, bear_skin_item_price = quest_reward(rand_amount, bear_skin_item_amount, bear_skin_item_price, 10, 4, 6)
                        rand_amount = 0
                    else:
                        bear_flesh_item_amount, bear_flesh_item_price = quest_reward(rand_amount, bear_flesh_item_amount, bear_flesh_item_price, 16, 2, 4)
                        rand_amount = 0
                        bear_skin_item_amount, bear_skin_item_price = quest_reward(rand_amount, bear_skin_item_amount, bear_skin_item_price, 10, 2, 4)
                        rand_amount = 0
                else:
                    bear_flesh_item_amount, bear_flesh_item_price = quest_reward(rand_amount, bear_flesh_item_amount, bear_flesh_item_price, 16, 1, 2)
                    rand_amount = 0
                    bear_skin_item_amount, bear_skin_item_price = quest_reward(rand_amount, bear_skin_item_amount, bear_skin_item_price, 10, 1, 2)
                    rand_amount = 0

                xp_to_next_level -= random.randint(29, 36)

                pygame.time.set_timer(QUEST_3, 0)
                clicked = False

                quest_3_timer = 60
            elif event.type == QUEST_4:
                if fishermans_rod_bought == True:
                    if jack_of_all_trades_bought == True:
                        fish_item_amount, fish_item_price = quest_reward(rand_amount, fish_item_amount, fish_item_price, 21, 6, 7)
                        rand_amount = 0
                    else:
                        fish_item_amount, fish_item_price = quest_reward(rand_amount, fish_item_amount, fish_item_price, 21, 3, 4)
                        rand_amount = 0
                else:
                    fish_item_amount, fish_item_price = quest_reward(rand_amount, fish_item_amount, fish_item_price, 21, 1, 2)
                    rand_amount = 0

                xp_to_next_level -= random.randint(48, 54)

                pygame.time.set_timer(QUEST_4, 0)
                clicked = False

                quest_4_timer = 120

            # If mousebutton down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.is_over(mouse_pos):
                    running = False
                    shop()
                if quest_button.is_over(mouse_pos) and clicked == False:
                    clicked = True
                    if woodmans_axe_bought == True:
                        quest_1_timer -= 2
                        quest_1_timer_text = timer_font.render("08", True, (WHITE))

                        current_timer = quest_1_timer
                        current_timer_text = quest_1_timer_text

                        pygame.time.set_timer(QUEST_1, 8000)
                        pygame.time.set_timer(TIMER, 1000)
                    else:
                        quest_1_timer_text = timer_font.render("10", True, (WHITE))
                        current_timer = quest_1_timer
                        current_timer_text = quest_1_timer_text

                        pygame.time.set_timer(QUEST_1, 10000)
                        pygame.time.set_timer(TIMER, 1000)

                elif quest_button_2.is_over(mouse_pos) and clicked == False and level >= 3:
                    clicked = True
                    if miners_pickaxe_bought == True:
                        quest_2_timer -= 5
                        quest_2_timer_text = timer_font.render("25", True, (WHITE))
                        current_timer = quest_2_timer
                        current_timer_text = quest_2_timer_text

                        pygame.time.set_timer(QUEST_2, 25000)
                        pygame.time.set_timer(TIMER, 1000)
                    else:
                        quest_2_timer_text = timer_font.render("30", True, (WHITE))
                        current_timer = quest_2_timer
                        current_timer_text = quest_2_timer_text

                        pygame.time.set_timer(QUEST_2, 30000)
                        pygame.time.set_timer(TIMER, 1000)
                elif quest_button_3.is_over(mouse_pos) and clicked == False and level >= 5:
                    clicked = True
                    if hunters_bow_bought == True:
                        quest_3_timer -= 15
                        quest_3_timer_text = timer_font.render("45", True, (WHITE))
                        current_timer = quest_3_timer
                        current_timer_text = quest_3_timer_text

                        pygame.time.set_timer(QUEST_3, 45000)
                        pygame.time.set_timer(TIMER, 1000)
                    else:
                        quest_3_timer_text = timer_font.render("60", True, (WHITE))
                        current_timer = quest_3_timer
                        current_timer_text = quest_3_timer_text

                        pygame.time.set_timer(QUEST_3, 60000)
                        pygame.time.set_timer(TIMER, 1000)
                elif quest_button_4.is_over(mouse_pos) and clicked == False and level >= 8:
                    clicked = True
                    if fishermans_rod_bought == True:
                        quest_4_timer -= 30
                        quest_4_timer_text = timer_font.render("90", True, (WHITE))
                        current_timer = quest_4_timer
                        current_timer_text = quest_4_timer_text

                        pygame.time.set_timer(QUEST_4, 90000)
                        pygame.time.set_timer(TIMER, 1000)
                    else:
                        quest_4_timer_text = timer_font.render("120", True, (WHITE))
                        current_timer = quest_4_timer
                        current_timer_text = quest_4_timer_text

                        pygame.time.set_timer(QUEST_4, 120000)
                        pygame.time.set_timer(TIMER, 1000)



                # Check if player pressed the sell button
                if sell_button.is_over(mouse_pos):
                    if sell_debug_item == True:
                        debug_item_amount, debug_item_price = sell_item(debug_item_amount, debug_item_price)
                        sell_debug_item = False
                    elif sell_wood == True:
                        wood_item_amount, wood_item_price = sell_item(wood_item_amount, wood_item_price)
                        sell_wood = False
                    elif sell_stone == True:
                        stone_item_amount, stone_item_price = sell_item(stone_item_amount, stone_item_price)
                        sell_stone = False
                    elif sell_iron == True:
                        iron_item_amount, iron_item_price = sell_item(iron_item_amount, iron_item_price)
                        sell_iron = False
                    elif sell_bear_flesh == True:
                        bear_flesh_item_amount, bear_flesh_item_price = sell_item(bear_flesh_item_amount, bear_flesh_item_price)
                        sell_bear_flesh = False
                    elif sell_bear_skin == True:
                        bear_skin_item_amount, bear_skin_item_price = sell_item(bear_skin_item_amount, bear_skin_item_price)
                        sell_bear_skin = False
                    elif sell_fish == True:
                        fish_item_amount, fish_item_price = sell_item(fish_item_amount, fish_item_price)
                        sell_fish = False
                    elif sell_woodmans_axe == True:
                        woodmans_axe_amount, woodmans_axe_price = sell_item(woodmans_axe_amount, woodmans_axe_price)
                        woodmans_axe_bought = False
                        sell_woodmans_axe = False
                    elif sell_miners_pickaxe == True:
                        miners_pickaxe_amount, miners_pickaxe_price = sell_item(miners_pickaxe_amount, miners_pickaxe_price)
                        miners_pickaxe_bought = False
                        sell_miners_pickaxe = False
                    elif sell_hunters_bow == True:
                        hunters_bow_amount, hunters_bow_price = sell_item(hunters_bow_amount, hunters_bow_price)
                        hunters_bow_bought = False
                        sell_hunters_bow = False
                    elif sell_fighters_sword == True:
                        fighters_sword_amount, fighters_sword_price = sell_item(fighters_sword_amount, fighters_sword_price)
                        fighters_sword_bought = False
                        sell_fighters_sword = False
                    elif sell_fishermans_rod == True:
                        fishermans_rod_amount, fishermans_rod_price = sell_item(fishermans_rod_amount, fishermans_rod_price)
                        fishermans_rod_bought = False
                        sell_fishermans_rod = False
                    elif sell_jack_of_all_trades == True:
                        jack_of_all_trades_amount, jack_of_all_trades_price = sell_item(jack_of_all_trades_amount, jack_of_all_trades_price)
                        jack_of_all_trades_bought = False
                        sell_jack_of_all_trades = False
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
                elif bear_flesh_item_button.is_over(mouse_pos) and bear_flesh_item_amount >= 1:
                    draw_texts_to_item_display("Bear Flesh", f'Price: {bear_flesh_item_price}')
                    sell_bear_flesh = True
                elif bear_skin_item_button.is_over(mouse_pos) and bear_skin_item_amount >= 1:
                    draw_texts_to_item_display("Bear Skin", f'Price: {bear_skin_item_price}')
                    sell_bear_skin = True
                elif fish_item_button.is_over(mouse_pos) and fish_item_amount >= 1:
                    draw_texts_to_item_display("Fish", f'Price: {fish_item_price}')
                    sell_fish = True
                elif woodmans_axe_item_button.is_over(mouse_pos) and woodmans_axe_amount >= 1:
                    draw_texts_to_item_display("Woodman's Axe", f'Price: {woodmans_axe_price}')
                    sell_woodmans_axe = True
                elif miners_pickaxe_item_button.is_over(mouse_pos) and miners_pickaxe_amount >= 1:
                    draw_texts_to_item_display("Miner's Pickaxe", f'Price: {miners_pickaxe_price}')
                    sell_miners_pickaxe = True
                elif hunters_bow_item_button.is_over(mouse_pos) and hunters_bow_amount >= 1:
                    draw_texts_to_item_display("Hunter's Bow", f'Price: {hunters_bow_price}')
                    sell_hunters_bow = True
                elif fighters_sword_item_button.is_over(mouse_pos) and fighters_sword_amount >= 1:
                    draw_texts_to_item_display("Fighter's Sword", f'Price: {fighters_sword_price}')
                    sell_fighters_sword = True
                elif fishermans_rod_item_button.is_over(mouse_pos) and fishermans_rod_amount >= 1:
                    draw_texts_to_item_display("Fisherman's Rod", f'Price: {fishermans_rod_price}')
                    sell_fishermans_rod = True
                elif jack_of_all_trades_item_button.is_over(mouse_pos) and jack_of_all_trades_amount >= 1:
                    draw_texts_to_item_display("Jack Of All Trades", f'Price: {jack_of_all_trades_price}')
                    sell_jack_of_all_trades = True

        if xp_to_next_level <= 0:
            level += 1
            current_xp_to_next_level += 100
            xp_to_next_level = current_xp_to_next_level


        quest_button_2.draw(screen, (CYAN))
        if level < 3:
            quest_button_2.draw_locked_text(screen)
        else:
            quest_button_2.draw_text(screen)

        quest_button_3.draw(screen, (CYAN))
        if level < 5:
            quest_button_3.draw_locked_text(screen)
        else:
            quest_button_3.draw_text(screen)

        quest_button_4.draw(screen, (CYAN))
        if level < 8:
            quest_button_4.draw_locked_text(screen)
        else:
            quest_button_4.draw_text(screen)


        # Draw inventory
        item_inventory.draw(screen,(CYAN))

        # Draw gold
        gold_display.draw(screen, (CYAN))
        gold_display.draw_text(screen, f'Gold: {gold_amount}')

        # Draw level
        level_display.draw(screen, (CYAN))
        level_display.draw_level_text(screen, f'Level: {level}')
        level_display.draw_xp_text(screen, f'XP to next level: {xp_to_next_level}')


        quest_timer_box.draw(screen, (CYAN))

        # Draw buttons
        # Quest buttons
        quest_button.draw(screen, (CYAN))
        quest_button.draw_text(screen)

        # Draw inventory buttons
        debug_item_button.draw(screen, (BLACK))
        wood_item_button.draw(screen, (BLACK))
        stone_item_button.draw(screen, (BLACK))
        iron_item_button.draw(screen, (BLACK))
        bear_flesh_item_button.draw(screen, (BLACK))
        bear_skin_item_button.draw(screen, (BLACK))
        fish_item_button.draw(screen, (BLACK))
        woodmans_axe_item_button.draw(screen, (BLACK))
        miners_pickaxe_item_button.draw(screen, (BLACK))
        hunters_bow_item_button.draw(screen, (BLACK))
        fighters_sword_item_button.draw(screen, (BLACK))
        fishermans_rod_item_button.draw(screen, (BLACK))
        jack_of_all_trades_item_button.draw(screen, (BLACK))

        # Shop button
        shop_button.draw(screen, (CYAN))
        shop_button.draw_text(screen)


        # Draw timers to butons
        if current_timer_text == None:
            screen.blit(quest_1_timer_text, (100, 15))
            screen.blit(quest_2_timer_text, (465, 15))
            screen.blit(quest_3_timer_text, (832, 15))
            screen.blit(quest_4_timer_text, (100, 195))
        else:
            screen.blit(current_timer_text, (840, 525))

        # Draw texts to inventory
        if debug_item_amount >= 1:
            debug_item_button.draw_inventory_text(screen, f'Debug Item: {debug_item_amount}', f'Price: {debug_item_price}')
        if wood_item_amount >= 1:
            wood_item_button.draw_inventory_text(screen, f'Wood: {wood_item_amount}', f'Price: {wood_item_price}')
        if stone_item_amount >= 1:
            stone_item_button.draw_inventory_text(screen, f'Stone: {stone_item_amount}', f'Price: {stone_item_price}')
        if iron_item_amount >= 1:
            iron_item_button.draw_inventory_text(screen, f'Iron: {iron_item_amount}', f'Price: {iron_item_price}')
        if bear_flesh_item_amount >= 1:
            bear_flesh_item_button.draw_inventory_text(screen, f'Bear Flesh: {bear_flesh_item_amount}', f'Price: {bear_flesh_item_price}')
        if bear_skin_item_amount >= 1:
            bear_skin_item_button.draw_inventory_text(screen, f'Bear Skin: {bear_skin_item_amount}', f'Price: {bear_skin_item_price}')
        if fish_item_amount >= 1:
            fish_item_button.draw_inventory_text(screen, f'Fish: {fish_item_amount}', f'Price: {fish_item_price}')
        if woodmans_axe_amount >= 1:
            woodmans_axe_item_button.draw_inventory_text(screen, f"Woodman's Axe: {woodmans_axe_amount}", f'Price: {woodmans_axe_price}')
        if miners_pickaxe_amount >= 1:
            miners_pickaxe_item_button.draw_inventory_text(screen, f"Miner's Pickaxe: {miners_pickaxe_amount}", f'Price: {miners_pickaxe_price}')
        if hunters_bow_amount >= 1:
            hunters_bow_item_button.draw_inventory_text(screen, f"Hunter's Bow: {hunters_bow_amount}", f'Price: {hunters_bow_price}')
        if fighters_sword_amount >= 1:
            fighters_sword_item_button.draw_inventory_text(screen, f"Fighter's Sword: {fighters_sword_amount}", f'Price: {fighters_sword_price}')
        if fishermans_rod_amount >= 1:
            fishermans_rod_item_button.draw_inventory_text(screen, f"Fisherman's Rod: {fishermans_rod_amount}", f'Price: {fishermans_rod_price}')
        if jack_of_all_trades_amount >= 1:
            jack_of_all_trades_item_button.draw_inventory_text(screen, f"Jack Of All Trades: {jack_of_all_trades_amount}", f'Price: {jack_of_all_trades_price}')

        # Update the display
        pygame.display.update()

        clock.tick(FPS)


# Cyan box around the screen
shop_box = Shop((BLACK), 2, 2, 1275, 712)

# Display gold in the shop
gold_display_shop = Gold((BLACK), 255, 600, 250, 115, 259, 637)

# Display shop inventory
shop_item_display = Inventory((BLACK), 2, 2, 503, 595)

# Display items in shop inventory
woodmans_axe = InventoryButton((BLACK), 2, 2, 500, 20, 4, 2, 20, 2, f"Woodman's Axe: {woodmans_axe_cost}")
miners_pickaxe = InventoryButton((BLACK), 2, 22, 500, 20, 4, 22, 20, 22, f"Miner's Pickaxe: {miners_pickaxe_cost}")
hunters_bow = InventoryButton((BLACK), 2, 42, 500, 20, 4, 42, 20, 42, f"Hunter's Bow: {hunters_bow_cost}")
fighters_sword = InventoryButton((BLACK), 2, 62, 500, 20, 4, 62, 20, 62, f"Fighter's Sword: {fighters_sword_cost}")
fishermans_rod = InventoryButton((BLACK), 2, 82, 500, 20, 4, 82, 20, 82, f"Fisherman's Rod: {fishermans_rod_cost}")
jack_of_all_trades = InventoryButton((BLACK), 2, 102, 500, 20, 4, 102, 20, 102, f"Jack Of All Trades: {jack_of_all_trades_cost}")

# Back button to go back to the game
back_button = Button((BLACK), 2, 600, 250, 115, 40, "BACK")

# Booleans to check if item has been bought
woodmans_axe_bought = False
miners_pickaxe_bought = False
hunters_bow_bought = False
fighters_sword_bought = False
fishermans_rod_bought = False
jack_of_all_trades_bought = False

def shop():
    running = True
    rand_amount = 0

    global gold_amount

    global woodmans_axe_amount
    global woodmans_axe_price
    global miners_pickaxe_amount
    global miners_pickaxe_price
    global hunters_bow_amount
    global hunters_bow_price
    global fighters_sword_amount
    global fighters_sword_price
    global fishermans_rod_amount
    global fishermans_rod_price
    global jack_of_all_trades_amount
    global jack_of_all_trades_price

    global woodmans_axe_bought
    global miners_pickaxe_bought
    global hunters_bow_bought
    global fighters_sword_bought
    global fishermans_rod_bought
    global jack_of_all_trades_bought

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # User pressed a key?
            if event.type == KEYDOWN:
                # If the key is escape
                if event.key == K_ESCAPE:
                    # Go back to the game
                    run_game()
            # User hit the cross in top right corner
            elif event.type == QUIT:
                # Shutdown the program
                running == False
                terminate()

            if event.type == MOUSEBUTTONDOWN:
                if back_button.is_over(mouse_pos):
                    running = False
                    run_game()

                if woodmans_axe.is_over(mouse_pos) and gold_amount >= 70:
                    gold_amount -= 70
                    woodmans_axe_amount, woodmans_axe_price = quest_reward(rand_amount, woodmans_axe_amount, woodmans_axe_price, 40, 1, 1)
                    woodmans_axe_bought = True
                    rand_amount = 0
                if miners_pickaxe.is_over(mouse_pos) and gold_amount >= 320:
                    gold_amount -= 320
                    miners_pickaxe_amount, miners_pickaxe_price = quest_reward(rand_amount, miners_pickaxe_amount, miners_pickaxe_price, 120, 1, 1)
                    miners_pickaxe_bought = True
                    rand_amount = 0
                if hunters_bow.is_over(mouse_pos) and gold_amount >= 900:
                    gold_amount -= 900
                    hunters_bow_amount, hunters_bow_price = quest_reward(rand_amount, hunters_bow_amount, hunters_bow_price, 720, 1, 1)
                    hunters_bow_bought = True
                    rand_amount = 0
                if fighters_sword.is_over(mouse_pos) and gold_amount >= 2500:
                    gold_amount -= 2500
                    fighters_sword_amount, fighters_sword_price = quest_reward(rand_amount, fighters_sword_amount, fighters_sword_price, 1900, 1, 1)
                    fighters_sword_bought = True
                    rand_amount = 0
                if fishermans_rod.is_over(mouse_pos) and gold_amount >= 5300:
                    gold_amount -= 5300
                    fishermans_rod_amount, fishermans_rod_price = quest_reward(rand_amount, fishermans_rod_amount, fishermans_rod_price, 4400, 1, 1)
                    fishermans_rod_bought = True
                    rand_amount = 0
                if jack_of_all_trades.is_over(mouse_pos) and gold_amount >= 10000:
                    gold_amount -= 10000
                    jack_of_all_trades_amount, jack_of_all_trades_price = quest_reward(rand_amount, jack_of_all_trades_amount, jack_of_all_trades_price, 8000, 1, 1)
                    jack_of_all_trades_bought = True
                    rand_amount = 0



        # Draw box around the shop
        shop_box.draw(screen, (CYAN))

        # Draw outlines for shop
        shop_item_display.draw(screen, (CYAN))

        # Draw items on screen
        woodmans_axe.draw(screen)
        woodmans_axe.draw_inventory_text(screen, f"Woodman's Axe : {woodmans_axe_cost} Gold")

        miners_pickaxe.draw(screen)
        miners_pickaxe.draw_inventory_text(screen, f"Miner's Pickaxe : {miners_pickaxe_cost} Gold")

        hunters_bow.draw(screen)
        hunters_bow.draw_inventory_text(screen, f"Hunter's Bow : {hunters_bow_cost} Gold")

        fighters_sword.draw(screen)
        fighters_sword.draw_inventory_text(screen, f"Fighter's Sword : {fighters_sword_cost} Gold")

        fishermans_rod.draw(screen)
        fishermans_rod.draw_inventory_text(screen, f"Fisherman's Rod : {fishermans_rod_cost} Gold")

        jack_of_all_trades.draw(screen)
        jack_of_all_trades.draw_inventory_text(screen, f"Jack Of All Trades : {jack_of_all_trades_cost} Gold")

        # Draw gold
        gold_display_shop.draw(screen, (CYAN))
        gold_display_shop.draw_text(screen, f'Gold: {gold_amount}')

        # Buttons
        back_button.draw(screen, (CYAN))
        back_button.draw_text(screen)

        # Update the display
        pygame.display.update()


# Function to shutdown the program
def terminate():
    pygame.quit()
    sys.exit()


# Go to the main function
if __name__ == "__main__":
    main()
