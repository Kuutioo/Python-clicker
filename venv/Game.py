import pygame
import random
import sys
import time
import json
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
    "Woodmans axe" : [0, 0],
    "Miners pickaxe" : [0, 0],
    "Hunters bow" : [0, 0],
    "Fighters sword" : [0, 0],
    "Fishermans rod" : [0, 0],
    "Jack of all trades" : [0, 0]
}

player_attributes = {
    "Gold" : 0,
    "Level" : 0,
    "Xp to next level" : 100,
    "Current xp to next level" : 0
}

shop_items = {
    "Woodmans axe" : 70,
    "Miners pickaxe" : 320,
    "Hunters bow" : 900,
    "Fighters sword" : 2500,
    "Fishermans rod" : 5300,
    "Jack of all trades" : 10000
}

try:
    with open("Game_data.txt") as score_file:
        items = json.load(score_file)
    with open("Player_data.txt") as player_file:
        player_attributes = json.load(player_file)
except:
    print("No file yet created")


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

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)


class BuyBox():
    def __init__(self, color, x, y, width, height, item_name_x, item_name_y, item_price_x, item_price_y, item_info_x, item_info_y):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.item_name_x = item_name_x
        self.item_name_y = item_name_y
        self.item_price_x = item_price_x
        self.item_price_y = item_price_y
        self.item_info_x = item_info_x
        self.item_info_y = item_info_y

    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

    def draw_item_name(self, screen, _item_name=""):
        font = pygame.font.Font(None, 50)
        text = font.render(_item_name, True, (WHITE))
        screen.blit(text, (self.item_name_x, self.item_name_y))

    def draw_item_price(self, screen, _item_price=""):
        font = pygame.font.Font(None, 50)
        text = font.render(_item_price, True, (WHITE))
        screen.blit(text, (self.item_price_x, self.item_price_y))

    def draw_item_info(self, screen, _item_info=""):
        font = pygame.font.Font(None, 30)
        text = font.render(_item_info, True, (WHITE))
        screen.blit(text, (self.item_info_x, self.item_info_y))


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

    player_attributes["Gold"] += item_price
    gold_display.draw_text(screen, f'Gold: {player_attributes["Gold"]}')
    item_amount -= item_amount
    item_price -= item_price

    return item_amount, item_price


# Declare stuff here for global variables
# Items and amounts

# Gold
gold_display = Gold((BLACK), 748, 600, 250, 115, 752, 637)

# Level
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
debug_item_button = InventoryButton((BLACK), 1000, 2, 278, 20, 1002, 4, 1150, 4, f'Debug Item: {items["Debug item"][0]}', f'Price: {items["Debug item"][1]}')
wood_item_button = InventoryButton((BLACK), 1000, 22, 278, 20, 1002, 24, 1150, 24, f'Wood: {items["Wood"][0]}', f'Price: {items["Wood"][1]}')
stone_item_button = InventoryButton((BLACK), 1000, 42, 278, 20, 1002, 44, 1150, 44, f'Stone: {items["Stone"][0]}', f'Price: {items["Stone"][1]}')
iron_item_button = InventoryButton((BLACK), 1000, 62, 278, 20, 1002, 64, 1150, 64, f'Iron: {items["Iron"][0]}', f'Price: {items["Iron"][1]}')
bear_flesh_item_button = InventoryButton((BLACK), 1000, 82, 278, 20, 1002, 84, 1150, 84, f'Bear Flesh: {items["Bear flesh"][0]}', f'Price: {items["Bear flesh"][1]}')
bear_skin_item_button = InventoryButton((BLACK), 1000, 102, 278, 20, 1002, 104, 1150, 104, f'Bear Skin: {items["Bear skin"][0]}', f'Price: {items["Bear skin"][1]}')
fish_item_button = InventoryButton((BLACK), 1000, 122, 278, 20, 1002, 124, 1150, 124, f'Fish: {items["Fish"][0]}', f'Price: {items["Wood"][1]}')
woodmans_axe_item_button = InventoryButton((BLACK), 1000, 142, 278, 20, 1002, 144, 1160, 144, f'Woodmans axe: {items["Woodmans axe"][0]}', f'Price: {items["Woodmans axe"][1]}')
miners_pickaxe_item_button = InventoryButton((BLACK), 1000, 162, 278, 20, 1002, 164, 1170, 164, f'Miners pickaxe: {items["Miners pickaxe"][0]}', f'Price: {items["Miners pickaxe"][1]}')
hunters_bow_item_button = InventoryButton((BLACK), 1000, 182, 278, 20, 1002, 184, 1150, 184, f'Hunters Bow: {items["Hunters bow"][0]}', f'Price: {items["Hunters bow"][1]}')
fighters_sword_item_button = InventoryButton((BLACK), 1000, 202, 278, 20, 1002, 204, 1170, 204, f'Fighters Sword: {items["Fighters sword"][0]}', f'Price: {items["Fighters sword"][1]}')
fishermans_rod_item_button = InventoryButton((BLACK), 1000, 222, 278, 20, 1002, 224, 1180, 224, f'Fishermans Rod: {items["Fishermans rod"][0]}', f'Price: {items["Fishermans rod"][1]}')
jack_of_all_trades_item_button = InventoryButton((BLACK), 1000, 242, 278, 20, 1002, 244, 1180, 244, f'Jack Of All Trades: {items["Jack of all trades"][0]}', f'Price: {items["Jack of all trades"][1]}')

