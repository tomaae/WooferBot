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
##########################################################################

import json
import requests
import uuid
import random
import threading
import time
import os

#---------------------------
#   Woofer logic
#---------------------------
class Woofer:
	def __init__(self, settings, overlay, nanoleaf):
		self.settings       = settings
		self.overlay        = overlay
		self.nanoleaf       = nanoleaf
		
		self.queue          = []
		self.greetedUsers   = []
		self.greetedUsers.append(self.settings.TwitchChannel)
		self.greetedUsers.append(self.settings.TwitchChannel + "bot")
		
		self.lurkingUsers   = []
		self.unlurkingUsers = []
		self.hostingUsers   = []
		self.shoutoutUsers  = []
		
		for message in self.settings.ScheduledMessages:
			currentEpoch = int(time.time())
			message['LastShown'] = currentEpoch
		threading.Timer(300, self.woofer_timer).start()
		return
		
	#---------------------------
	#   ProcessJson
	#---------------------------
	def ProcessJson(self, jsonData):
		#
		# Commands
		#
		if jsonData['custom-tag'] == 'command':
			# shoutout
			if jsonData['command'] == '!so' or jsonData['command'] == '!shoutout':
				if self.settings.Enabled["shoutout"]:
					self.woofer_shoutout(jsonData)
				return
			# lurk/unlurk
			if self.settings.Enabled["lurk"]:
				if jsonData['command'] == '!lurk':
					self.woofer_lurk(jsonData)
					return
				if jsonData['command'] == '!unlurk' or jsonData['command'] == '!back':
					self.woofer_unlurk(jsonData)
					return
					
			# custom commands
			if jsonData['command'] in self.settings.Commands:
				self.woofer_commands(jsonData)
			return

		#
		# Messages
		#
		if jsonData['custom-tag'] == 'message':
			# alerts from streamlabs chatbot
			if jsonData['sender'] == self.settings.TwitchChannel + "bot" or jsonData['sender'] == "streamlabs" or jsonData['sender'] == "streamelements":
				# follow
				if jsonData['message'].find(self.settings.FollowMessage) > 0 and self.settings.Enabled["follow"]:
					line = jsonData['message'].split(" ")
					jsonData['display-name'] = line[0].rstrip(',')
					self.woofer_follow(jsonData)
					return
				return
				
			# bits
			if int(jsonData['bits']) > 0 and int(jsonData['bits']) >= self.settings.MinBits and self.settings.Enabled["bits"]:
				self.woofer_bits(jsonData)
				return
			
			# greeting
			commonBots = set(self.settings.commonBots)
			customBots = set(self.settings.Bots)
			if self.settings.Enabled["greet"] and jsonData['sender'] not in commonBots and jsonData['sender'] not in customBots:
				self.woofer_greet(jsonData)
		
			return
			
		#
		# Rituals
		#
		if jsonData['custom-tag'] == 'new_chatter' and self.settings.Enabled["new_chatter"]:
			self.woofer_new_chatter(jsonData)
			return

		#
		# Raid/host/autohost
		#
		if jsonData['custom-tag'] == 'raid' and self.settings.Enabled["raid"]:
			self.woofer_raid(jsonData)
			return
			
		if jsonData['custom-tag'] == 'host' and self.settings.Enabled["host"]:
			self.woofer_host(jsonData)
			return
			
		if jsonData['custom-tag'] == 'autohost' and self.settings.Enabled["autohost"]:
			self.woofer_host(jsonData)
			return
			
		#
		# Sub
		#
		if jsonData['custom-tag'] == 'sub' and self.settings.Enabled["sub"]:
			self.woofer_sub(jsonData)
			return
			
		if jsonData['custom-tag'] == 'resub' and self.settings.Enabled["resub"]:
			self.woofer_resub(jsonData)
			return
			
		if jsonData['custom-tag'] == 'subgift' and self.settings.Enabled["subgift"]:
			self.woofer_giftsub(jsonData)
			return
			
		if jsonData['custom-tag'] == 'anonsubgift' and self.settings.Enabled["anonsubgift"]:
			self.woofer_giftsub(jsonData)
			return
			
	#---------------------------
	#   woofer_timer
	#---------------------------
	def woofer_timer(self):
		
		# Check if overlay is connected
		if self.overlay.active < 1:
			threading.Timer(30, self.woofer_timer).start()
			return
			
		for message in self.settings.ScheduledMessages:
			if message['Enabled'] == 0:
				continue
			
			currentEpoch = int(time.time())
			if (currentEpoch - message['LastShown']) >= (message['Timer'] * 60):
				message['LastShown'] = currentEpoch
				self.woofer_addtoqueue({
					"message"    : message['Message'],
					"image"      : self.settings.pathRoot + "\\images\\" + message['Image'],
					"sender"     : "",
					"customtag"  : "ScheduledMessage",
					"mascot"     : self.mascotImagesFile(message['Name']),
					"mascotmouth": self.mascotImagesMouthHeight(message['Name']),
					"time"       : self.mascotImagesTime(message['Name']),
					"audio"      : self.mascotAudioFile(message['Name']),
					"volume"     : self.mascotAudioVolume(message['Name']),
					"nanoleaf"	 : self.mascotNanoleafScene(message['Name'])
				})

			
		# Reset to default after X seconds
		threading.Timer(60, self.woofer_timer).start()
		return
	
	#---------------------------
	#   woofer_queue
	#---------------------------
	def woofer_queue(self, queue_id, jsonData):
		if not self.queue:
			return
		
		# Check if overlay is connected
		if self.overlay.active < 1:
			print("waiting")
			threading.Timer(3, self.woofer_queue, args=(queue_id, jsonData)).start()
			return
		
		# Check if our turn in queue
		if self.queue[0] != queue_id:
			threading.Timer(0.5, self.woofer_queue, args=(queue_id, jsonData)).start()
			return
		
		# Send to overlay, retry later if overlay buffer is full
		if self.overlay.Send("EVENT_WOOFERBOT", jsonData) == 1:
			threading.Timer(1, self.woofer_queue, args=(queue_id, jsonData)).start()
			return
		
		# nanoleaf
		if 'nanoleaf' in jsonData and jsonData['nanoleaf'] != "":
			self.nanoleaf.Scene(jsonData['nanoleaf'])
		
		# default_woofer
		def default_woofer(queue_id):
			mascotIdleImage = self.settings.mascotImages['Idle']['Image']
			if not os.path.exists(mascotIdleImage):
				mascotIdleImage = ""
			
			if 'Idle' in self.settings.PoseMapping and self.settings.PoseMapping['Idle']['Image'] in self.settings.mascotImages:
				tmp = self.settings.mascotImages[self.settings.PoseMapping['Idle']['Image']]['Image']
				if os.path.exists(tmp):
					mascotIdleImage = tmp
			
			jsonData = {
				"mascot": mascotIdleImage,
			}
			self.overlay.Send("EVENT_WOOFERBOT", jsonData)
			self.nanoleaf.Off()
			if self.queue:
				self.queue.remove(queue_id)
			return
		
		# Reset to default after X seconds
		threading.Timer(jsonData['time'] / 1000, default_woofer, args=(queue_id,)).start()
		return

	#---------------------------
	#   woofer_addtoqueue
	#---------------------------
	def woofer_addtoqueue(self,jsonResponse):
		print("{0}: {1}".format(jsonResponse['customtag'], jsonResponse['sender']))
		# add to queue and wait for slot
		queue_id = uuid.uuid4()
		self.queue.append(queue_id)
		threading.Thread(target=self.woofer_queue, args=(queue_id, jsonResponse)).start()
		return

	#---------------------------
	#   woofer_new_chatter
	#---------------------------
	def woofer_new_chatter(self,jsonData):
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['new_chatter']),
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('new_chatter'),
			"mascotmouth": self.mascotImagesMouthHeight('new_chatter'),
			"time"       : self.mascotImagesTime('new_chatter'),
			"audio"      : self.mascotAudioFile('new_chatter'),
			"volume"     : self.mascotAudioVolume('new_chatter'),
			"nanoleaf"	 : self.mascotNanoleafScene('new_chatter')
		})
		return

	#---------------------------
	#   woofer_follow
	#---------------------------
	def woofer_follow(self,jsonData):
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['follow']),
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('follow'),
			"mascotmouth": self.mascotImagesMouthHeight('follow'),
			"time"       : self.mascotImagesTime('follow'),
			"audio"      : self.mascotAudioFile('follow'),
			"volume"     : self.mascotAudioVolume('follow'),
			"nanoleaf"	 : self.mascotNanoleafScene('follow')
		})
		return

	#---------------------------
	#   woofer_sub
	#---------------------------
	def woofer_sub(self,jsonData):
		# "msg-param-sub-plan": "", #(Sent only on sub, resub, subgift, anonsubgift) The type of subscription plan being used. Valid values: Prime, 1000, 2000, 3000. 1000, 2000, and 3000 refer to the first, second, and third levels of paid subscriptions, respectively (currently $4.99, $9.99, and $24.99).
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['sub']),
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('sub'),
			"mascotmouth": self.mascotImagesMouthHeight('sub'),
			"time"       : self.mascotImagesTime('sub'),
			"audio"      : self.mascotAudioFile('sub'),
			"volume"     : self.mascotAudioVolume('sub'),
			"nanoleaf"	 : self.mascotNanoleafScene('sub')
		})
		return
		
	#---------------------------
	#   woofer_resub
	#---------------------------
	def woofer_resub(self,jsonData):
		# "msg-param-sub-plan": "", #(Sent only on sub, resub, subgift, anonsubgift) The type of subscription plan being used. Valid values: Prime, 1000, 2000, 3000. 1000, 2000, and 3000 refer to the first, second, and third levels of paid subscriptions, respectively (currently $4.99, $9.99, and $24.99).
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['resub']),
			"sender"     : jsonData['display-name'],
			"months"     : jsonData['msg-param-cumulative-months'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('resub'),
			"mascotmouth": self.mascotImagesMouthHeight('resub'),
			"time"       : self.mascotImagesTime('resub'),
			"audio"      : self.mascotAudioFile('resub'),
			"volume"     : self.mascotAudioVolume('resub'),
			"nanoleaf"	 : self.mascotNanoleafScene('resub')
		})
		return
		
	#---------------------------
	#   woofer_giftsub
	#---------------------------
	def woofer_giftsub(self,jsonData):
		# "msg-param-sub-plan": "", #(Sent only on sub, resub, subgift, anonsubgift) The type of subscription plan being used. Valid values: Prime, 1000, 2000, 3000. 1000, 2000, and 3000 refer to the first, second, and third levels of paid subscriptions, respectively (currently $4.99, $9.99, and $24.99).
		if jsonData['custom-tag'] == 'anonsubgift':
			jsonData['display-name'] = 'anonymous'
		
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['giftsub']),
			"sender"     : jsonData['display-name'],
			"recipient"  : jsonData['msg-param-recipient-display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('giftsub'),
			"mascotmouth": self.mascotImagesMouthHeight('giftsub'),
			"time"       : self.mascotImagesTime('giftsub'),
			"audio"      : self.mascotAudioFile('giftsub'),
			"volume"     : self.mascotAudioVolume('giftsub'),
			"nanoleaf"	 : self.mascotNanoleafScene('giftsub')
		})
		return
	
	#---------------------------
	#   woofer_bits
	#---------------------------
	def woofer_bits(self,jsonData):
		# "bits_total"
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['bits']),
			"sender"     : jsonData['display-name'],
			"bits"       : jsonData['bits'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('bits'),
			"mascotmouth": self.mascotImagesMouthHeight('bits'),
			"time"       : self.mascotImagesTime('bits'),
			"audio"      : self.mascotAudioFile('bits'),
			"volume"     : self.mascotAudioVolume('bits'),
			"nanoleaf"	 : self.mascotNanoleafScene('bits')
		})
		return
	
	#---------------------------
	#   woofer_raid
	#---------------------------
	def woofer_raid(self,jsonData):
		#"msg-param-viewerCount": "", # (Sent only on raid) The number of viewers watching the source channel raiding this channel.
		# Check if user has already raided/hosted
		s = set(self.hostingUsers)
		if jsonData['sender'] in s:
			return
			
		self.hostingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['raid']),
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('raid'),
			"mascotmouth": self.mascotImagesMouthHeight('raid'),
			"time"       : self.mascotImagesTime('raid'),
			"audio"      : self.mascotAudioFile('raid'),
			"volume"     : self.mascotAudioVolume('raid'),
			"nanoleaf"	 : self.mascotNanoleafScene('raid')
		})
		return
		
	#---------------------------
	#   woofer_host
	#---------------------------
	def woofer_host(self,jsonData):
		# Check if user has already raided/hosted
		s = set(self.hostingUsers)
		if jsonData['sender'] in s:
			return
			
		self.hostingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['host']),
			"sender"     : jsonData['sender'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('host'),
			"mascotmouth": self.mascotImagesMouthHeight('host'),
			"time"       : self.mascotImagesTime('host'),
			"audio"      : self.mascotAudioFile('host'),
			"volume"     : self.mascotAudioVolume('host'),
			"nanoleaf"	 : self.mascotNanoleafScene('host')
		})
		return

	#---------------------------
	#   woofer_greet
	#---------------------------
	def woofer_greet(self,jsonData):
		# Check if user was already greeted
		s = set(self.greetedUsers)
		if jsonData['sender'] in s:
			return
			
		self.greetedUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['greet']),
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('greet'),
			"mascotmouth": self.mascotImagesMouthHeight('greet'),
			"time"       : self.mascotImagesTime('greet'),
			"audio"      : self.mascotAudioFile('greet'),
			"volume"     : self.mascotAudioVolume('greet'),
			"nanoleaf"	 : self.mascotNanoleafScene('greet')
		})
		return
		
	#---------------------------
	#   woofer_commands
	#---------------------------
	def woofer_commands(self, jsonData):
		if 'Enabled' in self.settings.Commands[jsonData['command']] and int(self.settings.Commands[jsonData['command']]['Enabled']) == 0:
			return;
			
		if 'Access' in self.settings.Commands[jsonData['command']] and (self.settings.Commands[jsonData['command']]['Access'] == 'mod' or self.settings.Commands[jsonData['command']]['Access'] == 'mods'):
			if int(jsonData['moderator']) != 1:
				return;

		if 'Access' in self.settings.Commands[jsonData['command']] and self.settings.Commands[jsonData['command']]['Access'] == 'broadcaster':
			if int(jsonData['broadcaster']) != 1:
				return;
				
		image = ""
		if 'Image' in  self.settings.Commands[jsonData['command']]:
			image = self.settings.pathRoot + "\\images\\" + self.settings.Commands[jsonData['command']]['Image']
			if not os.path.exists(image):
				image = ""
		
		self.woofer_addtoqueue({
			"message"    : self.settings.Commands[jsonData['command']]['Message'],
			"image"      : image,
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile(jsonData['command']),
			"mascotmouth": self.mascotImagesMouthHeight(jsonData['command']),
			"time"       : self.mascotImagesTime(jsonData['command']),
			"audio"      : self.mascotAudioFile(jsonData['command']),
			"volume"     : self.mascotAudioVolume(jsonData['command']),
			"nanoleaf"	 : self.mascotNanoleafScene(jsonData['command'])
		})
		return
		
	#---------------------------
	#   woofer_lurk
	#---------------------------
	def woofer_lurk(self, jsonData):
		
		# Check if user was already lurking
		s = set(self.lurkingUsers)
		if jsonData['sender'] in s:
			return
		
		self.lurkingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['lurk']),
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('lurk'),
			"mascotmouth": self.mascotImagesMouthHeight('lurk'),
			"time"       : self.mascotImagesTime('lurk'),
			"audio"      : self.mascotAudioFile('lurk'),
			"volume"     : self.mascotAudioVolume('lurk'),
			"nanoleaf"	 : self.mascotNanoleafScene('lurk')
		})
		return
		
	#---------------------------
	#   woofer_unlurk
	#---------------------------
	def woofer_unlurk(self, jsonData):
		
		# Check if user was already lurking
		s = set(self.lurkingUsers)
		if jsonData['sender'] not in s:
			return
		
		s = set(self.unlurkingUsers)
		if jsonData['sender'] in s:
			return
			
		self.unlurkingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['unlurk']),
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('unlurk'),
			"mascotmouth": self.mascotImagesMouthHeight('unlurk'),
			"time"       : self.mascotImagesTime('unlurk'),
			"audio"      : self.mascotAudioFile('unlurk'),
			"volume"     : self.mascotAudioVolume('unlurk'),
			"nanoleaf"	 : self.mascotNanoleafScene('unlurk')
		})
		return
		
	#---------------------------
	#   woofer_shoutout
	#---------------------------
	def woofer_shoutout(self, jsonData):
		if jsonData['moderator'] != '1':
			return
			
		if not jsonData['command_parameter']:
			return
		
		if jsonData['command_parameter'].find('@') == 0:
			jsonData['command_parameter'] = jsonData['command_parameter'] [1:]
		
		# get user twitch info
		jsonResult = self.twitchGetUser(jsonData['command_parameter'])
		if not jsonResult:
			return
			
		s = set(self.shoutoutUsers)
		if jsonResult['display_name'] in s:
			return
			
		self.shoutoutUsers.append(jsonResult['display_name'])
		
		# get channel last game
		activity = self.twitchGetLastActivity(jsonResult['_id'])
		activity_text = random.SystemRandom().choice(self.settings.Activities["Game"])
		if activity in self.settings.Activities:
			activity_text = random.SystemRandom().choice(self.settings.Activities[activity])
		
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['shoutout']) + activity_text,
			"sender"     : jsonData['display-name'],
			"recipient"  : jsonResult['display_name'],
			"activity"   : activity,
			"image"      : jsonResult['logo'],
			"customtag"  : jsonData['custom-tag'],
			"mascot"     : self.mascotImagesFile('shoutout'),
			"mascotmouth": self.mascotImagesMouthHeight('shoutout'),
			"time"       : self.mascotImagesTime('shoutout'),
			"audio"      : self.mascotAudioFile('shoutout'),
			"volume"     : self.mascotAudioVolume('shoutout'),
			"nanoleaf"	 : self.mascotNanoleafScene('shoutout')
		})
		return
		
		
	#---------------------------
	#   twitchGetUser
	#---------------------------
	def twitchGetUser(self, targetUser):
		headers = {'Client-ID': self.settings.twitchClientID, 'Accept': 'application/vnd.twitchtv.v5+json'}
		result = requests.get("https://api.twitch.tv/kraken/users?login={0}".format(targetUser.lower()), headers=headers)

		if result.encoding is None:
			result.encoding = 'utf-8'

		jsonResult = json.loads(result.text)

		if result.status_code != 200:
			print("lookup user: {0}".format(jsonResult))
			return ""

		if not jsonResult['users']:
			print("Unknown Twitch Username")
			return ""
			
		jsonResult = jsonResult['users'][0]
		return jsonResult
		
	#---------------------------
	#   twitchGetLastActivity
	#---------------------------
	def twitchGetLastActivity(self, userId):
		headers = {'Client-ID': self.settings.twitchClientID, 'Accept': 'application/vnd.twitchtv.v5+json'}
		result = requests.get("https://api.twitch.tv/kraken/channels/{0}".format(userId), headers=headers)
		
		if result.encoding is None:
			result.encoding = 'utf-8'
			
		jsonResult = json.loads(result.text)
		
		if result.status_code == 200:
			return jsonResult['game']
			
		return ""
		
	#---------------------------
	#   mascotImagesFile
	#---------------------------
	def mascotImagesFile(self, action):
		if action in self.settings.PoseMapping and self.settings.PoseMapping[action]['Image'] in self.settings.mascotImages:
			tmp = self.settings.mascotImages[self.settings.PoseMapping[action]['Image']]['Image']
			if os.path.exists(tmp):
				return tmp
				
		return self.settings.mascotImages[self.settings.PoseMapping['DEFAULT']['Image']]['Image']
		
	#---------------------------
	#   mascotImagesMouthHeight
	#---------------------------
	def mascotImagesMouthHeight(self, action):
		if action in self.settings.PoseMapping and self.settings.PoseMapping[action]['Image'] in self.settings.mascotImages:
			if 'MouthHeight' in self.settings.mascotImages[self.settings.PoseMapping[action]['Image']]:
				MouthHeight = self.settings.mascotImages[self.settings.PoseMapping[action]['Image']]['MouthHeight']
				if MouthHeight == "" or MouthHeight == 0:
					return 80
				return MouthHeight - 5
				
		return 80
		
	#---------------------------
	#   mascotImagesTime
	#---------------------------
	def mascotImagesTime(self, action):
		if action in self.settings.PoseMapping and self.settings.PoseMapping[action]['Image'] in self.settings.mascotImages:
			return self.settings.mascotImages[self.settings.PoseMapping[action]['Image']]['Time']
		
		return self.settings.mascotImages[self.settings.PoseMapping['DEFAULT']['Image']]['Time']
		
	#---------------------------
	#   mascotAudioFile
	#---------------------------
	def mascotAudioFile(self, action):
		if action in self.settings.PoseMapping and self.settings.PoseMapping[action]['Audio'] in self.settings.mascotAudio:
			tmp = self.settings.mascotAudio[self.settings.PoseMapping[action]['Audio']]['Audio']
			if os.path.exists(tmp):
				return tmp
				
		return self.settings.mascotAudio[self.settings.PoseMapping['DEFAULT']['Audio']]['Audio']
		
	#---------------------------
	#   mascotAudioVolume
	#---------------------------
	def mascotAudioVolume(self, action):
		if action in self.settings.PoseMapping and self.settings.PoseMapping[action]['Audio'] in self.settings.mascotAudio:
			return self.settings.mascotAudio[self.settings.PoseMapping[action]['Audio']]['Volume']
				
		return self.settings.GlobalVolume
		
	#---------------------------
	#   mascotNanoleafScene
	#---------------------------
	def mascotNanoleafScene(self, action):
		if action in self.settings.PoseMapping and 'Nanoleaf' in self.settings.PoseMapping[action]:
			return self.settings.PoseMapping[action]['Nanoleaf']
		
		if 'Nanoleaf' in self.settings.PoseMapping['DEFAULT']:
			return self.settings.PoseMapping['DEFAULT']['Nanoleaf']
			
		return ""