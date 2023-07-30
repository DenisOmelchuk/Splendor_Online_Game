import copy
import pygame
from network import Network
from _thread import *
pygame.font.init()
from pygame.locals import *
import time

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
scale_factor = 0.8
# win = pygame.display.set_mode((1920, 1080), pygame.SCALED)
pygame.display.set_caption("Client")
image_of_cards = None
players_turn_indexes = {
    0: None,
    1: None,
    2: None,
    3: None,
}


def setFontSize(font_size):
    font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", font_size * scale_factor)
    return font

class Button:
    def __init__(self, x , y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
    def test_draw(self):
        pygame.draw.rect(win, [255, 255, 255], pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.display.update()

class Buttons_With_Text(Button):
    def __init__(self, x, y, width, height, text):
        super(Buttons_With_Text, self).__init__(x, y, width, height)
        self.text = text


class Chip(Button):
    def __init__(self, x, y, width, height, count, color):
        super(Chip, self).__init__(x, y, width, height)
        self.count = str(count)
        self.color = color

    def drawChip(self, win):
        chip_counter_text_location_x = self.x + 12
        chip_counter_text_location_y = self.y - 5
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.count, 1, (0, 0, 0))
        win.blit(text, (chip_counter_text_location_x, chip_counter_text_location_y))

class ButtonWithBackground(Button):
    def __init__(self, x, y, width, height, text, color):
        super(ButtonWithBackground, self).__init__(x, y, width, height)
        self.color = color
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        if self.text != None:
            font = pygame.font.SysFont("comicsans", int(40 * scale_factor))
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                            self.y + round(self.height / 2) - round(text.get_height() / 2)))

class Card(Button):
    def __init__(self, x, y, width, height, column, card_color, score, level, pw, pr, pbr, pg, pbl, image, bg_color, row, price):
        super(Card, self).__init__(x, y, width, height)
        self.bg_color = bg_color
        self.column = column
        self.card_color = card_color
        self.score = score
        self.level = level
        # price for the card consumption
        # pw = price (white chip), pg = price (green chip), etc...
        self.pw = pw
        self.pr = pr
        self.pbr = pbr
        self.pg = pg
        self.pbl = pbl
        self.image = image
        self.row = row
        self.price = price


class PlayersAtributes(Button):
    def __init__(self, x, y, width, height, cards_count, chips_count, atribute_counter_location):
        super(PlayersAtributes, self).__init__(x, y, width, height)
        self.cards_count = cards_count
        self.chips_count = chips_count
        self.atribute_counter_location = int(atribute_counter_location * scale_factor)

    def drawAtributes(self, win, index):
        # font = pygame.font.SysFont("comicsans", 67)
        # pygame.draw.rect(win, (100, 255, 255), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", int(67 * scale_factor))
        self.chips_count += 1
        self.cards_count += 2
        if index == 4:
            font_color = (0, 0, 0)
        else:
            font_color = (255, 255, 255)
        if index < 5:
            if self.cards_count > 0:
                text1 = font.render(str(self.cards_count), 1, font_color)
                win.blit(text1, (self.atribute_counter_location, int(938 * scale_factor)))

        if self.chips_count > 0:
            text2 = font.render(str(self.chips_count), 1, font_color)
            if index < 5:
                win.blit(text2, (self.atribute_counter_location + int(68 * scale_factor), int(938 * scale_factor)))
            else:
                self.width = 66
                win.blit(text2, (self.atribute_counter_location - int(8 * scale_factor), int(938 * scale_factor)))
            self.chips_count -= 1


card_btn_background = ButtonWithBackground(None, None, 210.92, 335, None, None)

chips = [Chip(934, 30, 125, 125, None, "red"),
         Chip(934, 181, 125, 125, None, "brown"),
         Chip(934, 331, 125, 125, None, "green"),
         Chip(934, 477, 125, 125, None, "blue"),
         Chip(934, 620, 125, 125, None, "white"),
         Chip(934, 768, 125, 125, None, "golden"),
         ]

card_btns = {
    0: (Card(30 * scale_factor, 30 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 0, None, None, None, None, None, None, None, None, None, None, 0, None),
        Card(256 * scale_factor, 30 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 1, None, None, None, None, None, None, None, None, None, None, 0, None),
        Card(482 * scale_factor, 30 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 2, None, None, None, None, None, None, None, None, None, None, 0, None),
        Card(708 * scale_factor, 30 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 3, None, None, None, None, None, None, None, None, None, None, 0, None),
        ),
    1: (Card(30 * scale_factor, 380 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 0, None, None, None, None, None, None, None, None, None, None, 1, None),
        Card(256 * scale_factor, 380 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 1, None, None, None, None, None, None, None, None, None, None, 1, None),
        Card(482 * scale_factor, 380 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 2, None, None, None, None, None, None, None, None, None, None, 1, None),
        Card(708 * scale_factor, 380 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 3, None, None, None, None, None, None, None, None, None, None, 1, None),
        ),
    2: (Card(30 * scale_factor, 730 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 0, None, None, None, None, None, None, None, None, None, None, 2, None),
        Card(256 * scale_factor, 730 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 1, None, None, None, None, None, None, None, None, None, None, 2, None),
        Card(482 * scale_factor, 730 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 2, None, None, None, None, None, None, None, None, None, None, 2, None),
        Card(708 * scale_factor, 730 * scale_factor, 195.92 * scale_factor, 320 * scale_factor, 3, None, None, None, None, None, None, None, None, None, None, 2, None),
        ),
    "reserved": [Card(30, 730, 195.92, 320, 0, None, None, None, None, None, None, None, None, None, None, None, None)],
}

# random_card_rsrv_data = Card(None, None, 122, 200, None, None, None, None, None, None, None, None, None, None, None, None, None)

# client_player_reserved_cards_btns = (
#     Card(256, 380, 195.92, 320, 1, None, None, None, None, None, None, None, None, None, None, 1, None),
#     Card(482, 380, 195.92, 320, 2, None, None, None, None, None, None, None, None, None, None, 1, None),
#     Card(708, 380, 195.92, 320, 3, None, None, None, None, None, None, None, None, None, None, 1, None),
# )

random_cards_reservation_buttons = (
    Buttons_With_Text(1419, 165, 119, 72, "0"),
    Buttons_With_Text(1568, 165, 119, 72, "1"),
    Buttons_With_Text(1717, 165, 119, 72, "2"),
)


card_consumption_menu_options_buttons = (
    Buttons_With_Text(1240.25, 551, 161, 95, "Auto"),
    Buttons_With_Text(1450.5, 551, 161, 95, "Accept"),
    Buttons_With_Text(1660.75, 551, 161, 95, "Cancel"),
)

card_consumption_payment_buttons = (
    Buttons_With_Text(955, 935, 148.4, 95, "red"),
    Buttons_With_Text(1123.4, 935, 148.4, 95, "brown"),
    Buttons_With_Text(1292, 935, 148.4, 95, "green"),
    Buttons_With_Text(1461, 935, 148.4, 95, "blue"),
    Buttons_With_Text(1630, 935, 148.4, 95, "white"),
    Buttons_With_Text(1799, 935, 74.2, 95, "golden"),
)

chips_consumption_approval_buttons = (
    Buttons_With_Text(1385, 135, 208, 42, "Again"),
    Buttons_With_Text(1385, 197, 208, 42, "Okay"),
)

chips_buttons = (
    Buttons_With_Text(935, 30, 125, 125, "red"),
    Buttons_With_Text(935, 177.4, 125, 125, "brown"),
    Buttons_With_Text(935, 324.8, 125, 125, "green"),
    Buttons_With_Text(935, 472.2, 125, 125, "blue"),
    Buttons_With_Text(935, 619.6, 125, 125, "white"),
    Buttons_With_Text(935, 767, 125, 125, "golden"),
)

aristocrats_location = (30, 206, 382, 558, 734)

consumption_btns_location = ([166, 82], [166, 194], [247, 0])
consumption_btns = (ButtonWithBackground(consumption_btns_location[0][0], consumption_btns_location[0][1], 140, 93, "BUY", [128,128,128]),
                    ButtonWithBackground(consumption_btns_location[1][0], consumption_btns_location[1][1], 140, 93, "RSRV",[128,128,128]),
                    ButtonWithBackground(consumption_btns_location[2][0], consumption_btns_location[2][1], 59, 59, "EXIT", None)
                    )

chips_consumption_menu_buttons = (ButtonWithBackground(1385, 135, 208, 42, "Again", [255, 10, 10]),
                                  ButtonWithBackground(1385, 197, 208, 42, "Okay!", [58, 202, 7])
                                  )

list_of_all_the_buttons = [random_cards_reservation_buttons, card_consumption_menu_options_buttons, card_consumption_payment_buttons,
                           chips_consumption_approval_buttons, chips_buttons, consumption_btns, chips_consumption_menu_buttons]

