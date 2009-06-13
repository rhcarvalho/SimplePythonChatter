# -*- coding: utf-8 -*-
from twisted.internet import protocol, reactor, defer
from twisted.protocols.basic import LineReceiver

from users import UserManager


_ = lambda m: m


class SimpleChatProtocol(LineReceiver):

    def connectionMade(self):
        self.user = self.factory.newUser(self.transport.getPeer(), self.transport.write)

        defer.Deferred().addCallback(
            self.user.write, self.factory.welcome_message
        ).addCallback(
            self.announceNewUser, self.user
        ).addCallback(
            self.sendStats
        ).addCallback(
            self.factory.setStatusMessage
        )

    def connectionLost(self, reason):
        pass

    def lineReceived(self, line):
        pass

    def announceNewUser(self, user):
        for online_user in self.factory.user_manager.online_users:
            online_user.write("USER %s %s %s" % (user.id, user.name, user.ip))

    def sendStats(self):
        stats = self.factory.user_manager.stats
        online_users = stats['online_users']
        known_users = stats['known_users']
        self.transport.write("STATS %s %s" % (online_users, known_users))


class SimpleChatFactory(protocol.ServerFactory):
    protocol = SimpleChatProtocol

    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.welcome_message = _("Welcome to Simple Python Chatter")

    def newUser(self, peer, write):
        user = self.user_manager.new()
        user.ip = peer.host
        user.write = write
        return user

    def setStatusMessage(self, last_user):
        stats = self.factory.user_manager.stats
        online_users = stats['online_users']
        known_users = stats['known_users']
        status_message = (_("Currently there are %s users online and %s known "
                            "users.\nLast user connected at %s: UID=<%s>, IP=<%s>") %
                           (online_users, known_users, last_user.created, last_user.id, last_user.ip))
        print "[Status]", status_message


reactor.listenTCP(6666, SimpleChatFactory(UserManager()))
reactor.run()