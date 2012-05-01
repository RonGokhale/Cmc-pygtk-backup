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

from helper import *

gtk.threads_init()


class UpdateLabel(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		global menu_items
		global st
		
		while not st.stopthread.isSet() :
			gtk.threads_enter()
			finish = datetime.datetime.now()
			delta = finish - start
			t = "Syncing %s" % (delta)
			menu_items.set_label(t)
			gtk.threads_leave()
			
			time.sleep(0.1)

		if st.stopthread.isSet() :
			a = "%s/NeedRepoScript" % (configdir)
			b = "%s/NoDeviceC" % (configdir)
			c = "%s/GenError" % (configdir)
			if os.path.exists(a):
				ind.set_icon(cmcIntE)
				menu_items.set_label("Repo Script needs setup")
			elif os.path.exists(b):
				ind.set_icon(cmcIntE)
				menu_items.set_label("No device configured!")
			elif os.path.exists(b):
				ind.set_icon(cmcIntE)
				menu_items.set_label("General sync error. Run in terminal")
			else:
				menu_items.set_label("Complete!")
				sendNoti("Syncing Complete", "Your cyanogenmod repo is finished syncing!", cmcIcon)
			
	def stop(self):
		self.stopthread.set()

class SyncThread(threading.Thread):
	stopthread = threading.Event()
	
	def run(self):
		
		while not self.stopthread.isSet() :
			gtk.threads_enter()
			repo_sync_go()
			menu_items1.set_sensitive(True)
			menu_items2.set_sensitive(True)
			ind.set_icon(cmcIntD)
			gtk.threads_leave()
			self.stop()
			
	def stop(self):
		self.stopthread.set()

def main_quit(obj):
	global st
	global ul
	st.stop()
	ul.stop()
	sys.exit()

def goCompile(obj):
	cmd = "/usr/bin/cmc --compile &"
	os.system(cmd)
	sys.exit()

def repo_sync_go():

	repo_path = read_parser("repo_path")
	repo_branch = read_parser("branch")

	chk_repo = common_chk()

	if chk_repo == 1:
		cmd1 = "repo init -u %s -b %s" % (cmGit, repo_branch)
		cmd2 = "repo sync -j1"
		d = "%s/.repo" % (repo_path)
		if not os.path.exists(d):
			os.system(cmd1)
		os.system(cmd2)

	elif chk_repo == 0:
		r = "%s/NeedRepoScript" % (configdir)
		file(r, 'w').close()

	elif chk_repo == 2:
		d = "%s/NoDeviceC" % (configdir)
		file(d, 'w').close()

	else:
		g = "%s/GenError" % (configdir)
		file(g, 'w').close()

if __name__ == "__main__":
	sendNoti("Syncing Cyanogenmod", "Your cyanogenmod repo sync is starting", cmcIcon)
	time.sleep(5)
	ind = appindicator.Indicator("example-simple-client", cmcInt, appindicator.CATEGORY_APPLICATION_STATUS)
	ind.set_status(appindicator.STATUS_ACTIVE)
	ind.set_attention_icon(cmcInt)

	# create a menu
	menu = gtk.Menu()
	menu_items = gtk.MenuItem()
	menu_items.set_label("Compiling...")
	menu_items.set_sensitive(False)
	menu.append(menu_items)
	menu_items.show()

	menu_items2 = gtk.MenuItem("Compile")
	menu_items2.set_sensitive(False)
	menu.append(menu_items2)
	menu_items2.connect("activate" ,  goCompile)
	menu_items2.show()

	menu_items1 = gtk.MenuItem("Quit")
	menu_items1.set_sensitive(False)
	menu.append(menu_items1)
	menu_items1.connect("activate" ,  main_quit)
	menu_items1.show()

	ind.set_menu(menu)

	start = datetime.datetime.now()
	ul = UpdateLabel()
	st = SyncThread()
	ul.start()
	st.start()

	gtk.main()

