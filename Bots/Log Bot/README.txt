Log Bot for Python LAN Chat


** What's this?

	This bot can keep a log of the conversation.


** How do I run a LogBot?

	Open Bot.py in a text-editor (like Notepad, Gedit, Kedit, vim, emacs, etc.) and change the last line:

	from: runReactor("localhost", 2727, log, "FileBot", msg)
	to: runReactor("host to connect to", port, log (don't change this), "FileBotName", msg (don't change this))

	After you've done that, save the file and open a terminal. Once you're there, travel to the place 
	you've copied the bot to and type 'python Bot.py' (on Linux) or 'python.exe Bot.py' (on Windows)
	and press enter. The bot will then run and try to connect to the server specified in Bot.py.

	If the login was succesful you will see the bot's name apear in the client's user list and you will
	see that it's listening in the terminal.

	The bot will save all output to the file log.txt, but you could off course change this (see Log.py)
