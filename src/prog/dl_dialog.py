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

repo_path = read_parser("repo_path")
repo_branch = read_parser("branch")
build_device = read_parser("device")

if __name__ == "__main__":

	dl_version = None
	dl_url = None
	dl_device = None
	mylist = []

	def get_download_urls(device, version):
		RURL = "http://download.cyanogenmod.com"
		URL = "http://download.cyanogenmod.com/?device=%s&type=%s" % (device, version)
		htmlpage = urllib2.urlopen(URL).read()
		alllinks = re.findall('<a href=\".*?\">.*?zip</a>',htmlpage)
		count=1
		global mylist
		for links in alllinks:
			x = "%s%s" % (RURL, links)
			x = x.split("\"")
			x = x[1]
			y = x.split("/")

			if y[2] == "artifacts":
				y = y[6]
			elif y[2] == "RC":
				y = y[3]
			else:
				y = y[4]

			s = "%s%s" % (RURL, x)
			mylist.append(s)

			if count == 5:
				break
			else:
				count += 1

		return

	def downloadList(obj):
		def callback_url(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			global dl_url
			dl_url = data

		dl_list.hide()
		branch_tbl.hide()
		deviceICS_scroll.hide()
		deviceGB_scroll.hide()
		version_tbl.hide()

		table3 = gtk.Table(5, 1, False)
		table3.set_row_spacings(15)
		table3.set_col_spacings(15)
		table3.show()
		dialog.vbox.pack_start(table3, True, True, 0)

		url = gtk.RadioButton(None, None)

		button_count = 0
		get_download_urls(dl_device, dl_version)
		print mylist
		for lines in mylist:

			button_count += 1
			button = "button%s" % (button_count)
			x = lines.split("/")
			x = x[-1]

			print x

			button = gtk.RadioButton(group=url, label="%s" % (x))
			button.connect("toggled", callback_url, "%s" % (lines))
			table3.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
			button.show()

	def callback_device(widget, data=None):
		print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
		global dl_device
		dl_device = data
		if not dl_version == None and not dl_device == None:
			dl_list.show()
		

	def callback_version(widget, data=None):
		print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
		global dl_version
		dl_version = data
		if not dl_version == None and not dl_device == None:
			dl_list.show()

	def callback_branch(widget, data=None):
		print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

		if widget.get_active() == True:
			if data == "ics":
				deviceICS_scroll.show()
				version_tbl.show()

			if data == "gingerbread":
				deviceGB_scroll.show()
				version_tbl.show()

		if widget.get_active() == False:
			if data == "ics":
				deviceICS_scroll.hide()
				version_tbl.hide()

			if data == "gingerbread":
				deviceGB_scroll.hide()
				version_tbl.hide()

	dialog = gtk.Dialog("Download Cyanogenmod", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
	dialog.set_resizable(False)

	branch_tbl = gtk.Table(1, 2, False)
	branch_tbl.set_row_spacings(20)
	branch_tbl.set_col_spacings(40)
	branch_tbl.show()
	dialog.vbox.pack_start(branch_tbl, True, True, 0)

	branch = gtk.RadioButton(None, None)

	button_count = 0
	for radio in list(["ics", "gingerbread"]):

		button_count += 1
		button = "button%s" % (button_count)

		button = gtk.RadioButton(group=branch, label="%s" % (radio))
		button.connect("toggled", callback_branch, "%s" % (radio))
		branch_tbl.attach(button, button_count-1, button_count, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		button.show()

	deviceICS_scroll = gtk.ScrolledWindow()
	deviceICS_scroll.set_border_width(10)
	deviceICS_scroll.set_size_request(200, 180)
	deviceICS_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	deviceICS_scroll.hide()
	dialog.vbox.pack_start(deviceICS_scroll, True, True, 0)

	try:
		filehandle = urllib.urlopen(urlCmIcs)
	except IOError:
		custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")
		sys.exit()

	count = 0
	for lines in filehandle.readlines():
		count += 1

	filehandle.close()

	deviceICS_tbl = gtk.Table(count, 1, False)
	deviceICS_tbl.set_row_spacings(5)

	deviceICS_scroll.add_with_viewport(deviceICS_tbl)
	deviceICS_tbl.show()

	device = gtk.RadioButton(None, None)

	try:
		filehandle = urllib.urlopen(urlCmIcs)
	except IOError:
		custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

	button_count = 0
	for lines in filehandle.readlines():

		if "combo" in lines:
			button_count += 1
			button = "button%s" % (button_count)

			x = lines.split(" ")
			radio = x[1]
			x = radio.split("_")
			radio = x[1]
			x = radio.split("-")
			radio = x[0]

			button = gtk.RadioButton(group=device, label="%s" % (radio))
			button.connect("toggled", callback_device, "%s" % (radio))
			deviceICS_tbl.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
			button.show()

	filehandle.close()

	deviceGB_scroll = gtk.ScrolledWindow()
	deviceGB_scroll.set_border_width(10)
	deviceGB_scroll.set_size_request(200, 180)
	deviceGB_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
	dialog.vbox.pack_start(deviceGB_scroll, True, True, 0)
	deviceGB_scroll.hide()

	try:
		filehandle = urllib.urlopen(urlCmGb)
	except IOError:
		custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")
		sys.exit()

	count = 0
	for lines in filehandle.readlines():
		count += 1

	filehandle.close()

	deviceGB_tbl = gtk.Table(count, 1, False)
	deviceGB_tbl.set_row_spacings(5)

	deviceGB_scroll.add_with_viewport(deviceGB_tbl)
	deviceGB_tbl.show()

	device = gtk.RadioButton(None, None)

	try:
		filehandle = urllib.urlopen(urlCmGb)
	except IOError:
		custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

	button_count = 0
	for lines in filehandle.readlines():

		if "combo" in lines:
			button_count += 1
			button = "button%s" % (button_count)

			x = lines.split(" ")
			radio = x[1]
			x = radio.split("_")
			radio = x[1]
			x = radio.split("-")
			radio = x[0]

			button = gtk.RadioButton(group=device, label="%s" % (radio))
			button.connect("toggled", callback_device, "%s" % (radio))
			deviceGB_tbl.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
			button.show()

	filehandle.close()

	version_tbl = gtk.Table(1, 3, False)
	version_tbl.set_row_spacings(15)
	version_tbl.set_row_spacings(15)
	version_tbl.hide()
	dialog.vbox.pack_start(version_tbl, True, True, 0)

	version = gtk.RadioButton(None, None)

	button_count = 0
	for lines in list(["nightly", "RC", "stable"]):

		button_count += 1
		button = "button%s" % (button_count)

		button = gtk.RadioButton(group=version, label="%s" % (lines))
		button.connect("toggled", callback_version, "%s" % (lines))
		version_tbl.attach(button, button_count-1, button_count, 0, 1, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
		button.show()

	dl_list = gtk.Button("Download List")
	dl_list.set_size_request(140, 28)
	dl_list.connect("clicked", downloadList)
	dl_list.hide()
	dialog.vbox.pack_start(dl_list, True, True, 15)

	dialog.run()
	dialog.destroy()
	if not dl_url == None:
		cmd = "python /usr/share/cmc/prog/download.pyc %s &" % (dl_url)
		os.system(cmd)
	else:
		custom_dialog(gtk.MESSAGE_WARNING, "No Download Choosen", "You didn't select a download, can't download anything for you!")

