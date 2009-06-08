#!/usr/bin/env python
import time
import pygtk
pygtk.require('2.0')
import gtk
from twisted.internet.protocol import Protocol, Factory
from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor
from User import User
from Users import Users

#APP VARIABLES
APP_NAME = "Python LAN Chat Server"
APP_VERSION = "1.1"

#LOG Variables
LOG_INFO = 1
LOG_SEND = 2
LOG_RECV = 3
LOG_ERR = 4
LOG_CONN = 5
LOG_SERVER = 6

#BROADCAST Message variables
BROADCAST_EVERYBODY = 1
BROADCAST_CHAT = 2
BROADCAST_GAME = 3
BROADCAST_PM = 4

#PATHs
PATH_WELCOME_MSG = "serverData/welcome.msg"
PATH_DEFAULT_MAP_NAME = "Militia"
PATH_DEFAULT_MAP = "serverData/default.map"


class RPG(Protocol):

    def connectionMade(self):
        ID = self.factory.users.addUser()
        onlineUsers = self.factory.users.numUser
        registeredUsers = self.factory.users.regUsers()
        addText(self.factory.textbuffer,"Established connection UID " + str(ID) + "\n", LOG_CONN)

        IP = self.transport.getPeer()
        IP = IP.host
        welcome = self.factory.welcome
        msg = "UID " + str(ID) + " " + str(registeredUsers) + " " + str(onlineUsers) + " " + IP
        msg2 = "Currently there are " + str(onlineUsers) + " users online and " + str(registeredUsers) + " known users. " + time.ctime() + " Last user connected: " + str(ID) + " (" + IP + ")"
        welcome += "\r\n\r\n" + msg +"\r\n"
        self.transport.write(welcome)

        messageid = self.factory.statusbar[0].push(self.factory.statusbar[1], msg2)

        addText(self.factory.textbuffer,welcome, LOG_SEND)

        self.factory.clients.append(self)
        self.broadcast("CONN UID " + str(ID))

        self.ID = ID
        self.init = True
        self.inGAME = False
        self.inCHAT = False

    def dataReceived(self, data):
        if self.init:
            addText(self.factory.textbuffer, "UID" + str(self.ID) + " : " +  data, LOG_RECV)
            if data[0:4] != "USER":
                self.transport.loseConnection()
                addText(self.factory.textbuffer, "Dropping user UID " +str( self.ID) + " unknown protocol", LOG_ERR)
            else:
                data = data.split("\r\n")
                data = data[0].split(" ")
                try:
                    name = data[1]
                    if name == "":
                        self.transport.write("USER Fault"+ "\r\n")
                        addText(self.factory.textbuffer, "UID" + str(self.ID) + " USER Fault", LOG_ERR)
                    else:
                        if self.factory.users.addName(self.ID, name):
                            self.transport.write("USER OK\r\nchanged name to '" + name + "'\r\n")
                            self.name = name
                            addText(self.factory.textbuffer, "UID" + str(self.ID) + " changed his/her name to "  + name, LOG_SERVER)
                            self.broadcast("CONN UID " + str(self.ID) + " " + name)
                            self.init= False
                        else:
                            addText(self.factory.textbuffer, "UID" + str(self.ID) + " USER AlreadyExists " + name, LOG_ERR)
                            self.transport.write("USER AlreadyExists " + name + "\r\n")
                            self.transport.loseConnection()
                except:
                    self.transport.write("USER Fault"+ "\r\n")
                    addText(self.factory.textbuffer, "UID" + str(self.ID) + " USER Fault")

        else:
            addText(self.factory.textbuffer, str(self.name) + " : " +  data, LOG_RECV)
            self.checkCommands(data)

    def connectionLost(self, reason):
        self.factory.users.remUser(self.ID)
        ID = self.ID
        onlineUsers = self.factory.users.numUser
        registeredUsers = self.factory.users.regUsers()
        IP = self.transport.getPeer()
        IP = IP.host
        msg2 = "Currently there are " + str(onlineUsers) + " users online and " + str(registeredUsers) + " known users. " + time.ctime() + " Last user disconnected: " + str(ID) + " (" + IP + ")"
        messageid = self.factory.statusbar[0].push(self.factory.statusbar[1], msg2)
        addText(self.factory.textbuffer,"Lost connection: \n" + str(reason), LOG_CONN)
        self.broadcast("EXIT UID " + str(ID))
        self.factory.clients.remove(self)

    def broadcast(self, msg, broadcast = BROADCAST_EVERYBODY, to =""):
        if broadcast == BROADCAST_EVERYBODY:
            for c in self.factory.clients:
                c.message(msg)
        elif broadcast == BROADCAST_GAME:
            for c in self.factory.clients:
                if c.inGAME:
                    c.message(msg)
        elif broadcast == BROADCAST_CHAT:
            for c in self.factory.clients:
                if c.inCHAT:
                    c.message(msg)
        elif broadcast == BROADCAST_PM:
            for c in self.factory.clients:
                if c.name == to and c.inCHAT:
                    c.message(msg)
        addText(self.factory.textbuffer, msg, LOG_SERVER)

    def message(self, msg):
        self.transport.write(msg + "\n")

    def checkCommands(self, data):
        dataLineSplit = data.split("\r\n")
        dataLine = dataLineSplit[0]
        dataSpaceSplit = dataLine.split(" ")
        command = dataSpaceSplit[0].upper()

        if command == "QUIT":
            self.transport.loseConnection()
        elif command == "USERS":
            ID =self.ID
            onlineUsers = self.factory.users.numUser
            registeredUsers = self.factory.users.regUsers()

            IP = self.transport.getPeer()
            IP = IP.host

            msg = "USERS " + self.name + "UID " + str(ID) + " " + str(registeredUsers) + " " + str(onlineUsers) + " " + IP + "\r\n"
            self.transport.write(msg)
            addText(self.factory.textbuffer, self.name + " " +msg, LOG_SEND)
        elif command == "USERLIST":
            offline = False
            try:
                if  dataSpaceSplit[1].upper() == "OFFLINE":
                    offline = True
            except:
                offline = False
            msg = ""
            for user in self.factory.users.users:
                if user.online : online = "Online"
                else: online = "Offline"
                if offline:
                    msg += "USERLIST\t" + str(user.ID) +"\t" + user.name + "\t[" + online +"]\r\n"
                else:
                    if user.online:
                        msg += "USERLIST\t" + str( user.ID) +"\t" + user.name + "\t[" + online +"]\r\n"
            self.transport.write(msg)
            addText(self.factory.textbuffer, self.name + " " +msg + "\r\n", LOG_SEND)
        elif command == "SERV":
            msg = "SERV\r\nChat: main chat room and private messaging\r\nGame: retreive game maps"
            self.transport.write(msg + "\r\n\r\n")
            addText(self.factory.textbuffer, self.name + " " +msg, LOG_SEND)
        elif command == "GAME":
            nOU = 1;
            numberOfUsers = 5;
            if nOU < numberOfUsers:
                msg = "GAME OK " + PATH_DEFAULT_MAP_NAME
            else:
                msg = "GAME Fault TooManyUsers"
            self.transport.write(msg + "\r\n\r\n")
            addText(self.factory.textbuffer, self.name + " " +msg, LOG_SEND)
        elif command == "JOIN":
            try:
                serv = dataSpaceSplit[1].upper()
                if serv == "GAME":
                    self.inGAME = True
                    self.transport.write("JOIN GAME OK 20 20")
                    self.broadcast("JOIN GAME UID " + str(self.ID) + " " +self.name, BROADCAST_GAME)
                    addText(self.factory.textbuffer, self.name + " joined the game", LOG_SERVER)
                elif serv == "CHAT":
                    self.inCHAT = True
                    self.broadcast("JOIN CHAT UID " + str(self.ID) + " " +self.name, BROADCAST_CHAT)
                    addText(self.factory.textbuffer, self.name + " joined the chat", LOG_SERVER)
            except:
                msg = "JOIN Fault ServiceNotKnown"
                self.transport.write(msg + "\r\n\r\n")
                addText(self.factory.textbuffer, self.name + " " + msg, LOG_ERR)
        elif command == "MAP":
            path = PATH_DEFAULT_MAP
            f = open (path, "r")
            msg = f.read()
            self.transport.write("MAP OK " + msg + "\r\n\r\n")
            addText(self.factory.textbuffer, self.name + " " +msg, LOG_SEND)
        elif command == "MSG":
            try:
                serv =dataSpaceSplit[1].upper()
                msg = dataSpaceSplit[2]

                if serv == "GAME":
                    if self.inGAME:
                        self.broadcast("MSG GAME UID " + str(self.ID) + " " + msg + "\r\n", BROADCAST_GAME)
                        addText(self.factory.textbuffer, self.name + " is sending a GAME message: " + msg, LOG_INFO)
                    else:
                        self.transport.write("MSG Fault NotInGame\r\n")
                        addText(self.factory.textbuffer, self.name + " tried to send a GAME message but wasn't in a GAME", LOG_ERR)
                elif serv == "CHAT":
                    if self.inCHAT:
                        self.broadcast("MSG CHAT UID " + str(self.ID) + " " + msg + "\r\n", BROADCAST_CHAT)
                        addText(self.factory.textbuffer, self.name + " is sending a CHAT message: " + msg, LOG_INFO)
                    else:
                        self.transport.write("MSG Fault NotInChat\r\n")
                        addText(self.factory.textbuffer, self.name + " tried to send a CHAT message but wasn't in a CHAT", LOG_ERR)
                elif serv == "PM":
                    addText(self.factory.textbuffer, "PM message..", LOG_INFO)
                    if self.inCHAT:
                        to = dataSpaceSplit[2]
                        msg =  dataSpaceSplit[3]
                        self.message("MSG PM " + self.name + " " + to + " " + msg)
                        self.broadcast("MSG PM " + self.name + " "+ to + " " + msg, BROADCAST_PM, to)
            except:
                self.transport.write("MSG Fault ServiceNotKnown\r\n")
                addText(self.factory.textbuffer, self.name + " tried to send a message to unknown service (" + serv + ")", LOG_ERR)
        else:
            msg = "FAULT Unknown command " +  command
            self.transport.write(msg + "\r\n")
            addText(self.factory.textbuffer, self.name + " " +msg, LOG_SEND)


