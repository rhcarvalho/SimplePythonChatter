===============================================================

	Simple Python Chatter

	written by Rodolfo Carvalho, 2009
	http://github.com/rhcarvalho/SimplePythonChatter


	based on the original

	Python LAN Chat

	written by Bart Spaans, 2007
	http://www.onderstekop.nl/

	Released under the GNU General Public License (GPL)

================================================================

This package contains:

	Simple Python Chatter Server
	Simple Python Chatter Client
	Simple Python Chatter File Bot
	Simple Python Chatter Log Bot

================================================================

FREQUENTLY ASKED QUESTIONS

================================================================

Q: I just want to connect to a server and chat, what do I need?

	You will only need to copy the Client directory and its contents. And run the Client.py file.

Q: How do I run .py files in Windows?

	Click 'Start', click 'Run', type 'cmd' and hit enter. A terminal will open. You will need to
	navigate to the directory where the .py file is located. For example, if you want to open
	C:\python\SPC\Client\Client.py you will need to type 'cd c:\python\SPC\Client' to enter
	the directory. Once you there type 'python.exe Client.py' and the .py should be running

Q: How do I run .py files in Linux?

	Open a terminal, navigate to the directory and run the .py file by typing ./Client.py (for instance).
	On most distros	you could also doubleclick the file and it will ask you to run it.

Q: I'm running the .py file but I'm getting an error?

	You need to have Python, GTK+ and Twisted installed to properly run Simple Python Chatter. On linux most of these
	packages are installed by default, but on Windows they aren't. You can see INSTALL.txt for more details.

	If you still receive errors, but have these programs installed leave me a message on http://github.com/rhcarvalho/SimplePythonChatter.

Q: How do I setup Simple Python Chatter on my own local network?

	Pick a PC that will run the server. This PC must be stable, because it will host the chat channel. Copy the Server directory
	and run Server.py. After changing some settings you can start the service. Your channel will now be available to other
	computers in your LAN with the Simple Python Chatter client (simply copy the Client directory and run Client.py)

