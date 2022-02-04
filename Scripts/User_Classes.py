'''
@author Matthew Fuss

This file will define the classes required for the main user to interface with the device

'''
class Player:   
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        #self.stats = 0

class User:

    def __init__(self, name):
        #the user name should be the name of the coach
        self.name = name
        #initialize the players list as an empty list. The list will be updated later
        self.players = []

    def change_user_name(self, name):
        self.name = name

    def add_player(self, player):
        self.players.append(player)