import PyQt5.QtCore
import time
from server.error import Error
from server.player import *
from server.servercode import Server

__author__ = 'Wes'

if __name__ == "__main__":
    def input_type(client):
        options = ''
        for type_str in PlayerType.get_types_str():
            options += '\n* ' + type_str

        str_type = GAME.client_prompt(client, "Input your player type, here are your options", options)

        actual_type = PlayerType.NORMAL

        if str_type != Error.READING:
            print(Error.READING)
            actual_type = PlayerType.from_string(str_type)
        else:
            print(Error.READING)

        if actual_type == PlayerType.INVALID:
            client.write('Your input was invalid, try again')
            input_type(client)

    def client_connect(client):
        print('Client Connected, making player')
        client.write('We are now going to begin making a player')
        name = GAME.client_prompt(client, "Input your username")
        if name == Error.READING:
            print(Error.READING)
            name = "user"

        GAME.add_player(Player(name, client, input_type(client)))
        print("Player added " + name)

    GAME = Game([])
    SERVER = Server(client_connect)

    while True:
        GAME.turn()
        time.sleep(1)

