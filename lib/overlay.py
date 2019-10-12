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

import websockets
import json
import asyncio
import threading
import os

#---------------------------
#   Overlay Handling
#---------------------------
class Overlay:
	def __init__(self, settings, chatbot):
		self.bindIP       = '127.0.0.1'
		self.bindPort     = 3339
		self.active       = 0
		self.sendQueue    = None
		self.serverSocket = None
		self.loop         = None
		self.loopThread   = None
		self.settings     = settings
		self.chatbot      = chatbot

	#---------------------------
	#   Start
	#---------------------------
	def Start(self):
		print("Starting overlay server...")
		self.serverSocket = websockets.serve(self.Connection, self.bindIP, self.bindPort)
		print("Overlay server waiting for connection...")
		self.loop = asyncio.get_event_loop()
		self.loop.run_until_complete(self.serverSocket)
		self.loopThread = threading.Thread(target=self.loop.run_forever)
		self.loopThread.daemon = True
		self.loopThread.start()
		return
		
	#---------------------------
	#   Stop
	#---------------------------
	def Stop(self):
		self.loop.stop()
		return
		
	#---------------------------
	#   Send
	#---------------------------
	def Send(self, event, jsonData, init = 0):
		if self.sendQueue:
			return 1
			
		if 'mascot' in jsonData:
			if os.path.isfile(jsonData["mascot"]):
				jsonData["mascot"] = "file:///" + jsonData["mascot"]
			else:
				jsonData["mascot"] = ""
				
		if 'audio' in jsonData:
			if os.path.isfile(jsonData["audio"]):
				jsonData["audio"] = "file:///" + jsonData["audio"]
			else:
				jsonData["audio"] = ""
			
		if 'image' in jsonData:
			if os.path.isfile(jsonData["image"]):
				jsonData["image"] = "file:///" + jsonData["image"]
			else:
				if jsonData["image"].find('https://') != 0:
					jsonData["image"] = ""

		jsonDataRaw = {
			"event": event,
			"data": jsonData
		}
		if init == 1:
			jsonDataRaw["styles"] = self.get_styles()
			
		self.sendQueue = jsonDataRaw
		return 0
		
	async def Connection(self, websocket, path):
		print("Initializing overlay...")
		self.active = self.active + 1
		if not self.sendQueue:
			mascotIdleImage = self.settings.mascotImages['Idle']['Image']
			if not os.path.isfile(mascotIdleImage):
				mascotIdleImage = ""
			if 'Idle' in self.settings.PoseMapping and self.settings.PoseMapping['Idle']['Image'] in self.settings.mascotImages:
				tmp = self.settings.mascotImages[self.settings.PoseMapping['Idle']['Image']]['Image']
				if os.path.isfile(tmp):
					mascotIdleImage = tmp
			jsonData = {
				"mascot": mascotIdleImage
			}
			self.Send(event = "EVENT_WOOFERBOT", jsonData = jsonData, init = 1)
		pingSend = 0
		while True:
			pingSend = pingSend + 1
			if self.sendQueue:
				jsonDataRaw = self.sendQueue
				try:
					await websocket.send(json.dumps(jsonDataRaw))
					if 'message' in jsonDataRaw['data']:
						#print(json.dumps(jsonDataRaw['data'], indent=4, sort_keys=True))
						self.chatbot.Send(jsonDataRaw['data']['message'])
				except websockets.exceptions.ConnectionClosed:
					print("Connection closed by overlay...")
					self.active = self.active - 1
					break
				else:
					pingSend = 0
					self.sendQueue = None
			else:
				if pingSend >= 40:
					jsonDataRaw = json.dumps({
						"event": "EVENT_PING",
						"data": ""
					})
					try:
						await websocket.send(jsonDataRaw)
					except websockets.exceptions.ConnectionClosed:
						self.active = self.active - 1
						if self.active == 0:
							print("Connection closed by overlay...")
						break
					else:
						pingSend = 0
					
			await asyncio.sleep(0.5)
		return
		
	#---------------------------
	#   get_styles
	#---------------------------
	def get_styles(self):
		css = {}
		
		if not self.settings.mascotStyles["MascotMaxWidth"]:
			self.settings.mascotStyles["MascotMaxWidth"] = 150
		
		css[".mascot|width"] = str(self.settings.mascotStyles["MascotMaxWidth"]) + "px"
		
		if self.settings.AlignMascot == "right":
			css[".mascot|left"] = "auto"
			css[".mascot|right"] = "0"
			css[".message|right"] = str(int(self.settings.mascotStyles["MascotMaxWidth"]) + 10 ) + "px"
			css[".message|left"] = "auto"
			css[".mainbox|text-align"] = "right"
			css[".message::after|display"] = "none"
			css[".message div:first-child|display"] = "none"
			css[".message::before|display"] = "block"
			css[".message div:last-child|display"] = "block"
		else:
			css[".mascot|left"] = "0"
			css[".mascot|right"] = "auto"
			css[".message|left"] = str(int(self.settings.mascotStyles["MascotMaxWidth"]) + 10 ) + "px"
			css[".message|right"] = "auto"
			css[".mainbox|text-align"] = "left"
			css[".message::after|display"] = "block"
			css[".message div:first-child|display"] = "block"
			css[".message::before|display"] = "none"
			css[".message div:last-child|display"] = "none"
		
		HighlightTextStrokeColor = ""
		HighlightTextShadowColor = ""
		HighlightTextShadowOffset = ""
		
		for style in self.settings.Styles:
			val = self.settings.Styles[style]
			
			if style == "BackgroundColor":
				css[".message|background-color"] = val
				
			if style == "BorderColor":
				css[".message|border-color"] = val
				css[".image|border-color"] = val
				css[".message div:first-child|border-right-color"] = val
				css[".message div:last-child|border-right-color"] = val
				
			if style == "BorderWidth":
				css[".message|border-width"] = val
				css[".image|border-width"] = (val / 2)

			if style == "BorderRadius":
				css[".message|border-radius"] = str(val) + 'px'
				css[".image|border-radius"] = str(int(val) * 2) + 'px'
			
			if style == "BorderStrokeColor":
				if val == "":
					css[".message|box-shadow"] = ""
					css[".message::after|border-right-color"] = "transparent" # Not working
					css[".message::before|border-right-color"] = "transparent" # Not working
				else:
					css[".message|box-shadow"] = "-1px -1px 0 " + val + ", 1px -1px 0 " + val + ", -1px 1px 0 " + val + ", 1px 1px 0 " + val
					css[".message::after|border-right-color"] = val  # Not working
					css[".message::before|border-right-color"] = val  # Not working
					
					
			if style == "TextFontFamily":
				css[".message|font-family"] = val

			if style == "TextSize":
				css[".message|font-size"] = str(val) + 'px'
				
			if style == "TextWeight":
				css[".message|font-weight"] = val
				
			if style == "TextColor":
				css[".message|color"] = val
				
			if style == "HighlightTextSize":
				css[".user|font-size"] = str(val) + 'px'
				
			if style == "HighlightTextSpacing":
				css[".user|letter-spacing"] = val
					
			if style == "HighlightTextColor":
				css[".user|color"] = val
				
			if style == "HighlightTextStrokeColor":
				HighlightTextStrokeColor = val
				
			if style == "HighlightTextShadowColor":
				HighlightTextShadowColor = val
				
			if style == "HighlightTextShadowOffset":
				HighlightTextShadowOffset = val
			
			if HighlightTextStrokeColor != "" and HighlightTextShadowColor != "" and HighlightTextShadowOffset != "":
				HighlightTextShadowOffset = str(HighlightTextShadowOffset)
				if HighlightTextShadowOffset != "0":
					HighlightTextShadowOffset = HighlightTextShadowOffset + "px"
				css[".user|text-shadow"] = "-1px -1px 0 " + HighlightTextStrokeColor + ", 1px -1px 0 " + HighlightTextStrokeColor + ", -1px 0 0 " + HighlightTextStrokeColor + ", 1px 0 0 " + HighlightTextStrokeColor + ", -1px 1px 0 " + HighlightTextStrokeColor + ", 0 -1px 0 " + HighlightTextStrokeColor + ", 0 1px 0 " + HighlightTextStrokeColor + ", 1px 1px 0 " + HighlightTextStrokeColor + ", " + HighlightTextShadowOffset + " " + HighlightTextShadowOffset + " " + HighlightTextShadowOffset + " " + HighlightTextShadowColor
				
		return css
	