def buttons_scale():
    for btns in list_of_all_the_buttons:
        for btn in btns:
            btn.x = btn.x * scale_factor
            btn.y = btn.y * scale_factor
            btn.height = btn.height * scale_factor
            btn.width = btn.width * scale_factor


players_atributes = (PlayersAtributes(955, 935, 148.4, 87, 1, 1, 983),
                     PlayersAtributes(1123.4, 935, 148.4, 87, 1, 1, 1148),
                     PlayersAtributes(1292, 935, 148.4, 87, 1, 1, 1317),
                     PlayersAtributes(1461, 935, 148.4, 87, 1, 1, 1486),
                     PlayersAtributes(1630, 935, 148.4, 87, 1, 1, 1651),
                     PlayersAtributes(1799, 935, 148.4, 87, 1, 1, 1821),
                     )
player_info_panel_location = ((1365, 288),
                              (1643, 288),
                              (1365, 488),
                              (1643, 488)
                              )

players_info_panel_atrubutes_images_cards = (
    ("images/splendor_info_panel_atributes/info_panel_redCard.png", "images/splendor_info_panel_atributes/info_panel_redCard_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_brownCard.png", "images/splendor_info_panel_atributes/info_panel_brownCard_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_greenCard.png", "images/splendor_info_panel_atributes/info_panel_greenCard_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_blueCard.png", "images/splendor_info_panel_atributes/info_panel_blueCard_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_whiteCard.png", "images/splendor_info_panel_atributes/info_panel_whiteCard_empty.png"),
    "images/splendor_info_panel_atributes/reserved_cards_icon.png"
)

players_info_panel_atrubutes_images_chips = (
    ("images/splendor_info_panel_atributes/info_panel_redChip.png", "images/splendor_info_panel_atributes/info_panel_redChip_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_brownChip.png", "images/splendor_info_panel_atributes/info_panel_brownChip_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_greenChip.png", "images/splendor_info_panel_atributes/info_panel_greenChip_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_blueChip.png", "images/splendor_info_panel_atributes/info_panel_blueChip_empty.png"),
    ("images/splendor_info_panel_atributes/info_panel_whiteChip.png", "images/splendor_info_panel_atributes/info_panel_whiteChip_empty.png"),
)


basic_game_objects = {
    "default_background.png": None,
    "card_consumption_menu_extended.png": None,
    "chips_consumption_approval.png": None,
    "card_consumption_menu.png": None,
    "info_panel_blueCard.png": None,
    "info_panel_blueCard_empty.png": None,
    "info_panel_blueChip.png": None,
    "info_panel_blueChip_empty.png": None,
    "info_panel_redCard.png": None,
    "info_panel_redCard_empty.png": None,
    "info_panel_redChip.png": None,
    "info_panel_redChip_empty.png": None,
    "info_panel_brownCard.png": None,
    "info_panel_brownCard_empty.png": None,
    "info_panel_brownChip.png": None,
    "info_panel_brownChip_empty.png": None,
    "info_panel_greenCard.png": None,
    "info_panel_greenCard_empty.png": None,
    "info_panel_greenChip.png": None,
    "info_panel_greenChip_empty.png": None,
    "info_panel_whiteCard.png": None,
    "info_panel_whiteCard_empty.png": None,
    "info_panel_whiteChip.png": None,
    "info_panel_whiteChip_empty.png": None,
    "reserved_cards_icon.png": None,
    "chips.png": None,
    "card_frame_green.png": None,
    "card_consumption_menu_green.png": None,
    "card_frame_red.png": None,
    "card_consumption_menu_red.png": None,
    "card_frame_blue.png": None,
    "card_consumption_menu_blue.png": None,
    "card_frame_white.png": None,
    "card_consumption_menu_white.png": None,
    "card_frame_brown.png": None,
    "card_consumption_menu_brown.png": None,
    "player_info_panel.png": None,
    "client_player_cards_and_chips_panel.png": None,
    "small_golden_chip.png": None,
    "card_price_identification_blue.png": None,
    "card_price_identification_red.png": None,
    "card_price_identification_green.png": None,
    "card_price_identification_brown.png": None,
    "card_price_identification_white.png": None,
    "chips_consumption_approval.png": None,
    "blue_chip.png": None,
    "red_chip.png": None,
    "brown_chip.png": None,
    "green_chip.png": None,
    "white_chip.png": None,
    "chips_consumption_approval_background.png": None,
    "client_player_reserved_cards_background.png": None,
    "aristocrats_background.png": None,
    "chips_give_away_panel_highlighted.png": None,
    "chips_to_give_away_info_panel.png": None,
    "random_cards_reservation_panel.png": None,
    "players_turn_info_panel.png": None,
    "your_turn_info_panel.png": None,
    }

def outOfChips(chips_amount):
    for chip in chips_amount.values():
        if chip != 0:
            return False
        else:
            return True


def blit_text(font_size, font_color, blited_value, x, y, card_or_chip_size):
    x = x * scale_factor
    y = y * scale_factor
    font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", int(font_size * scale_factor))
    text = font.render(str(blited_value), 1, font_color)
    if card_or_chip_size != None:
        win.blit(text, (x + round(int(card_or_chip_size[0] * scale_factor) / 2) - round(text.get_width() / 2),
                        y + round(int(card_or_chip_size[1] * scale_factor) / 2) - round(text.get_height() / 2)))
    else:
        win.blit(text, (x, y))


def draw_client_player_attributes(win, player_chips, player_cards, player_index, card_cons_menu_extended, is_highlighted, player_score):
    win.blit(basic_game_objects["client_player_cards_and_chips_panel.png"], (int(904 * scale_factor), int(scale_factor * 905)))
    font_color = [255, 255, 255]
    for index, (cards_type, cards_count) in enumerate(player_cards.items()):
    # for index, card_count in enumerate(cards_count):
        if cards_count > 0:
            if cards_type != "reserved":
                if cards_type == "white":
                    font_color = [0, 0, 0]
                blit_text(67, font_color, cards_count, 964 + 168.4 * index, 944, (73, 77))
        font_color = [255, 255, 255]
    # for index, chip_count in enumerate(chips_count):
    for index, (chips_type, chips_count) in enumerate(player_chips.items()):
        if chips_count > 0 or chips_type == "owned":
            x = 1040 + 168.4 * index
            if chips_type == "white":
                font_color = [0, 0, 0]
            elif chips_type == "golden":
                x = 1806
            elif chips_type == "owned":
                if not card_cons_menu_extended:
                    win.blit(basic_game_objects["player_info_panel.png"], (int(player_info_panel_location[player_index][0] * scale_factor),
                              int(player_info_panel_location[player_index][1] * scale_factor)))
                    owned_chips_counter = str(chips_count) + "/10"
                    blit_text(45, [0, 0, 0], owned_chips_counter, player_info_panel_location[player_index][0] + 129,
                              player_info_panel_location[player_index][1] + 92, None)
                    blit_text(28, [0, 0, 0], player_score, player_info_panel_location[player_index][0] + 54,
                              player_info_panel_location[player_index][1] + 49, None)
                    blit_text(22, [0, 0, 0], "ME", player_info_panel_location[player_index][0] + 20,
                              player_info_panel_location[player_index][1] + 19, (208, 27))
                    rectangle1 = pygame.Rect(int(player_info_panel_location[player_index][0] * scale_factor) + int(129 * scale_factor),
                              int(player_info_panel_location[player_index][1] + scale_factor) + int(92 + scale_factor), int(248 * scale_factor), int(170 * scale_factor))
                    pygame.display.update()
            blit_text(67, font_color, chips_count, x, 944, (61, 77))
    if is_highlighted:
        win.blit(basic_game_objects["chips_give_away_panel_highlighted.png"], (int(925 * scale_factor), int(905 * scale_factor)))
    rectangle = pygame.Rect(int(904 * scale_factor), int(905 * scale_factor), int(998 * scale_factor), int(155 * scale_factor))
    pygame.display.update(rectangle)


def draw_aristocrats(aristocrats_images):
    win.blit(basic_game_objects["aristocrats_background.png"], (int(1081 * scale_factor), int(30 * scale_factor)))
    for index, aristocrat_image in enumerate(aristocrats_images):
        win.blit(basic_game_objects[aristocrat_image], (int(1081 * scale_factor), int(aristocrats_location[index] * scale_factor)))
    rectangle = pygame.Rect(int(1081 * scale_factor), int(30 * scale_factor), int(231 * scale_factor), int(863 * scale_factor))
    pygame.display.update(rectangle)


