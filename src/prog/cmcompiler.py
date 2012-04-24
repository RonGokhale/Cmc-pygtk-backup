#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import os
import sys
import webbrowser
import array
import urllib
import shutil
import time
import gtk
import pynotify
import commands
from glob import glob
from xml.dom.minidom import parseString
import ConfigParser

# Path variables
u_home = os.environ['HOME']
gitconfig = "%s/.gitconfig" % (u_home)
configdir = "%s/.cmc/" % (u_home)
cmcconfig = "%s/.cmc/cmc.cfg" % (u_home)
build_script = "/usr/share/cmc/build-it.sh"
askConfirm = "%s/.cmc/ask.confim" % (u_home)
repo_config = "%s/.cmc/repo_list" % (u_home)
default_repo_path = "%s/.cmc/build/" % (u_home)
cmcMainImage = "/usr/share/cmc/images/cmc-main.png"
cmcIcon = "/usr/share/cmc/images/cmc-icon.png"
cmcTheme = "/usr/share/cmc/images/theme/"
cmcThemeSmall = "/usr/share/cmc/images/theme/small/"
tmpManifest = "/tmp/manifest"
default_branch = "ics"

# URL
cmcUrl = "http://forum.xda-developers.com/showthread.php?t=1415661"
donateUrl = "http://forum.xda-developers.com/donatetome.php?u=2709018"
urlCmIcs = "https://raw.github.com/CyanogenMod/android_vendor_cm/ics/vendorsetup.sh"
urlCmGb = "https://raw.github.com/CyanogenMod/android_vendor_cyanogen/gingerbread/vendorsetup.sh"
cmGit = "https://github.com/CyanogenMod/android.git"
repoToolUrl = "https://dl-ssl.google.com/dl/googlesource/git-repo/repo"

# Config file definitions
configDeviceName = "config_device_name:"
configCustomRepoPath = "config_custom_repo_path:"
configBranch = "config_branch:"

placeIcon = gtk.gdk.pixbuf_new_from_file(cmcIcon)