clock = pygame.time.Clock()

# Custom quest events
TIMER = pygame.USEREVENT + 1

QUEST_1 = pygame.USEREVENT + 2
QUEST_2 = pygame.USEREVENT + 3
QUEST_3 = pygame.USEREVENT + 4
QUEST_4 = pygame.USEREVENT + 5

# player_attributes["Current xp to next level"] = player_attributes["Xp to next level"]

def run_game():
    screen.fill((BLACK))
    item_inventory_display.draw(screen, (CYAN))

    # Items and amounts
    global debug_item_amount
    global debug_item_price

    # Test buttons
    global quest_button
    global quest_button_2

    # Gold
    global gold_amount
    global gold_text

    # Level
    player_attributes["Current xp to next level"] = player_attributes["Xp to next level"]

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
    quest_1_timer_text = timer_font.render("10", True, (WHITE))

    quest_2_timer = 30
    quest_2_timer_text = timer_font.render("30", True, (WHITE))

    quest_3_timer = 60
    quest_3_timer_text = timer_font.render("60", True, (WHITE))

    quest_4_timer = 120
    quest_4_timer_text = timer_font.render("120", True, (WHITE))

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
                    with open ("Game_data.txt", "w") as score_file:
                        json.dump(items, score_file)
                    with open("Player_data.txt", "w") as player_file:
                        json.dump(player_attributes, player_file)

                    running = False
                    terminate()
            # User hit the cross in top rightcorner
            elif event.type == QUIT:
                with open("Game_data.txt", "w") as score_file:
                    json.dump(items, score_file)
                with open("Player_data.txt", "w") as player_file:
                    json.dump(player_attributes, player_file)
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
                        items["Wood"][0], items["Wood"][1] = quest_reward(rand_amount, items["Wood"][0], items["Wood"][1], 4, 6, 9)
                        rand_amount = 0
                        player_attributes["Xp to next level"] -= random.randint(15, 20)
                    else:
                        items["Wood"][0], items["Wood"][1] = quest_reward(rand_amount, items["Wood"][0], items["Wood"][1], 4, 3, 4)
                        rand_amount = 0
                        player_attributes["Xp to next level"] -= random.randint(12, 15)
                else:
                    items["Wood"][0], items["Wood"][1] = quest_reward(rand_amount, items["Wood"][0], items["Wood"][1], 4, 1, 3)
                    rand_amount = 0
                    player_attributes["Xp to next level"] -= random.randint(8, 12)

                pygame.time.set_timer(QUEST_1, 0)

                clicked = False
                print(items)
                quest_1_timer = 10
            elif event.type == QUEST_2:
                if miners_pickaxe_bought == True:
                    if jack_of_all_trades_bought == True:
                        items["Stone"][0], items["Stone"][1] = quest_reward(rand_amount, items["Stone"][0], items["Stone"][1], 2, 8, 12)
                        rand_amount = 0
                        items["Iron"][0], items["Iron"][1] = quest_reward(rand_amount, items["Iron"][0], items["Iron"][1], 8, 5, 7)
                        rand_amount = 0
                        player_attributes["Xp to next level"] -= random.randint(27, 34)
                    else:
                        items["Stone"][0], items["Stone"][1] = quest_reward(rand_amount, items["Stone"][0], items["Stone"][1], 2, 5, 8)
                        rand_amount = 0
                        items["Iron"][0], items["Iron"][1] = quest_reward(rand_amount, items["Iron"][0], items["Iron"][1], 3, 2, 4)
                        rand_amount = 0

                        player_attributes["Xp to next level"] -= random.randint(23, 27)
                else:
                    items["Stone"][0], items["Stone"][1] = quest_reward(rand_amount, items["Stone"][0], items["Stone"][1], 2, 2, 5)
                    rand_amount = 0
                    items["Iron"][0], items["Iron"][1] = quest_reward(rand_amount, items["Iron"][0], items["Iron"][1], 3, 1, 2)
                    rand_amount = 0

                    player_attributes["Xp to next level"] -= random.randint(16, 23)

                pygame.time.set_timer(QUEST_2, 0)

                clicked = False
                print(items)
                quest_2_timer = 30
            elif event.type == QUEST_3:
                if fighters_sword_bought == True:
                    if jack_of_all_trades_bought == True:
                        items["Bear flesh"][0], items["Bear flesh"][1] = quest_reward(rand_amount, items["Bear flesh"][0], items["Bear flesh"][1], 16, 4, 6)
                        rand_amount = 0
                        items["Bear skin"][0], items["Bear skin"][1] = quest_reward(rand_amount, items["Bear skin"][0], items["Bear skin"][1], 10, 4, 6)
                        rand_amount = 0
                        player_attributes["Xp to next level"] -= random.randint(43, 48)
                    else:
                        items["Bear flesh"][0], items["Bear flesh"][1] = quest_reward(rand_amount, items["Bear flesh"][0], items["Bear flesh"][1], 16, 2, 4)
                        rand_amount = 0
                        items["Bear skin"][0], items["Bear skin"][1] = quest_reward(rand_amount, items["Bear skin"][0], items["Bear skin"][1], 10, 2, 4)
                        rand_amount = 0

                        player_attributes["Xp to next level"] -= random.randint(36, 43)
                else:
                    items["Bear flesh"][0], items["Bear flesh"][1] = quest_reward(rand_amount, items["Bear flesh"][0], items["Bear flesh"][1], 16, 1, 2)
                    rand_amount = 0
                    items["Bear skin"][0], items["Bear skin"][1] = quest_reward(rand_amount, items["Bear skin"][0], items["Bear skin"][1], 10, 1, 2)
                    rand_amount = 0

                    player_attributes["Xp to next level"] -= random.randint(29, 36)

                pygame.time.set_timer(QUEST_3, 0)
                clicked = False
                print(items)
                quest_3_timer = 60
            elif event.type == QUEST_4:
                if fishermans_rod_bought == True:
                    if jack_of_all_trades_bought == True:
                        items["Fish"][0], items["Fish"][1] = quest_reward(rand_amount, items["Fish"][0], items["Fish"][1], 21, 6, 7)
                        rand_amount = 0

                        player_attributes["Xp to next level"] -= random.randint(61, 68)
                    else:
                        items["Fish"][0], items["Fish"][1] = quest_reward(rand_amount, items["Fish"][0], items["Fish"][1], 21, 3, 4)
                        rand_amount = 0

                        player_attributes["Xp to next level"] -= random.randint(54, 61)
                else:
                    items["Fish"][0], items["Fish"][1] = quest_reward(rand_amount, items["Fish"][0], items["Fish"][1], 21, 1, 2)
                    rand_amount = 0

                    player_attributes["Xp to next level"] -= random.randint(48, 54)

                pygame.time.set_timer(QUEST_4, 0)
                clicked = False
                print(items)
                quest_4_timer = 120

            # If mousebutton down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shop_button.is_over(mouse_pos):
                    running = False
                    shop()
                if quest_button.is_over(mouse_pos) and clicked == False:
                    clicked = True
                    if woodmans_axe_bought == True:
                        quest_1_timer -= 5
                        quest_1_timer_text = timer_font.render("05", True, (WHITE))

                        current_timer = quest_1_timer
                        current_timer_text = quest_1_timer_text

                        pygame.time.set_timer(QUEST_1, 5000)
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
                        quest_2_timer -= 15
                        quest_2_timer_text = timer_font.render("15", True, (WHITE))
                        current_timer = quest_2_timer
                        current_timer_text = quest_2_timer_text

                        pygame.time.set_timer(QUEST_2, 15000)
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
                        quest_3_timer -= 30
                        quest_3_timer_text = timer_font.render("30", True, (WHITE))
                        current_timer = quest_3_timer
                        current_timer_text = quest_3_timer_text

                        pygame.time.set_timer(QUEST_3, 30000)
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
                        quest_4_timer -= 60
                        quest_4_timer_text = timer_font.render("60", True, (WHITE))
                        current_timer = quest_4_timer
                        current_timer_text = quest_4_timer_text

                        pygame.time.set_timer(QUEST_4, 60000)
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
                        items["Wood"][0], items["Wood"][1] = sell_item(items["Wood"][0], items["Wood"][1])
                        sell_wood = False
                    elif sell_stone == True:
                        items["Stone"][0], items["Stone"][1] = sell_item(items["Stone"][0], items["Stone"][1])
                        sell_stone = False
                    elif sell_iron == True:
                        items["Iron"][0], items["Iron"][1] = sell_item(items["Iron"][0], items["Iron"][1])
                        sell_iron = False
                    elif sell_bear_flesh == True:
                        items["Bear flesh"][0], items["Bear flesh"][1] = sell_item(items["Bear flesh"][0], items["Bear flesh"][1])
                        sell_bear_flesh = False
                    elif sell_bear_skin == True:
                        items["Bear skin"][0], items["Bear skin"][1] = sell_item(items["Bear skin"][0], items["Bear skin"][1])
                        sell_bear_skin = False
                    elif sell_fish == True:
                        items["Fish"][0], items["Fish"][1] = sell_item(items["Fish"][0], items["Fish"][1])
                        sell_fish = False
                    elif sell_woodmans_axe == True:
                        items["Woodmans axe"][0], items["Woodmans axe"][1] = sell_item(items["Woodmans axe"][0], items["Woodmans axe"][1])
                        woodmans_axe_bought = False
                        sell_woodmans_axe = False
                    elif sell_miners_pickaxe == True:
                        items["Miners pickaxe"][0], items["Miners pickaxe"][1] = sell_item(items["Miners pickaxe"][0], items["Miners pickaxe"][1])
                        miners_pickaxe_bought = False
                        sell_miners_pickaxe = False
                    elif sell_hunters_bow == True:
                        items["Hunters bow"][0], items["Hunters bow"][1] = sell_item(items["Hunters bow"][0], items["Hunters bow"][1])
                        hunters_bow_bought = False
                        sell_hunters_bow = False
                    elif sell_fighters_sword == True:
                        items["Fighters sword"][0], items["Fighters sword"][1] = sell_item(items["Fighters sword"][0], items["Fighters sword"][1])
                        fighters_sword_bought = False
                        sell_fighters_sword = False
                    elif sell_fishermans_rod == True:
                        items["Fishermans rod"][0], items["Fishermans rod"][1] = sell_item(items["Fishermans rod"][0], items["Fishermans rod"][1])
                        fishermans_rod_bought = False
                        sell_fishermans_rod = False
                    elif sell_jack_of_all_trades == True:
                        items["Jack of all trades"][0], items["Jack of all trades"][1] = sell_item(items["Jack of all trades"][0], items["Jack of all trades"][1])
                        jack_of_all_trades_bought = False
                        sell_jack_of_all_trades = False
                    item_inventory_display.draw(screen, (CYAN))


                # Check if player pressed a button/text in the inventory
                if debug_item_button.is_over(mouse_pos) and items["Debug item"][0] >= 1:
                    draw_texts_to_item_display("Debug item", f'Price: {items["Debug item"][1]}')
                    sell_debug_item = True
                elif wood_item_button.is_over(mouse_pos) and items["Wood"][0] >= 1:
                    draw_texts_to_item_display("Wood", f'Price: {items["Wood"][1]}')
                    sell_wood = True
                elif stone_item_button.is_over(mouse_pos) and items["Stone"][0] >= 1:
                    draw_texts_to_item_display("Stone", f'Price: {items["Stone"][1]}')
                    sell_stone = True
                elif iron_item_button.is_over(mouse_pos) and items["Iron"][0] >= 1:
                    draw_texts_to_item_display("Iron", f'Price: {items["Iron"][1]}')
                    sell_iron = True
                elif bear_flesh_item_button.is_over(mouse_pos) and items["Bear flesh"][0] >= 1:
                    draw_texts_to_item_display("Bear Flesh", f'Price: {items["Bear flesh"][1]}')
                    sell_bear_flesh = True
                elif bear_skin_item_button.is_over(mouse_pos) and items["Bear skin"][0] >= 1:
                    draw_texts_to_item_display("Bear Skin", f'Price: {items["Bear skin"][1]}')
                    sell_bear_skin = True
                elif fish_item_button.is_over(mouse_pos) and items["Fish"][0] >= 1:
                    draw_texts_to_item_display("Fish", f'Price: {items["Fish"][1]}')
                    sell_fish = True
                elif woodmans_axe_item_button.is_over(mouse_pos) and items["Woodman's axe"][0] >= 1:
                    draw_texts_to_item_display("Woodman's Axe", f'Price: {items["Woodmans axe"][1]}')
                    sell_woodmans_axe = True
                elif miners_pickaxe_item_button.is_over(mouse_pos) and items["Miners pickaxe"][0] >= 1:
                    draw_texts_to_item_display("Miner's Pickaxe", f'Price: {items["Miners pickaxe"][1]}')
                    sell_miners_pickaxe = True
                elif hunters_bow_item_button.is_over(mouse_pos) and items["Hunters bow"][0] >= 1:
                    draw_texts_to_item_display("Hunter's Bow", f'Price: {items["Hunters bow"][1]}')
                    sell_hunters_bow = True
                elif fighters_sword_item_button.is_over(mouse_pos) and items["Fighters sword"][0] >= 1:
                    draw_texts_to_item_display("Fighter's Sword", f'Price: {items["Fighters sword"][1]}')
                    sell_fighters_sword = True
                elif fishermans_rod_item_button.is_over(mouse_pos) and items["Fishermans rod"][0] >= 1:
                    draw_texts_to_item_display("Fisherman's Rod", f'Price: {items["Fishermans rod"][1]}')
                    sell_fishermans_rod = True
                elif jack_of_all_trades_item_button.is_over(mouse_pos) and items["Jack of all trades"][0] >= 1:
                    draw_texts_to_item_display("Jack Of All Trades", f'Price: {items["Jack of all trades"][1]}')
                    sell_jack_of_all_trades = True

        if player_attributes["Xp to next level"] <= 0:
            player_attributes["Level"] += 1
            player_attributes["Current xp to next level"] += 100
            player_attributes["Xp to next level"] = player_attributes["Current xp to next level"]


        quest_button_2.draw(screen, (CYAN))
        if player_attributes["Level"] < 3:
            quest_button_2.draw_locked_text(screen)
        else:
            quest_button_2.draw_text(screen)

        quest_button_3.draw(screen, (CYAN))
        if player_attributes["Level"] < 5:
            quest_button_3.draw_locked_text(screen)
        else:
            quest_button_3.draw_text(screen)

        quest_button_4.draw(screen, (CYAN))
        if player_attributes["Level"] < 8:
            quest_button_4.draw_locked_text(screen)
        else:
            quest_button_4.draw_text(screen)


        # Draw inventory
        item_inventory.draw(screen,(CYAN))

        # Draw gold
        gold_display.draw(screen, (CYAN))
        gold_display.draw_text(screen, f'Gold: {player_attributes["Gold"]}')

        # Draw level
        level_display.draw(screen, (CYAN))
        level_display.draw_level_text(screen, f'Level: {player_attributes["Level"]}')
        level_display.draw_xp_text(screen, f'XP to next level: {player_attributes["Xp to next level"]}')


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
            screen.blit(quest_1_timer_text, (120, 15))
            screen.blit(quest_2_timer_text, (485, 15))
            screen.blit(quest_3_timer_text, (852, 15))
            screen.blit(quest_4_timer_text, (110, 195))
        else:
            screen.blit(current_timer_text, (840, 525))

        # Draw texts to inventory
        if items["Debug item"][0] >= 1:
            debug_item_button.draw_inventory_text(screen, f'Debug Item: {items["Debug item"][0]}', f'Price: {items["Debug item"][1]}')
        if items["Wood"][0] >= 1:
            wood_item_button.draw_inventory_text(screen, f'Wood: {items["Wood"][0]}', f'Price: {items["Wood"][1]}')
        if items["Stone"][0] >= 1:
            stone_item_button.draw_inventory_text(screen, f'Stone: {items["Stone"][0]}', f'Price: {items["Stone"][1]}')
        if items["Iron"][0] >= 1:
            iron_item_button.draw_inventory_text(screen, f'Iron: {items["Iron"][0]}', f'Price: {items["Iron"][1]}')
        if items["Bear flesh"][0] >= 1:
            bear_flesh_item_button.draw_inventory_text(screen, f'Bear Flesh: {items["Bear flesh"][0]}', f'Price: {items["Bear flesh"][1]}')
        if items["Bear skin"][0] >= 1:
            bear_skin_item_button.draw_inventory_text(screen, f'Bear Skin: {items["Bear skin"][0]}', f'Price: {items["Bear skin"][1]}')
        if items["Fish"][0] >= 1:
            fish_item_button.draw_inventory_text(screen, f'Fish: {items["Fish"][0]}', f'Price: {items["Fish"][1]}')
        if items["Woodmans axe"][0] >= 1:
            woodmans_axe_item_button.draw_inventory_text(screen, f'Woodmans Axe: {items["Woodmans axe"][0]}', f'Price: {items["Woodmans axe"][1]}')
        if items["Miners pickaxe"][0] >= 1:
            miners_pickaxe_item_button.draw_inventory_text(screen, f'Miners Pickaxe: {items["Miners pickaxe"][0]}', f'Price: {items["Miners pickaxe"][1]}')
        if items["Hunters bow"][0] >= 1:
            hunters_bow_item_button.draw_inventory_text(screen, f'Hunters Bow: {items["Hunters bow"][0]}', f'Price: {items["Hunters bow"][1]}')
        if items["Fighters sword"][0] >= 1:
            fighters_sword_item_button.draw_inventory_text(screen, f'Fighters Sword: {items["Fighters sword"][0]}', f'Price: {items["Fighters sword"][1]}')
        if items["Fishermans rod"][0] >= 1:
            fishermans_rod_item_button.draw_inventory_text(screen, f'Fishermans Rod: {items["Fishermans rod"][0]}', f'Price: {items["Fishermans rod"][1]}')
        if items["Jack of all trades"][0] >= 1:
            jack_of_all_trades_item_button.draw_inventory_text(screen, f'Jack Of All Trades: {items["Jack of all trades"][0]}', f'Price: {items["Jack of all trades"][1]}')

        # Update the display
        pygame.display.update()

        clock.tick(FPS)