def drawPlayersAtributes(win, player_index, player, game_data):
    # Blit info panel to the screen
    win.blit(basic_game_objects["player_info_panel.png"], (int(player_info_panel_location[player_index][0] * scale_factor),
                  int(player_info_panel_location[player_index][1] * scale_factor)))
    # Blit player's score
    blit_text(28, [0, 0, 0], game_data["playersScore"][player], player_info_panel_location[player_index][0] + 54,
              player_info_panel_location[player_index][1] + 49, None)
    blit_text(22,[0,0,0], game_data["players_names"][player], player_info_panel_location[player_index][0] + 20,
              player_info_panel_location[player_index][1] + 19, (208, 27))

    for index, (key, value) in enumerate(game_data["playersChips"][player].items()):
        # if key == "owned":
        #     owned_chips_counter = str(value) + "/10"
        #     blit_text(45, [0, 0, 0], owned_chips_counter, player_info_panel_location[player_index][0] + 129,
        #               player_info_panel_location[player_index][1] + 92, None)
        if key == "golden" and value > 0:
            x = player_info_panel_location[player_index][0] + 122
            y = player_info_panel_location[player_index][1] + 50
            x_scaled = int((player_info_panel_location[player_index][0] + 122) * scale_factor)
            y_scaled = int((player_info_panel_location[player_index][1] + 50) * scale_factor)
            image = basic_game_objects["small_golden_chip.png"]
            win.blit(image, (x_scaled, y_scaled))
            blit_text(28, [0, 0, 0], value, x + 28 + 8, player_info_panel_location[player_index][1] + 49, None)
        elif key != "golden" and key != "owned":
            x = player_info_panel_location[player_index][0] + 22 + 43 * index
            y = player_info_panel_location[player_index][1] + 131
            x_scaled = (player_info_panel_location[player_index][0] + 22 + 43 * index) * scale_factor
            y_scaled = (player_info_panel_location[player_index][1] + 131) * scale_factor
            image_dict_key = "info_panel_" + key + "Chip"
            if value > 0:
                image_dict_key += ".png"
            else:
                image_dict_key += "_empty.png"
            win.blit(basic_game_objects[image_dict_key], (x_scaled, y_scaled))
            if value > 0:
                font_color = [255, 255, 255]
                # index 4 means that chip is white, so I changed color of text to black
                if index == 4:
                    font_color = [0, 0, 0]
                blit_text(26, font_color, value, x, y, [32, 32])

    for index, (key, value) in enumerate(game_data["playersCards"][player].items()):
        if key == "reserved" and value > 0 and key != "owned":
            x = player_info_panel_location[player_index][0] + 185.57
            y = player_info_panel_location[player_index][1] + 52
            x_scaled = int((player_info_panel_location[player_index][0] + 185.57) * scale_factor)
            y_scaled = int((player_info_panel_location[player_index][1] + 52) * scale_factor)
            image = basic_game_objects["reserved_cards_icon.png"]
            win.blit(image, (x_scaled, y_scaled))
            blit_text(28, [0, 0, 0], value, x + 29 * scale_factor, player_info_panel_location[player_index][1] + 49, None)
        elif key != "reserved" and key != "owned":
            x = player_info_panel_location[player_index][0] + 20 + 43 * index
            y = player_info_panel_location[player_index][1] + 79
            x_scaled = int((player_info_panel_location[player_index][0] + 20 + 43 * index) * scale_factor)
            y_scaled = int((player_info_panel_location[player_index][1] + 79) * scale_factor)
            image_dict_key = "info_panel_" + key + "Card"
            if value > 0:
                image_dict_key += ".png"
            else:
                image_dict_key += "_empty.png"
            win.blit(basic_game_objects[image_dict_key], (x_scaled, y_scaled))
            if value > 0:
                font_color = [255, 255, 255]
                # index 4 means that card is white, so I changed color of text to black
                if index == 4:
                    font_color = [0, 0, 0]
                blit_text(28, font_color, value, x, y + 3 * scale_factor, [36, 47])
    rectangle345 = pygame.Rect(player_info_panel_location[player_index][0] * scale_factor,
                  player_info_panel_location[player_index][1] * scale_factor, 248 * scale_factor, 170 * scale_factor)
    pygame.display.update(rectangle345)

chips_counter_location = (
    (935, 30),
    (935, 177.4),
    (935, 324.8),
    (935, 472,2),
    (935, 619.6),
    (935, 767),
)

client_player_reserved_cards_location = (
    (1395, 687),
    (1566.7, 687),
    (1738.4, 687),
)


def draw_avaiable_chips_count(chips_count):
    chips_are_over = True
    win.blit(basic_game_objects["chips.png"], (int(904 * scale_factor), int(0 * scale_factor)))
    for index, chip_count in enumerate(chips_count.values()):
        # blit_text(67, font_color, chip_count, x, 944, (61, 77))
        if chips_are_over == True and chip_count > 0:
            chips_are_over = False
        blit_text(40, [0, 0, 0], chip_count, chips_counter_location[index][0], chips_counter_location[index][1], (50, 50))
    rectangle = pygame.Rect(int(904 * scale_factor), int(20 * scale_factor), int(156 * scale_factor), int(896 * scale_factor))
    pygame.display.update(rectangle)
    return chips_are_over


def save_cards_image():
    subsurface_rect = pygame.Rect(int(20 * scale_factor), int(20 * scale_factor), int(894 * scale_factor), int(1040 * scale_factor))
    subsurface = win.subsurface(subsurface_rect)

    # # CHIPS
    # # pygame.image.save(subsurface, "cards.png")
    # subsurface_rect1 = pygame.Rect(int(904 * scale_factor), int(905 * scale_factor), int(998 * scale_factor), int(155 * scale_factor))
    # subsurface1 = win.subsurface(subsurface_rect1)
    # pygame.image.save(subsurface1, "client_player_cards_and_chips_panel.png")

    pygame.image.save(subsurface, "cards.png")
    global image_of_cards
    image_of_cards = pygame.image.load("cards.png").convert_alpha()


def draw_card_and_load_atributes(new_card, row, column, random_reserved):
    card_btns[row][column].card_color = new_card[0]
    card_btns[row][column].score = new_card[1]
    card_btns[row][column].level = new_card[2]
    card_btns[row][column].pw = new_card[3]
    card_btns[row][column].pr = new_card[4]
    card_btns[row][column].pbr = new_card[5]
    card_btns[row][column].pg = new_card[6]
    card_btns[row][column].pbl = new_card[7]
    card_btns[row][column].x = card_btns[row][column].x
    card_btns[row][column].y = card_btns[row][column].y
    card_btns[row][column].width = card_btns[row][column].width
    card_btns[row][column].height = card_btns[row][column].height
    if not random_reserved:
        card_btns[row][column].image = pygame.transform.smoothscale(pygame.image.load(new_card[8]).convert_alpha(), (195.92 * scale_factor, 320 * scale_factor))
        win.blit(card_btns[row][column].image, (card_btns[row][column].x, card_btns[row][column].y))
    else:
        card_btns[row][column].image = pygame.transform.smoothscale(pygame.image.load(new_card[8]).convert_alpha(),
                                                                    (int(122 * scale_factor), int(200 * scale_factor)))



    # if card.card_color == 'green':
    #     card.bg_color = (0, 142, 64)
    # elif card.card_color == 'red':
    #     card.bg_color = (186, 40, 11)
    # elif card.card_color == 'blue':
    #     card.bg_color = (11, 81, 186)
    # elif card.card_color == 'brown':
    #     card.bg_color = (94, 61, 18)
    # elif card.card_color == 'white':
    #     card.bg_color = (232, 231, 230)


def load_and_draw_all_basic_game_objects(win, game_data, player_id):
    cards = game_data["cards"]
    for key, value in basic_game_objects.items():
        image_location = "images/basic_game_objects_images/" + str(key)
        basic_game_objects[key] = pygame.image.load(image_location).convert_alpha()
        if scale_factor != 1:
            scaled_width = basic_game_objects[key].get_width() * scale_factor
            scaled_height = basic_game_objects[key].get_height() * scale_factor
            basic_game_objects[key] = pygame.transform.smoothscale(basic_game_objects[key], (scaled_width, scaled_height))
    win.blit(basic_game_objects["default_background.png"], (0, 0))
    for aristoctar_image in game_data["aristocrats_images"]:
        if scale_factor == 1:
            basic_game_objects[aristoctar_image] = pygame.image.load(aristoctar_image).convert_alpha()
        else:
            basic_game_objects[aristoctar_image] = pygame.transform.smoothscale(pygame.image.load(aristoctar_image).convert_alpha(), ((int(231 * scale_factor), int(159 * scale_factor))))
    draw_aristocrats(game_data["aristocrats_images"])
    for row in range(3):
        for column in range(4):
            draw_card_and_load_atributes(cards[row][column], row, column, False)
    save_cards_image()
    draw_avaiable_chips_count(game_data["chipsAmount"])
    win.blit(basic_game_objects["random_cards_reservation_panel.png"], (int(1365 * scale_factor), int(115 * scale_factor)))
    for player_turn_index, player in enumerate(game_data["players_queue"]):
        if player != game_data["player_id"]:
            drawPlayersAtributes(win, player_turn_index, player, game_data)
        else:
            # chips_owned = [value for key, value in game_data["playersChips"][player].items()]
            # cards_owned = [value for key, value in game_data["playersCards"][player].items()][:5]
            draw_client_player_attributes(win, game_data["playersChips"][player], game_data["playersCards"][player],
                                          player_turn_index, False, False, game_data["playersScore"][player])
    buttons_scale()
    print_player_turn_to_move_name(game_data["players_names"],game_data["players_queue"][0], player_id)
    pygame.display.update()

