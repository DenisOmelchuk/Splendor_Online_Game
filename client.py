import nt
import pygame
from network import Network
from _thread import *
pygame.font.init()

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Client")

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


class Chip(Button):
    def __init__(self, x, y, width, height, image, count, color):
        super(Chip, self).__init__(x, y, width, height)
        self.image = image
        self.count = str(count)
        self.color = color

    def drawChip(self, win):
        drawImage(win, self.image, self.x, self.y, 125, 125)
        chip_counter_background_location_x = self.x + 24
        chip_counter_text_location_x = self.x + 12
        chip_counter_text_location_y = self.y - 5
        pygame.draw.circle(win, (255,255,255), (chip_counter_background_location_x, self.y + 25), 25, 0)
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
            font = pygame.font.SysFont("comicsans", 40)
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                            self.y + round(self.height / 2) - round(text.get_height() / 2)))

class Card(Button):
    def __init__(self, x, y, width, height, column, card_color, score, level, pw, pr, pbr, pg, pbl, image, bg_color):
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


class PlayersAtributes(Button):
    def __init__(self, x, y, width, height, cards_count, chips_count, atribute_counter_location):
        super(PlayersAtributes, self).__init__(x, y, width, height)
        self.cards_count = cards_count
        self.chips_count = chips_count
        self.atribute_counter_location = atribute_counter_location

    def drawAtributes(self, win, index):
        # font = pygame.font.SysFont("comicsans", 67)
        # pygame.draw.rect(win, (100, 255, 255), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", 67)
        self.chips_count += 1
        self.cards_count += 2
        if index == 4:
            font_color = (0, 0, 0)
        else:
            font_color = (255, 255, 255)
        if index < 5:
            if self.cards_count > 0:
                text1 = font.render(str(self.cards_count), 1, font_color)
                win.blit(text1, (self.atribute_counter_location, 938))

        if self.chips_count > 0:
            text2 = font.render(str(self.chips_count), 1, font_color)
            if index < 5:
                win.blit(text2, (self.atribute_counter_location + 68, 938))
            else:
                self.width = 66
                win.blit(text2, (self.atribute_counter_location - 8, 938))
            self.chips_count -= 1


card_btn_background = ButtonWithBackground(None, None, 210.92, 335, None, None)

chips = [Chip(934, 30, 125, 125, "images/chips/red_chip.png", None, "red"),
         Chip(934, 181, 125, 125, "images/chips/brown_chip.png", None, "brown"),
         Chip(934, 331, 125, 125, "images/chips/green_chip.png", None, "green"),
         Chip(934, 477, 125, 125, "images/chips/blue_chip.png", None, "blue"),
         Chip(934, 620, 125, 125, "images/chips/golden_chip.png", None, "white"),
         Chip(934, 768, 125, 125, "images/chips/golden_chip.png", None, "golden"),
         ]

card_btns = (Card(30, 30, 195.92, 320, 0, None, None, None, None, None, None, None, None, None, None),
        Card(256, 30, 195.92, 320, 1, None, None, None, None, None, None, None, None, None, None),
        Card(482, 30, 195.92, 320, 2, None, None, None, None, None, None, None, None, None, None),
        Card(708, 30, 195.92, 320, 3, None, None, None, None, None, None, None, None, None, None),
        )

# card_consumption_menu_options_buttons = (
#     Button(1240.25, 551),
#     Button(1450.5, 551),
#     Button(1660.75, 551),
# )

consumption_btns_location = ([166, 82], [166, 194], [247, 0])
consumption_btns = (ButtonWithBackground(consumption_btns_location[0][0], consumption_btns_location[0][1], 140, 93, "BUY", [128,128,128]),
                    ButtonWithBackground(consumption_btns_location[1][0], consumption_btns_location[1][1], 140, 93, "RSRV",[128,128,128]),
                    ButtonWithBackground(consumption_btns_location[2][0], consumption_btns_location[2][1], 140, 93, "EXIT", None)
                    )

chips_consumption_menu_buttons = (ButtonWithBackground(1385, 135, 208, 42, "Again", [255, 10, 10]),
                                  ButtonWithBackground(1385, 197, 208, 42, "Okay!", [58, 202, 7])
                                  )

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