class cmcStartClass():
	# Setup dialog
	def setup_dialog(self, obj):

		chk_config()

		def callback_device(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			parser("device", data)

		def callback_branch(widget, data=None):
			print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
			parser("branch", data)

		def choose_branch(obj):

			dialog = gtk.Dialog("Choose branch", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(260, 200)

			scroll = gtk.ScrolledWindow()
			scroll.set_border_width(10)
			scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
			dialog.vbox.pack_start(scroll, True, True, 0)
			scroll.show()

			table = gtk.Table(2, 1, False)
			table.set_row_spacings(45)

			scroll.add_with_viewport(table)
			table.show()

			device = gtk.RadioButton(None, None)

			button_count = 0
			for radio in list(["ics", "gingerbread"]):

				button_count += 1
				button = "button%s" % (button_count)

				button = gtk.RadioButton(group=device, label="%s" % (radio))
				button.connect("toggled", callback_branch, "%s" % (radio))
				table.attach(button, 0, 1, 0, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
				button.show()

			dialog.run()
			dialog.destroy()

		def choose_repo_path(obj):
			direct = gtk.FileChooserDialog("Repo path...", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER, buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			r = direct.run()
			repo_dir = direct.get_filename()
			direct.destroy()
			if r == gtk.RESPONSE_ACCEPT:
				try:
					parser("repo_path", repo_dir)
				except NameError:
					pass

		def remove_config(obj):
			q = question_dialog("Remove config?", "Are you sure you want to remove your current config?\n\nOnce this is done it can't be undone.")
			if q == True:
				os.remove(cmcconfig)
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

		def view_config(obj):

			def btn(obj):
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

			dialog = gtk.Dialog("Cmc configuration", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(500, 400)

			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			textview = gtk.TextView()
			textbuffer = textview.get_buffer()
			sw.add(textview)
			sw.show()
			textview.show()

			dialog.vbox.pack_start(sw, True, True, 0)

			try:
				infile = open(cmcconfig, "r")
				string = infile.read()
				infile.close()
				textbuffer.set_text(string)
			except IOError:
				custom_dialog(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

			dialog.run()
			dialog.destroy()

		def viewgit_config(obj):

			def btn(obj):
				custom_dialog(gtk.MESSAGE_INFO, "Configuration removed", "Your configuration has been removed. Please restart the application to re-configure.")

			dialog = gtk.Dialog("Cmc git configuration", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
			dialog.set_size_request(500, 400)

			sw = gtk.ScrolledWindow()
			sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			textview = gtk.TextView()
			textbuffer = textview.get_buffer()
			sw.add(textview)
			sw.show()
			textview.show()

			dialog.vbox.pack_start(sw, True, True, 0)

			try:
				infile = open(gitconfig, "r")
				string = infile.read()
				infile.close()
				textbuffer.set_text(string)
			except IOError:
				custom_dialog(gtk.MESSAGE_ERROR, "Failed reading configuration", "Can't currently read the config file.\n\nIs it open somewhere else?\n\nPlease try again.")

			dialog.run()
			dialog.destroy()

		def device_list(obj):

			b = read_parser("branch")
			if "Default" in b:
				custom_dialog(gtk.MESSAGE_ERROR, "No branch choosen", "Please select a branch so I know which device list to pull.\n\nThanks!")
				chk_config = 0
			elif "gingerbread" in b:
				useBranch = urlCmGb
				chk_config = 1
			elif "ics" in b:
				useBranch = urlCmIcs
				chk_config = 1
			else:
				useBranch = "null"
				chk_config = 0

			if chk_config == True:
				try:
					filehandle = urllib.urlopen(useBranch)
				except IOError:
					custom_dialog(gtk.MESSAGE_ERROR, "Can't read file!", "Can't read the file to setup devices!\n\nPlease check you internet connections and try again!")

				count = 0
				for lines in filehandle.readlines():
					count += 1

				filehandle.close()

				dialog = gtk.Dialog("Choose device", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
				dialog.set_size_request(260, 400)

				scroll = gtk.ScrolledWindow()
				scroll.set_border_width(10)
				scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
				dialog.vbox.pack_start(scroll, True, True, 0)
				scroll.show()

				table = gtk.Table(count, 1, False)
				table.set_row_spacings(5)

				scroll.add_with_viewport(table)
				table.show()

				device = gtk.RadioButton(None, None)

				try:
					filehandle = urllib.urlopen(useBranch)
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
						table.attach(button, 0, 1, button_count-1, button_count, xoptions=gtk.FILL, yoptions=gtk.SHRINK)
						button.show()

				filehandle.close()

				dialog.run()
				dialog.destroy()

		def ThemeClicked(widget, event, data):
			if data == "a-default.png":
				data = "Default"
				icon = "/home/lithid/Documents/cmc/src/images/theme/small/a-default.png"
				sendNoti("Cmc theme", "Default theme has been set", icon)
			else:
				icon = "/home/lithid/Documents/cmc/src/images/theme/small/%s" % data
				sendNoti("Cmc theme", "Theme has been set", icon)
			parser("theme", data)

		dialog = gtk.Dialog("CMC Setup", None, gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT, gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
		dialog.set_position(gtk.WIN_POS_CENTER)
		dialog.set_resizable(False)

		settings_lab = gtk.Label("Configure your settings here")
		settings_lab.show()
		dialog.vbox.pack_start(settings_lab, False, False, 10)

		table = gtk.Table(6, 2, False)
		table.set_row_spacings(5)
		table.show()

		dialog.vbox.pack_start(table, True, True, 15)

		device_btn = gtk.Button("Choose device")
		device_btn.set_size_request(140, 28)
		device_btn.connect("clicked", device_list)
		device_btn.show()

		branch_btn = gtk.Button("Choose branch")
		branch_btn.set_size_request(140, 28)
		branch_btn.connect("clicked", choose_branch)
		branch_btn.show()

		repo_path_btn = gtk.Button("Choose repo path")
		repo_path_btn.set_size_request(140, 28)
		repo_path_btn.connect("clicked", choose_repo_path)
		repo_path_btn.show()

		viewgit_btn = gtk.Button("View git config")
		viewgit_btn.set_size_request(140, 28)
		viewgit_btn.connect("clicked", viewgit_config)
		viewgit_btn.show()

		view_btn = gtk.Button("View config")
		view_btn.set_size_request(140, 28)
		view_btn.connect("clicked", view_config)
		view_btn.show()

		config_btn = gtk.Button("Remove config")
		config_btn.set_size_request(140, 28)
		config_btn.connect("clicked", remove_config)
		config_btn.show()

		table.attach(device_btn, 0, 1, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(branch_btn, 1, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(repo_path_btn, 0, 1, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(viewgit_btn, 1, 2, 1, 2, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(view_btn, 0, 1, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
		table.attach(config_btn, 1, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)


		theme_label = gtk.Label()
		theme_label.set_markup("<small>To change the theme, please select your preference from <b>below</b></small>")
		theme_label.show()
		dialog.vbox.pack_start(theme_label, False, False, 0)

		scroll = gtk.ScrolledWindow()
		scroll.set_size_request(400, 180)
		scroll.set_border_width(10)
		scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
		dialog.vbox.pack_start(scroll, True, True, 0)
		scroll.show()

		tab = gtk.Table(1, 8, True)
		tab.set_col_spacings(10)
		scroll.add_with_viewport(tab)
		tab.show()

		dirList = custom_listdir(cmcThemeSmall)
		count = 0
		for x in dirList:
			count+=1

			event = "event%s" % (count)
			image = "image%s" % (count)

			tooltips = gtk.Tooltips()
			event = gtk.EventBox()
			image = gtk.Image()
			path = "%s%s" % (cmcThemeSmall, x)
			image.set_from_file(path)
			event.connect("button_press_event", ThemeClicked, x)
			tooltips.set_tip(event, x)
			event.add(image)
			tab.attach(event, count-1, count, 0, 1)
			image.show()
			event.show()

		b = read_parser("branch")
		d = read_parser("device")
		r = read_parser("repo_path")
		if r == "Default":
			r = default_repo_path
		settings_info = gtk.Label()
		settings_info.set_alignment(0, 0)
		settings_info.set_markup("<small><small>Device: <b>%s</b>\nBranch: <b>%s</b>.\nRepo path: <b>%s</b></small></small>" % (d,b,r))
		settings_info.show()
		dialog.vbox.pack_start(settings_info, False, False, 10)

		dialog.run()
		dialog.destroy()

	#Start/Compile dialog
	def repo_sync_go(self, obj):
		chk_repo = common_chk()

		if chk_repo == 1:
			cmd1 = "repo init -u %s -b %s" % (cmGit, repo_branch)
			cmd2 = "repo sync -j1"
			d = "%s.repo" % (repo_path)
			if not os.path.exists(d):
				os.system(cmd1)
			os.system(cmd2)
			custom_dialog(gtk.MESSAGE_INFO, "Sync complete!", "Sync is now complete, we can now compile!")

	def repo_build_go(self, obj):
		def build_gb():
			CHECKS = 0
			build_device = read_parser("device")
			build_manu = getManu(build_device)

			d = "%s.repo" % (repo_path)
			if not os.path.exists(d):
				CHECKS+=1
				custom_dialog(gtk.MESSAGE_WARNING, "Errors preventing build", "Need to sync repo before moving forward.")

			if CHECKS == 0:
				d = "%sdevice/%s/%s" % (repo_path, build_manu, build_device)
				if not os.path.exists(d):
					custom_dialog(gtk.MESSAGE_WARNING, "Errors preventing build", "Could not change directories for you device. Does it exist?")

				if CHECKS == 0:
					d = "%svendor/%s/%s/proprietary" % (repo_path, build_manu, build_device)
					if not os.path.exists(d):
						c = checkAdb()
						if c == False:
							CHECKS+=1
							custom_dialog(gtk.MESSAGE_WARNING, "Errors preventing build", "Adb is not running, enable and restart.")
					if CHECKS == 0:
						c = extractFiles(repo_path, build_manu, build_device)
						if c == False:
							CHECKS+=1
							custom_dialog(gtk.MESSAGE_WARNING, "Errors preventing build", "Extract files came back false, might be issues with the extract script.")
						if CHECKS == 0:
							os.chdir(repo_path)
							cacheran = "%scacheran" % configdir
							if not os.path.exists(cacheran):
								cmd = "/bin/bash prebuilt/linux-x86/ccache/ccache -M 50G"
								os.system(cmd)
								file(cacheran, 'w').close()
							cmd = "/bin/bash %s/vendor/cyanogen/get-rommanager" % (repo_path)
							os.system(cmd)
							cmd = "/bin/bash %s %s %s" % (build_script, build_device, repo_path)
							os.system(cmd)
							d = "%sbuild.failed" % (configdir)
							if os.path.exists(d):
								custom_dialog(gtk.MESSAGE_ERROR, "Build failed", "Please run the build again, or run cmc via terminal to catch exact errors.")
							else:
								t = "%sout/target/product/%s" % (repo_path, build_device)
								rom = glob('%s/*signed.zip' %t)
								q = question_dialog("Build complete", "Your rom is located:\n\n%s\n\nWould you like to go there now?" % (t))
								if q == True:
									cmd = "nautilus %s" % (t)
									os.system(cmd)

		def build_ics():
			CHECKS = 0
			build_device = read_parser("device")
			build_manu = getManu(build_device)

			d = "%s.repo" % (repo_path)
			if not os.path.exists(d):
				CHECKS+=1
				custom_dialog(gtk.MESSAGE_ERROR, "Errors preventing build", "Need to sync repo before moving forward.")

			if CHECKS == 0:
				d = "%sdevice/%s/%s" % (repo_path, build_manu, build_device)
				if not os.path.exists(d):
					os.chdir(repo_path)
					cmd = "python build/tools/roomservice.py cm_" + build_device
					os.system(cmd)
					time.sleep(2)
					build_manu = getManu(build_device)
					nd = "%sdevice/%s/%s" % (repo_path, build_manu, build_device)
					print nd
					if not os.path.exists(nd):
						CHECKS+=1
						custom_dialog(gtk.MESSAGE_ERROR, "Errors preventing build", "Could not change directories for you device. Does it exist?")

				if CHECKS == 0:
					d = "%svendor/%s/%s/proprietary" % (repo_path, build_manu, build_device)
					if not os.path.exists(d):
						c = checkAdb()
						if c == False:
							CHECKS+=1
							custom_dialog(gtk.MESSAGE_ERROR, "Errors preventing build", "Adb is not running, enable and restart.")
					if CHECKS == 0:
						c = extractFiles(repo_path, build_manu, build_device)
						if c == False:
							CHECKS+=1
							custom_dialog(gtk.MESSAGE_ERROR, "Errors preventing build", "Extract files came back false, might be issues with the extract script.")
						if CHECKS == 0:
							os.chdir(repo_path)
							cacheran = "%scacheran" % configdir
							if not os.path.exists(cacheran):
								cmd = "/bin/bash prebuilt/linux-x86/ccache/ccache -M 50G"
								os.system(cmd)
								file(cacheran, 'w').close()
							cmd = "/bin/bash %s/vendor/cm/get-prebuilts" % (repo_path)
							os.system(cmd)
							cmd = "/bin/bash %s %s %s" % (build_script, build_device, repo_path)
							os.system(cmd)
							d = "%sbuild.failed" % (configdir)
							if os.path.exists(d):
								custom_dialog(gtk.MESSAGE_ERROR, "Build failed", "Please run the build again, or run cmc via terminal to catch exact errors.")
							else:
								t = "%sout/target/product/%s" % (repo_path, build_device)
								rom = glob('%s/*signed.zip' %t)
								q = question_dialog("Build complete", "Your rom is located:\n\n%s\n\nWould you like to go there now?" % (t))
								if q == True:
									cmd = "nautilus %s" % (t)
									os.system(cmd)

		def start_build():
			chk_repo = common_chk()
			if chk_repo == 1:
				print repo_branch
				if repo_branch == "ics":
					build_ics()
				elif repo_branch == "gingerbread":
					build_gb()
				else:
					print "Default"

		start_build()
		
	# About dialog
	def about_dialog(self, obj):
    		dialog = gtk.AboutDialog()
    		dialog.set_name("CMC")
		dialog.set_version("0.1 Beta")
		dialog.set_comments("The cyanogenmod compiler was written, not to dismiss the need to learn the android system, but to release the need consistly remember menial tasks.\n\nPlease intend to learn the system, contribute back to any upstream.\n\nHappy compiling,\n\nJeremie Long")
		dialog.set_copyright("CMC - 2012")
		dialog.set_website_label("Donate")
		dialog.set_website(donateUrl)
   		dialog.run()
    		dialog.destroy()
 
	def main_quit(self, obj):
		gtk.main_quit()
 
	# Main program
	def main(self):
		if not os.path.exists(askConfirm):
			get_askConfirm()

		if not os.path.exists(gitconfig):
			set_git_Text()

   		def menuItem(parent, imageNam, num):
       			num = gtk.HBox(False, 0)
       			num.set_border_width(2)
       			image = gtk.Image()
       			image.set_from_file(imageNam)
      			num.pack_start(image, False, False, 3)
      			image.show()
       			return num

		def imageClicked(widget, event):
 	  		webbrowser.open_new_tab(cmcUrl)

		tooltips = gtk.Tooltips()

		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("CMC")
		window.set_icon(placeIcon)
		window.set_size_request(260, 454)
		window.set_position(gtk.WIN_POS_CENTER)
		window.set_resizable(False)

		vbox = gtk.VBox(False, 5)
		hbox = gtk.HBox(True, 3)
		h1box = gtk.HBox(True, 3)

     		valign = gtk.Alignment(0, 1, 0, 0)
        	vbox.pack_start(valign)

		event = gtk.EventBox()
		image = gtk.Image()
		t = read_parser("theme")
		if t == "Default":
			image.set_from_file(cmcMainImage)
		else:
			themePath = "%s%s" % (cmcTheme, t)
			image.set_from_file(themePath)
		event.set_size_request(260, 358)
		event.connect("button_press_event", imageClicked)
		tooltips.set_tip(event, "Go to XDA thread!")
		event.add(image)

        	setup = gtk.Button("Setup")
		setup.connect("clicked", self.setup_dialog)

        	close = gtk.Button("Close")
		close.connect("clicked", self.main_quit)

        	about = gtk.Button("About")
		about.connect("clicked", self.about_dialog)

        	about1 = gtk.Button("Compile")
		about1.connect("clicked", self.repo_build_go)

        	about2 = gtk.Button("Sync")
		about2.connect("clicked", self.repo_sync_go)

		vbox.add(event)
		h1box.add(about1)
		h1box.add(about2)

        	h1align = gtk.Alignment(.50, 0, .75, 0)
        	h1align.add(h1box)
		vbox.pack_start(h1align, False, False, 3)

		hbox.add(setup)
		hbox.add(about)
        	hbox.add(close)

        	halign = gtk.Alignment(.50, 0, .75, 0)
        	halign.add(hbox)
        	vbox.pack_start(halign, False, False, 3)

		author_lab = gtk.Label()
		author_lab.set_markup("<small><small>Built by <b><i>lithid</i></b> open and free!</small></small>")
		vbox.pack_start(author_lab, False, False, 2)

        	window.add(vbox)

		image.show()
		event.show()
        	window.connect('destroy', self.main_quit)
       		window.show_all()
 
		gtk.main()

def common_chk():
	chk_repo = 0
	global repo_path
	global repo_branch
	p = read_parser("repo_path")
	if not p == "Default":
		repo_path = read_parser("repo_path")
	else:
		repo_path = default_repo_path

	repo_branch = read_parser("branch")
	chk_dev = read_parser("device")
	if not chk_dev == "Default":
		if not os.path.exists(repo_path):
			os.makedirs(repo_path)
		os.chdir(repo_path)
		p = which("repo")
		if p == None:
			q = question_dialog("Install repo script?", "Repo script isn't installed. Is this something I can do?\nPath:\n<b>/usr/local/sbin/</b>\n\nThis will ask for root!")
			if q == True:
				install_repo()
				chk_repo = 1
			else:
				custom_dialog(gtk.MESSAGE_ERROR, "No repo script", "No repo script found in path and no repo script installed. Please install this script, or let me do it. Either way, can't proceed without that script!")
				chk_repo = 0
		else:
			chk_repo = 1
	else:
		custom_dialog(gtk.MESSAGE_ERROR, "Check device config...", "Sorry, did not find a device configured in:\n<b>%s</b>\n\nPlease go into Setup and select a device." % (config))
		chk_repo = 0

	return chk_repo


def get_askConfirm():
	def askedClicked():
		if not os.path.exists(askConfirm):
			file(askConfirm, 'w').close()

	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_title("**** User Confirmation ****")
	dialog.set_markup("<small>This is what <b>YOU</b> do to <b>YOUR</b> phone.</small>")
	dialog.format_secondary_markup("<small>By no means what so ever is this software or cyanogenmod responsible for what you do to your phone. \
You are taking the risks, you are choosing to this to your phone. By proceeding you are aware, you are warned. No crying or moaning. This software \
was tested by human beings, not cybogs from your mothers closet. Please keep this in mind when something breaks, or hangs.  If you have an issue \
with this software, please let me know.\n\nBy clicking this ok button, you have given me your soul.\n\nPlay safe.\n\n</small>\
<small><small><b>Note:\n- </b><i>This will not proceed unless you agree.</i></small>\n\
<small><b>-</b><i> Cyanogenmod doesn't consider source builds offical, please keep this in mind if you plan on bug reporting.</i></small></small>")
	dialog.set_resizable(False)

	r = dialog.run()
	if r == gtk.RESPONSE_OK:
		askedClicked()
	else:
		exit()
	dialog.destroy()

def set_git_Text():

	def loginClicked(name, email):
		if not os.path.exists(gitconfig):
			file(gitconfig, 'w').close()
			f = open(gitconfig, 'w')
			f.write("[color]\n")
			f.write("	ui = auto\n")
			f.write("[user]\n")
			f.write("	name = %s\n" % name)
			f.write("	email = %s\n" % email)
			f.write("[review \"review.cyanogenmod.com\"]\n")
			f.write("	username = %s\n" % name)
			f.close()

	def loginChecked(name, email):
		if "ex" in name:
			custom_dialog(gtk.MESSAGE_ERROR, "Bad username", "This error only comes about if you made no attempt to change your user, please do so when you start this again.")
			exit()
		elif "ex" in email:
			custom_dialog(gtk.MESSAGE_ERROR, "Bad email", "This error only comes about if you made no attempt to change your user, please do so when you start this again.")
			exit()
		else:
			loginClicked(name, email)

	dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK)
	dialog.set_title("User settings for repo config..")
	dialog.set_markup("<small>This will be used for <i>identification</i> purposes only</small>")
	dialog.format_secondary_markup("<small>This will be used to create a config file used by the repo script. This script is used to sync the repo locally. This information is not being used in any other way. You can look at the git config here:\n\n<b>%s/.gitconfig</b>\n\n<small><b>Note:</b> <i>This will be needed before we can start using cyanogenmod compiler.</i></small></small>" % u_home)
	dialog.set_resizable(False)

	table = gtk.Table(4, 1, True)
	table.set_row_spacings(5)
	table.show()

	dialog.vbox.pack_start(table, True, True, 0)

	user_entry = gtk.Entry()
	user_entry.set_text("ex. lithid")
	user_lab = gtk.Label("User:")
	user_entry.show()
	user_lab.show()
	email_entry = gtk.Entry()
	email_entry.set_text("ex. mrlithid@gmail.com")
	email_lab = gtk.Label("Email:")
	email_entry.show()
	email_lab.show()

	table.attach(user_lab, 0, 2, 0, 1, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
	table.attach(user_entry, 0, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=50, ypadding=0)
	table.attach(email_lab, 0, 2, 2, 3, xoptions=gtk.EXPAND, yoptions=gtk.EXPAND)
	table.attach(email_entry, 0, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=50, ypadding=0)

	r = dialog.run()
	if r == gtk.RESPONSE_OK:
		name = user_entry.get_text()
		email = email_entry.get_text()
		loginChecked(name, email)
	else:
		exit()
	dialog.destroy()

def getManu(arg):
	s = None
	paths = glob("device/*/*/cm.mk")
	for x in paths:
		if arg in x:
			s = x.split("/")
			s = s[1]
	if s:
		return s
	else:
		return None

def custom_dialog(dialog_type, title, message):
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               type=dialog_type,
                               buttons=gtk.BUTTONS_OK)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    dialog.run()
    dialog.destroy()
    return True

def question_dialog(title, message):
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               type=gtk.MESSAGE_QUESTION,
                               buttons=gtk.BUTTONS_YES_NO)
    dialog.set_markup("<b>%s</b>" % title)
    dialog.format_secondary_markup(message)
    response = dialog.run()
    dialog.destroy()

    if response == gtk.RESPONSE_YES:
       return True
    else:
       return False

def chk_config():
	if not os.path.exists(configdir):
		os.makedirs(configdir)

def install_repo():
	cmd1 = "curl https://dl-ssl.google.com/dl/googlesource/git-repo/repo > %srepo" % (configdir)
	cmd2 = "chmod a+x %srepo" % (configdir)
	cmd3 = "gksudo mv %srepo /usr/local/sbin/" % (configdir)
	os.system(cmd1)
	os.system(cmd2)
	os.system(cmd3)

def which(program):
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file

	return None

def custom_listdir(path):
    dirs = sorted([d for d in os.listdir(path) if os.path.isdir(path + os.path.sep + d)])
    dirs.extend(sorted([f for f in os.listdir(path) if os.path.isfile(path + os.path.sep + f)]))

    return dirs

def checkAdb():
	cmd = "adb devices"
	c = commands.getoutput(cmd)
	c = c.split(" ")
	c = c[2]
	if c == "not":
		return False
	else:
		return True

def extractFiles(parg, marg, darg):
	os.chdir(repo_path)
	d = "%sdevice/%s/%s" % (parg, marg, darg)
	if os.path.exists(d):
		os.chdir(d)
	if os.path.exists("extract-files.sh"):
		d = "%svendor/%s/%s/proprietary" % (parg, marg, darg)
		if not os.path.exists(d):
			cmd = "sh extract-files.sh"
			os.system(cmd)
			d = "%svendor/%s/%s/proprietary" % (parg, marg, darg)
			if os.path.exists(d):
				return True
			else:
				return False
		else:
			return True
	else:
		return False

def sendNoti(title, summary, icon, time):
	pynotify.init("Theme")
	n = pynotify.Notification(title, summary, icon)
	n.show()

def read_parser(arg):
	title = "Cmc"
	default = "Default"
	try:
		config = ConfigParser.RawConfigParser()
		config.read(cmcconfig)
		c = config.get(title, arg)

	except ConfigParser.NoSectionError:
		c = "%s" % (default)

	return c

def parser(arg, value):
	title = "Cmc"
	default = "Default"
	try:
		config = ConfigParser.RawConfigParser()
		config.read(cmcconfig)
		getTheme = config.get(title, 'theme')
		getDevice = config.get(title, 'device')
		getBranch = config.get(title, 'branch')
		getRepoPath = config.get(title, 'repo_path')
	except ConfigParser.NoSectionError:
		getTheme = None
		getDevice = None
		getBranch = None
		getRepoPath = None

	config = ConfigParser.RawConfigParser()
	config.add_section(title)

	if arg == "device":
		config.set(title, 'device', value)
	elif getDevice:
		config.set(title, 'device', getDevice)
	else:
		config.set(title, 'device', default)

	if arg == "theme":
		config.set(title, 'theme', value)
	elif getTheme:
		config.set(title, 'theme', getTheme)
	else:
		config.set(title, 'theme', default)

	if arg == "branch":
		config.set(title, 'branch', value)
	elif getBranch:
		config.set(title, 'branch', getBranch)
	else:
		config.set(title, 'branch', default)

	if arg == "repo_path":
		config.set(title, 'repo_path', value)
	elif getRepoPath:
		config.set(title, 'repo_path', getRepoPath)
	else:
		config.set(title, 'repo_path', default)

	with open(cmcconfig, 'wb') as configfile:
    		config.write(configfile)
 
if __name__ == '__main__':
	go = cmcStartClass()
	go.main()
