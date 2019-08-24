##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for twitch.tv
#    Copyright (C) 2019  Tomaae
#    (https://github.com/tomaae/WooferBot)
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
		if not os.path.exists(self.pathRoot + "wooferbot.py"):
			print("Working directory incorrect.")
			exit(1)
		if not os.path.exists(self.pathRoot + "settings.json"):
			print("Configuration file \"settings.json\" is missing.")
			exit(1)
			
		self.Reload()
		self.ReloadMascot()
		return
		
		
	def ReloadMascot(self):
		print("Loading mascot settings...")
		self.mascotImages = {}
		self.mascotAudio  = {}
		self.mascotStyles = {}

		try:
			with codecs.open(self.pathRoot + "mascots\\" + self.CurrectMascot + "\\mascot.json", encoding="utf-8-sig", mode="r") as f:
				data = json.load(f, encoding="utf-8")
				for key, value in data.items():
						self.__dict__[key] = value 
		except:
			print("Unable to load mascot.json")
			exit(1)
		
		for action in self.mascotImages:
			self.mascotImages[action]['Image'] = self.pathRoot + "mascots\\" + self.CurrectMascot + "\\images\\" + self.mascotImages[action]['Image']
			
		for action in self.mascotAudio:
			for idx, val in enumerate(self.mascotAudio[action]['Audio']):
				self.mascotAudio[action]['Audio'][idx] = self.pathRoot + "mascots\\" + self.CurrectMascot + "\\audio\\" + self.mascotAudio[action]['Audio'][idx]
		
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
		self.CurrectMascot     = "malamute"
		self.pathImages        = self.pathRoot + "mascots" + '\\' + self.CurrectMascot + '\\' + "images" + '\\'
		self.pathAudio         = self.pathRoot + "mascots" + '\\' + self.CurrectMascot + '\\' + "audio" + '\\'
		self.HostMessage       = ""
		self.AutohostMessage   = ""
		self.FollowMessage     = ""
		self.GlobalVolume      = 0.2
		self.MinBits           = 0
		self.Bots              = []
		self.commonBots        = ["nightbot", "streamlabs", "streamelements", "stay_hydrated_bot", "botisimo", "wizebot"]
		self.ScheduledMessages = []
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
			self.CurrectMascot = self.CurrectMascot.lower()
			self.Bots = [x.lower() for x in self.Bots]
			#
			# DEFAULT
			#
			if self.CurrectMascot == "":
				self.CurrectMascot = "tomaae"
			if self.HostMessage == "":
				self.HostMessage = "is now hosting you."
			if self.AutohostMessage == "":
				self.AutohostMessage = "is auto hosting you"
			if self.FollowMessage == "":
				self.FollowMessage = "Thank you for the follow!"
			if not self.MinBits:
				self.MinBits = 0
				
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
				self.Styles["BackgroundColor"] = "#fef7ed"
			if "BorderColor" not in self.Styles:
				self.Styles["BorderColor"] = "#ffba70"
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
				self.Styles["TextColor"] = "#b16a16"
			if "HighlightTextSize" not in self.Styles:
				self.Styles["HighlightTextSize"] = 24
			if "HighlightTextSpacing" not in self.Styles:
				self.Styles["HighlightTextSpacing"] = 3
			if "HighlightTextColor" not in self.Styles:
				self.Styles["HighlightTextColor"] = "#ffba70"
			if "HighlightTextStrokeColor" not in self.Styles:
				self.Styles["HighlightTextStrokeColor"] = "#b16a16"
			if "HighlightTextShadowColor" not in self.Styles:
				self.Styles["HighlightTextShadowColor"] = "#ffba70"
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
			if "giftsub" not in self.Messages:
				self.Messages["giftsub"] = [
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