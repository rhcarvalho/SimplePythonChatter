import time
from clientVars import *

class Log:
	pid = 0;
	
	def __init__(self, msgObject):
		self.privateLogs = []
		self.messages = msgObject
	
	def log(self, msg, style = LOG_INFO):
		
		if style == LOG_INFO: 
			id = "[INFO]"
		elif style == LOG_RECV: 
			id = "[RECV]"
		elif style == LOG_SEND: 
			id = "[SEND]"
		elif style == LOG_ERR: 
			id = "[ERR]"
		elif style == LOG_CONN: 
			id = "[CONN]"
		elif style == LOG_SERVER:
			id = "[SERV]"
		elif style == LOG_MSG:
			id = "[MSG]"
		elif style == LOG_PM_SENT:
			id = "[PM_S]"
		elif style == LOG_PM_RECV:
			id = "[PM_R]"
		print id + " " + msg + "\n"
		
