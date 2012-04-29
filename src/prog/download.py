#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import threading
import random, time, datetime
import gtk
import gobject
import appindicator
import os
import sys
import array
import urllib
import shutil
import time
import pynotify
import commands
from glob import glob
import ConfigParser
import urllib2
import re

from helper import *



gtk.threads_init()

class UpdateLabel(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		global ct
		
		while not ct.stopthread.isSet() :
			gtk.threads_enter()
			f = "%s/Downloads/%s" % (u_home, file_name)
			if os.path.exists(f):
				statinfo = os.stat(f)
				delta = statinfo.st_size / 1024
				fs = file_size / 1024
				t = "Downloading MB: %s / %s" % (delta / 1024, fs / 1024)
			else:
				t = "Downloading..."
			menu_items.set_label(t)
			gtk.threads_leave()
			
			time.sleep(0.1)

		if ct.stopthread.isSet() :
			menu_items.set_label("Complete!")
			sendNoti("Compiling Complete", "Your cyanogenmod build has finished", cmcIcon)
			
	def stop(self):
		self.stopthread.set()

class CompileThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet() :
			gtk.threads_enter()
			t = "%s/Downloads/%s" % (u_home, file_name)
			urllib.urlretrieve(url, t)
			menu_items1.set_sensitive(True)
			menu_items2.set_sensitive(True)
			ind.set_icon(cmcIntD)
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		self.stopthread.set()

def openFolder(obj):
	t = "%s/Downloads" % (u_home)
	cmd = "nautilus %s" % (t)
	os.system(cmd)
	gtk.main_quit()

def main_quit(obj):
	global ct
	global ul
	ct.stop()
	ul.stop()
	gtk.main_quit()

if __name__ == "__main__":
	os.chdir("/tmp")
	url = sys.argv[1]
	file_name = url.split('/')[-1]
	sendNoti("Downloading Cyanogenmod", "Your cyanogenmod download is starting\n\n%s" % file_name, cmcIcon,)
	time.sleep(2)
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	time.sleep(3)
	if os.path.exists(file_name):
		os.remove(file_name)
	ind = appindicator.Indicator("example-simple-client", cmcInt, appindicator.CATEGORY_APPLICATION_STATUS)
	ind.set_status(appindicator.STATUS_ACTIVE)
	ind.set_attention_icon(cmcInt)

	# create a menu
	menu = gtk.Menu()

	menu_items = gtk.MenuItem()
	menu_items.set_label("Downloading...")
	menu_items.set_sensitive(False)
	menu_items.show()

	menu_items2 = gtk.MenuItem("Open")
	menu_items2.set_sensitive(False)
	menu_items2.connect("activate", openFolder)
	menu_items2.show()

	menu_items1 = gtk.MenuItem("Quit")
	menu_items1.set_sensitive(False)
	menu_items1.connect("activate" ,  main_quit)
	menu_items1.show()

	submenu = gtk.Menu()

	subitem = gtk.MenuItem("Filename")
	subitem.set_submenu(submenu)
	subitem.show()

	subFile = gtk.MenuItem(file_name)
	subFile.show()
	submenu.append(subFile)

	menu.append(menu_items)
	menu.append(subitem)
	menu.append(menu_items2)
	menu.append(menu_items1)

	ind.set_menu(menu)

	ul = UpdateLabel()
	ct = CompileThread()
	ul.start()
	ct.start()

	gtk.main()

