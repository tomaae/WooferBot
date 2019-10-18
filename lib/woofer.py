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
	def __init__(self, settings, overlay, nanoleaf, hue, chatbot):
		self.settings       = settings
		self.overlay        = overlay
		self.nanoleaf       = nanoleaf
		self.hue            = hue
		self.chatbot        = chatbot
		
		self.queue          = []
		self.greetedUsers   = []
		self.greetedUsers.append(self.settings.TwitchChannel)
		self.greetedUsers.append(self.settings.TwitchChannel + "bot")
		
		self.lurkingUsers          = []
		self.unlurkingUsers        = []
		self.hostingUsers          = []
		self.shoutoutUsers         = []
		self.commandsViewerOnce    = {}
		self.commandsViewerTimeout = {}
		self.commandsGlobalTimeout = {}
		
		self.changedLightsNanoleaf = ""
		self.changedLightsHue      = {}
		
		## Start timer for ScheduledMessages
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
			## Shoutout
			if jsonData['command'] == '!so' or jsonData['command'] == '!shoutout':
				if self.settings.Enabled["shoutout"]:
					self.woofer_shoutout(jsonData)
				return
			
			## Lurk/unlurk
			if self.settings.Enabled["lurk"]:
				if jsonData['command'] == '!lurk':
					self.woofer_lurk(jsonData)
					return
				if jsonData['command'] == '!unlurk' or jsonData['command'] == '!back':
					self.woofer_unlurk(jsonData)
					return
			
			## Custom commands
			if jsonData['command'] in self.settings.Commands:
				self.woofer_commands(jsonData)
				
			for action in self.settings.Commands:
				for alias in self.settings.Commands[action]['Aliases']:
					if jsonData['command'] == alias:
						jsonData['command'] = action
						self.woofer_commands(jsonData)
				
			return
		
		#
		# Messages
		#
		if jsonData['custom-tag'] == 'message':
			commonBots = set(self.settings.commonBots)
			customBots = set(self.settings.Bots)
			## Alerts from chatbots
			if jsonData['sender'] == self.settings.TwitchChannel + "bot" or jsonData['sender'] in commonBots or jsonData['sender'] in customBots:
				## Follow
				if jsonData['message'].find(self.settings.FollowMessage) > 0 and self.settings.Enabled["follow"]:
					line = jsonData['message'].split(" ")
					jsonData['display-name'] = line[0].rstrip(',')
					self.woofer_follow(jsonData)
					return
				return
			
			## Bits
			if int(jsonData['bits']) > 0 and int(jsonData['bits']) >= self.settings.MinBits and self.settings.Enabled["bits"]:
				self.woofer_bits(jsonData)
				return
			
			## Greeting
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
			self.woofer_subgift(jsonData)
			return
		
		if jsonData['custom-tag'] == 'anonsubgift' and self.settings.Enabled["anonsubgift"]:
			self.woofer_subgift(jsonData)
			return
		
	#---------------------------
	#   woofer_timer
	#---------------------------
	def woofer_timer(self):
		## Check if overlay is connected
		if self.overlay.active < 1:
			threading.Timer(30, self.woofer_timer).start()
			return
		
		## Check if timer is enabled
		for action in self.settings.ScheduledMessages:
			if not action['Enabled']:
				continue
			
			currentEpoch = int(time.time())
			if (currentEpoch - self.settings.scheduleTable[action['Name']]) >= (action['Timer'] * 60):
				self.settings.scheduleTable[action['Name']] = currentEpoch
				
				if 'Command' in action:
					self.woofer_commands({
						"command"      : action['Command'],
						"broadcaster"  : 1,
						"sender"       : self.settings.TwitchChannel.lower(),
						"display-name" : self.settings.TwitchChannel,
						"custom-tag"   : 'command'
					})
				else:
					self.woofer_addtoqueue({
						"message"    : random.SystemRandom().choice(self.settings.Messages[action['Name']]),
						"image"      : self.settings.pathRoot + "\\images\\" + action['Image'],
						"sender"     : "",
						"customtag"  : "ScheduledMessage",
						"id"         : action['Name']
					})
		
		## Reset to default after X seconds
		threading.Timer(60, self.woofer_timer).start()
		return
		
	#---------------------------
	#   woofer_queue
	#---------------------------
	def woofer_queue(self, queue_id, jsonData):
		#
		# Check if there is somethign in queue
		#
		if not self.queue:
			return
		
		#
		# Check if overlay is connected
		#
		if self.overlay.active < 1:
			print("waiting")
			threading.Timer(3, self.woofer_queue, args=(queue_id, jsonData)).start()
			return
		
		#
		# Check if our turn in queue
		#
		if self.queue[0] != queue_id:
			threading.Timer(0.5, self.woofer_queue, args=(queue_id, jsonData)).start()
			return
		
		#
		# Send to overlay, retry later if overlay buffer is full
		#
		if self.overlay.Send("EVENT_WOOFERBOT", jsonData) == 1:
			threading.Timer(1, self.woofer_queue, args=(queue_id, jsonData)).start()
			return
		
		#
		# Execute custom scripts
		#
		if 'script' in jsonData and jsonData['script'] != "":
			os.system("\"" + jsonData['script'] + "\"")
		
		#
		# Turn on Nanoleaf
		#
		if 'nanoleaf' in jsonData and jsonData['nanoleaf'] != "":
			self.nanoleaf.Scene(jsonData['nanoleaf'])
			if 'nanoleafpersistent' in jsonData and jsonData['nanoleafpersistent']:
				self.changedLightsNanoleaf = jsonData['nanoleaf']
		
		#
		# Turn on Hue
		#
		if 'hue' in jsonData:
			for device in jsonData['hue']:
				if 'Brightness' in jsonData['hue'][device] and jsonData['hue'][device]['Brightness'] >= 1 and 'Color' in jsonData['hue'][device] and len(jsonData['hue'][device]['Color']) >= 6 and len(jsonData['hue'][device]['Color']) <= 7:
					self.hue.state(device = device, bri = jsonData['hue'][device]['Brightness'], col = jsonData['hue'][device]['Color'])
			
			if 'huepersistent' in jsonData and jsonData['huepersistent']:
				self.changedLightsHue = jsonData['hue']
		
		#
		# Reset to default after X seconds
		#
		threading.Timer(jsonData['time'] / 1000, self.woofer_queue_default, args=(queue_id,jsonData)).start()
		return
		
	#---------------------------
	#   woofer_queue_default
	#---------------------------
	def woofer_queue_default(self,queue_id, old_jsonData):
		#
		# Set default Idle image
		#
		mascotIdleImage = self.settings.mascotImages['Idle']['Image']
		if not os.path.isfile(mascotIdleImage):
			mascotIdleImage = ""
		
		#
		# Check mapping for custom Idle image
		#
		if 'Idle' in self.settings.PoseMapping and 'Image' in self.settings.PoseMapping['Idle'] and self.settings.PoseMapping['Idle']['Image'] in self.settings.mascotImages:
			tmp = self.settings.mascotImages[self.settings.PoseMapping['Idle']['Image']]['Image']
			if os.path.isfile(tmp):
				mascotIdleImage = tmp
		
		#
		# Send to overlay, retry later if overlay buffer is full
		#
		jsonData = {
			"mascot": mascotIdleImage
		}
		if self.overlay.Send("EVENT_WOOFERBOT", jsonData) == 1:
			threading.Timer(1, self.woofer_queue_default, args=(queue_id, old_jsonData)).start()
			return
		
		#
		# Reset Nanoleaf to Idle
		#
		if 'nanoleaf' in old_jsonData and old_jsonData['nanoleaf']:
			## Reset to persistent lights
			if self.changedLightsNanoleaf:
				self.nanoleaf.Scene(self.changedLightsNanoleaf)
			## Reset to Idle lights
			elif 'Nanoleaf' in self.settings.PoseMapping['Idle']:
				self.nanoleaf.Scene(self.settings.PoseMapping['Idle']['Nanoleaf'])
			## Turn off lights
			else:
				self.nanoleaf.Scene()
		
		#
		# Reset Hue to Idle
		#
		if 'hue' in old_jsonData:
			## Reset to persistent lights
			if self.changedLightsHue:
				for device in self.changedLightsHue:
					if 'Brightness' in self.changedLightsHue[device] and self.changedLightsHue[device]['Brightness'] >= 1 and 'Color' in self.changedLightsHue[device] and len(self.changedLightsHue[device]['Color']) >= 6 and len(self.changedLightsHue[device]['Color']) <= 7:
						self.hue.state(device = device, bri = self.changedLightsHue[device]['Brightness'], col = self.changedLightsHue[device]['Color'])
				
				for device in old_jsonData['hue']:
					if 'Brightness' in old_jsonData['hue'][device] and old_jsonData['hue'][device]['Brightness'] >= 1 and 'Color' in old_jsonData['hue'][device] and len(old_jsonData['hue'][device]['Color']) >= 6 and len(old_jsonData['hue'][device]['Color']) <= 7:
						if device not in self.changedLightsHue:
							self.hue.state(device = device)
			
			## Reset to Idle lights
			elif 'Hue' in self.settings.PoseMapping['Idle']:
				for device in self.settings.PoseMapping['Idle']['Hue']:
					if 'Brightness' in self.settings.PoseMapping['Idle']['Hue'][device] and self.settings.PoseMapping['Idle']['Hue'][device]['Brightness'] >= 1 and 'Color' in self.settings.PoseMapping['Idle']['Hue'][device] and len(self.settings.PoseMapping['Idle']['Hue'][device]['Color']) >= 6 and len(self.settings.PoseMapping['Idle']['Hue'][device]['Color']) <= 7:
						self.hue.state(device = device, bri = self.settings.PoseMapping['Idle']['Hue'][device]['Brightness'], col = self.settings.PoseMapping['Idle']['Hue'][device]['Color'])
				
				for device in old_jsonData['hue']:
					if 'Brightness' in old_jsonData['hue'][device] and old_jsonData['hue'][device]['Brightness'] >= 1 and 'Color' in old_jsonData['hue'][device] and len(old_jsonData['hue'][device]['Color']) >= 6 and len(old_jsonData['hue'][device]['Color']) <= 7:
						if device not in self.settings.PoseMapping['Idle']:
							self.hue.state(device = device)
			
			## Turn off lights
			else:
				for device in old_jsonData['hue']:
					if 'Brightness' in old_jsonData['hue'][device] and old_jsonData['hue'][device]['Brightness'] >= 1 and 'Color' in old_jsonData['hue'][device] and len(old_jsonData['hue'][device]['Color']) >= 6 and len(old_jsonData['hue'][device]['Color']) <= 7:
						self.hue.state(device = device)
		
		#
		# Remove notification from queue
		#
		if self.queue:
			self.queue.remove(queue_id)
			
		return
		
	#---------------------------
	#   woofer_addtoqueue
	#---------------------------
	def woofer_addtoqueue(self,jsonResponse):
		print("{0}: {1}".format(jsonResponse['customtag'], jsonResponse['sender']))
		
		if 'message' not in jsonResponse or jsonResponse["message"] == "":
			if jsonResponse["id"] in self.settings.Messages:
				jsonResponse["message"]             = random.SystemRandom().choice(self.settings.Messages[jsonResponse["id"]])
			else:
				jsonResponse["message"] = ""
		
		jsonResponse["mascot"]             = self.mascotImagesFile(jsonResponse["id"])
		jsonResponse["mascotmouth"]        = self.mascotImagesMouthHeight(jsonResponse["id"])
		jsonResponse["time"]               = self.mascotImagesTime(jsonResponse["id"])
		jsonResponse["audio"]              = self.mascotAudioFile(jsonResponse["id"])
		jsonResponse["volume"]             = self.mascotAudioVolume(jsonResponse["id"])
		jsonResponse["nanoleaf"]           = self.mascotNanoleafScene(jsonResponse["id"])
		jsonResponse["nanoleafpersistent"] = self.mascotNanoleafPersistent(jsonResponse["id"])
		jsonResponse["hue"]                = self.mascotHueDevices(jsonResponse["id"])
		jsonResponse["huepersistent"]      = self.mascotHuePersistent(jsonResponse["id"])
		
		## Add to queue
		queue_id = uuid.uuid4()
		self.queue.append(queue_id)
		threading.Thread(target=self.woofer_queue, args=(queue_id, jsonResponse)).start()
		return
		
	#---------------------------
	#   woofer_new_chatter
	#---------------------------
	def woofer_new_chatter(self,jsonData):
		self.woofer_addtoqueue({
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : 'new_chatter'
		})
		return
		
	#---------------------------
	#   woofer_follow
	#---------------------------
	def woofer_follow(self,jsonData):
		self.woofer_addtoqueue({
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : 'follow'
		})
		return
		
	#---------------------------
	#   woofer_sub
	#---------------------------
	def woofer_sub(self,jsonData):
		self.woofer_addtoqueue({
			"message"    : random.SystemRandom().choice(self.settings.Messages['sub']),
			"sender"     : jsonData['display-name'],
			"months"       : jsonData['months'],
			"months_streak": jsonData['months_streak'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : 'sub'
		})
		return
		
	#---------------------------
	#   woofer_resub
	#---------------------------
	def woofer_resub(self,jsonData):
		## Check for custom sub definitions
		customId = 'resub'
		for customObj in self.settings.CustomSubs:
			if int(jsonData['months']) >= int(customObj['From']) and int(jsonData['months']) <= int(customObj['To']):
				customId = customObj['Name']
		
		self.woofer_addtoqueue({
			"sender"       : jsonData['display-name'],
			"months"       : jsonData['months'],
			"months_streak": jsonData['months_streak'],
			"customtag"    : jsonData['custom-tag'],
			"id"           : customId
		})
		return
		
	#---------------------------
	#   woofer_subgift
	#---------------------------
	def woofer_subgift(self,jsonData):
		if jsonData['custom-tag'] == 'anonsubgift':
			jsonData['display-name'] = 'anonymous'
		
		self.woofer_addtoqueue({
			"sender"     : jsonData['display-name'],
			"recipient"  : jsonData['msg-param-recipient-display-name'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : 'subgift'
		})
		return
		
	#---------------------------
	#   woofer_bits
	#---------------------------
	def woofer_bits(self,jsonData):
		## Check for custom bits definitions
		customId = 'bits'
		for customObj in self.settings.CustomBits:
			if int(jsonData['bits']) >= int(customObj['From']) and int(jsonData['bits']) <= int(customObj['To']):
				customId = customObj['Name']
		
		self.woofer_addtoqueue({
			"sender"     : jsonData['display-name'],
			"bits"       : jsonData['bits'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : customId
		})
		return
		
	#---------------------------
	#   woofer_raid
	#---------------------------
	def woofer_raid(self,jsonData):
		## Check if user has already raided/hosted
		s = set(self.hostingUsers)
		if jsonData['sender'] in s:
			return
		
		self.hostingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"viewers"    : jsonData['viewers'],
			"id"         : 'raid'
		})
		
		## Automatic shoutout
		if self.settings.AutoShoutout:
			jsonData['moderator'] = '1'
			jsonData['command_parameter'] = jsonData['display-name']
			jsonData['custom-tag'] = 'shoutout'
			threading.Timer(self.settings.AutoShoutoutTime, self.woofer_shoutout, args=[jsonData]).start()
			
		return
		
	#---------------------------
	#   woofer_host
	#---------------------------
	def woofer_host(self,jsonData):
		## Check if user has already raided/hosted
		s = set(self.hostingUsers)
		if jsonData['sender'] in s:
			return
		
		self.hostingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"sender"     : jsonData['sender'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : 'host'
		})
		
		## Automatic shoutout
		if self.settings.AutoShoutout:
			jsonData['moderator'] = '1'
			jsonData['command_parameter'] = jsonData['display-name']
			jsonData['custom-tag'] = 'shoutout'
			threading.Timer(self.settings.AutoShoutoutTime, self.woofer_shoutout, args=[jsonData]).start()
		
		return
		
	#---------------------------
	#   woofer_greet
	#---------------------------
	def woofer_greet(self,jsonData):
		## Check if user was already greeted
		s = set(self.greetedUsers)
		if jsonData['sender'] in s:
			return
		
		self.greetedUsers.append(jsonData['sender'])
		
		## Check for custom greeting definitions
		customMessage = ""
		if 'viewer_' + jsonData['display-name'] in self.settings.Messages:
			customMessage = random.SystemRandom().choice(self.settings.Messages['viewer_' + jsonData['display-name']])
		
		customId = 'greet'
		if 'viewer_' + jsonData['display-name'] in self.settings.PoseMapping:
			customId = 'viewer_' + jsonData['display-name']
		
		self.woofer_addtoqueue({
			"message"    : customMessage,
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : customId
		})
		return
		
	#---------------------------
	#   woofer_commands
	#---------------------------
	def woofer_commands(self, jsonData):
		#
		# Check if command is enabled
		#
		if not self.settings.Commands[jsonData['command']]['Enabled']:
			return
		
		#
		# Check access rights
		#
		if self.settings.Commands[jsonData['command']]['Access'] != "":
			if int(jsonData['broadcaster']) == 1:
				if self.settings.Commands[jsonData['command']]['Access'] not in ['sub', 'subs', 'subscriber', 'subscribers', 'vip', 'vips', 'mod', 'mods', 'moderator', 'moderators', 'broadcaster']:
					return
			elif int(jsonData['moderator']) == 1:
				if self.settings.Commands[jsonData['command']]['Access'] not in ['sub', 'subs', 'subscriber', 'subscribers', 'vip', 'vips', 'mod', 'mods', 'moderator', 'moderators']:
					return
			elif int(jsonData['vip']) == 1:
				if self.settings.Commands[jsonData['command']]['Access'] not in ['sub', 'subs', 'subscriber', 'subscribers', 'vip', 'vips']:
					return
			elif int(jsonData['subscriber']) == 1:
				if self.settings.Commands[jsonData['command']]['Access'] not in ['sub', 'subs', 'subscriber', 'subscribers']:
					return
			else:
				return
		
		#
		# ViewerOnce
		#
		if self.settings.Commands[jsonData['command']]['ViewerOnce']:
			if jsonData['command'] in self.commandsViewerOnce and jsonData['sender'] in self.commandsViewerOnce[jsonData['command']]:
				return
			
			if jsonData['command'] not in self.commandsViewerOnce:
				self.commandsViewerOnce[jsonData['command']] = []
			
			self.commandsViewerOnce[jsonData['command']].append(jsonData['sender'])
		
		#
		# ViewerTimeout
		#
		if self.settings.Commands[jsonData['command']]['ViewerTimeout'] > 0:
			currentEpoch = int(time.time())
			
			if jsonData['command'] in self.commandsViewerTimeout and jsonData['sender'] in self.commandsViewerTimeout[jsonData['command']] and (currentEpoch - self.commandsViewerTimeout[jsonData['command']][jsonData['sender']]) < self.settings.Commands[jsonData['command']]['ViewerTimeout']:
				return
			
			if jsonData['command'] not in self.commandsViewerTimeout:
				self.commandsViewerTimeout[jsonData['command']] = {}
			
			self.commandsViewerTimeout[jsonData['command']][jsonData['sender']] = currentEpoch
		
		#
		# GlobalTimeout
		#
		if self.settings.Commands[jsonData['command']]['GlobalTimeout'] > 0:
			currentEpoch = int(time.time())
			if jsonData['command'] in self.commandsGlobalTimeout and (currentEpoch - self.commandsGlobalTimeout[jsonData['command']]) < self.settings.Commands[jsonData['command']]['GlobalTimeout']:
				return
			
			self.commandsGlobalTimeout[jsonData['command']] = currentEpoch
		
		#
		# Check custom image
		#
		image = ""
		if self.settings.Commands[jsonData['command']]['Image'] != "":
			image = self.settings.pathRoot + "\\images\\" + self.settings.Commands[jsonData['command']]['Image']
			if not os.path.isfile(image):
				image = ""
		
		#
		# Check custom script
		#
		script = ""
		if self.settings.Commands[jsonData['command']]['Script'] != "":
			script = self.settings.pathRoot + "\\scripts\\" + self.settings.Commands[jsonData['command']]['Script']
			if not os.path.isfile(script):
				script = ""
		
		self.woofer_addtoqueue({
			"image"      : image,
			"script"     : script,
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : jsonData['command']
		})
		return
		
	#---------------------------
	#   woofer_lurk
	#---------------------------
	def woofer_lurk(self, jsonData):
		
		## Check if user was already lurking
		s = set(self.lurkingUsers)
		if jsonData['sender'] in s:
			return
		
		self.lurkingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : 'lurk'
		})
		return
		
	#---------------------------
	#   woofer_unlurk
	#---------------------------
	def woofer_unlurk(self, jsonData):
		
		## Check if user was already lurking
		s = set(self.lurkingUsers)
		if jsonData['sender'] not in s:
			return
		
		## Check if user already used unlurk
		s = set(self.unlurkingUsers)
		if jsonData['sender'] in s:
			return
			
		self.unlurkingUsers.append(jsonData['sender'])
		
		self.woofer_addtoqueue({
			"sender"     : jsonData['display-name'],
			"customtag"  : jsonData['custom-tag'],
			"id"         : 'unlurk'
		})
		return
		
	#---------------------------
	#   woofer_shoutout
	#---------------------------
	def woofer_shoutout(self, jsonData):
		#
		# Check access rights
		#
		if jsonData['moderator'] != '1':
			return
		
		#
		# Check if channel parameter was specified
		#
		if not jsonData['command_parameter']:
			return
		
		if jsonData['command_parameter'].find('@') == 0:
			jsonData['command_parameter'] = jsonData['command_parameter'] [1:]
		
		#
		# Get user info
		#
		jsonResult = self.twitchGetUser(jsonData['command_parameter'])
		if not jsonResult:
			return
		
		s = set(self.shoutoutUsers)
		if jsonResult['display_name'] in s:
			return
		
		self.shoutoutUsers.append(jsonResult['display_name'])
		
		#
		# Get channel last game
		#
		activity = self.twitchGetLastActivity(jsonResult['_id'])
		activity_text = ""
		if activity:
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
			"id"         : 'shoutout'
		})
		return
		
	#---------------------------
	#   twitchGetUser
	#---------------------------
	def twitchGetUser(self, targetUser):
		## Get user info from API
		headers = {'Client-ID': self.settings.twitchClientID, 'Accept': 'application/vnd.twitchtv.v5+json'}
		result = requests.get("https://api.twitch.tv/kraken/users?login={0}".format(targetUser.lower()), headers=headers)
		
		## Check encoding
		if result.encoding is None:
			result.encoding = 'utf-8'
		
		jsonResult = json.loads(result.text)
		
		## Check exit code
		if result.status_code != 200:
			print("lookup user: {0}".format(jsonResult))
			return ""
		
		## User defined in result json
		if 'users' not in jsonResult and not jsonResult['users']:
			print("Unknown Twitch Username")
			return ""
		
		return jsonResult['users'][0]
		
	#---------------------------
	#   twitchGetLastActivity
	#---------------------------
	def twitchGetLastActivity(self, userId):
		## Get channel activity from API
		headers = {'Client-ID': self.settings.twitchClientID, 'Accept': 'application/vnd.twitchtv.v5+json'}
		result = requests.get("https://api.twitch.tv/kraken/channels/{0}".format(userId), headers=headers)
		
		## Check encoding
		if result.encoding is None:
			result.encoding = 'utf-8'
		
		jsonResult = json.loads(result.text)
		
		## Check exit code
		if result.status_code != 200:
			return ""
		
		return jsonResult['game']
		
	#---------------------------
	#   mascotImagesFile
	#---------------------------
	def mascotImagesFile(self, action):
		if action in self.settings.PoseMapping and self.settings.PoseMapping[action]['Image'] in self.settings.mascotImages:
			tmp = self.settings.mascotImages[self.settings.PoseMapping[action]['Image']]['Image']
			if os.path.isfile(tmp):
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
				
		return self.settings.mascotImages[self.settings.PoseMapping['DEFAULT']['Image']]['MouthHeight'] - 5
		
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
			tmp = random.SystemRandom().choice(self.settings.mascotAudio[self.settings.PoseMapping[action]['Audio']]['Audio'])
			if os.path.isfile(tmp):
				return tmp
		
		if self.settings.PoseMapping['DEFAULT']['Audio'] in self.settings.mascotAudio:
			return random.SystemRandom().choice(self.settings.mascotAudio[self.settings.PoseMapping['DEFAULT']['Audio']]['Audio'])
		
		return ""
		
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
		
	#---------------------------
	#   mascotNanoleafPersistent
	#---------------------------
	def mascotNanoleafPersistent(self, action):
		if action in self.settings.PoseMapping and 'NanoleafPersistent' in self.settings.PoseMapping[action]:
			return self.settings.PoseMapping[action]['NanoleafPersistent']
		
		if 'NanoleafPersistent' in self.settings.PoseMapping['DEFAULT']:
			return self.settings.PoseMapping['DEFAULT']['NanoleafPersistent']
		
		return ""
		
	#---------------------------
	#   mascotHueDevices
	#---------------------------
	def mascotHueDevices(self, action):
		if action in self.settings.PoseMapping and 'Hue' in self.settings.PoseMapping[action]:
			return self.settings.PoseMapping[action]['Hue']
		
		if 'Hue' in self.settings.PoseMapping['DEFAULT']:
			return self.settings.PoseMapping['DEFAULT']['Hue']
		
		return ""
		
	#---------------------------
	#   mascotHuePersistent
	#---------------------------
	def mascotHuePersistent(self, action):
		if action in self.settings.PoseMapping and 'HuePersistent' in self.settings.PoseMapping[action]:
			return self.settings.PoseMapping[action]['HuePersistent']
		
		if 'HuePersistent' in self.settings.PoseMapping['DEFAULT']:
			return self.settings.PoseMapping['DEFAULT']['HuePersistent']
		
		return ""