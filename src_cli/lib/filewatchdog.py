##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for streamers
#    Copyright (C) 2019  Tomaae
#    (https://wooferbot.com/)
#
#    This file is part of WooferBot.
#
#    WooferBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
##########################################################################

import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


#---------------------------
#   _WatchdogCustomHandler
#---------------------------
class _WatchdogCustomHandler(FileSystemEventHandler):
	def __init__(self, settings, woofer, WatchdogName):
		self.settings = settings
		self.woofer = woofer
		self.filename = ""
		self.WatchdogName = WatchdogName
		
		for action in self.settings.Watchdog:
			if action['Name'] != self.WatchdogName:
				continue
			
			self.filename = action['Filename']
			
		return
	
	#---------------------------
	#   on_created
	#---------------------------
	def on_created(self, event):
		self._check_modification(event.src_path)
		return
	
	#---------------------------
	#   on_modified
	#---------------------------
	def on_modified(self, event):
		self._check_modification(event.src_path)
		return
	
	#---------------------------
	#   _check_modification
	#---------------------------
	def _check_modification(self, filename):
		if self.filename == filename:
			for action in self.settings.Watchdog:
				if action['Name'] == self.WatchdogName:
					f = open(self.filename, "r")
					
					if 'Command' in action:
						self.woofer_commands({
							"command"      : action['Command'],
							"broadcaster"  : 1,
							"sender"       : action['Name'],
							"display-name" : action['Name'],
							"custom-tag"   : 'watchdog'
						})
					else:
						self.woofer.woofer_addtoqueue({
							"image"      : action['Image'],
							"message"    : action['Message'] + f.read(),
							"sender"     : action['Name'],
							"id"         : "watchdog"
						})
		
		return


#---------------------------
#   Watchdog
#---------------------------
class Watchdog:
	def __init__(self, settings, woofer):
		self.settings = settings
		self.woofer = woofer
		self.watchdog = {}
		
		for action in self.settings.Watchdog:
			if not action['Enabled']:
				continue
			
			path, filename = os.path.split(action['Filename'])
			self.watchdog[action['Name']] = Observer()
			self.watchdog[action['Name']].schedule(_WatchdogCustomHandler(settings, woofer, action['Name']), path, recursive=False)
			self.watchdog[action['Name']].start()
		
		return
	
	#---------------------------
	#   stop
	#---------------------------
	def stop(self):
		for action in self.watchdog:
			action.stop()
		
		for action in self.watchdog:
			action.join()
		
		return