# def checkPlayerConsumption(player_id, card_price, game, action):
#     if action == "BUY":
#         deficient_chips = 0
#         if player_id == 1:
#              if game.p1WhiteCards + game.p1WhiteChips < card_price[3]:
#                 deficient_chips = card_price[3] - game.p1WhiteCards - game.p1WhiteChips
#              if game.p1BlueCards + game.p1BlueChips < card_price[4]:
#                 deficient_chips = card_price[4] - game.p1BlueCards - game.p1BlueChips
#              if game.p1GreenCards + game.p1GreenChips < card_price[5]:
#                 deficient_chips = card_price[5] - game.p1GreenCards - game.p1GreenChips
#              if game.p1RedCards + game.p1RedChips < card_price[6]:
#                 deficient_chips = card_price[6] - game.p1RedCards - game.p1RedChips
#              if game.p1BrownCards + game.p1BrownChips < card_price[7]:
#                 deficient_chips = card_price[7] - game.p1BrownCards - game.p1BrownChips
#              if deficient_chips == 0:
#                  return True
#              elif game.p1GoldenChips >= deficient_chips:
#                  return
#              else:
#                  return False
#         if player_id == 2:
#              if game.p2WhiteCards + game.p2WhiteChips < card_price[3]:
#                 deficient_chips = card_price[3] - game.p2WhiteCards - game.p2WhiteChips
#              if game.p2BlueCards + game.p2BlueChips < card_price[4]:
#                 deficient_chips = card_price[4] - game.p2BlueCards - game.p2BlueChips
#              if game.p2GreenCards + game.p2GreenChips < card_price[5]:
#                 deficient_chips = card_price[5] - game.p2GreenCards - game.p2GreenChips
#              if game.p2RedCards + game.p2RedChips < card_price[6]:
#                 deficient_chips = card_price[6] - game.p2RedCards - game.p2RedChips
#              if game.p2BrownCards + game.p2BrownChips < card_price[7]:
#                 deficient_chips = card_price[7] - game.p2BrownCards - game.p2BrownChips
#              if deficient_chips == 0:
#                  return True
#              elif game.p1GoldenChips >= deficient_chips:
#                  return
#              else:
#                  return False
#         if player_id == 3:
#              if game.p3WhiteCards + game.p3WhiteChips < card_price[3]:
#                 deficient_chips = card_price[3] - game.p3WhiteCards - game.p3WhiteChips
#              if game.p3BlueCards + game.p3BlueChips < card_price[4]:
#                 deficient_chips = card_price[4] - game.p3BlueCards - game.p3BlueChips
#              if game.p3GreenCards + game.p3GreenChips < card_price[5]:
#                 deficient_chips = card_price[5] - game.p3GreenCards - game.p3GreenChips
#              if game.p3RedCards + game.p3RedChips < card_price[6]:
#                 deficient_chips = card_price[6] - game.p3RedCards - game.p3RedChips
#              if game.p3BrownCards + game.p3BrownChips < card_price[7]:
#                 deficient_chips = card_price[7] - game.p3BrownCards - game.p3BrownChips
#              if deficient_chips == 0:
#                  return True
#              elif game.p1GoldenChips >= deficient_chips:
#                  return
#              else:
#                  return False
#
#         if player_id == 4:
#              if game.p4WhiteCards + game.p4WhiteChips < card_price[3]:
#                 deficient_chips = card_price[3] - game.p4WhiteCards - game.p4WhiteChips
#              if game.p4BlueCards + game.p4BlueChips < card_price[4]:
#                 deficient_chips = card_price[4] - game.p4BlueCards - game.p4BlueChips
#              if game.p4GreenCards + game.p4GreenChips < card_price[5]:
#                 deficient_chips = card_price[5] - game.p4GreenCards - game.p4GreenChips
#              if game.p4RedCards + game.p4RedChips < card_price[6]:
#                 deficient_chips = card_price[6] - game.p4RedCards - game.p4RedChips
#              if game.p4BrownCards + game.p4BrownChips < card_price[7]:
#                 deficient_chips = card_price[7] - game.p4BrownCards - game.p4BrownChips
#              if deficient_chips == 0:
#                  return True
#              elif game.p1GoldenChips >= deficient_chips:
#                  return
#              else:
#                  return False
#     else:
#         reserve_capability = [False, False]
#         if player_id == 1:
#             if game.p1ReservedCards < 3:
#                 reserve_capability[0] = True
#             if game.p1OwnedChips != 10:
#                 reserve_capability[1] = True
#         if player_id == 2:
#             if game.p2ReservedCards < 3:
#                  reserve_capability = True
#             if game.p2OwnedChips != 10:
#                 reserve_capability[1] = True
#         if player_id == 3:
#             if game.p3ReservedCards < 3:
#                 reserve_capability = True
#             if game.p3OwnedChips != 10:
#                 reserve_capability[1] = True
#         if player_id == 4:
#             if game.p4ReservedCards < 3:
#                 reserve_capability = True
#             if game.p4OwnedChips != 10:
#                 reserve_capability[1] = True
#         if reserve_capability[0] and reserve_capability[1]:
#             return True
#         elif reserve_capability[0] and not reserve_capability[1]:
#             return
#         else:
#             return False

