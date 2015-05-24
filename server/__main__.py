from server.error import Error
from server.game import Game
from server.player import *
from server.servercode import Server

__author__ = 'Wes'

if __name__ == "__main__":
    GAME = Game([])
    SERVER = Server()

    def input_type(client):
        options = ''
        for type_str in PlayerType.types:
            options += '\n* ' + type_str

        GAME.client_prompt(client, "Input your player type, here are your options", options)

        actual_type = PlayerType.from_string(type)

        if actual_type == PlayerType.INVALID:
            client.write('Your input was invalid, try again')
            input_type(client)

    def client_connect(client):
        print('Client Connected, making player')
        name = GAME.client_prompt(client, "Input your username")
        if name == Error.READING:
            print(Error.READING)
            name = "user"

        GAME.add_player(Player(name, client, input_type(client)))
        print("Player added " + name)

    SERVER.newCliSig.connect(client_connect)

    while True:
        GAME.turn()

