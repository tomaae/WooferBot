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
from time import time

#---------------------------
#   Settings Handling
#---------------------------
class Settings:
	def __init__(self, pathRoot=None):
		self.pathRoot     = pathRoot + '\\'
		if not os.path.isdir(self.pathRoot):
			print("Working directory not detected.")
			exit(1)
		if not os.path.isfile(self.pathRoot + "wooferbot.py"):
			print("Working directory incorrect.")
			exit(1)
		if not os.path.isfile(self.pathRoot + "settings.json"):
			print("Configuration file \"settings.json\" is missing.")
			exit(1)
			
		self.Reload()
		self.ReloadMascot()
		self.CheckMascotDependencies()
		return
		
	def CheckMascotDependencies(self):
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
			error = 2
		else:
			if self.PoseMapping['DEFAULT']['Audio'] not in self.mascotAudio:
				print("Default pose mapping Audio reference does not exist.")
				error = 2			

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
				
			if 'Message' not in action:
				print("ScheduledMessages missing Message: ")
				print(action)
				exit(1)
			
			if not isinstance(action['Message'], list):
				print("ScheduledMessages Message is not a list: ")
				print(action)
				exit(1)
				
		#
		# Check Commands
		#
		for action in self.Commands:
			if 'Message' not in self.Commands[action]:
				print("Commands missing Message: " + action)
				exit(1)
				
			if not isinstance(self.Commands[action]['Message'], list):
				print("Commands message is not a list: " + action)
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
				
			if action['From'] >= action['To']:
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
				
			if action['From'] >= action['To']:
				print("CustomSubs From value is higher or equal to To: " + action['Name'])
				exit(1)
		
		#
		# CustomGreets
		#
		for action in self.CustomGreets:
			if not isinstance(self.CustomGreets[action], list):
				print("CustomGreets message is not a list: " + action)
				exit(1)
				
			
		if error == 2:
			print("Mandatory dependencies are broken, see above.")
			exit(1)
		
		return
		
	def ReloadMascot(self):
		print("Loading mascot settings...")
		self.mascotImages = {}
		self.mascotAudio  = {}
		self.mascotStyles = {}

		try:
			with codecs.open(self.pathRoot + "mascots\\" + self.CurrentMascot + "\\mascot.json", encoding="utf-8-sig", mode="r") as f:
				data = json.load(f, encoding="utf-8")
				for key, value in data.items():
						self.__dict__[key] = value 
		except:
			print("Unable to load mascot.json")
			exit(1)
		
		for action in self.mascotImages:
			if 'Image' not in self.mascotImages[action]:
				print("Mascot Image variable is missing for action: " + action)
				exit(1)
			
			self.mascotImages[action]['Image'] = self.pathRoot + "mascots\\" + self.CurrentMascot + "\\images\\" + self.mascotImages[action]['Image']
			
		for action in self.mascotAudio:
			if not isinstance(self.mascotAudio[action]['Audio'],list):
				print("Mascot audio is not a list for action: " + action)
				exit(1)
				
			for idx, val in enumerate(self.mascotAudio[action]['Audio']):
				self.mascotAudio[action]['Audio'][idx] = self.pathRoot + "mascots\\" + self.CurrentMascot + "\\audio\\" + self.mascotAudio[action]['Audio'][idx]
		
		return


	def Reload(self):
		print("Loading settings...")
		self.TwitchChannel     = ""
		self.TwitchOAUTH       = ""
		self.twitchClientID    = "zpm94cuvrntu030mauvxvz9cv2ldja"
		self.Styles            = {}
		self.Messages          = {}
		self.Activities        = {}
		self.Enabled           = {}
		self.PoseMapping       = {}
		self.CurrentMascot     = "malamute"
		self.pathImages        = self.pathRoot + "mascots" + '\\' + self.CurrentMascot + '\\' + "images" + '\\'
		self.pathAudio         = self.pathRoot + "mascots" + '\\' + self.CurrentMascot + '\\' + "audio" + '\\'
		self.HostMessage       = ""
		self.AutohostMessage   = ""
		self.FollowMessage     = ""
		self.GlobalVolume      = 0.2
		self.MinBits           = 0
		self.AutoShoutout      = False
		self.AutoShoutoutTime  = 10
		self.Bots              = []
		self.commonBots        = ["nightbot", "streamlabs", "streamelements", "stay_hydrated_bot", "botisimo", "wizebot", "moobot"]
		self.ScheduledMessages = []
		self.CustomBits        = []
		self.CustomSubs        = []
		self.CustomGreets      = {}
		self.Commands          = {}
		
		self.NanoleafEnabled   = False
		self.NanoleafIP        = ""
		self.NanoleafToken     = ""
		
		try:
			with codecs.open(self.pathRoot + "settings.json", encoding="utf-8-sig", mode="r") as f:
				data = json.load(f, encoding="utf-8")
				for key, value in data.items():
						self.__dict__[key] = value 
		except:
			print("Unable to load settings.json")
			exit(1)
		finally:
			#
			# CONVERT
			#
			self.TwitchChannel = self.TwitchChannel.lower()
			self.CurrentMascot = self.CurrentMascot.lower()
			self.Bots = [x.lower() for x in self.Bots]
			#
			# DEFAULT
			#
			if self.CurrentMascot == "":
				self.CurrentMascot = "tomaae"
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
				self.Enabled["new_chatter"] = 1
			if "greet" not in self.Enabled:
				self.Enabled["greet"] = 1
			if "follow" not in self.Enabled:
				self.Enabled["follow"] = 1
			if "raid" not in self.Enabled:
				self.Enabled["raid"] = 1
			if "host" not in self.Enabled:
				self.Enabled["host"] = 1
			if "autohost" not in self.Enabled:
				self.Enabled["autohost"] = 1
			if "sub" not in self.Enabled:
				self.Enabled["sub"] = 1
			if "resub" not in self.Enabled:
				self.Enabled["resub"] = 1
			if "subgift" not in self.Enabled:
				self.Enabled["subgift"] = 1
			if "anonsubgift" not in self.Enabled:
				self.Enabled["anonsubgift"] = 1
			if "bits" not in self.Enabled:
				self.Enabled["bits"] = 1
			if "lurk" not in self.Enabled:
				self.Enabled["lurk"] = 1
			if "shoutout" not in self.Enabled:
				self.Enabled["shoutout"] = 1
				
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
				
		self.Verify()
		
		return

	def Save(self):
		tmp = {}
		try:
			for key in self.__dict__:
				if key[:1].isupper():
					tmp[key] = self.__dict__[key]
		except:
			print("Failed to export configuration")
			
		try:
			with codecs.open(self.pathRoot + "settings.json", encoding="utf-8-sig", mode="w+") as f:
				json.dump(tmp, f, indent=4)
		except:
			print("Failed to save settings.json")
			exit(1)
			
		try:
			with codecs.open(self.pathRoot + "settings.bak", encoding="utf-8-sig", mode="w+") as f:
				json.dump(tmp, f, indent=4)
		except:
			print("Failed to save settings.bak")
			exit(1)
			
	def Verify(self):
		if len(self.TwitchChannel) < 1:
			print("Twitch channel not specified")
			exit(1)
			
		if self.TwitchOAUTH.find('oauth:') != 0:
			print("Twitch OAUTH is invalid")
			exit(1)
			
		if len(self.twitchClientID) < 1:
			print("Twitch ClientID not specified. See https://dev.twitch.tv/docs/v5/#getting-a-client-id")
			exit(1)
			
		return