# def playerConsumprion(player_id, card_price, game):
#     if player_id == 1:
#         if game.p1WhiteCards + game.p1WhiteChips < card_price[3]:
#             deficient_chips = card_price[3] - game.p1WhiteCards - game.p1WhiteChips

def outOfChips(chips_amount):
    for chip in chips_amount.values():
        if chip != 0:
            return False
        else:
            return True

def drawImage(win, img, x, y, width, height):
    image = pygame.image.load(img).convert_alpha()
    if width != None and height != None:
        image = pygame.transform.smoothscale(image, (width, height))
    win.blit(image, (x, y))

def drawCardBackground(win, card_bg_color, card_x, card_y):
        card_btn_background.x = card_x - 7
        card_btn_background.y = card_y - 7
        card_btn_background.color = card_bg_color
        card_btn_background.draw(win)


def drawPlayersAtributes(win, player_index, atribute_index, type, atribute_count, width, height, font_size):
    if type == "chips_amount":
        font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", font_size)
        current_chips_amount = str(atribute_count)
        max_chips_amount = "/10"
        text_to_render = current_chips_amount + max_chips_amount
        text = font.render(text_to_render, 1, [0, 0, 0])
        win.blit(text,(player_info_panel_location[player_index][0] + 129, player_info_panel_location[player_index][1] + 92))
    if type == "score":
        font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", font_size)
        text = font.render(str(atribute_count), 1, [0, 0, 0])
        win.blit(text, (player_info_panel_location[player_index][0] + 54, player_info_panel_location[player_index][1] + 49))
    is_atribute_empty = 1
    if atribute_count > 0:
        is_atribute_empty = 0
        if type == "reserved_cards" or type == "golden_chips":
            if type == "reserved_cards":
                x = player_info_panel_location[player_index][0] + 185.57
                y = player_info_panel_location[player_index][1] + 52
                image = players_info_panel_atrubutes_images_cards[atribute_index]
            if type == "golden_chips":
                x = player_info_panel_location[player_index][0] + 122
                y = player_info_panel_location[player_index][1] + 50
                image = "images/chips/golden_chip.png"
            drawImage(win, image, x, y, width, height)
            font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", font_size)
            text = font.render(str(atribute_count), 1, [0, 0, 0])
            win.blit(text, (x + width + 5, player_info_panel_location[player_index][1] + 49))

    if atribute_index == 4:
        text_color = [0, 0, 0]
    else:
        text_color = [255, 255, 255]
    if type == "card":
        x = player_info_panel_location[player_index][0] + 20 + 43 * atribute_index
        y = player_info_panel_location[player_index][1] + 79
        image = players_info_panel_atrubutes_images_cards[atribute_index][is_atribute_empty]
        drawImage(win, image, x, y, 40, 47)

    if type == "chip":
        x = player_info_panel_location[player_index][0] + 22 + 43 * atribute_index
        y = player_info_panel_location[player_index][1] + 131
        image = players_info_panel_atrubutes_images_chips[atribute_index][is_atribute_empty]
        drawImage(win, image, x, y, width, height)
    if type == "card" or type == "chip":
        if atribute_count > 0:
            font = pygame.font.Font("font/Inter-VariableFont_slnt,wght.ttf", font_size)
            text = font.render(str(atribute_count), 1, text_color)
            win.blit(text, (x + round(width / 2) - round(text.get_width() / 2),
                            y + round(height / 2) - round(text.get_height() / 2)))


def card_price_identification(pw, pbl, pr, pg, pbr):
    chips_needed_for_card_comsumption = {
        "red": pr,
        "green": pr,
        "blue": pbl,
        "brown": pbr,
        "white": pw
    }
    return chips_needed_for_card_comsumption


