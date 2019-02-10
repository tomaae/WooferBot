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

import socket
import threading
import json
import re

#---------------------------
#   Twitch API
#---------------------------
class Twitch:
	def __init__(self, settings, woofer):
		self.settings = settings
		self.woofer   = woofer
		self.host     = "irc.twitch.tv"                           # Hostname of the IRC-Server in this case twitch's
		self.port     = 6667                                      # Default IRC-Port
		self.chrset   = 'UTF-8'
		self.con      = socket.socket()
		return
		
	#---------------------------
	#   Connect
	#---------------------------
	def Connect(self):
		threading.Thread(target=self.Connection).start()
		return
		
	#---------------------------
	#   Connection
	#---------------------------
	def Connection(self):
		print("Connecting to Twitch...")
		try:
			self.con = socket.socket()
			self.con.connect((self.host, self.port))
			self.con.send(bytes('PASS %s\r\n'  % self.settings.TwitchOAUTH,         self.chrset)) # www.twitchapps.com/tmi/ will help to retrieve the required authkey
			self.con.send(bytes('NICK %s\r\n'  % self.settings.TwitchChannel,       self.chrset))
			self.con.send(bytes('JOIN #%s\r\n' % self.settings.TwitchChannel, self.chrset))
			self.con.send(bytes('CAP REQ :twitch.tv/tags twitch.tv/commands\r\n',  self.chrset))
		except:
			print("Unable to connect to Twitch...")
			return 1
		print("Connected to Twitch...")
		
		data = ""
		while True:
			try:
				data = data+self.con.recv(1024).decode(self.chrset)
				data_split = re.split(r"[~\r\n]+", data)
				data = data_split.pop()
				
				threading.Thread(target=self.ProcessData, args=(data_split,)).start()
				
			except socket.error:
				print("Twitch socket error")
			
			except socket.timeout:
				print("Twitch socket timeout")
		return
		
	#---------------------------
	#   ProcessData
	#---------------------------
	def ProcessData(self, data):
		for line in data:
			line = line.strip()
			line = line.split(" ")
			print(line)
								
			if len(line) >= 1:
				if line[0] == 'PING':
					self.con.send(bytes('PONG %s\r\n' % line[1], self.chrset))
					continue

				jsonData = self.fill_tags()
				#
				# DM
				#
				if len(line) >= 2 and line[1] == 'PRIVMSG':
					jsonData['sender'] = self.get_sender(line[3])
					jsonData['message'] = self.get_message(line)
					
					# HOST
					if jsonData['message'] == self.settings.HostMessage:
						jsonData['custom-tag'] = 'host'
						self.woofer.ProcessJson(jsonData)
						continue
					
					# AUTOHOST
					if jsonData['message'].find(self.settings.AutohostMessage) == 0:
						jsonData['custom-tag'] = 'autohost'
						self.woofer.ProcessJson(jsonData)
						continue
					continue
				
				#
				# CHAT
				#
				if len(line) >= 3 and line[2] == 'PRIVMSG':
					jsonData = self.parse_tags(jsonData, line[0])
					jsonData['sender'] = self.get_sender(line[1])
					jsonData['message'] = self.get_message(line)
					#jsonData['message'] = self.remove_emotes(jsonData['message'], jsonData['emotes'])
					
					# COMMAND
					if jsonData['message'].find('!') == 0:
						val = jsonData['message'].split(' ', 1)
						jsonData['command'] = val[0]
						if len(val) >= 2:
							jsonData['command_parameter'] = val[1]
						jsonData['custom-tag'] = 'command'
						self.woofer.ProcessJson(jsonData)
						continue
					else:
						# NORMAL MESSAGE
						jsonData['custom-tag'] = 'message'
						self.woofer.ProcessJson(jsonData)
						continue
					continue
					
				#
				# USERNOTICE
				#
				if len(line) >= 3 and line[2] == 'USERNOTICE':
					if line[0].find('@') == 0:
						jsonData = self.parse_tags(jsonData, line[0])
					
					# RAID
					if jsonData['msg-id'] == 'raid':
						jsonData['custom-tag'] = 'raid'
						self.woofer.ProcessJson(jsonData)
						continue
					
					# SUB
					if jsonData['msg-id'] == 'sub':
						jsonData['custom-tag'] = 'sub'
						self.woofer.ProcessJson(jsonData)
						continue
						
					# RESUB
					if jsonData['msg-id'] == 'resub':
						jsonData['custom-tag'] = 'resub'
						self.woofer.ProcessJson(jsonData)
						continue
						
					# SUBGIFT
					if jsonData['msg-id'] == 'subgift':
						jsonData['custom-tag'] = 'subgift'
						self.woofer.ProcessJson(jsonData)
						continue
						
					# ANON SUBGIFT
					if jsonData['msg-id'] == 'anonsubgift':
						jsonData['custom-tag'] = 'anonsubgift'
						self.woofer.ProcessJson(jsonData)
						continue
					
					# RITUAL NEW CHATTER
					if jsonData['msg-id'] == 'ritual' and jsonData['msg-param-ritual-name'] == 'new_chatter':
						jsonData['sender'] = jsonData['display-name']
						jsonData['message'] = self.get_message(line)
						jsonData['custom-tag'] = 'new_chatter'
						self.woofer.ProcessJson(jsonData)
						continue
					
					continue
		return

	#---------------------------
	#   fill_tags
	#---------------------------
	def fill_tags(self):
		result = {
			"moderator": "0",
			"subscriber": "0",
			"broadcaster": "0",
			"bits_total": "0",
			"bits": "0",
			"display-name": "",
			"msg-id": "", # Valid values: sub, resub, subgift, anonsubgift, raid, ritual.
			"msg-param-viewerCount": "", # (Sent only on raid) The number of viewers watching the source channel raiding this channel.
			"msg-param-recipient-display-name": "", # (Sent only on subgift, anonsubgift) The display name of the subscription gift recipient.
			"msg-param-sub-plan": "", #(Sent only on sub, resub, subgift, anonsubgift) The type of subscription plan being used. Valid values: Prime, 1000, 2000, 3000. 1000, 2000, and 3000 refer to the first, second, and third levels of paid subscriptions, respectively (currently $4.99, $9.99, and $24.99).
			"msg-param-months": "", # (Sent only on sub, resub, subgift, anonsubgift) The number of consecutive months the user has subscribed for, in a resub notice.
			"msg-param-cumulative-months": "", #(Sent only on sub, resub) The total number of months the user has subscribed. This is the same as msg-param-months but sent for different types of user notices.
			"msg-param-streak-months": "", #(Sent only on sub, resub) The number of consecutive months the user has subscribed. This is 0 if msg-param-should-share-streak is 0.
			"msg-param-ritual-name": "", # (Sent only on ritual) The name of the ritual this notice is for. Valid value: new_chatter.
			"login": "",
			"emotes": "", # <emote ID>:<first index>-<last index>,<another first index>-<another last index>/<another emote ID>:<first index>-<last index>...
			"command": "",
			"command_parameter": "",
			"sender": "",
			"message": "",
			"custom-tag": ""
		}
		return result

	#---------------------------
	#   parse_tags
	#---------------------------
	def parse_tags(self, jsonData, msg):
		tags = msg.split(";")
		for tag in tags:
			tag = tag.split("=")
			#"@badges": "", # Comma-separated list of chat badges and the version of each badge (each in the format <badge>/<version>. Valid badge values: admin, bits, broadcaster, global_mod, moderator, subscriber, staff, turbo.
			if tag[0] == '@badges':
				badges = tag[1].split(",")
				for badge in badges:
					badge = badge.split("/")
					if badge[0] == 'broadcaster' or badge[0] == 'moderator' or badge[0] == 'subscriber':
						if badge[0] in jsonData:
							jsonData[badge[0]] = badge[1]
							if badge[0] == 'broadcaster':
								jsonData["moderator"] = "1"
								jsonData["broadcaster"] = "1"
					if badge[0] == 'bits':
						jsonData["bits_total"] = badge[1]
			else:
				if tag[0] in jsonData:
					jsonData[tag[0]] = tag[1]
		return jsonData

	#---------------------------
	#   get_sender
	#---------------------------
	def get_sender(self, msg):
		result = ""
		for char in msg:
			if char == "!":
				break
			if char != ":":
				result += char
		return result

	#---------------------------
	#   get_message
	#---------------------------
	def get_message(self, msg):
		result = ""
		i = 4
		length = len(msg)
		while i < length:
			result += msg[i] + " "
			i += 1
		result = result.lstrip(':')
		result = result.strip()
		return result
		
	#---------------------------
	#   remove_emotes
	#---------------------------
	def remove_emotes(self, msg, emotes):
		if not emotes:
			return msg
			
		emotes = emotes.replace('/', ',')
		emotes = emotes.split(",")
		for emote in reversed(emotes):
			if emote.find(':') >= 0:
				emote = emote.split(":")[1]
			emote = emote.split("-")
			msg = msg[:int(emote[0])] + msg[int(emote[1])+1:]
		print(msg)
		return msg
