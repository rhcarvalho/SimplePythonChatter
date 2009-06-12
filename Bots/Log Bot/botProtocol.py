from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import gtk2reactor
gtk2reactor.install()
from twisted.internet import reactor, defer
from clientVars import *
from Messages import Messages
from urllib import quote_plus, unquote_plus
from Users import Users, User

class clientProtocol(Protocol):

	def connectionMade(self):
		self.factory.log.log("You are connected to the server!\n", LOG_CONN)
		self.init = True
		self.message = 0;
		self.pm = 0;
		d = self.sendMessages();
		d.addCallback(self.sendMessages);


	def dataReceived(self, data):
		if self.init:
			self.factory.log.log("********** SERVER MESSAGE **********", LOG_SERVER)
			block = data.split("\r\n\r\n")
			welcome = block[0]
			self.factory.log.log(welcome, LOG_SERVER)

			connData = block[1]
			connData = connData.split("\r\n");
			for lines in connData:
				if lines[0:3] == "UID":
					params = lines.split(" ")
					self.factory.Users.usersEver = params[2]
					self.factory.Users.usersOnline = params[3]
					self.factory.Users.addUser(params[1], self.factory.alias)
			self.factory.log.log("There are currently " + params[3] + " users online. This server had " + params[2] + " logins\n", LOG_SERVER)
			self.factory.log.log("********** JOINING CHAT **********", LOG_INFO)
			self.sendMsg("USER "  + self.factory.alias)
			self.init = False
		else:
			if data[0:7] == "USER OK":
				self.factory.log.log("You've succesfully authenticated yourself on the server\n", LOG_INFO)
				self.sendMsg("JOIN CHAT")
			elif data[0:9] == "JOIN CHAT":
				block = data.split("\r\n\r\n")
				params = block[0].split(" ")
				try:
					ID = params[3]
				except:
					self.factory.log.log("You've joined the chat as " + self.factory.alias + "\n", LOG_INFO)
					return
				try:
					name = params[4]
					name = name.split("\n")
					self.factory.log.log(name[0] + " joined the chat!" , LOG_RECV)
					if name[0] == self.factory.alias:
						self.sendMsg("USERLIST")
				except:
					name[0] = "NameNotSet";
				self.factory.Users.addUser(ID, name[0], True)
			elif data[0:8] == "USERLIST":
				lines = data.split("\r\n");
				for block in lines:
					params = block.split("\t")
					try:
						ID = params[1]
					except:
						ID = -1;
					try:
						name = params[2]
					except:
						name = "NameNotSet";
					self.factory.Users.addUser(ID, name, True);
			elif data[0:8] == "CONN UID":
				params = data.split(" ")
			elif data[0:8] == "EXIT UID":
				data = data.split("\n")
				data = data[0]
				params = data.split(" ")
				try:
					ID = params[2]
					name = self.factory.Users.getName(ID)
					if name != "Unknown User":
						self.factory.log.log(name + " left the premises", LOG_RECV);
						self.factory.Users.removeUser(ID)
				except:
					params = ""
			elif data[0:6] == "MSG PM":
				block = data.split("\n")
				params = block[0].split(" ")
				fromUser = params[2]
				toUser = params[3]
				msg = unquote_plus(params[4])
				if self.factory.alias != fromUser:
					self.factory.log.log(fromUser + " >>> " + msg, LOG_PM_RECV)
				else:
					self.factory.log.log(toUser + " <<<" +  msg, LOG_PM_SENT)

			elif data[0:13] == "MSG CHAT UID ":
				block = data.split("\r\n\r\n")
				params = block[0].split(" ")
				msg = params[4].split("\r\n");
				msg = msg[0]
				msg = unquote_plus(msg)
				if msg[0:3] == "/me":
					self.factory.log.log(self.factory.Users.getName(params[3]) + msg[3:], LOG_MSG)
				else:
					self.factory.log.log(self.factory.Users.getName(params[3]) + " >>> " + msg, LOG_MSG)
			elif data[0:8] == "GAME OK ":
				block = data.split("\r\n\r\n")
				params = block[0].split(" ")
				try:
					m = params[2]
					self.factory.log.log("Current server map is: " + unquote_plus(m))
					f = open("maps/knownmaps")
					knownmaps = f.read()
					maps = knownmaps.split("\n")
					mFound = False
					self.map = m
					for map in maps:
						if map == m:
							self.factory.log.log("Your map is up to date!")
							mFound = True
							f.close()
					if not mFound:
						self.factory.log.log("Retreiving map..")
						f.close()
						self.sendMsg("MAP")
				except:
					self.factory.log.log("Couldn't verify which map is in use", LOG_ERR)
			elif data[0:7] == "MAP OK ":
				map = data.split("\r\n\r\n")
				map = map[0]
				map = map[7:]
				f = open ("maps/" + self.map, "w")
				f.write(map)
				f.close()
				f = open("maps/knownmaps", "a")
				f.write(self.map + "\n")
				f.close()
				self.factory.log.log(self.map + " has been updated!")
			else:
				self.factory.log.log("[" + str(self.factory.pid) + "] " +data, LOG_ERR)

	def connectionLost(self, reason):
		self.factory.log.log("\n\n===Lost connection to the server ===", LOG_CONN);
		self.factory.Users.clear()

	def sendMessages(self):
		d = defer.Deferred()
		msglen = len(self.factory.messages.messages);
		pmlen = len(self.factory.messages.privateMessages);
		if msglen != self.message:
			while self.message != msglen:
				m = self.factory.messages.messages[self.message]
				if m[0:9] != "/COMMAND ":
					self.sendMsg("MSG CHAT " + quote_plus(m))
				else:
					self.sendMsg(m[9:])
				self.message = self.message + 1
			d.callback("SEND MESSAGES")
		elif pmlen != self.pm:
			while self.pm != pmlen:
				prim = self.factory.messages.privateMessages[self.pm];
				msg = prim[0]
				to = prim[1]
				self.sendMsg("MSG PM " + quote_plus(to) +" " + quote_plus(msg))
				self.pm = self.pm + 1
			d.callback("SEND MESSAGES")
		reactor.callLater(CHECK_FOR_MESSAGES_TO_SEND_TIMEOUT, self.sendMessages);
		return d;

	def sendMsg(self, msg):
		self.factory.pid += 1
		self.transport.write(msg + "\r\n\r\n")

class clientProtocolFactory(ClientFactory):

	protocol = clientProtocol

	def __init__(self, log, alias, msgObject):
		self.log = log
		self.messages = msgObject
		self.alias = alias
		self.pid = 1
		self.Users = Users();
		self.Users.addUser("1", alias);

	def clientConnectionFailed(self, reason, bla):
		self.log.log("Couldn't connect...\n", LOG_ERR)

def runReactor(host, port, log, alias, msgObject):
	f = clientProtocolFactory(log, alias, msgObject)
	reactor.connectTCP(host, port, f)
	reactor.run()

def stopReactor():
	reactor.stop()

