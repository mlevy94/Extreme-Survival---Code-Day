from server.game import Game
from server.player import *
from server.servercode import Server

__author__ = 'Wes'

if __name__ == "__main__":
    GAME = Game([])
    SERVER = Server()

    def client_connect(client):
        client.write("prompt('Input your username')")
        name = ''
        while name == '':
            name = client.read()

        def input_type():
            client.write("prompt('Input your player type, here are your options')")

            for type_str in PlayerType.types:
                client.write("print(* " + type_str + ")")

            type = ''
            while type == '':
                type = client.read()

            actual_type = PlayerType.from_string(type)

            if actual_type == PlayerType.INVALID:
                input_type()

        GAME.add_player(Player(name, client, input_type()))
        print("Player added " + name)

    SERVER.newCliSig.connect(client_connect)

    while True:
        GAME.turn()

