#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Python Game and Chat client
#
#    Written by Bart Spaans, Sep-Oct 2007
#    http://www.onderstekop.nl/coding/p8_Python_Game_and_Chat_Client/
#
#    Keep checking for new updates (automatic updating has not been covered yet
#    because this version is still very buggy
#

from clientVars import *
from clientVars import _
from GUI import *
from Messages import *

print APP_NAME, APP_VERSION, _("started...\n")

msg = Messages()
startGUI(msg)