def draw_buy_box(text_1, text_2, text_3):
    global buy_box_display
    global buy_button

    buy_box_display.draw(screen, (CYAN))
    buy_box_display.draw_item_name(screen, text_1)
    buy_box_display.draw_item_price(screen, text_2)
    buy_box_display.draw_item_info(screen, text_3)
    buy_button.draw(screen, (CYAN))
    buy_button.draw_text(screen)


# Cyan box around the screen
shop_box = Shop((BLACK), 2, 2, 1275, 712)

# Display gold in the shop
gold_display_shop = Gold((BLACK), 255, 600, 250, 115, 259, 637)

# Display shop inventory
shop_item_display = Inventory((BLACK), 2, 2, 503, 595)

# Buy box display
buy_box_display = BuyBox((BLACK), 530, 20, 725, 670, 540, 30, 1000, 30, 540, 90)

# Buy button on box display
buy_button = Button((BLACK), 760, 570, 250, 100, 40, "BUY", "LEVEL 10 REQUIRED")

# Display items in shop inventory
woodmans_axe = InventoryButton((BLACK), 2, 2, 500, 20, 4, 2, 20, 2, f'Woodmans Axe: {shop_items["Woodmans axe"]}')
miners_pickaxe = InventoryButton((BLACK), 2, 22, 500, 20, 4, 22, 20, 22, f'Miners Pickaxe: {shop_items["Miners pickaxe"]}')
hunters_bow = InventoryButton((BLACK), 2, 42, 500, 20, 4, 42, 20, 42, f'Hunters Bow: {shop_items["Hunters bow"]}')
fighters_sword = InventoryButton((BLACK), 2, 62, 500, 20, 4, 62, 20, 62, f'Fighters Sword: {shop_items["Fighters sword"]}')
fishermans_rod = InventoryButton((BLACK), 2, 82, 500, 20, 4, 82, 20, 82, f'Fishermans Rod: {shop_items["Fishermans rod"]}')
jack_of_all_trades = InventoryButton((BLACK), 2, 102, 500, 20, 4, 102, 20, 102, f'Jack Of All Trades: {shop_items["Jack of all trades"]}')

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
    woodmans_axe_clicked = False
    miners_pickaxe_clicked = False
    hunters_bow_clicked = False
    fighters_sword_clicked = False
    fishermans_rod_clicked = False
    jack_of_all_trades_clicked = False

    running = True
    rand_amount = 0

    global gold_amount
    global level

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

                if woodmans_axe.is_over(mouse_pos) and player_attributes["Gold"] >= 70:
                    woodmans_axe_clicked = True

                    miners_pickaxe_clicked = False
                    hunters_bow_clicked = False
                    fighters_sword_clicked = False
                    fishermans_rod_clicked = False
                    jack_of_all_trades_clicked = False
                if miners_pickaxe.is_over(mouse_pos) and player_attributes["Gold"] >= 320:
                    miners_pickaxe_clicked = True

                    woodmans_axe_clicked = False
                    hunters_bow_clicked = False
                    fighters_sword_clicked = False
                    fishermans_rod_clicked = False
                    jack_of_all_trades_clicked = False
                if hunters_bow.is_over(mouse_pos) and player_attributes["Gold"] >= 900:
                    hunters_bow_clicked = True

                    miners_pickaxe_clicked = False
                    woodmans_axe_clicked = False
                    fighters_sword_clicked = False
                    fishermans_rod_clicked = False
                    jack_of_all_trades_clicked = False
                if fighters_sword.is_over(mouse_pos) and player_attributes["Gold"] >= 2500:
                    fighters_sword_clicked = True

                    miners_pickaxe_clicked = False
                    hunters_bow_clicked = False
                    woodmans_axe_clicked = False
                    fishermans_rod_clicked = False
                    jack_of_all_trades_clicked = False
                if fishermans_rod.is_over(mouse_pos) and player_attributes["Gold"] >= 5300:
                    fishermans_rod_clicked = True

                    miners_pickaxe_clicked = False
                    hunters_bow_clicked = False
                    fighters_sword_clicked = False
                    woodmans_axe_clicked = False
                    jack_of_all_trades_clicked = False
                if jack_of_all_trades.is_over(mouse_pos) and player_attributes["Gold"] >= 10000:
                    jack_of_all_trades_clicked = True

                    miners_pickaxe_clicked = False
                    hunters_bow_clicked = False
                    fighters_sword_clicked = False
                    fishermans_rod_clicked = False
                    woodmans_axe_clicked = False

                if buy_button.is_over(mouse_pos):
                    if woodmans_axe_clicked == True:
                        player_attributes["Gold"] -= 70
                        items["Woodmans axe"][0], items["Woodmans axe"][1] = quest_reward(rand_amount, items["Woodmans axe"][0], items["Woodmans axe"][1], 40, 1, 1)
                        woodmans_axe_bought = True
                        rand_amount = 0
                        woodmans_axe_clicked = False
                    elif miners_pickaxe_clicked == True:
                        player_attributes["Gold"] -= 320
                        items["Miners pickaxe"][0], items["Miners pickaxe"][1] = quest_reward(rand_amount, items["Miners pickaxe"][0], items["Miners pickaxe"][1], 120, 1, 1)
                        miners_pickaxe_bought = True
                        rand_amount = 0
                        miners_pickaxe_clicked = False
                    elif hunters_bow_clicked == True:
                        player_attributes["Gold"] -= 900
                        items["Hunters bow"][0], items["Hunters bow"][1] = quest_reward(rand_amount, items["Hunters bow"][0], items["Hunters bow"][1], 720, 1, 1)
                        hunters_bow_bought = True
                        rand_amount = 0
                        hunters_bow_clicked = False
                    elif fighters_sword_clicked == True:
                        player_attributes["Gold"] -= 2500
                        items["Fighters sword"][0], items["Fighters sword"][1] = quest_reward(rand_amount, items["Fighters sword"][0], items["Fighters sword"][1], 1900, 1, 1)
                        fighters_sword_bought = True
                        rand_amount = 0
                        fighters_sword_clicked = False
                    elif fishermans_rod_clicked == True:
                        player_attributes["Gold"] -= 5300
                        items["Fishermans rod"][0], items["Fishermans rod"][1] = quest_reward(rand_amount, items["Fishermans rod"][0], items["Fishermans rod"][1], 4400, 1, 1)
                        fishermans_rod_bought = True
                        rand_amount = 0
                        fishermans_rod_clicked = False
                    elif jack_of_all_trades_clicked == True and level >= 10:
                        player_attributes["Gold"] -= 10000
                        items["Jack of all trades"][0], items["Jack of all trades"][1] = quest_reward(rand_amount, items["Jack of all trades"][0], items["Jack of all trades"][1], 8000, 1, 1)
                        jack_of_all_trades_bought = True
                        rand_amount = 0
                        jack_of_all_trades_clicked = False



        # Draw box around the shop
        shop_box.draw(screen, (CYAN))

        # Draw outlines for shop
        shop_item_display.draw(screen, (CYAN))

        if woodmans_axe_clicked == True:
            draw_buy_box("Woodmans Axe", f'Price: {shop_items["Woodmans axe"]}', "Reduces wood chopping time, get more wood and receive more xp")
        elif miners_pickaxe_clicked == True:
            draw_buy_box("Miners Pickaxe", f'Price: {shop_items["Miners pickaxe"]}', "Reduces mining time, get more ores and receive more xp")
        elif hunters_bow_clicked == True:
            draw_buy_box("Hunters Bow", f'Price: {shop_items["Hunters bow"]}', "Reduces hunting time")
        elif fighters_sword_clicked == True:
            draw_buy_box("Fighters Sword", f'Price: {shop_items["Fighters sword"]}', "Get more items when hunting and receive more xp")
        elif fishermans_rod_clicked == True:
            draw_buy_box("Fishermans Rod", f'Price: {shop_items["Fishermans rod"]}', "Reduces fishing time, get more fish and receive more xp")
        elif jack_of_all_trades_clicked == True and level >= 10:
            draw_buy_box("Jack Of All Trades", f'Price: {shop_items["Jack of all trades"]}', "Get more items from quest and receive more xp")
        elif jack_of_all_trades_clicked == True and level <= 10:
            buy_box_display.draw(screen, (CYAN))
            buy_box_display.draw_item_name(screen, "Jack Of All Trades")
            buy_box_display.draw_item_price(screen, f'Price: {shop_items["Jack of all trades"]}')
            buy_box_display.draw_item_info(screen, "Reduces all quest times and get more items")
            buy_button.draw(screen, (CYAN))
            buy_button.draw_locked_text(screen)



        # Draw items on screen
        woodmans_axe.draw(screen)
        woodmans_axe.draw_inventory_text(screen, f'Woodmans Axe : {shop_items["Woodmans axe"]} Gold')

        miners_pickaxe.draw(screen)
        miners_pickaxe.draw_inventory_text(screen, f'Miners Pickaxe : {shop_items["Miners pickaxe"]} Gold')

        hunters_bow.draw(screen)
        hunters_bow.draw_inventory_text(screen, f'Hunters Bow : {shop_items["Hunters bow"]} Gold')

        fighters_sword.draw(screen)
        fighters_sword.draw_inventory_text(screen, f'Fighters Sword : {shop_items["Fighters sword"]} Gold')

        fishermans_rod.draw(screen)
        fishermans_rod.draw_inventory_text(screen, f'Fishermans Rod : {shop_items["Fishermans rod"]} Gold')

        jack_of_all_trades.draw(screen)
        jack_of_all_trades.draw_inventory_text(screen, f'Jack Of All Trades : {shop_items["Jack of all trades"]} Gold')

        # Draw gold
        gold_display_shop.draw(screen, (CYAN))
        gold_display_shop.draw_text(screen, f'Gold: {player_attributes["Gold"]}')

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
