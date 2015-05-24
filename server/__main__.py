from server.error import Error
from server.game import Game
from server.player import *
from server.servercode import Server

__author__ = 'Wes'

if __name__ == "__main__":
    GAME = Game([])
    SERVER = Server()

    def client_connect(client):
        name = GAME.prompt(client, "Input your username")
        if name == Error.READING:
            print(Error.READING)
            name = "user"

        def input_type():
            options = ''
            for type_str in PlayerType.types:
                options += '\n* ' + type_str

            GAME.prompt(client, "Input your player type, here are your options", options)

            actual_type = PlayerType.from_string(type)

            if actual_type == PlayerType.INVALID:
                client.write("print('Your input was invalid, try again')")
                input_type()

        GAME.add_player(Player(name, client, input_type()))
        print("Player added " + name)

    SERVER.newCliSig.connect(client_connect)

    while True:
        GAME.turn()

