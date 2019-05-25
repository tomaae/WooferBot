##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for twitch.tv
#    Copyright (C) 2019  Tomaae
#    (https://github.com/tomaae/WooferBot)
#
#    This file is part of WooferBot.
#
#    WooferBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WooferBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WooferBot.  If not, see <https://www.gnu.org/licenses/>.
#
##########################################################################\

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
				print("11 - Giftsub")

			#
			# Start
			#
			if cmd == "0":
				self.woofer.woofer_addtoqueue({
						"message"    : self.settings.Commands['!start']['Message'],
						"sender"     : "testname",
						"customtag"  : "follow",
						"id"         : "!start"
					})

			#
			# Follow
			#
			if cmd == "1":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['follow']),
						"sender"     : "testname",
						"customtag"  : "follow",
						"id"         : "follow"
					})
					
			#
			# Greet
			#
			if cmd == "2":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['greet']),
						"sender"     : "testname",
						"customtag"  : "greet",
						"id"         : "greet"
					})
					
			#
			# Shoutout
			#
			if cmd == "3":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.settings.Messages['shoutout']) + random.SystemRandom().choice(self.settings.Activities["Game"]),
						"sender"     : "testname",
						"recipient"  : "testname",
						"activity"   : "Pong",
						"customtag"  : "shoutout",
						"id"         : "greet"
					})
					
			#
			# Lurk
			#
			if cmd == "4":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['lurk']),
						"sender"     : "testname",
						"customtag"  : "lurk",
						"id"         : "lurk"
					})
					
			#
			# Bits
			#
			if cmd == "5":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['bits']),
						"sender"     : "testname",
						"bits"       : "1000",
						"customtag"  : "bits",
						"id"         : "bits"
					})
					
			#
			# New chatter
			#
			if cmd == "6":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['new_chatter']),
						"sender"     : "testname",
						"customtag"  : "new_chatter",
						"id"         : "new_chatter"
					})
					
			#
			# Raid
			#
			if cmd == "7":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['raid']),
						"sender"     : "testname",
						"customtag"  : "raid",
						"id"         : "raid"
					})
					
			#
			# Host
			#
			if cmd == "8":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['host']),
						"sender"     : "testname",
						"customtag"  : "host",
						"id"         : "host"
					})
					
			#
			# Sub
			#
			if cmd == "9":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['sub']),
						"sender"     : "testname",
						"customtag"  : "sub",
						"id"         : "sub"
					})
					
			#
			# Resub
			#
			if cmd == "10":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['resub']),
						"sender"     : "testname",
						"months"     : "3",
						"customtag"  : "resub",
						"id"         : "resub"
					})
					
			#
			# Giftsub
			#
			if cmd == "11":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['giftsub']),
						"sender"     : "testname",
						"recipient"  : "testname",
						"customtag"  : "giftsub",
						"id"         : "giftsub"
					})
				
			
			#print(cmd)
		return
		
		