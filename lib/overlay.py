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

import websockets
import json
import asyncio
import threading
import os

#---------------------------
#   Overlay Handling
#---------------------------
class Overlay:
	def __init__(self, settings):
		self.bindIP       = '127.0.0.1'
		self.bindPort     = 3338
		self.active       = 0
		self.sendQueue    = None
		self.serverSocket = None
		self.loop         = None
		self.loopThread   = None
		self.settings     = settings

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
		
	def Stop(self):
		self.loop.stop()
		return
		
	def Send(self, event, jsonData, init = 0):
		if self.sendQueue:
			return 1
			
		if 'mascot' in jsonData:
			if os.path.exists(jsonData["mascot"]):
				jsonData["mascot"] = "file:///" + jsonData["mascot"]
			else:
				jsonData["mascot"] = ""
				
		if 'audio' in jsonData:
			if os.path.exists(jsonData["audio"]):
				jsonData["audio"] = "file:///" + jsonData["audio"]
			else:
				jsonData["audio"] = ""
			
		if 'image' in jsonData:
			if os.path.exists(jsonData["image"]):
				jsonData["image"] = "file:///" + jsonData["image"]
			else:
				if jsonData["image"].find('https://') != 0:
					jsonData["image"] = ""

		jsonDataRaw = {
			"event": event,
			"data": json.dumps(jsonData)
		}
		if init == 1:
			jsonDataRaw["styles"] = self.get_styles()
			
		self.sendQueue = json.dumps(jsonDataRaw)
		return 0
		
	async def Connection(self, websocket, path):
		print("Initializing overlay...")
		self.active = self.active + 1
		if not self.sendQueue:
			mascotIdleImage = self.settings.mascotImages['Idle']['Image']
			if not os.path.exists(mascotIdleImage):
				mascotIdleImage = ""
			if 'Idle' in self.settings.PoseMapping and self.settings.PoseMapping['Idle']['Image'] in self.settings.mascotImages:
				tmp = self.settings.mascotImages[self.settings.PoseMapping['Idle']['Image']]['Image']
				if os.path.exists(tmp):
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
					await websocket.send(jsonDataRaw)
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
		
	def get_styles(self):
		css = {}
		
		if not self.settings.mascotStyles["MascotMaxWidth"]:
			self.settings.mascotStyles["MascotMaxWidth"] = 150
		
		css[".mascot|width"] = str(self.settings.mascotStyles["MascotMaxWidth"]) + "px"
		css[".message|left"] = str(int(self.settings.mascotStyles["MascotMaxWidth"]) + 10 ) + "px"
		
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
				else:
					css[".message|box-shadow"] = "-1px -1px 0 " + val + ", 1px -1px 0 " + val + ", -1px 1px 0 " + val + ", 1px 1px 0 " + val
					css[".message::after|border-right-color"] = val  # Not working
					
					
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
	