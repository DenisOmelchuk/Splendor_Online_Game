class Game:
    def __init__(self, id):
        self.id = id
        # Finished moves of the players during the round
        self.players_goal_achieved = []
        self.cards_counter = {
            0: 3,
            1: 3,
            2: 3,
        }
        self.data_updated = True
        self.players_names = {
            1: "1",
            2: "2",
            3: "3",
            4: "4",
        }
        self.card3_counter = 3
        self.card2_counter = 3
        self.card1_counter = 3
        self.card_num = {
            0: {
                0: 0,
                1: 1,
                2: 2,
                3: 3,
            },
            1: {
                0: 0,
                1: 1,
                2: 2,
                3: 3,
            },
            2: {
                0: 0,
                1: 1,
                2: 2,
                3: 3,
            },
        }
        self.card3_num = [0, 1, 2, 3]
        self.card2_num = [0, 1, 2, 3]
        self.card1_num = [0, 1, 2, 3]
        self.p1Went = False
        self.p2Went = False
        self.p3Went = False
        self.p4Went = False
        self.allWent = False
        self.game_changes = {
            "player": None,
            "change_type": None,
            "change_data": None
        }
        self.game_update = {
            "player": None,
            "type_of_update": None
        }
        self.winner = []
        self.player_index_turn = 0
        self.players_queue = [1, 2, 3, 4]
        self.player_id_turn_to_move = self.players_queue[self.player_index_turn]
        # All players are ready for the game (4)
        # Change it to False
        self.ready = True
        # Amount of chips available
        self.chipsAmount = {
            "red": 7,
            "brown": 7,
            "green": 7,
            "blue": 7,
            "white": 7,
            "golden": 5,
        }
        self.playersScore = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
        }
        # Player's Cards
        self.playersCards = {
            1: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "reserved": 0,
                "owned": 0
            },
            2: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "reserved": 0,
                "owned": 0
            },
            3: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "reserved": 0,
                "owned": 0
            },
            4: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "reserved": 0,
                "owned": 0
            }
        }

        self.game_aristocrats = None

        self.playersReservedCards = {
            1: [],
            2: [],
            3: [],
            4: []
        }

        self.playersChips = {
            1: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "golden": 0,
                "owned": 0,
            },
            2: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "golden": 0,
                "owned": 0,
            },
            3: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "golden": 0,
                "owned": 0,
            },
            4: {
                "red": 0,
                "brown": 0,
                "green": 0,
                "blue": 0,
                "white": 0,
                "golden": 0,
                "owned": 0,
            }
        }

        self.cards = {
            0: [('red', 3, 3, 3, 0, 3, 3, 5, 'images/cards3/3c0.png'),
                ('blue', 3, 3, 3, 3, 5, 3, 0 ,'images/cards3/3c1.png'),
                ('green', 3, 3, 5, 3, 3, 0, 3, 'images/cards3/3c2.png'),
                ('brown', 3, 3, 3, 3, 0, 5, 3, 'images/cards3/3c3.png'),
                ('white', 3, 3, 0, 5, 3, 3, 3, 'images/cards3/3c4.png'),
                ('green', 5, 3, 0, 0, 0, 3, 7, 'images/cards3/3c5.png'),
                ('green', 4, 3, 0, 0, 0, 0, 7, 'images/cards3/3c6.png'),
                ('green', 4, 3, 3, 0, 0, 3, 6, 'images/cards3/3c7.png'),
                ('blue', 4, 3, 7, 0, 0, 0, 0, 'images/cards3/3c8.png'),
                ('blue', 4, 3, 6, 0, 3, 0, 3, 'images/cards3/3c9.png'),
                ('blue', 5, 3, 7, 0, 0, 0, 3, 'images/cards3/3c10.png'),
                ('red', 5, 3, 0, 3, 0, 7, 0, 'images/cards3/3c11.png'),
                ('red', 4, 3, 0, 0, 0, 7, 0, 'images/cards3/3c12.png'),
                ('red', 4, 3, 0, 3, 0, 6, 3, 'images/cards3/3c13.png'),
                ('white', 4, 3, 0, 0, 7, 0, 0, 'images/cards3/3c14.png'),
                ('white', 4, 3, 3, 3, 6, 0, 0, 'images/cards3/3c15.png'),
                ('white', 5, 3, 3, 0, 7, 0, 0, 'images/cards3/3c16.png'),
                ('brown', 5, 3, 0, 7, 3, 0, 0, 'images/cards3/3c17.png'),
                ('brown', 4, 3, 0, 6, 3, 3, 0, 'images/cards3/3c18.png'),
                ('brown', 4, 3, 0, 7, 0, 0, 0, 'images/cards3/3c19.png')
                      ],
            1: [('green', 2, 2, 4, 0, 1, 0, 2, 'images/cards2/2c0.png'),
                ('green', 1, 2, 2, 0, 2, 0, 3, 'images/cards2/2c1.png'),
                ('green', 1, 2, 3, 3, 0, 2, 0, 'images/cards2/2c2.png'),
                ('green', 2, 2, 0, 0, 0, 3, 5, 'images/cards2/2c3.png'),
                ('green', 2, 2, 0, 0, 0, 5, 0, 'images/cards2/2c4.png'),
                ('green', 3, 2, 0, 0, 0, 6, 0, 'images/cards2/2c5.png'),
                ('blue', 3, 2, 0, 0, 0, 0, 6, 'images/cards2/2c6.png'),
                ('blue', 2, 2, 0, 0, 0, 0, 5, 'images/cards2/2c7.png'),
                ('blue', 1, 2, 0, 3, 0, 2, 2, 'images/cards2/2c8.png'),
                ('blue', 1, 2, 0, 0, 3, 3, 2, 'images/cards2/2c9.png'),
                ('brown', 1, 2, 3, 0, 0, 2, 2, 'images/cards2/2c10.png'),
                ('blue', 2, 2, 5, 0, 0, 0, 3, 'images/cards2/2c11.png'),
                ('red', 2, 2, 1, 0, 0, 2, 5, 'images/cards2/2c12.png'),
                ('red', 1, 2, 2, 2, 3, 0, 0, 'images/cards2/2c13.png'),
                ('red', 2, 2, 3, 0, 5, 0, 0, 'images/cards2/2c14.png'),
                ('red', 2, 2, 0, 0, 5, 0, 0, 'images/cards2/2c15.png'),
                ('red', 1, 2, 0, 2, 3, 0, 3, 'images/cards2/2c16.png'),
                ('red', 3, 2, 0, 6, 0, 0, 0, 'images/cards2/2c17.png'),
                ('white', 3, 2, 6, 0, 0, 0, 0, 'images/cards2/2c18.png'),
                ('white', 2, 2, 0, 4, 2, 1, 0, 'images/cards2/2c19.png'),
                ('white', 2, 2, 0, 5, 0, 0, 0, 'images/cards2/2c20.png'),
                ('white', 1, 2, 2, 3, 0, 0, 3, 'images/cards2/2c21.png'),
                ('white', 2, 2, 0, 5, 3, 0, 0, 'images/cards2/2c22.png'),
                ('white', 1, 2, 0, 2, 2, 3, 0, 'images/cards2/2c23.png'),
                ('brown', 2, 2, 0 ,2, 0, 4, 1, 'images/cards2/2c24.png'),
                ('brown', 3, 2, 0, 0, 6, 0, 0, 'images/cards2/2c25.png'),
                ('brown', 1, 2, 3, 0, 0, 2, 2, 'images/cards2/2c26.png'),
                ('brown', 1, 2, 3, 0, 2, 3, 0, 'images/cards2/2c27.png'),
                ('brown', 2, 2, 0, 3, 0, 5, 0, 'images/cards2/2c28.png'),
                ('brown', 2, 2, 5, 0, 0, 0, 0, 'images/cards2/2c29.png'),
            ],
            2: [('green', 0, 1, 1, 1, 2, 0, 1, 'images/cards1/1c0.png'),
                ('green', 0, 1, 1, 1, 1, 0, 1, 'images/cards1/1c1.png'),
                ('green', 0, 1, 1, 0, 0, 1, 3, 'images/cards1/1c2.png'),
                ('green', 0, 1, 0, 2, 2, 0, 1, 'images/cards1/1c3.png'),
                ('green', 0, 1, 0, 2, 0, 0, 2, 'images/cards1/1c4.png'),
                ('green', 0, 1, 0, 3, 0, 0, 0, 'images/cards1/1c5.png'),
                ('green', 0, 1, 2, 0, 0, 0, 1, 'images/cards1/1c6.png'),
                ('green', 1, 1, 0, 0, 4, 0, 0 ,'images/cards1/1c7.png'),
                ('red', 0, 1, 1, 0, 1, 1, 1, 'images/cards1/1c8.png'),
                ('white', 0, 1, 0, 1, 1, 2, 1, 'images/cards1/1c9.png'),
                ('red', 0, 1, 3, 0, 0, 0, 0, 'images/cards1/1c10.png'),
                ('red', 0, 1, 1, 1, 3, 0, 0, 'images/cards1/1c11.png'),
                ('white', 0, 1, 0, 0, 2, 0, 2, 'images/cards1/1c12.png'),
                ('brown', 0, 1, 0, 3, 1, 1, 0, 'images/cards1/1c13.png'),
                ('white', 0, 1, 3, 0, 1, 0, 1, 'images/cards1/1c14.png'),
                ('green', 0, 1, 2, 0, 0, 0, 1, 'images/cards1/1c15.png'),
                ('white', 0, 1, 0, 0, 0, 0, 3, 'images/cards1/1c16.png'),
                ('blue', 0, 1, 0, 0, 3, 0, 0, 'images/cards1/1c17.png'),
                ('red', 0, 1, 2, 0, 2, 1, 0, 'images/cards1/1c18.png'),
                ('brown', 1, 1, 0, 0, 0, 0, 4, 'images/cards1/1c19.png'),
                ('brown', 0, 1, 0, 1, 0, 2, 0, 'images/cards1/1c20.png'),
                ('brown', 0, 1, 1, 1, 0, 1, 1, 'images/cards1/1c21.png'),
                ('brown', 0, 1, 2, 1, 0, 0, 2, 'images/cards1/1c22.png'),
                ('brown', 0, 1, 0, 0, 0, 3, 0, 'images/cards1/1c23.png'),
                ('brown', 0, 1, 1, 1, 0, 1, 2, 'images/cards1/1c24.png'),
                ('brown', 0, 1, 2, 0, 0, 2, 0, 'images/cards1/1c25.png'),
                ('white', 0, 1, 0, 0, 1, 2, 2, 'images/cards1/1c26.png'),
                ('white', 0, 1, 0, 2, 1, 0, 0, 'images/cards1/1c27.png'),
                ('white', 0, 1, 0, 1, 1, 1, 1, 'images/cards1/1c28.png'),
                ('white', 1, 1, 0, 0, 0, 4, 0, 'images/cards1/1c29.png'),
                ('blue', 1, 1, 0, 4, 0, 0, 0, 'images/cards1/1c30.png'),
                ('blue', 0, 0, 1, 1, 1, 1, 0, 'images/cards1/1c31.png'),
                ('blue', 0, 1, 1, 2, 1, 1, 0, 'images/cards1/1c32.png'),
                ('blue', 0, 1, 0, 1, 0, 3, 1, 'images/cards1/1c33.png'),
                ('blue', 0, 1, 1, 2, 0, 2, 0, 'images/cards1/1c34.png'),
                ('blue', 0, 1, 1, 0, 2, 0, 0, 'images/cards1/1c35.png'),
                ('blue', 0, 1, 0, 0, 2, 2, 0, 'images/cards1/1c36.png'),
            ]
        }

        self.aristocrats = [
            (4, "images/aristocrats/aristocrat_0.png", "blue", "green"),
            (4, "images/aristocrats/aristocrat_1.png", "blue", "white"),
            (4, "images/aristocrats/aristocrat_2.png", "brown", "white"),
            (4, "images/aristocrats/aristocrat_3.png", "brown", "red"),
            (3, "images/aristocrats/aristocrat_4.png", "white", "brown", "blue"),
            (3, "images/aristocrats/aristocrat_5.png", "white", "brown", "red"),
            (3, "images/aristocrats/aristocrat_6.png", "green", "brown", "red"),
            (3, "images/aristocrats/aristocrat_7.png", "green", "red", "blue"),
            (3, "images/aristocrats/aristocrat_8.png", "white", "green", "blue"),
            (4, "images/aristocrats/aristocrat_9.png", "green", "red"),
        ]

    def set_game_aristocrats(self):
        random.shuffle(self.aristocrats)
        self.game_aristocrats = [aristocrat for aristocrat in self.aristocrats][:5]

    def name_enter(self, player_id, name):
        self.players_names[player_id] = name

    def change_player_index_turn_to_move(self):
        players_info_comparison = {}
        if self.player_index_turn == 3:
            if len(self.players_goal_achieved) > 0:
                max_score = 0
                min_count_card = 100
                winners = []
                if len(self.players_goal_achieved) == 1:
                    winners = self.players_goal_achieved[0]
                else:
                    for player_index in self.players_goal_achieved:
                        if self.playersScore[player_index] > max_score:
                            max_score = self.playersScore[player_index]
                            winners.clear()
                            winners.append(player_index)
                        elif self.playersScore[player_index] == max_score:
                            winners.append(player_index)
                    if len(winners) > 1:
                        for player_index in self.players_goal_achieved:
                            if self.playersCards[player_index]["owned"] < min_count_card:
                                winners.clear()
                                winners.append(player_index)
                                min_count_card = self.playersCards[player_index]["owned"]
                            elif self.playersCards[player_index]["owned"] == min_count_card:
                                winners.append(player_index)
                self.game_changes["change_type"] = "victory"
                self.game_changes["change_data"] = winners

            self.player_index_turn = 0
        else:
            self.player_index_turn += 1
        self.player_id_turn_to_move = self.players_queue[self.player_index_turn]

    def get_serializable_attributes(self):
        game = {
            "game_changes": self.game_changes,
            "players_queue": self.players_queue,
            "playersCards": self.playersCards,
            "playersScore": self.playersScore,
            "chipsAmount": self.chipsAmount,
            "playersChips": self.playersChips,
            "player_id_turn_to_move": self.player_id_turn_to_move,
            "players_names": self.players_names,
            "data_updated": self.data_updated
        }
        return game


    def allWent(self):
        return self.p1Went and self.p2Went and self.p3Went and self.p4Went

    def resetWent(self):
        self.p1Went = False
        self.p2Went = False
        self.p3Went = False
        self.p4Went = False

    def connected(self):
        return self.ready

    def shuffle_cards_and_queue(self):
        # for card_row in range(3):
        #     random.shuffle(self.cards[card_row])
        random.shuffle(self.players_queue)

        for key in self.cards.keys():
            random.shuffle(self.cards[key])

    def get_new_card(self, row, column):
        self.cards_counter[row] += 1
        new_card = self.cards[row][self.cards_counter[row]]
        self.game_changes["change_data"] = {
            "new_card": new_card,
            "row": row,
            "column": column
        }

    # def card_consumption(self, row, column, score, card_color, player_id, payed_chips, card_was_reservated, chip_to_give_away):
    #     if card_was_reservated == False:
    #         self.get_new_card(row, column)
    #     for chip_color, chip_count in payed_chips.items():
    #         self.playersChips[player_id][chip_color] -= chip_count
    #         self.playersChips[player_id]["owned"] -= chip_count
    #         self.chipsAmount[chip_color] += chip_count
    #     self.playersScore[player_id] += score
    #     self.playersCards[player_id][card_color] += 1
    #     self.playersCards[player_id]["owned"] += 1
    #     if self.playersCards[player_id]["owned"] >= 8:
    #         for aristocrat_data in self.game_aristocrats:
    #             if self.playersCards[player_id][aristocrat_data[2]] >= aristocrat_data[0] and self.playersCards[player_id][aristocrat_data[3]] >= aristocrat_data[0]:
    #                 if aristocrat_data[0] == 3:
    #                     if self.playersCards[player_id][aristocrat_data[4]] >= aristocrat_data[0]:
    #                         self.playersScore[player_id] += 3
    #                 else:
    #                     self.playersScore[player_id] += 3
    #     if self.playersScore[player_id] >= 15:
    #         self.players_goal_achieved.append(player_id)
    #     if card_was_reservated:
    #         self.playersCards[player_id]["reserved"] -= 1
    #         self.game_changes["change_data"] = "reserved_card"
    #     self.game_changes["player"] = player_id
    #     self.game_changes["change_type"] = "card_consumption"
    #     self.change_player_index_turn_to_move()
    #     self.data_updated = True
    #

    def owned_chips_count(self, player_id):
        owned_chips = 0
        for chip_type, chips_count in self.playersChips[player_id].items():
            if chip_type != "owned":
                owned_chips += chips_count
        self.playersChips[player_id]["owned"] = owned_chips

    def card_consumption(self, row, column, score, card_color, player_id, payed_chips, card_was_reservated):
        self.get_new_card(row, column)
        for chip_color, chip_count in payed_chips.items():
            self.playersChips[player_id][chip_color] -= chip_count
            self.playersChips[player_id]["owned"] -= chip_count
            self.chipsAmount[chip_color] += chip_count
        self.playersScore[player_id] += score
        self.playersCards[player_id][card_color] += 1
        self.playersCards[player_id]["owned"] += 1
        if self.playersCards[player_id]["owned"] >= 8:
            for aristocrat_data in self.game_aristocrats:
                if self.playersCards[player_id][aristocrat_data[2]] >= aristocrat_data[0] and \
                        self.playersCards[player_id][aristocrat_data[3]] >= aristocrat_data[0]:
                    if aristocrat_data[0] == 3:
                        if self.playersCards[player_id][aristocrat_data[4]] >= aristocrat_data[0]:
                            self.playersScore[player_id] += 3
                    else:
                        self.playersScore[player_id] += 3
        if self.playersScore[player_id] >= 15:
            self.players_goal_achieved.append(player_id)
        if card_was_reservated:
            self.playersCards[player_id]["reserved"] -= 1
        self.game_changes["player"] = player_id
        self.game_changes["change_type"] = "card_consumption"
        self.change_player_index_turn_to_move()
        self.owned_chips_count(player_id)


    def card_reservation(self, player_id, card_data, chip_to_give_away):
        if card_data["random"] != True:
            self.get_new_card(card_data["row"], card_data["column"])
            self.game_changes["change_type"] = "card_reservation"
        else:
            self.get_new_card(int(card_data["card_level"]), None)
            self.game_changes["change_type"] = "random_card_reservation"
        if chip_to_give_away is not None:
            self.chipsAmount[chip_to_give_away[0]] += 1
            self.playersChips[player_id][chip_to_give_away[0]] -= 1
            self.playersChips[player_id]["owned"] -= 1
        self.game_changes["player"] = player_id
        self.playersCards[player_id]["reserved"] += 1
        self.chipsAmount["golden"] -= 1
        self.playersChips[player_id]["golden"] += 1
        self.playersChips[player_id]["owned"] += 1
        self.change_player_index_turn_to_move()
        self.data_updated = True
        self.owned_chips_count(player_id)

    def chips_consumption(self, chips_cons_data, player_id):
        chips_taken = chips_cons_data["collected_chips"]
        if chips_cons_data["chips_to_give_away"] != None:
            chips_give_away = chips_cons_data["chips_to_give_away"]
            for chip_color in chips_give_away:
                self.chipsAmount[chip_color] += 1
                self.playersChips[player_id][chip_color] -= 1
                self.playersChips[player_id]["owned"] -= 1
        for chip_color in chips_taken:
            self.chipsAmount[chip_color] -= 1
            self.playersChips[player_id][chip_color] += 1
            self.playersChips[player_id]["owned"] += 1
        self.game_changes["player"] = player_id
        self.game_changes["change_type"] = "chips_consumption"
        self.change_player_index_turn_to_move()
        self.data_updated = True
        self.owned_chips_count(player_id)






    def changeCard(self, x, y):
        if x == 30:
            card_column_to_change = 0
            if y == 30:
                self.card3_counter += 1
                self.card3_num[card_column_to_change] = self.card3_counter
            if y == 380:
                self.card2_counter += 1
                self.card2_num[card_column_to_change] = self.card2_counter
            if y == 730:
                self.card1_counter += 1
                self.card1_num[card_column_to_change] = self.card1_counter
        if x == 256:
            card_column_to_change = 1
            if y == 30:
                self.card3_counter += 1
                self.card3_num[card_column_to_change] = self.card3_counter
            if y == 380:
                self.card2_counter += 1
                self.card2_num[card_column_to_change] = self.card2_counter
            if y == 730:
                self.card1_counter += 1
                self.card1_num[card_column_to_change] = self.card1_counter
        if x == 482:
            card_column_to_change = 2
            if y == 30:
                self.card3_counter += 1
                self.card3_num[card_column_to_change] = self.card3_counter
            if y == 380:
                self.card2_counter += 1
                self.card2_num[card_column_to_change] = self.card2_counter
            if y == 730:
                self.card1_counter += 1
                self.card1_num[card_column_to_change] = self.card1_counter
        if x == 708:
            card_column_to_change = 3
            if y == 30:
                self.card3_counter += 1
                self.card3_num[card_column_to_change] = self.card3_counter
            if y == 380:
                self.card2_counter += 1
                self.card2_num[card_column_to_change] = self.card2_counter
            if y == 730:
                self.card1_counter += 1
                self.card1_num[card_column_to_change] = self.card1_counter

    def changeChipsAmount(self, player, collected_chips):
       for chip in collected_chips:
           self.chipsAmount[chip] -= 1
           self.playersChips[player][chip] += 1

    def changePlayersCards(self, player, score, price_white, price_blue, price_green, price_red, price_brown, color):
        self.playersCards[player][color] += 1
        self.playersScore[player] += score

    def getNewCard(self, column):
        return self.cards[row][self.cards_counter][row]