def addText(textbuffer, text, log=LOG_INFO):
    oldtext = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter())
    if text[-1:] != "\n":
        text += "\n"
    if log == LOG_INFO:
        identifier = "[INFO]"
        color = "#008800"
    elif log == LOG_RECV:
        identifier = "[RECV]"
        color = "blue"
    elif log == LOG_SEND:
        identifier = "[SEND]"
        color = "orange"
    elif log == LOG_ERR:
        identifier = "[ERR]"
        color = "red"
    elif log == LOG_CONN:
        identifier = "[CONN]"
        color = "purple"
    elif log == LOG_SERVER:
        identifier = "[SERVER]"
        color = "#aa0000"

    identifier += " "

    startiter =  textbuffer.get_end_iter().get_offset()

    textbuffer.insert(textbuffer.get_iter_at_offset(startiter), identifier +time.ctime() + " " + text)
    startiter = textbuffer.get_iter_at_offset(startiter)
    enditer = textbuffer.get_end_iter()

    tag = textbuffer.create_tag(None, foreground = color)
    textbuffer.apply_tag(tag, startiter, enditer)


class GUI:
    def startService(self, widget, porttext, textbuffer, wtextbuffer):
        welcome = wtextbuffer.get_text(wtextbuffer.get_start_iter(), wtextbuffer.get_end_iter())
        startService(textbuffer,int(porttext.get_text()), welcome, (self.statusbar, self.context_id))

    def close_application(self, widget):
        try:
            reactor.stop()
        except:
            pass
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_resizable(True)
        self.window.connect("destroy", self.close_application)
        self.window.set_title(APP_NAME + " " + APP_VERSION)
        self.window.set_border_width(20)

        table = gtk.Table(11,7,True)
        self.window.add(table)

        label = gtk.Label("Port:")
        label.set_justify(gtk.JUSTIFY_LEFT)
        table.attach(label, 0, 1, 0, 1)
        label.show()
        label = gtk.Label("Welcome message:")
        label.set_justify(gtk.JUSTIFY_LEFT)
        table.attach(label, 0, 1, 1,2)
        label.show()
        label = gtk.Label("Game Map:")
        label.set_justify(gtk.JUSTIFY_LEFT)
        table.attach(label, 0, 1, 2, 3)
        label.show()

        f=open(PATH_WELCOME_MSG)
        welcomemsg = f.read()
        f.close()

        welcome = gtk.ScrolledWindow()
        welcome.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        welcome.set_shadow_type(gtk.SHADOW_IN)
        textview = gtk.TextView()
        textbufferWelcome = textview.get_buffer()
        textbufferWelcome.set_text(welcomemsg)
        welcome.add(textview)
        welcome.show()
        textview.show()
        table.attach(welcome, 1,4, 1, 2,gtk.FILL ,gtk.FILL,10,0)

        porttext = gtk.Entry(6)
        porttext.set_text("2727")
        table.attach(porttext, 1,2,0,1)
        porttext.show()

        map = gtk.Entry()
        map.set_text(PATH_DEFAULT_MAP)
        table.attach(map, 1,2,2,3)
        map.show()

        sw =gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        sw.set_shadow_type(gtk.SHADOW_IN)
        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_border_width(2)
        textbuffer = textview.get_buffer()
        sw.add(textview)
        sw.show()
        textview.show()
        table.attach(sw, 0, 7, 4, 10)

        button = gtk.Button("Start Service")
        button.connect("clicked", self.startService, porttext, textbuffer, textbufferWelcome)
        table.attach(button, 2,3,0,1, gtk.FILL,0)
        button.show()

        button = gtk.Button("Browse")
        button.connect("clicked", self.startService, porttext, textbuffer)
        table.attach(button, 2,3,2,3, gtk.FILL,0)
        button.show()

        frame1 = gtk.Frame("Server options")
        frame1.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        frame1.set_label_align(0.0, 0.0)
        table.attach(frame1,0,4,0,3)
        frame1.show()


        frame2 = gtk.Frame("Log options")
        frame2.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        frame2.set_label_align(1.0, 0.0)
        table.attach(frame2, 4,7,0,3)
        frame2.show()

        label = gtk.Label("Display options:")
        table.attach(label, 4,5, 0,1)
        label.show()

        check1 = gtk.CheckButton("[INFO]")
        check2 = gtk.CheckButton("[RECV]")
        check3 = gtk.CheckButton("[SEND]")
        check4 = gtk.CheckButton("[CONN]")
        check5 = gtk.CheckButton("[ERR]")
        check6 = gtk.CheckButton("[SERVER]")
        table.attach(check1, 5,6,0,1)
        table.attach(check2, 6,7,0,1)
        table.attach(check3, 5,6,1,2)
        table.attach(check4, 6,7,1,2)
        table.attach(check5, 5,6,2,3)
        table.attach(check6, 6,7,2,3)
        check1.show()
        check2.show()
        check3.show()
        check4.show()
        check5.show()
        check6.show()

        self.statusbar = gtk.Statusbar()
        self.context_id = self.statusbar.get_context_id("Users")
        table.attach(self.statusbar, 0, 6, 10,11)
        self.statusbar.show()

        table.show()
        self.window.show()


def main():
    gtk.main()
    return 0


def startService(textbuffer,port, welcome, statusbar):
    addText(textbuffer, APP_NAME, LOG_INFO)
    addText(textbuffer, "Version " + APP_VERSION, LOG_INFO)
    addText(textbuffer, "Attempting to start server at port " +str(port)+ "\n", LOG_INFO)
    addText(textbuffer, "Creating Factory", LOG_INFO)

    factory = Factory()
    factory.protocol = RPG
    factory.textbuffer = textbuffer
    factory.statusbar = statusbar
    factory.clients = []

    addText(textbuffer, "Saving welcome message...", LOG_INFO)
    factory.welcome = welcome
    f = open(PATH_WELCOME_MSG, "w")
    f.write(welcome)
    f.close()
    addText(textbuffer, "Setting up Users datastructure", LOG_INFO)
    factory.users = Users()
    addText(textbuffer, "Listening for incoming connections...", LOG_INFO)
    reactor.listenTCP(port, factory)
    reactor.run()


GUI()
main()