test = (
    Button(None, None, None, None),
    Button(None, None, None, None),
    Button(None, None, None, None),
    Button(None, None, None, None),
)

def print_player_turn_to_move_name(players_names, player_to_move_index, client_player_index):
    if client_player_index == player_to_move_index:
        win.blit(basic_game_objects["your_turn_info_panel.png"], (1365 * scale_factor, 30 * scale_factor))
    else:
        win.blit(basic_game_objects["players_turn_info_panel.png"], (1365 * scale_factor, 30 * scale_factor))
        blited_value = players_names[player_to_move_index] + " TURN!"
        blit_text(32, [0, 0, 0], blited_value, 1365, 30, (526, 55))
    rectangle = pygame.Rect(int(1365 * scale_factor), int(30 * scale_factor), int(526 * scale_factor), int(55 * scale_factor))
    pygame.display.update(rectangle)

def redraw_whole_screen(game_data, player_id, aristocrats_images, client_player_reserved_cards):
    win.blit(basic_game_objects["default_background.png"], (0, 0))
    draw_avaiable_chips_count(game_data["chipsAmount"])
    draw_aristocrats(aristocrats_images)
    chips_consumption_approval_background()
    for player_turn_index, player in enumerate(game_data["players_queue"]):
        if player != player_id:
            # test[player_turn_index].x = player_info_panel_location[player_turn_index][0] * scale_factor
            # test[player_turn_index].y = player_info_panel_location[player_turn_index][1] * scale_factor
            # test[player_turn_index].width = 248 * scale_factor
            # test[player_turn_index].height = 170 * scale_factor
            # test[player_turn_index].test_draw()
            # print("1")
            drawPlayersAtributes(win, player_turn_index, player, game_data)
            # chips_owned = [value for key, value in game_data["playersChips"][player].items()]
            # cards_owned = [value for key, value in game_data["playersCards"][player].items()][:5]
        else:
            draw_client_player_attributes(win, game_data["playersChips"][player_id], game_data["playersCards"][player_id],
                                          player_turn_index, False, False, game_data["playersScore"][player_id])
    draw_client_player_reserved_cards(client_player_reserved_cards)
    win.blit(image_of_cards, (int(20 * scale_factor), int(20 * scale_factor)))
    print_player_turn_to_move_name(game_data["players_names"], game_data["player_id_turn_to_move"], player_id)
    pygame.display.update()

    #

cards_save = False
previous_mouse_position = None
previous_card = None
current_mouse_position = None
need_to_update = False

chips_approval_location = (
    (1627, 145),
    (1714, 145),
    (1801, 145),
)

def draw_chips_approval_panel_with_chips(collected_chips):
    for index, chip_color in enumerate(collected_chips):
        image_dict_key = str(chip_color) + "_chip.png"
        x = int(chips_approval_location[index][0] * scale_factor)
        y = int(chips_approval_location[index][1] * scale_factor)
        win.blit(basic_game_objects[image_dict_key], (x, y))
    rectangle = pygame.Rect(int(1365 * scale_factor), int(115 * scale_factor), int(526 * scale_factor), int(143 * scale_factor))
    pygame.display.update(rectangle)

def draw_card_consumption_menu(display):
    x = display["additional_data"].x - 10 * scale_factor
    y = display["additional_data"].y - 10 * scale_factor
    card_cons_menu_image = "card_consumption_menu_" + str(display["additional_data"].card_color) + ".png"
    win.blit(basic_game_objects[card_cons_menu_image], (x, y))
    rectangle = pygame.Rect(x, y, int(343 * scale_factor), int(340 * scale_factor))
    for index, btn in enumerate(consumption_btns):
        btn.x = scale_factor * consumption_btns_location[index][0] + display["additional_data"].x
        btn.y = scale_factor * consumption_btns_location[index][1] + display["additional_data"].y
    pygame.display.update(rectangle)

card_price_identification_buttons = (
    Buttons_With_Text(None, 308 * scale_factor, 161 * scale_factor, 95 * scale_factor, None),
    Buttons_With_Text(None, 308 * scale_factor, 161 * scale_factor, 95 * scale_factor, None),
    Buttons_With_Text(None, 308 * scale_factor, 161 * scale_factor, 95 * scale_factor, None),
    Buttons_With_Text(None, 308 * scale_factor, 161 * scale_factor, 95 * scale_factor, None),
)
active_card_price_identification_buttons_made = False
active_card_price_identification_buttons = []

def draw_cards_cons_extended_menu_payment_chips_count(chips_to_pay):
    global active_card_price_identification_buttons_made
    consumption_ended = True
    for index, (chip_color, chip_count) in enumerate(chips_to_pay.items()):
        image_dict_key = "card_price_identification_" + str(chip_color) + ".png"
        x = 1170.92 + 180.1 * index
        x_scaled = (1170.92 + 180.1 * index) * scale_factor
        win.blit(basic_game_objects[image_dict_key], (x_scaled, 308 * scale_factor))
        if chip_color == "white":
            font_color = [0, 0, 0]
        else:
            font_color = [255, 255, 255]
        blit_text(64, font_color, chip_count, x, 308, (161, 95))
        if not active_card_price_identification_buttons_made:
            card_price_identification_buttons[index].x = x * scale_factor
            card_price_identification_buttons[index].text = chip_color
            active_card_price_identification_buttons.append(card_price_identification_buttons[index])
        if consumption_ended == True and chip_count > 0:
            consumption_ended = False
    active_card_price_identification_buttons_made = True
    rectangle = pygame.Rect(1170.92 * scale_factor, 308 * scale_factor, 710 * scale_factor, 95 * scale_factor)
    pygame.display.update(rectangle)
    return consumption_ended

def draw_card_consumption_menu_extended(display, chips_to_pay):
    win.blit(basic_game_objects["card_consumption_menu_extended.png"], (935 * scale_factor, 288 * scale_factor))
    win.blit(display, (955 * scale_factor, 308 * scale_factor))
    rectangle = pygame.Rect(935 * scale_factor, 288 * scale_factor, 956 * scale_factor, 605 * scale_factor)
    pygame.display.update(rectangle)
    draw_cards_cons_extended_menu_payment_chips_count(chips_to_pay)


def draw_cards_image():
    win.blit(image_of_cards, (20 * scale_factor, 20 * scale_factor))
    rectangle = pygame.Rect(20 * scale_factor, 20 * scale_factor, 894 * scale_factor, 1040 * scale_factor)
    pygame.display.update(rectangle)

def chips_consumption_approval_background():
    win.blit(basic_game_objects["random_cards_reservation_panel.png"], (1365 * scale_factor, 115 * scale_factor))
    rectangle = pygame.Rect(1365 * scale_factor, 115 * scale_factor, 526 * scale_factor, 143 * scale_factor)
    pygame.display.update(rectangle)

def draw_client_player_reserved_cards(reserved_cards):
    for index, card in enumerate(reserved_cards):
        win.blit(card.image, (client_player_reserved_cards_location[index][0] * scale_factor, client_player_reserved_cards_location[index][1] * scale_factor))
    rectangle = pygame.Rect(1395 * scale_factor, 687 * scale_factor, 465 * scale_factor, 200 * scale_factor)
    pygame.display.update(rectangle)

def redrawWindow(win, game, player_id, display):
    global previous_mouse_position
    global current_mouse_position
    global need_to_update
    mouse = pygame.mouse.get_pos()
    rectangle = None
    cursor_is_on_card = False
    if display["mode"] == "Regular":
        for i in range(3):
            for btn in card_btns[i]:
                rect = pygame.Rect(btn.x - 10 * scale_factor, btn.y - 10 * scale_factor, btn.width + 20 * scale_factor, btn.height + 20 * scale_factor)
                # checking if cursor is on card button // returns True if it is
                if rect.collidepoint(mouse):
                    current_mouse_position = rect
                    cursor_is_on_card = True
                    if previous_mouse_position != current_mouse_position:
                        previous_mouse_position = current_mouse_position
                        card_frame = "card_frame_" + str(btn.card_color) + ".png"
                        win.blit(image_of_cards, (20 * scale_factor, 20 * scale_factor))
                        win.blit(basic_game_objects[card_frame], (btn.x - 10 * scale_factor, btn.y - 10 * scale_factor))
                        rectangle = pygame.Rect(20 * scale_factor, 20 * scale_factor, 894 * scale_factor, 1040 * scale_factor)
                        need_to_update = True
                        break
        if cursor_is_on_card == False and need_to_update == True:
            previous_mouse_position = None
            need_to_update = False
            win.blit(image_of_cards, (20 * scale_factor, 20 * scale_factor))
            rectangle = pygame.Rect(20 * scale_factor, 20 * scale_factor, 894 * scale_factor, 1040 * scale_factor)

    if rectangle is not None:
        pygame.display.update(rectangle)

    # else:
        # print("not")
    # update_rect = pygame.Rect(b[0] - 40, b[1] - 40, 400, 400)
    # # pygame.draw.rect(win, [255,255,255], (a[0], a[1], 25, 25))
    # pygame.draw.circle(win, (255, 255, 255), (a[0], a[1]), 30, 0)
    # pygame.display.update(update_rect)

