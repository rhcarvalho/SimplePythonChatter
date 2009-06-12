# -*- coding: utf-8 -*-
from datetime import datetime


class _User:
    """Represent an user"""
    def __init__(self, id, name):
        """Create a user"""
        self.id = id
        self.name = name
        self.created = datetime.now()


class _UserManager:
    """Manage a group of users"""
    __id_counter = 0

    def __init__(self):
        """Create a new UserManager"""
        self.users = {}

    def add(self, name):
        """Add a new user registered under the given name."""
        id = self.getID()
        self.users[id] = User(id, name)

    def remove(self, id):
        """Remove the user registered under the given id.

        Will pass silently if there is no user with the given id.
        """
        self.users.pop(id, None)

    def getID(self):
        """Return an appropriate id for a new user"""
        self.__id_counter += 1
        return self.__id_counter


class User:

    def __init__(self, ID):
        self.name = ""
        self.loggedIN = False
        self.online = True
        self.ID = ID


class Users:

    def __init__(self):
        self.numUser = 0
        self.users = []
        self.cID = 1000

    def addUser(self):
        ID = self.cID
        self.cID += 1
        self.numUser += 1
        self.users.append(User(ID))
        return ID

    def remUser(self, ID):
        for user in self.users:
            if user.ID == ID:
                user.loggedIn = False
                user.online = False
        self.numUser -= 1

    def regUsers(self):
        return self.cID - 1000

    def addName(self, ID, name):
        for user in self.users:
            if user.name == name and user.loggedIn == True:
                return False
        for user in self.users:
            if user.ID == ID:
                user.name = name
                user.loggedIn = True
                return True
