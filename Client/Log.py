import time
from clientVars import *
from privateMessage import *

class Log:
	pid = 0;
	
	def __init__(self, textbuffer, view, msgObject):
		self.textbuffer = textbuffer
		self.view = view
		self.view.set_buffer(self.textbuffer)
		self.privateLogs = []
		self.messages = msgObject
		
	def dumplog(self):
		##save??
		self.pid = self.pid + 1
		
	def log(self, msg, style = LOG_INFO):
		
		if style == LOG_INFO: 
			color = "gray"
		elif style == LOG_RECV: 
			color = "black"
		elif style == LOG_SEND: 
			color = "orange"
		elif style == LOG_ERR: 
			color = "red"
		elif style == LOG_CONN: 
			color = "gray"
		elif style == LOG_SERVER:
			color = "blue"
		elif style == LOG_MSG:
			color = "blue"
		elif style == LOG_PM_SENT:
			color = "blue"
		elif style == LOG_PM_RECV:
			color = "black"
		
		iter = self.textbuffer.get_end_iter()
		offset = iter.get_offset()
		
		if style == LOG_MSG:
			self.textbuffer.insert(iter, time.ctime() + " >>> " + msg + "\n")
		elif style == LOG_PM_RECV:
			self.textbuffer.insert(iter, ">>> "  + msg + "\n")
		elif style == LOG_PM_SENT:
			self.textbuffer.insert(iter, "<<< "  + msg + "\n")
		else:
			self.textbuffer.insert(iter, msg + "\n")
		startiter = self.textbuffer.get_iter_at_offset(offset)
		enditer = self.textbuffer.get_end_iter()
		tag = self.textbuffer.create_tag(None, foreground = color)
		self.textbuffer.apply_tag(tag, startiter, enditer)
		
		self.view.scroll_to_mark(self.textbuffer.get_insert(),0)

		self.dumplog()
		
	def addPrivateLog (self, user, textview, textbuffer):
		self.privateLogs.append([user, textview, textbuffer])
		
	def plog(self, username, msg, style=LOG_INFO):

		windowOpen = False
		for logs in self.privateLogs:
			if logs[0] == username:
				windowOpen = True
				oldtb = self.textbuffer
				oldview = self.view
				self.view = logs[1]
				self.textbuffer = logs[2]
				self.log(msg, style)
				self.textbuffer = oldtb
				self.view = oldview
		if windowOpen == False:
			pm = privateMessage(username, self.messages, self)
			self.plog(username, msg, style)