def card_consumption_payment(chips_left_for_payment, client_player_owned_chips):
    client_player_payment = {
        "red": 0,
        "blue": 0,
        "green": 0,
        "white": 0,
        "brown": 0,
        "golden": 0,
    }
    # print("left", chips_left_for_payment)
    # print("owned", client_player_owned_chips)
    for chip_color, chips_count in chips_left_for_payment.items():
        difference_between_owned_chips_and_price = client_player_owned_chips[chip_color] - chips_count
        if difference_between_owned_chips_and_price > 0 or difference_between_owned_chips_and_price == 0:
            client_player_payment[chip_color] += chips_count
        elif difference_between_owned_chips_and_price < 0:
            client_player_payment[chip_color] += client_player_owned_chips[chip_color]
            client_player_payment["golden"] += abs(difference_between_owned_chips_and_price)
    return client_player_payment

def check_card_cunsumption_availability(card_price, player_id_chips, player_id_cards, golden_chips_avaiable):
    card_consumption_availability = {
        "reservation": True,
        "consumption": True,
        "chips_left_to_pay_for_card_consmp": None
    }
    total_missing_chips = 0
    chips_left_to_pay_for_card_consmp = {
        "white": None,
        "red": None,
        "brown": None,
        "green": None,
        "blue": None,
    }

    chips_that_not_presented_in_price = []
    for index, chip_color in enumerate(chips_left_to_pay_for_card_consmp.keys()):
        if card_price[index] == 0:
            chips_that_not_presented_in_price.append(str(chip_color))
        else:
            if card_price[index] - player_id_cards[chip_color] > 0:
                chips_left_to_pay_for_card_consmp[chip_color] = card_price[index] - player_id_cards[chip_color]
                missing_chips = chips_left_to_pay_for_card_consmp[chip_color] - player_id_chips[chip_color]
                if missing_chips > 0:
                    total_missing_chips += missing_chips
            else:
                chips_that_not_presented_in_price.append(str(chip_color))
    if total_missing_chips > player_id_chips["golden"]:
        card_consumption_availability["consumption"] = False
    else:
        card_consumption_availability["chips_left_to_pay_for_card_consmp"] = chips_left_to_pay_for_card_consmp
    if player_id_cards["reserved"] >= 3 or golden_chips_avaiable == 0:
        card_consumption_availability["reservation"] = False
    for chip_color in chips_that_not_presented_in_price:
        chips_left_to_pay_for_card_consmp.pop(chip_color)
    return card_consumption_availability





