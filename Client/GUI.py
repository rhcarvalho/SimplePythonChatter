# -*- coding: utf-8 -*-
## Python Chat and Game server client
## Written by Bart Spaans, Sep 2007
## See http://www.onderstekop.nl/coding/ for more scripts

#GUI libraries;
#See http://www.pygtk.org/ for documentation
import pygtk
pygtk.require('2.0')
import gtk

#Import protocol to start and stop connections and send messages
from clientProtocol import *

#Global macros
from clientVars import *
from clientVars import _

from Log import *
from userPanel import userPanel
import os
from privateMessage import *

## The Client's Graphical User Interface (GUI) is managed here (PyGTK+2,0)
class GUI:

    ##The constructor class
    def __init__(self, msgObject):
        self.messages = msgObject
        self.toggleDisabled = []

        #initiate the container window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_icon(gtk.gdk.pixbuf_new_from_file_at_size("user_icon.gif", 14, 16))
        self.window.set_resizable(True)
        self.window.connect("destroy", self.close_application)
        self.window.set_title(APP_NAME + " " + APP_VERSION)
        self.window.set_border_width(20)

        #adding widgets
        self.table = gtk.Table(18, 6, True)
        self.makeLabels()
        self.makeEntries()
        self.makeButtons()
        self.makeTextArea()
        self.makeFrames()
        self.makeTreeViews()
        self.window.add(self.table)

        #make the widgets visible
        self.table.show()
        self.window.show()

    ##Adds a number of labels to the widget table
    def makeLabels(self):
        labels = [_("Server:"), _("Port:"), _("Alias:")]
        a = 1
        for label in labels:
            l = gtk.Label(label)
            self.table.attach(l, 0, 1, a, a + 1)
            l.show()
            a = a + 1

    ##Adds a number of entries (textfields) to the widget table.
    def makeEntries(self):
        self.hostText = gtk.Entry()
        self.hostText.set_text("localhost")
        self.table.attach(self.hostText, 1, 3, 1, 2)
        self.hostText.show()

        self.portText = gtk.Entry()
        self.portText.set_text("2727")
        self.table.attach(self.portText, 1, 2, 2, 3)
        self.portText.show()

        self.aliasText = gtk.Entry()

        try:
            name = os.environ["USERNAME"]
        except:
            name = "Anonymous"
        self.aliasText.set_text(name)
        self.table.attach(self.aliasText, 1, 3, 3, 4)
        self.aliasText.show()

        self.msgText = gtk.Entry()
        self.msgText.connect("key-press-event", self.pressedMsgKey)
        self.table.attach(self.msgText, 0, 3, 17, 18)
        self.msgText.show()

    def pressedMsgKey(self, widget, event):
        if event.keyval == 65293:
            self.sendMessage("")



    ## Add and display Connect and Send buttons
    def makeButtons(self):
        b = gtk.Button(_("Connect"))
        b.connect("clicked", self.startService)
        self.table.attach(b, 2, 3, 2, 3)
        b.show()
        self.connectButton = b

        b = gtk.Button(_("Disconnect"))
        b.connect("clicked", self.stopService)
        self.table.attach(b, 3, 4, 2, 3)
        b.show()
        self.connectButton = b

        b = gtk.Button(_("Send"))
        b.connect("clicked", self.sendMessage)
        self.table.attach(b, 3, 4, 17, 18)
        b.show()
        self.sendButton = b


    ## Add the chat text area
    def makeTextArea(self):
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        sw.set_shadow_type(gtk.SHADOW_IN)
        textview = gtk.TextView()
        textview.set_editable(False)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        self.textbuffer = textview.get_buffer()
        self.log = Log(self.textbuffer, textview, self.messages)
        sw.add(textview)
        sw.show()
        textview.show()
        self.table.attach(sw, 0, 4, 5, 17)

    ##Adds a little layout frames
    def makeFrames(self):
        f = gtk.Frame(_("Client options"))
        f.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        f.set_label_align(0.0, 0.0)
        self.table.attach(f, 0, 4, 0, 5)
        f.show()

        f = gtk.Frame(_("Chat"))
        f.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        f.set_label_align(0.0, 0.0)
        self.table.attach(f, 0, 4, 5, 18)
        f.show()

        f = gtk.Frame(_("Users"))
        f.set_shadow_type(gtk.SHADOW_ETCHED_OUT)
        f.set_label_align(0.0, 0.0)
        self.table.attach(f, 4, 6, 0, 18)
        f.show()

    def makeTreeViews(self):
        self.treestore = gtk.TreeStore(str)
        self.tm = gtk.TreeModelSort(self.treestore)
        self.tm.set_sort_column_id(0, gtk.SORT_ASCENDING)

        self.treeview = gtk.TreeView(self.tm);
        self.tvcolumn = gtk.TreeViewColumn(_('Online Users'))
        self.treeview.append_column(self.tvcolumn)

        self.cell = gtk.CellRendererText()
        self.treeview.set_headers_clickable(True)
        self.treeview.connect("button_press_event", self.treeviewCallback, None)
        self.cellpb = gtk.CellRendererPixbuf()
        self.tvcolumn.pack_start(self.cellpb, True)
        self.tvcolumn.pack_start(self.cell, False)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)
        self.tvcolumn.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        self.tvcolumn.set_cell_data_func(self.cellpb, self.userImage)
        self.tvcolumn.set_sort_column_id(0)

        scrolled = gtk.ScrolledWindow()
        scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        scrolled.set_shadow_type(gtk.SHADOW_IN)
        scrolled.add(self.treeview)

        self.table.attach(scrolled, 4, 6, 1, 14, gtk.FILL, gtk.FILL, 20)
        self.table.show_all()

        self.userPanel = userPanel(self.treestore)

    ## Gets called when the user double clicked someone from the user panel
    def treeviewCallback(self, treeview, event, data=None):
        if event.type == gtk.gdk._2BUTTON_PRESS:
            x = int(event.x)
            y = int(event.y)

            treeselection = self.treeview.get_selection()
            (model, treeiter) = treeselection.get_selected()
            treeiter = self.tm.convert_iter_to_child_iter(None, treeiter)
            name = self.treestore.get_value(treeiter, 0)
            if name[0:5] != _(" ID: ") and name[0:14] != _(" Known Since: "):
                pm = privateMessage(str(name[2:]), self.messages, self.log)


    ## Event function that gets called when the client has clicked the connect button
    def startService(self, widget):
        host = self.hostText.get_text()
        port = int(self.portText.get_text())
        alias = self.aliasText.get_text()
        self.log.log(_("******** PRE-CONNECTION INFO *********"))
        self.log.log(_("%s is trying to connect to %s at port %s") % (APP_NAME, host, port))
        self.log.log(_("You are logging in under the name %s\n") % (alias,))
        self.log.log(_("********** CONNECTION INFO ***********"), LOG_CONN)
        runReactor(host, port, self.log, alias, self.messages, self.userPanel)

    ## Event function that gets called when the client has clicked the disconnect button
    def stopService(self, widget):
        self.log.log(_("****** DISCONNECTED FROM SERVER ******"))
        stopReactor()

    ## Event function that gets called when the client has clicked the send button
    def sendMessage(self, widget):
        msg = self.msgText.get_text()
        if msg != "":
            self.messages.addmsg(msg)
            self.msgText.set_text("")

    ## Function that gets called when the GUI is exited
    def close_application(self, widget):
        if REACTOR_RUNNING:
            stopReactor()
        gtk.main_quit()

    def userImage(self, column, cell, model, iter):
        pb = gtk.gdk.pixbuf_new_from_file_at_size("user_icon.gif", 14, 16)
        cell.set_property('pixbuf', pb)
        return


def startGUI(msgObject):
    GUI(msgObject)
    gtk.main()
    return 0
