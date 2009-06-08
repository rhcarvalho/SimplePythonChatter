File Bot for Python LAN Chat


** What's this?

	This file bot can serve text files to the main chat channel upon receiving commands from the users.
	You can use this bot to host often referenced material like channel rules, FAQ's, links and the like.


** How do I run a FileBot?

	Open Bot.py in a text-editor (like Notepad, Gedit, Kedit, vim, emacs, etc.) and change the last line:

	from: runReactor("localhost", 2727, log, "FileBot", msg)
	to: runReactor("host to connect to", port, log (don't change this), "FileBotName", msg (don't change this))

	After you've done that, save the file and open a terminal. Once you're there, travel to the place 
	you've copied the bot to and type 'python Bot.py' (on Linux) or 'python.exe Bot.py' (on Windows)
	and press enter. The bot will then run and try to connect to the server specified in Bot.py.

	If the login was succesful you will see the bot's name apear in the client's user list and you will
	see that it's listening in the terminal.

** Which commands can I use when the FileBot is running?

	There are currently two commands that you can use when the FileBot is active in a channel. From your client,
	send a message beginning with the word LIST and the bot will send a list of available files. You can simply
	add files to the 'shared/' directory and they will automatically show up.
	
	Each filename is preceded by a number. This number is the fileID. You can use this fileID to get the FileBot
	to send a specific file by using the GET command followed by the ID. For instance, if the FileBot sends back this 
	list after the LIST command:
		
		1.	channelRules.txt
		2.	FAQ.txt
		3.	it_was_a_dark_and_stormy_night.txt

	You can retreive the first file by typing 'GET 1'. The FileBot should then send the contents of channelRules.txt
	back to the channel. 
