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

import random

#---------------------------
#   CLI Handling
#---------------------------
class Cli:
	def __init__(self, settings, woofer):
		self.woofer   = woofer
		self.settings = settings

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

			#
			# Start
			#
			if cmd == "0":
				self.woofer.woofer_addtoqueue({
						"message"    : "{Sender}",
						"sender"     : self.settings.Commands['!start']['Message'],
						"customtag"  : "follow",
						"id"         : "!start"
					})

			#
			# Follow
			#
			if cmd == "1":
				self.woofer.woofer_follow({
						"display-name" : "testname",
						"custom-tag"   : "follow"
				})
					
			#
			# Greet
			#
			if cmd == "2":
				self.woofer.woofer_greet({
						"display-name" : "testname",
						"sender"       : "testname",
						"custom-tag"   : "greet"
				})
					
			#
			# Shoutout
			#
			if cmd == "3":
				self.woofer.woofer_shoutout({
						"moderator"    : "1",
						"display-name" : "testname",
						"sender"       : "testname",
						"command_parameter" : "testname",
						"custom-tag"   : "shoutout"
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
				self.woofer.woofer_bits({
						"display-name" : "testname",
						"bits"         : "1000",
						"custom-tag"   : "bits"
				})
					
			#
			# New chatter
			#
			if cmd == "6":
				self.woofer.woofer_new_chatter({
						"display-name" : "testname",
						"sender"       : "testname",
						"custom-tag"   : "new_chatter"
				})
				
			#
			# Raid
			#
			if cmd == "7":
				self.woofer.woofer_raid({
						"display-name" : "testname",
						"sender"       : "testname",
						"custom-tag"   : "raid"
				})
				
			#
			# Host
			#
			if cmd == "8":
				self.woofer.woofer_host({
						"display-name" : "testname",
						"sender"       : "testname",
						"custom-tag"   : "host"
				})
					
			#
			# Sub
			#
			if cmd == "9":
				self.woofer.woofer_sub({
						"display-name" : "testname",
						"sender"       : "testname",
						"custom-tag"   : "sub"
				})
				
			#
			# Resub
			#
			if cmd == "10":
				self.woofer.woofer_resub({
						"display-name" : "testname",
						"sender"       : "testname",
						"msg-param-cumulative-months" : "3",
						"custom-tag"   : "resub"
				})
					
			#
			# Subgift
			#
			if cmd == "11":
				self.woofer.woofer_subgift({
						"display-name" : "testname",
						"sender"       : "testname",
						"msg-param-recipient-display-name" : "testname2",
						"custom-tag"   : "subgift"
				})
			
			#print(cmd)
		return
		
		