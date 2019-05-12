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
						"mascot"     : self.woofer.mascotImagesFile('!start'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('!start'),
						"time"       : self.woofer.mascotImagesTime('!start'),
						"audio"      : self.woofer.mascotAudioFile('!start'),
						"volume"     : self.woofer.mascotAudioVolume('!start'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('!start')
					})

			#
			# Follow
			#
			if cmd == "1":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['follow']),
						"sender"     : "testname",
						"customtag"  : "follow",
						"mascot"     : self.woofer.mascotImagesFile('follow'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('follow'),
						"time"       : self.woofer.mascotImagesTime('follow'),
						"audio"      : self.woofer.mascotAudioFile('follow'),
						"volume"     : self.woofer.mascotAudioVolume('follow'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('follow')
					})
					
			#
			# Greet
			#
			if cmd == "2":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['greet']),
						"sender"     : "testname",
						"customtag"  : "greet",
						"mascot"     : self.woofer.mascotImagesFile('greet'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('greet'),
						"time"       : self.woofer.mascotImagesTime('greet'),
						"audio"      : self.woofer.mascotAudioFile('greet'),
						"volume"     : self.woofer.mascotAudioVolume('greet'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('greet')
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
						"mascot"     : self.woofer.mascotImagesFile('shoutout'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('shoutout'),
						"time"       : self.woofer.mascotImagesTime('shoutout'),
						"audio"      : self.woofer.mascotAudioFile('shoutout'),
						"volume"     : self.woofer.mascotAudioVolume('shoutout'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('shoutout')
					})
					
			#
			# Lurk
			#
			if cmd == "4":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['lurk']),
						"sender"     : "testname",
						"customtag"  : "lurk",
						"mascot"     : self.woofer.mascotImagesFile('lurk'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('lurk'),
						"time"       : self.woofer.mascotImagesTime('lurk'),
						"audio"      : self.woofer.mascotAudioFile('lurk'),
						"volume"     : self.woofer.mascotAudioVolume('lurk'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('lurk')
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
						"mascot"     : self.woofer.mascotImagesFile('bits'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('bits'),
						"time"       : self.woofer.mascotImagesTime('bits'),
						"audio"      : self.woofer.mascotAudioFile('bits'),
						"volume"     : self.woofer.mascotAudioVolume('bits'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('bits')
					})
					
			#
			# New chatter
			#
			if cmd == "6":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['new_chatter']),
						"sender"     : "testname",
						"customtag"  : "new_chatter",
						"mascot"     : self.woofer.mascotImagesFile('new_chatter'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('new_chatter'),
						"time"       : self.woofer.mascotImagesTime('new_chatter'),
						"audio"      : self.woofer.mascotAudioFile('new_chatter'),
						"volume"     : self.woofer.mascotAudioVolume('new_chatter'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('new_chatter')
					})
					
			#
			# Raid
			#
			if cmd == "7":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['raid']),
						"sender"     : "testname",
						"customtag"  : "raid",
						"mascot"     : self.woofer.mascotImagesFile('raid'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('raid'),
						"time"       : self.woofer.mascotImagesTime('raid'),
						"audio"      : self.woofer.mascotAudioFile('raid'),
						"volume"     : self.woofer.mascotAudioVolume('raid'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('raid')
					})
					
			#
			# Host
			#
			if cmd == "8":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['host']),
						"sender"     : "testname",
						"customtag"  : "host",
						"mascot"     : self.woofer.mascotImagesFile('host'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('host'),
						"time"       : self.woofer.mascotImagesTime('host'),
						"audio"      : self.woofer.mascotAudioFile('host'),
						"volume"     : self.woofer.mascotAudioVolume('host'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('host')
					})
					
			#
			# Sub
			#
			if cmd == "9":
				self.woofer.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.woofer.settings.Messages['sub']),
						"sender"     : "testname",
						"customtag"  : "sub",
						"mascot"     : self.woofer.mascotImagesFile('sub'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('sub'),
						"time"       : self.woofer.mascotImagesTime('sub'),
						"audio"      : self.woofer.mascotAudioFile('sub'),
						"volume"     : self.woofer.mascotAudioVolume('sub'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('sub')
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
						"mascot"     : self.woofer.mascotImagesFile('resub'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('resub'),
						"time"       : self.woofer.mascotImagesTime('resub'),
						"audio"      : self.woofer.mascotAudioFile('resub'),
						"volume"     : self.woofer.mascotAudioVolume('resub'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('resub')
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
						"mascot"     : self.woofer.mascotImagesFile('giftsub'),
						"mascotmouth": self.woofer.mascotImagesMouthHeight('giftsub'),
						"time"       : self.woofer.mascotImagesTime('giftsub'),
						"audio"      : self.woofer.mascotAudioFile('giftsub'),
						"volume"     : self.woofer.mascotAudioVolume('giftsub'),
						"nanoleaf"   : self.woofer.mascotNanoleafScene('giftsub')
					})
				
			
			#print(cmd)
		return
		
		