def main():
    pygame.init()
    run = True
    clock = pygame.time.Clock()
    n = Network()
    load_game_data = n.getPlayerIdAndCards()
    # if load_game_data["password"] != "BrngFUrwZmLfYYS":
    #     pass
    current_player_move = 0
    collected_chips = []
    chip_duplicated = False
    chip_consumption_allowed = True
    card_cunsumption_availability = {
        "reservation": None,
        "consumption": None,
        "chips_left_for_payment": None,
    }
    # DO IT IN SERVER
    for player_turn_index, player in enumerate(load_game_data["players_queue"]):
        players_turn_indexes[player] = player_turn_index
    player_id = load_game_data["player_id"]
    display= {
        "mode": "Players_Name_Entry",
        "additional_data": None
    }
    data_send_to_server = {
        "player_id": player_id,
        "action_type": None,
        "action_data": None
    }
    # choosed_card_info = {
    #     "image": None,
    #     "x": None,
    #     "y": None,
    #     "score": None,
    #     "card_color": None,
    #     "row": None,
    #     "column": None,
    # }
    choosed_card_info = None
    excess_chips_count = None
    reserved_card_consumption = False
    client_player_reserved_cards = []
    card_atributes_update_required = True
    chips_count_update_required = True
    # a = [0, 0]
    # b = [0, 0]
    client_player_random_card_reservation = False
    client_player_chips_payment_visualization = None
    client_player_cards_payment_visualization = None
    chips_give_away_while_card_reservation = False
    avaiable_chips_count_visualization = {}
    avaiable_chips_count_visualization_assigned = False
    client_player_payed_chips = {}
    collected_chips = []
    chips_to_give_away = []
    player_index_turn_to_move = 0
    player_id_turn_to_move = load_game_data["players_queue"][0]
    clicked = 0
    consumption_ended = False
    name_entrance_panel = pygame.transform.smoothscale(pygame.image.load("images/basic_game_objects_images/enter_your_name_panel.png").convert_alpha(),
                                 (1920 * scale_factor, 1080 * scale_factor))
    win.blit(name_entrance_panel, (0, 0))
    pygame.display.update()
    user_text = ""
    name_entered = False
    reserved_card_object_to_remove = None
    this_time = False
    players_names = {
        1: '1',
        2: '2',
        3: '3',
        4: '4'
    }
    all_names_changed = False
    names_changed_count = 0
    while run:
        clock.tick(60)
        # for i in range(2):
            # a[0] += 60
            # a[1] += 60
            # b[0] += 60
            # b[1] += 60

        # pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        try:
            # data = n.send("get")
            game_data = n.send("get")
            chips_count = [
                game_data["chipsAmount"]["red"],
                game_data["chipsAmount"]["brown"],
                game_data["chipsAmount"]["green"],
                game_data["chipsAmount"]["blue"],
                game_data["chipsAmount"]["white"],
                game_data["chipsAmount"]["golden"],
            ]
        except:
            run = False
            print("Couldn't get game")
            break

        # if card_atributes_update_required == True:
        #     load_card_atributes(game)
        #     card_atributes_update_required = False

        if name_entered == True:
            if not all_names_changed:
                for player_turn_index, player in enumerate(game_data["players_queue"]):
                    if player != player_id:
                        drawPlayersAtributes(win, player_turn_index, player, game_data)
                        names_changed_count += 1
                    if names_changed_count == 3:
                        all_names_changed = True
            if game_data["player_id_turn_to_move"] != player_id_turn_to_move:
                if game_data["game_changes"]["change_type"] == "victory":
                    win.fill((51, 51, 51))
                    winner_player_index = game_data["game_changes"]["change_data"]
                    blit_text(64, (255, 184, 3), game_data["players_names"][winner_player_index], 0, 0, (1920, 1080))
                    pygame.display.update()
                if player_id_turn_to_move != player_id:
                    drawPlayersAtributes(win, players_turn_indexes[player_id_turn_to_move], player_id_turn_to_move, game_data)
                else:
                    draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                  game_data["playersCards"][player_id],
                                                  players_turn_indexes[player_id],
                                                  False, False, game_data["playersScore"][player_id])
                if this_time:
                    print_player_turn_to_move_name(game_data["players_names"], game_data["player_id_turn_to_move"], player_id)
                this_time = True
                player_id_turn_to_move = game_data["player_id_turn_to_move"]
                if game_data["game_changes"]["change_type"] == "card_consumption" or game_data["game_changes"]["change_type"] == "card_reservation":
                    if game_data["game_changes"]["change_type"] == "card_consumption" and game_data["game_changes"]["change_data"] != "reserved_card":
                        new_card = game_data["game_changes"]["change_data"]["new_card"]
                        row = game_data["game_changes"]["change_data"]["row"]
                        column = game_data["game_changes"]["change_data"]["column"]
                        # win.blit(image_of_cards, (20, 20))
                        redraw_whole_screen(game_data, player_id, load_game_data["aristocrats_images"], client_player_reserved_cards)
                        draw_card_and_load_atributes(new_card, row, column, False)
                        # draw_avaiable_fchips_count(game_data["chipsAmount"])
                        # rectangle = pygame.Rect(20, 20, 894, 1040)
                        # pygame.display.update(rectangle)
                        pygame.display.update()
                        save_cards_image()
                    elif game_data["game_changes"]["change_type"] == "card_reservation":
                        new_card = game_data["game_changes"]["change_data"]["new_card"]
                        row = game_data["game_changes"]["change_data"]["row"]
                        column = game_data["game_changes"]["change_data"]["column"]
                        win.blit(image_of_cards, (20 * scale_factor, 20 * scale_factor))
                        draw_card_and_load_atributes(new_card, row, column, False)
                        draw_avaiable_chips_count(game_data["chipsAmount"])
                        rectangle = pygame.Rect(20 * scale_factor, 20 * scale_factor, 894 * scale_factor, 1040 * scale_factor)
                        pygame.display.update(rectangle)
                        draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                      game_data["playersCards"][player_id],
                                                      players_turn_indexes[player_id],
                                                      False, False, game_data["playersScore"][player_id])
                        save_cards_image()

                    else:
                        redraw_whole_screen(game_data, player_id, load_game_data["aristocrats_images"], client_player_reserved_cards)
                        # draw_avaiable_chips_count(game_data["chipsAmount"])
                        # if player_id != game_data["game_changes"]["player"]:
                        #     drawPlayersAtributes(win, players_turn_indexes[player_id_turn_to_move], player_id_turn_to_move,
                        #                      game_data)
                elif game_data["game_changes"]["change_type"] == "chips_consumption":
                    draw_avaiable_chips_count(game_data["chipsAmount"])
                    if player_id != game_data["game_changes"]["player"]:
                        drawPlayersAtributes(win, players_turn_indexes[player_id_turn_to_move], player_id_turn_to_move,
                                         game_data)


                elif game_data["game_changes"]["change_type"] == "random_card_reservation" and client_player_random_card_reservation:
                    draw_card_and_load_atributes(game_data["game_changes"]["change_data"]["new_card"], "reserved", 0, True)
                    choosed_card_info = copy.copy(card_btns["reserved"][0])
                    choosed_card_info.image = pygame.transform.scale(choosed_card_info.image,
                                                                     (122 * scale_factor, 199.27 * scale_factor))
                    reserved_card_location_dict_index = len(client_player_reserved_cards)
                    choosed_card_info.x = \
                        client_player_reserved_cards_location[reserved_card_location_dict_index][0] * scale_factor
                    choosed_card_info.y = \
                        client_player_reserved_cards_location[reserved_card_location_dict_index][1] * scale_factor
                    choosed_card_info.width = 122 * scale_factor
                    choosed_card_info.height = 199 * scale_factor
                    client_player_reserved_cards.append(copy.copy(choosed_card_info))
                    draw_client_player_reserved_cards(client_player_reserved_cards)
                    display["mode"] = "Regular"
                    draw_cards_image()
                    draw_avaiable_chips_count(game_data["chipsAmount"])
                    draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                  game_data["playersCards"][player_id],
                                                  players_turn_indexes[player_id],
                                                  False, False,
                                                  game_data["playersScore"][player_id])
                    client_player_random_card_reservation = False




            if display["mode"] == "Regular":
                chips_count_visualizer = {
                    "red": chips_count[0],
                    "brown": chips_count[1],
                    "green": chips_count[2],
                    "blue": chips_count[3],
                    "white": chips_count[4],
                    "golden": chips_count[5],
                }
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    pygame.quit()
            if display["mode"] == "Players_Name_Entry":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(user_text) > 0:
                            user_text = user_text[:-1]
                            win.blit(name_entrance_panel, (0, 0))
                            blit_text(64, [255, 184, 3], user_text.upper(), 863, 557, (194, 77))
                            pygame.display.update()
                    elif event.key == pygame.K_RETURN:
                        display["mode"] = "Regular"
                        data_send_to_server["action_type"] = "players_name_entry"
                        data_send_to_server["action_data"] = user_text
                        n.send(data_send_to_server)
                        name_entered = True
                        load_and_draw_all_basic_game_objects(win, load_game_data, player_id)
                        data_send_to_server["action_data"] = {}
                    else:
                        user_text += event.unicode
                        win.blit(name_entrance_panel, (0, 0))
                        blit_text(64, [255, 184, 3], user_text.upper(), 863, 557, (194, 77))
                        pygame.display.update()



            # if current_player_move == p:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if name_entered == True:
                    pos = pygame.mouse.get_pos()

                    if display["mode"] == "Card_Consumption_Menu":
                        for btn in consumption_btns:
                            if btn.click(pos):
                                # if card_cunsumption_availability["consumption"]:
                                if btn.text == "EXIT":
                                    display["mode"] = "Regular"
                                    if choosed_card_info.column == 3:
                                        draw_avaiable_chips_count(game_data["chipsAmount"])
                                        # chips_owned = [value for key, value in game_data["playersChips"][player_id].items()]
                                        # cards_owned = [value for key, value in game_data["playersCards"][player_id].items()][:5]
                                        draw_client_player_attributes(win, game_data["playersChips"][player_id], game_data["playersCards"][player_id], players_turn_indexes[player_id],
                                                                      False, False, game_data["playersScore"][player_id])
                                elif btn.text == "BUY":
                                    if card_cunsumption_availability["consumption"]:
                                    # if checkPlayerConsumption(player, choosed_card_info, game, btn.text)
                                        if game_data["playersChips"][player_id]["golden"] > 0:
                                            display["mode"] = "Card_Consumption_Menu_Extended"
                                            display["additional_data"] = choosed_card_info.image # choosed_card_info["price"],
                                            client_player_chips_payment_visualization = game_data["playersChips"][player_id]
                                            client_player_cards_payment_visualization = game_data["playersCards"][player_id]
                                            draw_cards_image()
                                            draw_avaiable_chips_count(game_data["chipsAmount"])
                                            draw_card_consumption_menu_extended(display["additional_data"],
                                                                                card_cunsumption_availability[
                                                                                    "chips_left_for_payment"])
                                        else:
                                            # client_player_chips_payment = card_consumption_payment(
                                            #     card_cunsumption_availability["chips_left_for_payment"],
                                            #     game_data["playersChips"][player])
                                            client_player_payed_chips = card_consumption_payment(
                                                card_cunsumption_availability["chips_left_for_payment"],
                                                game_data["playersChips"][player_id])
                                            # data_send_to_server["action_type"] = "card_consumption"
                                            # data_send_to_server["action_data"] = choosed_card_info
                                            # n.send(data_send_to_server)
                                            display["mode"]= "Regular"
                                            if choosed_card_info.column == 3:
                                                draw_avaiable_chips_count(game_data["chipsAmount"])

                                            card_consumption_menu_parameters = False
                                            data_send_to_server["action_type"] = "Card_Consumption"
                                            data_send_to_server["action_data"] = {
                                                "row": choosed_card_info.row,
                                                "column": choosed_card_info.column,
                                                "score": choosed_card_info.score,
                                                "card_color": choosed_card_info.card_color,
                                                "payed_chips": client_player_payed_chips,
                                                "card_was_reservated": False,
                                            }
                                            n.send(data_send_to_server)
                                elif btn.text == "RSRV":
                                    if len(client_player_reserved_cards) < 3 and game_data["chipsAmount"]["golden"] > 0:
                                        choosed_card_info.image = pygame.transform.scale(choosed_card_info.image, (122 * scale_factor, 199.27 * scale_factor))
                                        reserved_card_location_dict_index = len(client_player_reserved_cards)
                                        choosed_card_info.x = client_player_reserved_cards_location[reserved_card_location_dict_index][0] * scale_factor
                                        choosed_card_info.y = client_player_reserved_cards_location[reserved_card_location_dict_index][1] * scale_factor
                                        choosed_card_info.width = 122 * scale_factor
                                        choosed_card_info.height = 199 * scale_factor
                                        client_player_reserved_cards.append(copy.copy(choosed_card_info))
                                        draw_client_player_reserved_cards(client_player_reserved_cards)
                                        display["mode"] = "Regular"
                                        draw_cards_image()
                                        draw_avaiable_chips_count(game_data["chipsAmount"])
                                        draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                                      game_data["playersCards"][player_id],
                                                                      players_turn_indexes[player_id],
                                                                      False, False, game_data["playersScore"][player_id])
                                        data_send_to_server["action_type"] = "Card_Reservation"
                                        data_send_to_server["action_data"] = {
                                            "row": choosed_card_info.row,
                                            "column": choosed_card_info.column,
                                            "random": False,
                                            "chips_to_give_away": None
                                        }
                                        excess_chips_count = 1 + game_data["playersChips"][player_id]["owned"] - 10
                                        if excess_chips_count <= 0:
                                            n.send(data_send_to_server)
                                        else:
                                            display["mode"] = "Chips_Give_Away"
                                            win.blit(basic_game_objects["chips_to_give_away_info_panel.png"],
                                                     (1365 * scale_factor, 30 * scale_factor))
                                            win.blit(basic_game_objects["chips_give_away_panel_highlighted.png"],
                                                     (925 * scale_factor, 905 * scale_factor))
                                            rectangle = pygame.Rect(1365 * scale_factor, 30 * scale_factor,
                                                                    526 * scale_factor, 55 * scale_factor)
                                            pygame.display.update(rectangle)
                                            win.blit(basic_game_objects["chips_consumption_approval.png"],
                                                     (1365 * scale_factor, 115 * scale_factor))
                                            chips_left_to_give_away = len(chips_to_give_away)
                                            chips_left_to_give_away_text = str(chips_left_to_give_away) + "/" + str(
                                                excess_chips_count)
                                            blit_text(32, [0, 0, 0], chips_left_to_give_away_text,
                                                      1826, 215, None)
                                            draw_chips_approval_panel_with_chips(chips_to_give_away)
                                            draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                                          game_data["playersCards"][player_id],
                                                                          players_turn_indexes[player_id], False, True,
                                                                          game_data["playersScore"][player_id])
                                            chips_give_away_while_card_reservation = True


                    else:
                        if display["mode"] == "Card_Consumption_Menu_Extended_Golden_Chip":
                            for price_btn in active_card_price_identification_buttons:
                                if price_btn.click(pos):
                                    if card_cunsumption_availability["chips_left_for_payment"][price_btn.text] > 0:
                                        card_cunsumption_availability["chips_left_for_payment"][price_btn.text] -= 1
                                        client_player_chips_payment_visualization["golden"] -= 1
                                        consumption_ended = draw_cards_cons_extended_menu_payment_chips_count(
                                            card_cunsumption_availability["chips_left_for_payment"])
                                        draw_client_player_attributes(win,
                                                                      client_player_chips_payment_visualization,
                                                                      game_data["playersCards"][player_id],
                                                                      players_turn_indexes[player_id], True, False,
                                                                      game_data["playersScore"][player_id])
                                        display["mode"] = "Card_Consumption_Menu_Extended"



                        elif display["mode"] == "Card_Consumption_Menu_Extended":
                            for btn in card_consumption_payment_buttons:
                                if btn.click(pos):
                                    if btn.text == "golden" and client_player_chips_payment_visualization[btn.text] > 0:
                                    # if btn.text == "golden":
                                        display["mode"] = "Card_Consumption_Menu_Extended_Golden_Chip"
                                        if btn.text not in client_player_payed_chips:
                                            client_player_payed_chips[btn.text] = 0
                                        client_player_payed_chips[btn.text] += 1
                                    elif btn.text in card_cunsumption_availability["chips_left_for_payment"] \
                                            and client_player_chips_payment_visualization[btn.text] > 0:
                                        if card_cunsumption_availability["chips_left_for_payment"][btn.text] > 0:
                                            if btn.text not in client_player_payed_chips:
                                                client_player_payed_chips[btn.text] = 0
                                            client_player_payed_chips[btn.text] += 1
                                            card_cunsumption_availability["chips_left_for_payment"][btn.text] -= 1
                                            client_player_chips_payment_visualization[btn.text] -= 1
                                            consumption_ended = draw_cards_cons_extended_menu_payment_chips_count(card_cunsumption_availability["chips_left_for_payment"])
                                            draw_client_player_attributes(win, client_player_chips_payment_visualization,
                                                                          game_data["playersCards"][player_id],
                                                                          players_turn_indexes[player_id], True, False,
                                                                          game_data["playersScore"][player_id])


                            for btn in card_consumption_menu_options_buttons:
                                if btn.click(pos):
                                    if btn.text == "Accept" and consumption_ended == True or btn.text == "Auto":
                                        if btn.text == "Auto":
                                            client_player_payed_chips = card_consumption_payment(
                                                card_cunsumption_availability["chips_left_for_payment"],
                                                game_data["playersChips"][player_id])
                                        data_send_to_server["action_type"] = "Card_Consumption"
                                        data_send_to_server["action_data"] = {
                                            "row": choosed_card_info.row,
                                            "column": choosed_card_info.column,
                                            "score": choosed_card_info.score,
                                            "card_color": choosed_card_info.card_color,
                                            "payed_chips": client_player_payed_chips,
                                            "card_was_reservated": reserved_card_consumption,
                                        }
                                        if reserved_card_consumption:
                                            reserved_cards_count = len(client_player_reserved_cards)
                                            client_player_reserved_cards.remove(reserved_card_object_to_remove)
                                            if reserved_cards_count > 0:
                                                for count, reserved_card in enumerate(client_player_reserved_cards):
                                                    reserved_card.x = client_player_reserved_cards_location[count][0] * scale_factor
                                            data_send_to_server["action_data"] = {
                                                "row": reserved_card_object_to_remove.row,
                                                "column": reserved_card_object_to_remove.column,
                                                "score": reserved_card_object_to_remove.score,
                                                "card_color": reserved_card_object_to_remove.card_color,
                                                "payed_chips": client_player_payed_chips,
                                                "card_was_reservated": reserved_card_consumption
                                            }


                                        n.send(data_send_to_server)
                                        reserved_card_consumption = False
                                        display["mode"] = "Regular"
                                    if btn.text == "Cancel":
                                        display["mode"] = "Regular"
                                        redraw_whole_screen(game_data, player_id, load_game_data["aristocrats_images"], client_player_reserved_cards)

                        elif display["mode"] == "Chips_Give_Away":
                            for btn in card_consumption_payment_buttons:
                                if btn.click(pos):
                                    if game_data["playersChips"][player_id][btn.text] > 0:
                                        chips_to_give_away.append(btn.text)
                                        chips_left_to_give_away = len(chips_to_give_away)
                                        chips_left_to_give_away_text = str(chips_left_to_give_away) + "/" + str(
                                            excess_chips_count)
                                        win.blit(basic_game_objects["chips_consumption_approval.png"], (1365 * scale_factor, 115 * scale_factor))
                                        blit_text(32, [0, 0, 0], chips_left_to_give_away_text,
                                                  1826, 215, None)
                                        draw_chips_approval_panel_with_chips(chips_to_give_away)
                                        if len(chips_to_give_away) == excess_chips_count:
                                            display["mode"] = "Chips_Give_Away_Approval"
                                            break

                        elif display["mode"] == "Chips_Give_Away_Approval":
                            for apr_btn in chips_consumption_approval_buttons:
                                if apr_btn.click(pos):
                                    display["mode"] = "Regular"
                                    if apr_btn.text == "Okay":
                                        if chips_give_away_while_card_reservation:
                                            data_send_to_server["action_data"]["chips_to_give_away"] = chips_to_give_away
                                            data_send_to_server["action_type"] = "Card_Reservation"
                                            chips_give_away_while_card_reservation = False
                                        else:
                                            data_send_to_server["action_type"] = "Chips_Consumption"
                                            data_send_to_server["action_data"]["chips_to_give_away"] = chips_to_give_away
                                            data_send_to_server["action_data"]["collected_chips"] = collected_chips
                                        game_data = n.send(data_send_to_server)
                                        chips_to_give_away.clear()
                                        draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                                      game_data["playersCards"][player_id],
                                                                      players_turn_indexes[player_id], False, False,
                                                                      game_data["playersScore"][player_id])
                                        collected_chips.clear()
                                        chips_consumption_approval_background()
                                        avaiable_chips_count_visualization_assigned = False
                                        break
                                    else:
                                        display["mode"] = "Chips_Give_Away"
                                        win.blit(basic_game_objects["chips_consumption_approval.png"], (1365 * scale_factor, 115 * scale_factor))
                                        chips_to_give_away.clear()
                                        break

                        elif display["mode"] == "Collected_Chips_Approval":
                            for apr_btn in chips_consumption_approval_buttons:
                                if apr_btn.click(pos):
                                    display["mode"] = "Regular"
                                    if apr_btn.text == "Okay":
                                        excess_chips_count = len(collected_chips) + game_data["playersChips"][player_id]["owned"] - 10
                                        if excess_chips_count > 0:
                                            display["mode"] = "Chips_Give_Away"
                                            win.blit(basic_game_objects["chips_to_give_away_info_panel.png"], (1365 * scale_factor, 30 * scale_factor))
                                            win.blit(basic_game_objects["chips_give_away_panel_highlighted.png"], (925 * scale_factor, 905 * scale_factor))
                                            rectangle = pygame.Rect(1365 * scale_factor, 30 * scale_factor, 526 * scale_factor, 55 * scale_factor)
                                            pygame.display.update(rectangle)
                                            win.blit(basic_game_objects["chips_consumption_approval.png"], (1365 * scale_factor, 115 * scale_factor))
                                            chips_left_to_give_away = len(chips_to_give_away)
                                            chips_left_to_give_away_text = str(chips_left_to_give_away) + "/" + str(excess_chips_count)
                                            blit_text(32, [0, 0, 0], chips_left_to_give_away_text,
                                                      1826, 215, None)
                                            draw_chips_approval_panel_with_chips(chips_to_give_away)
                                            draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                                          game_data["playersCards"][player_id],
                                                                          players_turn_indexes[player_id], False, True,
                                                                          game_data["playersScore"][player_id])
                                            break
                                        else:
                                            data_send_to_server["action_type"] = "Chips_Consumption"
                                            data_send_to_server["action_data"] = {
                                                "collected_chips": collected_chips,
                                                "chips_to_give_away": None
                                            }
                                            game_data = n.send(data_send_to_server)
                                            draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                                          game_data["playersCards"][player_id],
                                                                          players_turn_indexes[player_id], False, False,
                                                                          game_data["playersScore"][player_id])
                                            collected_chips.clear()
                                            chips_consumption_approval_background()
                                            avaiable_chips_count_visualization_assigned = False

                                    else:
                                        draw_avaiable_chips_count(game_data["chipsAmount"])
                                        collected_chips.clear()
                                        chips_consumption_approval_background()
                                        avaiable_chips_count_visualization_assigned = False





                        elif display["mode"] == "Regular" or display["mode"] == "Collected_Chips":
                            if display["mode"] == "Regular":
                                for row in range(3):
                                    for column in range(4):
                                        # if btn.click(pos) and game.connected():
                                        if card_btns[row][column].click(pos):
                                            card_price = (card_btns[row][column].pw,
                                                          card_btns[row][column].pr,
                                                          card_btns[row][column].pbr,
                                                          card_btns[row][column].pg,
                                                          card_btns[row][column].pbl
                                                          )
                                            card_cons_check_result = check_card_cunsumption_availability(
                                                card_price,
                                                game_data["playersChips"][player_id],
                                                game_data["playersCards"][player_id],
                                                game_data["chipsAmount"]["golden"],
                                            )
                                            card_cunsumption_availability["reservation"] = card_cons_check_result["reservation"]
                                            card_cunsumption_availability["consumption"] = card_cons_check_result["consumption"]
                                            card_cunsumption_availability["chips_left_for_payment"] = card_cons_check_result[
                                                "chips_left_to_pay_for_card_consmp"]
                                            if card_cunsumption_availability["reservation"] or card_cunsumption_availability["consumption"]:
                                                display["mode"] = "Card_Consumption_Menu"
                                                # choosed_card_info["image"] = card_btns[row][column].image
                                                # choosed_card_info["price"] = card_price
                                                # choosed_card_info["x"] = card_btns[row][column].x
                                                # choosed_card_info["y"] = card_btns[row][column].y
                                                # choosed_card_info["score"] = card_btns[row][column].score
                                                # choosed_card_info["card_color"] = card_btns[row][column].card_color
                                                # choosed_card_info["column"] = column
                                                # choosed_card_info["row"] = row
                                                choosed_card_info = copy.copy(card_btns[row][column])
                                                display["additional_data"] = choosed_card_info
                                                draw_card_consumption_menu(display)

                                # if len(client_player_reserved_cards) > 0:
                                #     for reserved_card_btn in client_player_reserved_cards:
                                #         if reserved_card_btn.click(pos):
                                #             reserved_card_consumption = True
                                #             choosed_card_info = reserved_card_btn
                                #             display["mode"] = "Card_Consumption_Menu_Extended"\
                                for rsrv_btn in random_cards_reservation_buttons:
                                    if rsrv_btn.click(pos):
                                        if len(client_player_reserved_cards) < 3 and game_data["chipsAmount"]["golden"] > 0:
                                            data_send_to_server["action_type"] = "Card_Reservation"
                                            data_send_to_server["action_data"] = {
                                                "random": True,
                                                "card_level": rsrv_btn.text,
                                                "chips_to_give_away": None
                                            }
                                            # random_card_rsrv_data
                                            client_player_random_card_reservation = True
                                            excess_chips_count = 1 + game_data["playersChips"][player_id]["owned"] - 10
                                            if excess_chips_count <= 0:
                                                n.send(data_send_to_server)
                                            else:
                                                display["mode"] = "Chips_Give_Away"
                                                win.blit(basic_game_objects["chips_to_give_away_info_panel.png"],
                                                         (1365 * scale_factor, 30 * scale_factor))
                                                win.blit(basic_game_objects["chips_give_away_panel_highlighted.png"],
                                                         (925 * scale_factor, 905 * scale_factor))
                                                rectangle = pygame.Rect(1365 * scale_factor, 30 * scale_factor,
                                                                        526 * scale_factor, 55 * scale_factor)
                                                pygame.display.update(rectangle)
                                                win.blit(basic_game_objects["chips_consumption_approval.png"],
                                                         (1365 * scale_factor, 115 * scale_factor))
                                                chips_left_to_give_away = len(chips_to_give_away)
                                                chips_left_to_give_away_text = str(chips_left_to_give_away) + "/" + str(
                                                    excess_chips_count)
                                                blit_text(32, [0, 0, 0], chips_left_to_give_away_text,
                                                          1826, 215, None)
                                                draw_chips_approval_panel_with_chips(chips_to_give_away)
                                                draw_client_player_attributes(win, game_data["playersChips"][player_id],
                                                                              game_data["playersCards"][player_id],
                                                                              players_turn_indexes[player_id], False,
                                                                              True,
                                                                              game_data["playersScore"][player_id])
                                                chips_give_away_while_card_reservation = True
                            for chip_btn in chips_buttons:
                                if chip_btn.text != "golden":
                                    if chip_btn.click(pos):
                                        chips_duplicated = False
                                        if avaiable_chips_count_visualization_assigned == False:
                                            avaiable_chips_count_visualization = game_data["chipsAmount"]
                                            avaiable_chips_count_visualization_assigned = True
                                        collected_chip_count = len(collected_chips)
                                        if game_data["chipsAmount"][chip_btn.text] > 0 and collected_chip_count <=2:
                                            display["mode"] = "Collected_Chips"
                                            for collected_chip in collected_chips:
                                                if chip_btn.text == collected_chip:
                                                    chips_duplicated = True
                                                    if collected_chip_count <= 1 and game_data["chipsAmount"][chip_btn.text] >= 4:
                                                        display["mode"] = "Collected_Chips_Approval"
                                                        collected_chips.append(chip_btn.text)
                                                        avaiable_chips_count_visualization[chip_btn.text] -= 1
                                                        break
                                                    else:
                                                        break
                                            if chips_duplicated == False:
                                                collected_chips.append(chip_btn.text)
                                                avaiable_chips_count_visualization[chip_btn.text] -= 1
                                            win.blit(basic_game_objects["chips_consumption_approval.png"], (1365 * scale_factor, 115 * scale_factor))
                                            draw_chips_approval_panel_with_chips(collected_chips)
                                            chips_are_over = draw_avaiable_chips_count(avaiable_chips_count_visualization)

                                            if len(collected_chips) == 3 or chips_are_over == True:
                                                display["mode"] = "Collected_Chips_Approval"
                                            chips_duplicated = False
                            if len(client_player_reserved_cards) > 0:
                                for resv_card_btn in client_player_reserved_cards:
                                    if resv_card_btn.click(pos):
                                        card_price = (resv_card_btn.pw,
                                                      resv_card_btn.pr,
                                                      resv_card_btn.pbr,
                                                      resv_card_btn.pg,
                                                      resv_card_btn.pbl
                                                      )
                                        card_cons_check_result = check_card_cunsumption_availability(
                                            card_price,
                                            game_data["playersChips"][player_id],
                                            game_data["playersCards"][player_id],
                                            game_data["chipsAmount"]["golden"],
                                        )

                                        if card_cons_check_result["consumption"] == True:
                                            card_cunsumption_availability["reservation"] = card_cons_check_result["reservation"]
                                            card_cunsumption_availability["consumption"] = card_cons_check_result["consumption"]
                                            card_cunsumption_availability["chips_left_for_payment"] = card_cons_check_result[
                                                "chips_left_to_pay_for_card_consmp"]
                                            reserved_card_consumption = True
                                            choosed_card_info.row = resv_card_btn.row,
                                            choosed_card_info.column = resv_card_btn.column,
                                            choosed_card_info.score = resv_card_btn.score,
                                            choosed_card_info.card_color = resv_card_btn.card_color,
                                            display["mode"] = "Card_Consumption_Menu_Extended"
                                            display["additional_data"] = resv_card_btn.image
                                            client_player_chips_payment_visualization = game_data["playersChips"][player_id]
                                            client_player_cards_payment_visualization = game_data["playersCards"][player_id]
                                            draw_card_consumption_menu_extended(display["additional_data"],
                                                                                card_cunsumption_availability[
                                                                                    "chips_left_for_payment"])
                                            reserved_card_object_to_remove = resv_card_btn
                            if display["mode"] == "Collected_Chips":
                                if chips_consumption_menu_buttons[0].click(pos):
                                    display["mode"] = "Regular"
                                    draw_avaiable_chips_count(game_data["chipsAmount"])
                                    chips_consumption_approval_background()
                                    collected_chips.clear()
                                    avaiable_chips_count_visualization_assigned = False
            if display["mode"] != "Players_Name_Entry":
                redrawWindow(win, game_data, data_send_to_server["player_id"], display)
                # , display_mode, chips_count_visualizer)
main()

