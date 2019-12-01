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


#---------------------------
#   CLI Handling
#---------------------------
class Cli:
	def __init__(self, settings, woofer, twitch, twitchBot):
		self.woofer = woofer
		self.settings = settings
		self.twitch = twitch
		self.twitchBot = twitchBot
		return
	
	def Start(self):
		print("Starting cli...")
		while True:
			cmd = input("")
			
			if cmd == "x":
				print("exit")
			if cmd == "h":
				print(" === WooferBot Help ===")
				print(" 1 - Follow")
				print(" 2 - Greet")
				print(" 3 - Shoutout")
				print(" 4 - Lurk")
				print(" 5 - Bits")
				print(" 6 - New chatter")
				print(" 7 - Raid")
				print(" 8 - Host")
				print(" 9 - Sub")
				print("10 - Resub")
				print("11 - Subgift")
				print("r  - Reconnect to twitch")
			
			#
			# Start
			#
			if cmd == "0":
				self.woofer.woofer_commands({
					"display-name" : "testname",
					"sender"       : "testname",
					"broadcaster"  : 1,
					"command"      : "!start",
					"custom-tag"   : "!start"
				})
			
			#
			# Follow
			#
			if cmd == "1":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"custom-tag"   : "follow"
				})
			
			#
			# Greet
			#
			if cmd == "2":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"sender"       : "testname",
					"custom-tag"   : "greet"
				})
			
			#
			# Shoutout
			#
			if cmd == "3":
				self.woofer.woofer_shoutout({
					"subscriber"        : "1",
					"vip"               : "1",
					"moderator"         : "1",
					"broadcaster"       : "1",
					"display-name"      : "testname",
					"sender"            : "testname",
					"command_parameter" : "testname",
					"custom-tag"        : "shoutout"
				})
			
			#
			# Lurk
			#
			if cmd == "4":
				self.woofer.woofer_lurk({
					"display-name" : "testname",
					"sender"       : "testname",
					"custom-tag"   : "lurk"
				})
			
			#
			# Bits
			#
			if cmd == "5":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"bits"         : "1000",
					"custom-tag"   : "bits"
				})
			
			#
			# New chatter
			#
			if cmd == "6":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"sender"       : "testname",
					"custom-tag"   : "new_chatter"
				})
			
			#
			# Raid
			#
			if cmd == "7":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"sender"       : "testname",
					"viewers"      : "1",
					"custom-tag"   : "raid"
				})
			
			#
			# Host
			#
			if cmd == "8":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"sender"       : "testname",
					"custom-tag"   : "host"
				})
			
			#
			# Sub
			#
			if cmd == "9":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"sender"       : "testname",
					"sub_tier"     : "Tier 2",
					"months"       : "4",
					"months_streak": "4",
					"custom-tag"   : "sub"
				})
			
			#
			# Resub
			#
			if cmd == "10":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"sender"       : "testname",
					"sub_tier"     : "Tier 2",
					"months"       : "4",
					"months_streak": "4",
					"custom-tag"   : "resub"
				})
			
			#
			# Subgift
			#
			if cmd == "11":
				self.woofer.woofer_alert({
					"display-name" : "testname",
					"sender"       : "testname",
					"sub_tier"     : "Tier 2",
					"msg-param-recipient-display-name" : "testname2",
					"custom-tag"   : "subgift"
				})
			
			#
			# Reconnect to twitch
			#
			if cmd == "r":
				if self.twitch.connected:
					self.twitch.Disconnect()
				if self.twitchBot.connected:
					self.twitchBot.Disconnect()
			
			#print(cmd)
		return
