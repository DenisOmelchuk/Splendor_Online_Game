import random
import socket
from _thread import *
import pickle
from game import Game
import select, sys
import random


port = 3389

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(("", port))
except socket.error as e:
    str(e)

s.listen(5)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId, cards):
    global idCount

    basic_game_data = {
        "player_id": p,
        "cards": cards,
        "players_queue": games[gameId].players_queue,
        "playersCards": games[gameId].playersCards,
        "playersScore": games[gameId].playersScore,
        "playersChips": games[gameId].playersChips,
        "chipsAmount": games[gameId].chipsAmount,
        "player_id_turn_to_move": games[gameId].player_id_turn_to_move,
        "aristocrats_images": [aristocrat[1] for aristocrat in games[gameId].game_aristocrats],
        # "password": "BrngFUrwZmLfYYS",
        "players_names": games[gameId].players_names,
    }
    conn.send(pickle.dumps(basic_game_data))



    reply = ""
    while True:
        try:
            client_data = pickle.loads(conn.recv(4096*2000))

            if gameId in games:
                game = games[gameId]
                game_data = game.get_serializable_attributes()


                if not client_data:
                    print("no data")
                    break
                else:
                    if client_data == "reset":
                        game.resetWent()

                    elif client_data != "get":
                        if client_data["action_type"] == "Card_Consumption":
                            game.card_consumption(client_data["action_data"]["row"], client_data["action_data"]["column"],
                                             client_data["action_data"]["score"], client_data["action_data"]["card_color"],
                                             client_data["player_id"], client_data["action_data"]["payed_chips"],
                                             client_data["action_data"]["card_was_reservated"])
                        elif client_data["action_type"] == "Card_Reservation":
                            game.card_reservation(client_data["player_id"], client_data["action_data"], client_data["action_data"]["chips_to_give_away"])
                        elif client_data["action_type"] == "Chips_Consumption":
                            game.chips_consumption(client_data["action_data"], client_data["player_id"])
                        elif client_data["action_type"] == "players_name_entry":
                            game.name_enter(client_data["player_id"], client_data["action_data"])

                conn.sendall(pickle.dumps(game_data))
                game.data_updated = False
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

cards = {
        0: {
            0: None,
            1: None,
            2: None,
            3: None,
        },
        1: {
            0: None,
            1: None,
            2: None,
            3: None,
        },
        2: {
            0: None,
            1: None,
            2: None,
            3: None,
        },
    }

game_shuffle = True

while True:

    conn, addr = s.accept()
    idCount += 1
    gameId = (idCount - 1)// 4
    p = idCount - 4 * gameId
    if idCount % 4 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
        if game_shuffle:
            game = games[gameId]
            game.shuffle_cards_and_queue()
            game.set_game_aristocrats()
            # game_shuffle = False
        for row in range(3):
            for column in range(4):
                cards[row][column] = game.cards[row][column]
    else:
        games[gameId].ready = True
        game_shuffle = True

    start_new_thread(threaded_client, (conn, p, gameId, cards))