def redrawWindow(win, game, player_id, display_mode, chips_count_visualizer):
    i = 0
    win.fill((51, 51, 51))
    # drawImage(win, "images/background.jpg", 0, 0, 1920, 1080)
    for btn in card_btns:
        btn.card_color = game.cards[game.card3_num[i]][0]
        btn.score = game.cards[game.card3_num[i]][1]
        btn.level = game.cards[game.card3_num[i]][2]
        btn.pw = game.cards[game.card3_num[i]][3]
        btn.pr = game.cards[game.card3_num[i]][4]
        btn.pbr = game.cards[game.card3_num[i]][5]
        btn.pg = game.cards[game.card3_num[i]][6]
        btn.pbl = game.cards[game.card3_num[i]][7]
        btn.image = game.cards[game.card3_num[i]][8]
        if btn.card_color == 'green':
            btn.bg_color = (0, 142, 64)
        elif btn.card_color == 'red':
            btn.bg_color = (186, 40, 11)
        elif btn.card_color == 'blue':
            btn.bg_color = (11, 81, 186)
        elif btn.card_color == 'brown':
            btn.bg_color = (94, 61, 18)
        elif btn.card_color == 'white':
            btn.bg_color = (232, 231, 230)
        # btn.draw(win)
        # image = pygame.image.load(btn.image).convert_alpha()
        # image = pygame.transform.smoothscale(image, (195.92, 320))
        mouse = pygame.mouse.get_pos()
        rect = pygame.Rect(btn.x, btn.y, btn.width, btn.height)
        on_button = rect.collidepoint(mouse)
        if on_button and display_mode[0] == "Regular":
            drawCardBackground(win, btn.bg_color, btn.x, btn.y)
        elif display_mode[0] == "Card_Consumption_Menu":
            if display_mode[1][1] == btn.x and display_mode[1][2] == btn.y:
                drawCardBackground(win, btn.bg_color, btn.x, btn.y)
        # win.blit(image, (btn.x, btn.y))
        drawImage(win, btn.image, btn.x, btn.y, 195.92, 320)
        if i <= 3:
            i += 1
        else:
            i = 0

    for chip in chips:
        chip.count = str(chips_count_visualizer[chip.color])
        chip.drawChip(win)


    for player_index, player in enumerate(game.players_queue):
        player_cards_values = [x[1] for x in game.playersCards[player].items()]
        player_chips_values = [x[1] for x in game.playersChips[player].items()]
        drawImage(win, "images/informational_panel_background/player_info_panel.png",
                  player_info_panel_location[player_index][0],
                  player_info_panel_location[player_index][1], 248, 170)
        drawPlayersAtributes(win, player_index, None, "score", game.playersScore[player],
                             28, 28, 28)
        if player == player_id:
            drawImage(win, "images/informational_panel_background/players_cards_and_chips_panel.png", 935, 915, 956, 135)
            for atribute_index, player_atribute in enumerate(players_atributes):
                if atribute_index < 5:
                    player_atribute.cards_count = player_cards_values[atribute_index]
                else:
                    player_atribute.cards_count = 0
                player_atribute.cards_count = player_chips_values[atribute_index]
                player_atribute.drawAtributes(win, atribute_index)
                chips_amount = game.playersChips[player]["owned"]
                drawPlayersAtributes(win, player_index, None, "chips_amount", chips_amount,
                                    None, None, 45)
        if player != player_id:
            for atribute_index in range(6):
                if atribute_index <= 4:
                    drawPlayersAtributes(win, player_index, atribute_index, "card", player_cards_values[atribute_index],
                                     36, 47, 31)
                    drawPlayersAtributes(win, player_index, atribute_index, "chip", player_chips_values[atribute_index],
                                     32, 32, 25)
                else:
                    drawPlayersAtributes(win, player_index, atribute_index, "reserved_cards",player_cards_values[atribute_index],
                                         21.43, 25, 28)
                    drawPlayersAtributes(win, player_index, atribute_index, "golden_chips", player_cards_values[atribute_index],
                                         28, 28, 28)


    if display_mode[0] == "Chips_Consumption_Menu":
        drawImage(win, "images/informational_panel_background/chips_approval.png", 1365, 115, 526, 143)
        chips_locaction_in_consump_menu = (1627, 1714, 1801)
        for btn in chips_consumption_menu_buttons:
            btn.draw(win)
        for num in range(len(display_mode[1])):
            drawImage(win, display_mode[1][num].image, chips_locaction_in_consump_menu[num], 145, 70, 70)

    if display_mode[0] == "Card_Consumption_Menu":
        # drawCardBackground(win, card_cons_menu[0], card_cons_menu[1], card_cons_menu[2])
        pygame.draw.rect(win, display_mode[1][0], (display_mode[1][1] + 148 , display_mode[1][2] - 7, 176, 335))
        j = 0
        for btn in consumption_btns:
            btn.x = consumption_btns_location[j][0] + display_mode[1][1]
            btn.y = consumption_btns_location[j][1] + display_mode[1][2]
            if btn.text != "EXIT":
                btn.draw(win)
            else:
                drawImage(win, "images/button_icon/exit_icon.png", btn.x, btn.y, 59, 59)
            j += 1
            if j == 3:
                j = 0

    if display_mode[0] == "Card_Consumption_Menu_Extended":
        drawImage(win, "images/informational_panel_background/card_consumption_buy_options.png", 935, 288, 956, 605)
        drawImage(win, "images/cards3/0.png", 955, 308, 195.92, 320)

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player_id = int(n.getP())
    current_player_move = 0
    collected_chips = []
    chip_duplicated = False
    chip_consumption_allowed = True
    display_mode = ["Regular", None]
    data_send_to_server = {
        "player": player_id,
        "action_type": None,
        "action_data": None
    }
    choosed_card_info = {
        "price": None,
        "image": None,
        "additional_data": {
            "x": None,
            "y": None,
            "score": None
        }
    }

    while run:
        clock.tick(30)
        # pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
        try:
            game = n.send("get")
            chips_count = [
                game.chipsAmount["red"],
                game.chipsAmount["brown"],
                game.chipsAmount["green"],
                game.chipsAmount["blue"],
                game.chipsAmount["white"],
                game.chipsAmount["golden"],
            ]
        except:
            run = False
            print("Couldn't get game")
            break

        if display_mode[0] == "Regular":
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


            # if current_player_move == p:
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if display_mode[0] == "Card_Consumption_Menu":
                    for btn in consumption_btns:
                        if btn.click(pos):
                            if btn.text == "EXIT":
                                display_mode[0] = "Regular"
                            elif btn.text == "BUY":
                                # if checkPlayerConsumption(player, choosed_card_info, game, btn.text):
                                if game.playersChips["golden"] > 0:
                                    display_mode[0] = "Card_Consumption_Menu_Extended"
                                    display_mode[1] = [choosed_card_info["price"], choosed_card_info["image"]]
                                else:
                                    data_send_to_server["action_type"] = "card_consumption"
                                    data_send_to_server["action_data"] = choosed_card_info
                                    n.send(data_send_to_server)
                                    display_mode[0] = "Regular"
                                    card_consumption_menu_parameters = False
                            #     elif not checkPlayerConsumption(player, choosed_card_info, game, btn.text):
                            #
                            #
                            # elif btn.text == "RSRV":
                            #     if checkPlayerConsumption(player, choosed_card_info, game, btn.text):
                            #         n.send("RSRV", choosed_card_info)
                            #         card_consumption_menu_parameters = False

                else:
                    if display_mode[0] == "Regular":
                        for btn in card_btns:
                            # if btn.click(pos) and game.connected():
                            if btn.click(pos):
                                display_mode[0] = "Card_Consumption_Menu"
                                display_mode[1] = [btn.bg_color, btn.x, btn.y]
                                choosed_card_info["image"] = btn.image
                                choosed_card_info["price"] = card_price_identification(btn.pw, btn.pbl, btn.pr, btn.pg,
                                                                                       btn.pbr)
                                choosed_card_info["additional_data"] = [btn.x, btn.y, btn.score, btn.card_color, btn.column]

                    if display_mode[0] != "Card_Consumption_Menu" and len(collected_chips) < 3 and chip_consumption_allowed:
                        display_mode[1] = collected_chips
                        for num in range(5):
                            if chips_count_visualizer[chips[num].color] > 0:
                                if chips[num].click(pos):
                                    display_mode[0] = "Chips_Consumption_Menu"
                                    for chip in collected_chips:
                                        if chip.color == chips[num].color:
                                            if len(collected_chips) < 2:
                                                if chips_count[num] >= 4:
                                                    collected_chips.append(chips[num])
                                                    chips_count_visualizer[chips[num].color] -= 1
                                                    chip_consumption_allowed = False
                                            chip_duplicated = True

                                            # if not chip_consumption_allowed:


                                    if chip_consumption_allowed and not chip_duplicated:
                                        collected_chips.append(chips[num])
                                        chips_count_visualizer[chips[num].color] -= 1
                    if display_mode[0] == "Chips_Consumption_Menu":
                        for btn in chips_consumption_menu_buttons:
                            if btn.click(pos):
                                if btn.text == "Okay!":
                                    if len(collected_chips) == 3 or len(collected_chips) == 2 and chip_duplicated or outOfChips(game.chipsAmount):
                                        data_send_to_server["action_type"] = "сhips_collecting"
                                        data_send_to_server["action_data"] = [chip.color for chip in collected_chips]
                                        n.send(data_send_to_server)

                                display_mode[0] = "Regular"
                                chip_duplicated = False
                                chip_consumption_allowed = True
                                collected_chips.clear()













                        # if player == 0:
                            # if not game.p1Went:



                        # current_player_move +=1


                        # else:
                        #     if not game.p2Went:
                        #         n.send(btn.text)
                # if current_player_move < 4:
                #     current_player_move += 1
                # else:
                #     current_player_move = 0
                chip_duplicated = False
            print(clock.get_fps())
            redrawWindow(win, game, player_id, display_mode, chips_count_visualizer)
