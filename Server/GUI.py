# -*- coding: utf-8 -*-
import pygtk
pygtk.require('2.0')
import gtk

from serverVars import *
from serverVars import _


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

        label = gtk.Label(_("Port:"))
        label.set_justify(gtk.JUSTIFY_LEFT)
        table.attach(label, 0, 1, 0, 1)
        label.show()
        label = gtk.Label(_("Welcome message:"))
        label.set_justify(gtk.JUSTIFY_LEFT)
        table.attach(label, 0, 1, 1,2)
        label.show()
        label = gtk.Label(_("Game Map:"))
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

        button = gtk.Button(_("Start Service"))
        button.connect("clicked", self.startService, porttext, textbuffer, textbufferWelcome)
        table.attach(button, 2,3,0,1, gtk.FILL,0)
        button.show()

        button = gtk.Button(_("Browse"))
        button.connect("clicked", self.startService, porttext, textbuffer)
        table.attach(button, 2,3,2,3, gtk.FILL,0)
        button.show()

        frame1 = gtk.Frame(_("Server options"))
        frame1.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        frame1.set_label_align(0.0, 0.0)
        table.attach(frame1,0,4,0,3)
        frame1.show()


        frame2 = gtk.Frame(_("Log options"))
        frame2.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        frame2.set_label_align(1.0, 0.0)
        table.attach(frame2, 4,7,0,3)
        frame2.show()

        label = gtk.Label(_("Display options:"))
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
