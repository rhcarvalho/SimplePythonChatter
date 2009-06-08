#!/usr/bin/env python
#
#	Python Game and Chat client Bot Interface
#
#	Written by Bart Spaans, Sep-Oct 2007
#	http://www.onderstekop.nl/coding/p8_Python_Game_and_Chat_Client/
#
#	Extendable Bot Interface for use with the above mentioned Game and Chat server
#		

from clientVars import *
from Messages import *
from botProtocol import *
from Log import *

print APP_NAME, APP_VERSION, "started...\n"

msg = Messages();
log = Log(msg)


#change this last line. See README.txt for more information
runReactor("localhost", 2727, log, "LogBot", msg)