main()


# def redrawWindow(win, game, p):
#     win.fill((128,128,128))
#
#     if not(game.connected()):
#         font = pygame.font.SysFont("comicsans", 80)
#         text = font.render("Waiting for Player...", 1, (255,0,0), True)
#         win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
#     else:
#         font = pygame.font.SysFont("comicsans", 60)
#         text = font.render("Your Move", 1, (0, 255,255))
#         win.blit(text, (80, 200))
#
#         text = font.render("Opponents", 1, (0, 255, 255))
#         win.blit(text, (380, 200))
#
#         move1 = game.get_player_move(0)
#         move2 = game.get_player_move(1)
#         if game.bothWent():
#             text1 = font.render(move1, 1, (0,0,0))
#             text2 = font.render(move2, 1, (0, 0, 0))
#         else:
#             if game.p1Went and p == 0:
#                 text1 = font.render(move1, 1, (0,0,0))
#             elif game.p1Went:
#                 text1 = font.render("Locked In", 1, (0, 0, 0))
#             else:
#                 text1 = font.render("Waiting...", 1, (0, 0, 0))
#
#             if game.p2Went and p == 1:
#                 text2 = font.render(move2, 1, (0,0,0))
#             elif game.p2Went:
#                 text2 = font.render("Locked In", 1, (0, 0, 0))
#             else:
#                 text2 = font.render("Waiting...", 1, (0, 0, 0))
#
#         # if p == 1:
#         #     win.blit(text2, (100, 350))
#         #     win.blit(text1, (400, 350))
#         # else:
#         #     win.blit(text1, (100, 350))
#         #     win.blit(text2, (400, 350))
#
#         for btn in btns:
#             btn.draw(win)
#
#     pygame.display.update()
#
#
# btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
# def main():
#     run = True
#     clock = pygame.time.Clock()
#     n = Network()
#     player = int(n.getP())
#     print("You are player", player)
#
#     while run:
#         clock.tick(60)
#         try:
#             game = n.send("get")
#         except:
#             run = False
#             print("Couldn't get game")
#             break
#
#         if game.bothWent():
#             redrawWindow(win, game, player)
#             pygame.time.delay(500)
#             try:
#                 game = n.send("reset")
#             except:
#                 run = False
#                 print("Couldn't get game")
#                 break
#
#             font = pygame.font.SysFont("comicsans", 90)
#             if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
#                 text = font.render("You Won!", 1, (255,0,0))
#             elif game.winner() == -1:
#                 text = font.render("Tie Game!", 1, (255,0,0))
#             else:
#                 text = font.render("You Lost...", 1, (255, 0, 0))
#
#             win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
#             pygame.display.update()
#             pygame.time.delay(2000)
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.quit()
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 pos = pygame.mouse.get_pos()
#                 for btn in btns:
#                     if btn.click(pos) and game.connected():
#                         if player == 0:
#                             if not game.p1Went:
#                                 n.send(btn.text)
#                         else:
#                             if not game.p2Went:
#                                 n.send(btn.text)
#
#         redrawWindow(win, game, player)
#
# main()

# def menu_screen():
#     run = True
#     clock = pygame.time.Clock()
#
#     while run:
#         clock.tick(60)
#         win.fill((128, 128, 128))
#         font = pygame.font.SysFont("comicsans", 60)
#         text = font.render("Click to Play!", 1, (255,0,0))
#         win.blit(text, (100,200))
#         pygame.display.update()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 run = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 run = False
#
#     main()

# while True:
#     menu_screen()
