# -*- coding: utf-8 -*-
from datetime import datetime


class User(object):
    """Represent an user"""
    def __init__(self, id, name):
        """Create a user"""
        self.id = id
        self.name = name
        self.ip = None
        self.created = datetime.now()

    def write(self, message):
        """Write a message to self"""


class UserManager(object):
    """Manage a group of users"""
    __id_counter = 0

    def __init__(self):
        """Create a new UserManager"""
        self.online_users = {}
        self.offline_users = {}

    def new(self, name=""):
        """Return a new user registered under the given name."""
        id = self.getID()
        user = User(id, name)
        self.offline_users[user.id] = user
        return user

    def login(self, id):
        """Login an existing offline user registered under the given id.

        Will pass silently if there is no offline user with the given id.
        """
        user = self.offline_users.pop(id, None)
        if user is not None:
            self.online_users[user.id] = user

    def logout(self, id):
        """Logout an existing online user registered under the given id.

        Will pass silently if there is no online user with the given id.
        """
        user = self.online_users.pop(id, None)
        if user is not None:
            self.offline_users[user.id] = user

    @property
    def stats(self):
        online_users = len(self.online_users)
        offline_users = len(self.offline_users)
        known_users = online_users + offline_users
        return dict(online_users=online_users,
                    offline_users=offline_users,
                    known_users=known_users)

    def getID(self):
        """Return an appropriate id for a new user"""
        self.__id_counter += 1
        return self.__id_counter