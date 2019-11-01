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

import codecs
import json
import os
import time

#---------------------------
#   Settings Handling
#---------------------------
class Settings:
	def __init__(self, pathRoot=None):
		## Check paths
		self.pathRoot     = pathRoot + '\\'
		if not os.path.isdir(self.pathRoot):
			print("Working directory not detected.")
			exit(1)
		if not os.path.isfile(self.pathRoot + "wooferbot.py"):
			print("Working directory incorrect.")
			exit(1)
		if not os.path.isfile(self.pathRoot + "settings.json"):
			print("Configuration file is missing, recreating with defaults.")
		
		self.Reload()
		self.ReloadMascot()
		return
		
	#---------------------------
	#   ReloadMascot
	#---------------------------
	def ReloadMascot(self):
		print("Loading mascot settings...")
		self.mascotImages = {}
		self.mascotAudio  = {}
		self.mascotStyles = {}
		
		## Load mascot config
		try:
			with codecs.open(self.pathRoot + "mascots\\" + self.CurrentMascot + "\\mascot.json", encoding="utf-8-sig", mode="r") as f:
				data = json.load(f, encoding="utf-8")
				for key, value in data.items():
						self.__dict__[key] = value 
		except:
			print("Unable to load mascot.json")
			exit(1)
		
		## Check mascot images
		for action in self.mascotImages:
			if 'Image' not in self.mascotImages[action]:
				print("Mascot Image variable is missing for action: " + action)
				exit(1)
			
			self.mascotImages[action]['Image'] = self.pathRoot + "mascots\\" + self.CurrentMascot + "\\images\\" + self.mascotImages[action]['Image']
		
		## Check mascot audio
		for action in self.mascotAudio:
			if not isinstance(self.mascotAudio[action]['Audio'],list):
				print("Mascot audio is not a list for action: " + action)
				exit(1)
			
			for idx, val in enumerate(self.mascotAudio[action]['Audio']):
				self.mascotAudio[action]['Audio'][idx] = self.pathRoot + "mascots\\" + self.CurrentMascot + "\\audio\\" + self.mascotAudio[action]['Audio'][idx]
		
		self.CheckSettingsDependencies()
		return
		
	#---------------------------
	#   Reload
	#---------------------------
	def Reload(self):
		print("Loading settings...")
		self.TwitchChannel     = ""
		self.TwitchOAUTH       = ""
		self.TwitchBotChannel  = ""
		self.TwitchBotOAUTH    = ""
		self.UseChatbot        = False
		self.twitchClientID    = "zpm94cuvrntu030mauvxvz9cv2ldja"
		self.Styles            = {}
		self.Messages          = {}
		self.Activities        = {}
		self.Enabled           = {}
		self.PoseMapping       = {}
		self.CurrentMascot     = "malamute"
		self.AlignMascot       = "left"
		self.pathImages        = self.pathRoot + "mascots" + '\\' + self.CurrentMascot + '\\' + "images" + '\\'
		self.pathAudio         = self.pathRoot + "mascots" + '\\' + self.CurrentMascot + '\\' + "audio" + '\\'
		self.HostMessage       = ""
		self.AutohostMessage   = ""
		self.FollowMessage     = ""
		self.GlobalVolume      = 0.2
		self.MinBits           = 0
		self.AutoShoutout      = False
		self.AutoShoutoutTime  = 10
		self.ShoutoutAccess    = "mod"
		self.Bots              = []
		self.commonBots        = ["nightbot", "streamlabs", "streamelements", "stay_hydrated_bot", "botisimo", "wizebot", "moobot"]
		self.ScheduledMessages = []
		self.scheduleTable     = {}
		self.CustomBits        = []
		self.CustomSubs        = []
		self.Commands          = {}
		
		self.NanoleafEnabled   = False
		self.NanoleafIP        = ""
		self.NanoleafToken     = ""
		
		self.HueEnabled        = False
		self.HueIP             = ""
		self.HueToken          = ""
		
		self.YeelightEnabled   = False
		
		#
		# Load config
		#
		if os.path.isfile(self.pathRoot + "settings.json"):
			try:
				with codecs.open(self.pathRoot + "settings.json", encoding="utf-8-sig", mode="r") as f:
					data = json.load(f, encoding="utf-8")
					for key, value in data.items():
							self.__dict__[key] = value 
			except:
				print("Unable to load settings.json")
				exit(1)
				
			self.UpgradeSettingsFile()
		
		#
		# CONVERT
		#
		self.TwitchChannel = self.TwitchChannel.lower()
		self.TwitchBotChannel = self.TwitchBotChannel.lower()
		self.CurrentMascot = self.CurrentMascot.lower()
		if self.TwitchBotChannel and self.TwitchBotChannel not in self.Bots:
			self.Bots.append(self.TwitchBotChannel)
		self.Bots = [x.lower() for x in self.Bots]
		for action in self.Commands:
			self.Commands[action]['Hotkey'] = [key.lower() for key in self.Commands[action]['Hotkey']]
		
		#
		# Reset time on all ScheduledMessages
		#
		for action in self.ScheduledMessages:
			self.scheduleTable[action['Name']] = int(time.time())
		
		self.AutofillSettings()
		
		if not os.path.isfile(self.pathRoot + "settings.json"):
			self.Save()
			print("Default configuration file has been created.")
			exit(0)
		
		self.Verify()
		return
		
	#---------------------------
	#   AutofillSettings
	#---------------------------
	def AutofillSettings(self):
		#
		# DEFAULT
		#
		if self.CurrentMascot == "":
			self.CurrentMascot = "malamute"
		if self.HostMessage == "":
			self.HostMessage = "is now hosting you."
		if self.AutohostMessage == "":
			self.AutohostMessage = "is auto hosting you"
		if self.FollowMessage == "":
			self.FollowMessage = "Thank you for the follow!"
		if not self.MinBits:
			self.MinBits = 0
		if not self.AutoShoutout:
			self.AutoShoutout = False
		if not self.AutoShoutoutTime:
			self.AutoShoutoutTime = 10
		
		#
		# DEFAULT MAPPING
		#
		if "DEFAULT" not in self.PoseMapping:
			self.PoseMapping['DEFAULT'] = {}
			self.PoseMapping['DEFAULT']['Image'] = 'Wave'
			self.PoseMapping['DEFAULT']['Audio'] = 'Wave'
		
		#
		# ENABLED
		#
		if "new_chatter" not in self.Enabled:
			self.Enabled["new_chatter"] = True
		if "greet" not in self.Enabled:
			self.Enabled["greet"] = True
		if "follow" not in self.Enabled:
			self.Enabled["follow"] = True
		if "raid" not in self.Enabled:
			self.Enabled["raid"] = True
		if "host" not in self.Enabled:
			self.Enabled["host"] = True
		if "autohost" not in self.Enabled:
			self.Enabled["autohost"] = True
		if "sub" not in self.Enabled:
			self.Enabled["sub"] = True
		if "resub" not in self.Enabled:
			self.Enabled["resub"] = True
		if "subgift" not in self.Enabled:
			self.Enabled["subgift"] = True
		if "anonsubgift" not in self.Enabled:
			self.Enabled["anonsubgift"] = True
		if "bits" not in self.Enabled:
			self.Enabled["bits"] = True
		if "lurk" not in self.Enabled:
			self.Enabled["lurk"] = True
		if "shoutout" not in self.Enabled:
			self.Enabled["shoutout"] = True
		
		#
		# STYLES
		#
		if "BackgroundColor" not in self.Styles:
			self.Styles["BackgroundColor"] = "#fefeff"
		if "BorderColor" not in self.Styles:
			self.Styles["BorderColor"] = "#69656c"
		if "BorderWidth" not in self.Styles:
			self.Styles["BorderWidth"] = 4
		if "BorderRadius" not in self.Styles:
			self.Styles["BorderRadius"] = 4
		if "BorderStrokeColor" not in self.Styles:
			self.Styles["BorderStrokeColor"] = "#ffffff"
		if "TextFontFamily" not in self.Styles:
			self.Styles["TextFontFamily"] = "Fira Sans"
		if "TextSize" not in self.Styles:
			self.Styles["TextSize"] = 22
		if "TextWeight" not in self.Styles:
			self.Styles["TextWeight"] = 900
		if "TextColor" not in self.Styles:
			self.Styles["TextColor"] = "#69656c"
		if "HighlightTextSize" not in self.Styles:
			self.Styles["HighlightTextSize"] = 24
		if "HighlightTextSpacing" not in self.Styles:
			self.Styles["HighlightTextSpacing"] = 3
		if "HighlightTextColor" not in self.Styles:
			self.Styles["HighlightTextColor"] = "#ca5c67"
		if "HighlightTextStrokeColor" not in self.Styles:
			self.Styles["HighlightTextStrokeColor"] = "#8e4148"
		if "HighlightTextShadowColor" not in self.Styles:
			self.Styles["HighlightTextShadowColor"] = "#fc938f"
		if "HighlightTextShadowOffset" not in self.Styles:
			self.Styles["HighlightTextShadowOffset"] = 3
		
		#
		# Messages
		#
		if "new_chatter" not in self.Messages:
			self.Messages["new_chatter"] = [
				"Oh? {sender} is new here. Welcome~ ^..^"
			]
		if "follow" not in self.Messages:
			self.Messages["follow"] = [
				"Oh? We have a new friend! Welcome {sender} ^..^"
			]
		if "sub" not in self.Messages:
			self.Messages["sub"] = [
				"[Hello;Hi;Hey;Hewwo;Ello] {sender}, thank you for becoming our best friend ^..^"
			]
		if "resub" not in self.Messages:
			self.Messages["resub"] = [
				"[Hello;Hi;Hey;Hewwo;Ello] {sender}, thank you for being our best friend for {months} months ^..^"
			]
		if "subgift" not in self.Messages:
			self.Messages["subgift"] = [
				"[Hello;Hi;Hey;Hewwo;Ello] {sender}, thank you for gifting a sub to {recipient} ^..^"
			]
		if "bits" not in self.Messages:
			self.Messages["bits"] = [
				"Yay~! {sender} just gave me {bits} treats ^..^"
			]
		if "raid" not in self.Messages:
			self.Messages["raid"] = [
				"Oh? Is it a raid? {sender} raid?? Did they bring lots of treats??! ^..^"
			]
		if "host" not in self.Messages:
			self.Messages["host"] = [
				"Oh? Do I spy a host from {sender}?? Come on over and don't forget to bring treats! ^..^"
			]
		if "greet" not in self.Messages:
			self.Messages["greet"] = [
				"[Hello;Hi;Hey;Hewwo;Ello] {sender}, can I have some treats please?",
				"[Hello;Hi;Hey;Hewwo;Ello] {sender}!? Are you here to pet me? Or to give me wet food? Either one is fine, just let me know! ^..^"
			]
		if "lurk" not in self.Messages:
			self.Messages["lurk"] = [
				"Sit back, get some snacks and enjoy you lurk {sender}. But please share some with me~ ^..^"
			]
		if "unlurk" not in self.Messages:
			self.Messages["unlurk"] = [
				"Welcome back {sender}, can I have a treats now? Pretty please~ ^..^"
			]
		if "shoutout" not in self.Messages:
			self.Messages["shoutout"] = [
				"Please checkout {recipient}, they're a fantastic streamer"
			]
		
		#
		# Activities
		#
		if "Game" not in self.Activities:
			self.Activities["Game"] = [
				" and they were last playing {activity}"
			]
		if "Art" not in self.Activities:
			self.Activities["Art"] = [
				" and they were last streaming Art"
			]
		if "Makers and Crafting" not in self.Activities:
			self.Activities["Makers and Crafting"] = [
				" and they were last streaming Makers and Crafting"
			]
		if "Food & Drink" not in self.Activities:
			self.Activities["Food & Drink"] = [
				" and they were last streaming Food & Drink"
			]
		if "Music & Performing Arts" not in self.Activities:
			self.Activities["Music & Performing Arts"] = [
				" and they were last streaming Music & Performing Arts"
			]
		if "Beauty & Body Art" not in self.Activities:
			self.Activities["Beauty & Body Art"] = [
				" and they were last streaming Beauty & Body Art"
			]
		if "Science & Technology" not in self.Activities:
			self.Activities["Science & Technology"] = [
				" and they were last streaming Science & Technology activities"
			]
		if "Just Chatting" not in self.Activities:
			self.Activities["Just Chatting"] = [
				" and they were last chatting"
			]
		if "Travel & Outdoors" not in self.Activities:
			self.Activities["Travel & Outdoors"] = [
				" and they were last streaming Travel & Outdoors activities"
			]
		if "Sports & Fitness" not in self.Activities:
			self.Activities["Sports & Fitness"] = [
				" and they were last streaming Sports & Fitness activities"
			]
		if "Tabletop RPGs" not in self.Activities:
			self.Activities["Tabletop RPGs"] = [
				" and they were last playing IRL Tabletop RPG"
			]
		if "Special Events" not in self.Activities:
			self.Activities["Special Events"] = [
				" and they were last streaming a Special Event"
			]
		if "Talk Shows & Podcasts" not in self.Activities:
			self.Activities["Talk Shows & Podcasts"] = [
				" and they were last streaming a Talk Show or Podcast"
			]
		if "ASMR" not in self.Activities:
			self.Activities["ASMR"] = [
				" and they were last streaming ASMR"
			]
			
		## Autofill ScheduledMessages
		for action in self.ScheduledMessages:
			if 'Timer' not in action:
				action['Timer'] = 30
			if 'Enabled' not in action:
				action['Enabled'] = False
			if 'Command' not in action:
				action['Command'] = ""
			if 'Image' not in action:
				action['Image'] = ""
		
		## Autofill Commands
		for action in self.Commands:
			if 'Image' not in self.Commands[action]:
				self.Commands[action]['Image'] = ""
			if 'Script' not in self.Commands[action]:
				self.Commands[action]['Script'] = ""
			if 'Enabled' not in self.Commands[action]:
				self.Commands[action]['Enabled'] = False
			if 'ViewerOnce' not in self.Commands[action]:
				self.Commands[action]['ViewerOnce'] = False
			if 'ViewerTimeout' not in self.Commands[action]:
				self.Commands[action]['ViewerTimeout'] = 0
			if 'GlobalTimeout' not in self.Commands[action]:
				self.Commands[action]['GlobalTimeout'] = 0
			if 'Aliases' not in self.Commands[action]:
				self.Commands[action]['Aliases'] = []
			if 'Hotkey' not in self.Commands[action]:
				self.Commands[action]['Hotkey'] = []
			
			## Autofill CustomBits
			for action in self.CustomBits:
				if 'From' not in action:
					action['From'] = 0
				if 'To' not in action:
					action['To'] = 0
			
			## Autofill CustomSubs
			for action in self.CustomSubs:
				if 'From' not in action:
					action['From'] = 0
				if 'To' not in action:
					action['To'] = 0
				if 'Tier' not in action:
					action['Tier'] = ""
			
			## Autofill PoseMapping
			for action in self.PoseMapping:
				if 'Hue' in self.PoseMapping[action]:
					for light in self.PoseMapping[action]['Hue']:
						if 'Brightness' not in self.PoseMapping[action]['Hue'][light]:
							self.PoseMapping[action]['Hue'][light]['Brightness'] = 50
						if 'Color' not in self.PoseMapping[action]['Hue'][light]:
							self.PoseMapping[action]['Hue'][light]['Color'] = "#ffffff"
							
				if 'Yeelight' in self.PoseMapping[action]:
					for light in self.PoseMapping[action]['Yeelight']:
						if 'Brightness' not in self.PoseMapping[action]['Yeelight'][light]:
							self.PoseMapping[action]['Yeelight'][light]['Brightness'] = 50
						if 'Color' not in self.PoseMapping[action]['Yeelight'][light]:
							self.PoseMapping[action]['Yeelight'][light]['Color'] = "#ffffff"
						if 'Transition' not in self.PoseMapping[action]['Yeelight'][light]:
							self.PoseMapping[action]['Yeelight'][light]['Transition'] = True
						if 'TransitionTime' not in self.PoseMapping[action]['Yeelight'][light]:
							self.PoseMapping[action]['Yeelight'][light]['TransitionTime'] = 1000
		
		return
		
	#---------------------------
	#   CheckSettingsDependencies
	#---------------------------
	def CheckSettingsDependencies(self):
		error = 0
		
		#
		# Check mascot images configuration
		#
		for action in self.mascotImages:
			if not os.path.isfile(self.mascotImages[action]['Image']):
				print("Mascot image missing for action: " + action)
				if action == "Idle":
					error = 2
				
				if error < 2:
					error = 1
			
			if action != 'Idle':
				if 'MouthHeight' not in self.mascotImages[action]:
					print("Mascot image mouth height missing for action: " + action)
					error = 2
				else:
					if self.mascotImages[action]['MouthHeight'] < 1:
						print("Mascot image mouth height is too small for action: " + action)
						if error < 2:
							error = 1
				
				if 'Time' not in self.mascotImages[action]:
					print("Mascot image time missing for action: " + action)
					error = 2
				else:
					if self.mascotImages[action]['Time'] < 100:
						print("Mascot image time is too short for action: " + action)
						if error < 2:
							error = 1
		
		#
		# Check mascot audio configuration
		#
		for action in self.mascotAudio:
			for idx, val in enumerate(self.mascotAudio[action]['Audio']):
				if not os.path.isfile(self.mascotAudio[action]['Audio'][idx]):
					print("Mascot audio missing for action: " + action)
					if error < 2:
						error = 1
			
			if 'Volume' not in self.mascotAudio[action]:
				print("Mascot audio volume missing for action: " + action)
				error = 2
			else:
				if self.mascotAudio[action]['Volume'] > 0 and self.mascotAudio[action]['Volume'] <= 1:
					error = error
				else:
					print("Mascot audio volume value is invalid for action: " + action)
					if error < 2:
						error = 1
		
		#
		# Check mascot other configuration
		#
		if 'MascotMaxWidth' not in self.mascotStyles:
			print("Mascot MascotMaxWidth missing")
			error = 2
		else:
			if self.mascotStyles['MascotMaxWidth'] < 30:
				print("Mascot MascotMaxWidth is too small")
				if error < 2:
					error = 1
		
		#
		# Check default bindings
		#
		if 'Image' not in self.PoseMapping['DEFAULT']:
			print("Default pose mapping Image variable is missing.")
			error = 2
		else:
			if self.PoseMapping['DEFAULT']['Image'] not in self.mascotImages:
				print("Default pose mapping Image reference does not exist.")
				error = 2
		
		if 'Audio' not in self.PoseMapping['DEFAULT']:
			print("Default pose mapping Audio variable is missing.")
			if error < 2:
				error = 1
		else:
			if self.PoseMapping['DEFAULT']['Audio'] not in self.mascotAudio:
				print("Default pose mapping Audio reference does not exist.")
				if error < 2:
					error = 1
		
		#
		# Check other bindings
		#
		for action in self.PoseMapping:
			if 'Image' not in self.PoseMapping[action]:
				print("Pose mapping Image variable is missing for action: " + action)
				if error < 2:
					error = 1
			else:
				if self.PoseMapping[action]['Image'] not in self.mascotImages:
					print("Pose mapping Image reference does not exist for action: " + action)
					if error < 2:
						error = 1
			
			if 'Audio' in self.PoseMapping[action]:
				if self.PoseMapping[action]['Audio'] not in self.mascotAudio:
						print("Pose mapping Audio reference does not exist for action: " + action)
						if error < 2:
							error = 1
		
		#
		# Check messages
		#
		for action in self.Messages:
			if not isinstance(self.Messages[action], list):
				print("Message is not a list: " + action)
				exit(1)
		
		for action in self.Enabled:
			if action == 'autohost' or action == 'anonsubgift':
				continue
				
			if action not in self.Messages:
				print("Message does not exist: " + action)
				exit(1)
		
		#
		# Check ScheduledMessages
		#
		for action in self.ScheduledMessages:
			if 'Name' not in action:
				print("ScheduledMessages missing Name: ")
				print(action)
				exit(1)
			
			if not isinstance(action['Timer'], int):
				print("ScheduledMessages Timer value is not a number: " + action['Name'])
				exit(1)
			
			if action['Timer'] == 0:
				print("ScheduledMessages Timer value is 0: " + action['Name'])
				exit(1)
		
		#
		# Check Commands
		#
		for action in self.Commands:
			if not isinstance(self.Commands[action]['ViewerTimeout'], int):
				print("Commands ViewerTimeout value is not a number: " + action)
				exit(1)
			
			if not isinstance(self.Commands[action]['GlobalTimeout'], int):
				print("Commands GlobalTimeout value is not a number: " + action)
				exit(1)
		
		#
		# CustomBits
		#
		for action in self.CustomBits:
			if 'Name' not in action:
				print("CustomBits missing Name: ")
				print(action)
				exit(1)
				
			if 'From' not in action:
				print("CustomBits is missing parameter From: " + action['Name'])
				exit(1)
				
			if not isinstance(action['From'], int):
				print("CustomBits is From value is not a number: " + action['Name'])
				exit(1)
				
			if 'To' not in action:
				print("CustomBits is missing parameter From: " + action['Name'])
				exit(1)
				
			if not isinstance(action['To'], int):
				print("CustomBits is To value is not a number: " + action['Name'])
				exit(1)
				
			if action['To'] == 0:
				print("CustomBits To value is 0: " + action['Name'])
				exit(1)
				
			if action['From'] > action['To']:
				print("CustomBits From value is higher or equal to To: " + action['Name'])
				exit(1)
		
		#
		# CustomSubs
		#
		for action in self.CustomSubs:
			if 'Name' not in action:
				print("CustomSubs missing Name: ")
				print(action)
				exit(1)
			
			if 'From' not in action:
				print("CustomSubs is missing parameter From: " + action['Name'])
				exit(1)
			
			if not isinstance(action['From'], int):
				print("CustomSubs is From value is not a number: " + action['Name'])
				exit(1)
			
			if 'To' not in action:
				print("CustomSubs is missing parameter From: " + action['Name'])
				exit(1)
			
			if not isinstance(action['To'], int):
				print("CustomSubs is To value is not a number: " + action['Name'])
				exit(1)
				
			if action['To'] == 0:
				print("CustomSubs To value is 0: " + action['Name'])
				exit(1)
			
			if action['From'] > action['To']:
				print("CustomSubs From value is higher or equal to To: " + action['Name'])
				exit(1)
		
		if error == 2:
			print("Mandatory dependencies are broken, see above.")
			exit(1)
		
		return
		
	#---------------------------
	#   UpgradeSettingsFile
	#---------------------------
	def UpgradeSettingsFile(self):
		#
		# CurrectMascot fix v1.1
		#
		if hasattr(self, 'CurrectMascot'):
			self.CurrentMascot = self.CurrectMascot
			del self.CurrectMascot
		
		#
		# ScheduledMessages Messages and remove LastShown v1.2
		#
		for action in self.ScheduledMessages:
			if 'LastShown' in action:
				del action['LastShown']
			if 'Message' in action:
				if action['Name'] in self.Messages:
					print("Upgrade: Cannot migrate message values from ScheduledMessages to Messages. " + action['Name'] + " already exists in Messages.")
					exit(1)
				else:
					self.Messages[action['Name']] = action['Message']
					del action['Message']
		
		#
		# Commands Messages v1.2
		#
		for action in self.Commands:
			if 'Message' in self.Commands[action]:
				if action in self.Messages:
					print("Upgrade: Cannot migrate message values from Commands to Messages. " + action + " already exists in Messages.")
					exit(1)
				else:
					self.Messages[action] = self.Commands[action]['Message']
					del self.Commands[action]['Message']
		
		#
		# CustomGreets v1.2
		#
		if hasattr(self, 'CustomGreets'):
			for action in self.CustomGreets:
				if action in self.Messages:
					print("Upgrade: Cannot migrate CustomGreets to Messages. " + action + " already exists in Messages.")
					exit(1)
			
			for action in self.CustomGreets:
				self.Messages["viewer_" + action] = self.CustomGreets[action]
			
			del self.CustomGreets
		
		return
		
	#---------------------------
	#   Save
	#---------------------------
	def Save(self):
		## Export config
		tmp = {}
		try:
			for key in self.__dict__:
				if key[:1].isupper():
					tmp[key] = self.__dict__[key]
		except:
			print("Failed to export configuration")
		
		## Save config
		try:
			with codecs.open(self.pathRoot + "settings.json", encoding="utf-8-sig", mode="w+") as f:
				json.dump(tmp, f, indent=4)
		except:
			print("Failed to save settings.json")
			exit(1)
		
		## Save config copy
		try:
			with codecs.open(self.pathRoot + "settings.bak", encoding="utf-8-sig", mode="w+") as f:
				json.dump(tmp, f, indent=4)
		except:
			print("Failed to save settings.bak")
			exit(1)
		
		return
		
	#---------------------------
	#   Verify
	#---------------------------
	def Verify(self):
		code = 0
		## Check user name
		if len(self.TwitchChannel) < 1:
			print("Twitch channel not specified")
			code = 1
		
		## Check OAUTH
		if self.TwitchOAUTH.find('oauth:') != 0:
			print("Twitch OAUTH is invalid")
			code = 1
		
		## Check chatbot
		if self.UseChatbot:
			if len(self.TwitchBotOAUTH) > 0 and self.TwitchBotOAUTH.find('oauth:') != 0:
				print("Twitch Bot OAUTH is invalid")
				code = 1
		
		## Check twitch client ID
		if len(self.twitchClientID) < 1:
			print("Twitch ClientID not specified. See https://dev.twitch.tv/docs/v5/#getting-a-client-id")
			code = 1
		
		if code:
			exit(code)
			
		return