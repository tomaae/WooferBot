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
import asyncio
import threading
import os
import random
import websockets


#---------------------------
#   Overlay Handling
#---------------------------
class Overlay:
    def __init__(self, settings, nanoleaf, hue, yeelight, chatbot):
        self.bindIP = '127.0.0.1'
        self.bindPort = 3339
        self.active = 0
        self.sendQueue = None
        self.serverSocket = None
        self.loop = None
        self.loopThread = None
        self.settings = settings
        self.chatbot = chatbot
        self.nanoleaf = nanoleaf
        self.hue = hue
        self.yeelight = yeelight
        
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
    def Send(self, event, jsonData, init=0):
        if self.sendQueue:
            return 1
        
        ## Check mascot image
        if 'mascot' in jsonData:
            if os.path.isfile(jsonData["mascot"]):
                jsonData["mascot"] = "file:///" + jsonData["mascot"]
            else:
                jsonData["mascot"] = ""
        
        ## Check audio
        if 'audio' in jsonData:
            if os.path.isfile(jsonData["audio"]):
                jsonData["audio"] = "file:///" + jsonData["audio"]
            else:
                jsonData["audio"] = ""
        
        ## Check speech bubble image
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
        
        ## Append styles on overlay initialization
        if init == 1:
            jsonDataRaw["styles"] = self.get_styles()
        
        self.sendQueue = jsonDataRaw
        return 0
        
    #---------------------------
    #   Connection
    #---------------------------
    async def Connection(self, websocket, path):
        print("Initializing overlay...")
        self.active = self.active + 1
        
        #
        # Reset overlay to Idle on initialization
        #
        if not self.sendQueue:
            ## Get default mascot image
            mascotIdleImage = self.settings.mascotImages['Idle']['Image']
            if not os.path.isfile(mascotIdleImage):
                mascotIdleImage = ""
            
            ## Load Idle pose mapping if available
            if 'Idle' in self.settings.PoseMapping:
                ## Reset Image to Idle
                if 'Image' in self.settings.PoseMapping['Idle'] and self.settings.PoseMapping['Idle']['Image'] in self.settings.mascotImages:
                    tmp = self.settings.mascotImages[self.settings.PoseMapping['Idle']['Image']]['Image']
                    if os.path.isfile(tmp):
                        mascotIdleImage = tmp
                
                ## Reset Nanoleaf to Idle
                if 'Nanoleaf' in self.settings.PoseMapping['Idle']:
                    self.nanoleaf.scene(self.settings.PoseMapping['Idle']['Nanoleaf'])
                
                ## Reset Hue to Idle
                if 'Hue' in self.settings.PoseMapping['Idle']:
                    for device in self.settings.PoseMapping['Idle']['Hue']:
                        if 'Brightness' in self.settings.PoseMapping['Idle']['Hue'][device] and self.settings.PoseMapping['Idle']['Hue'][device]['Brightness'] >= 1 and 'Color' in self.settings.PoseMapping['Idle']['Hue'][device] and len(self.settings.PoseMapping['Idle']['Hue'][device]['Color']) >= 6 and len(self.settings.PoseMapping['Idle']['Hue'][device]['Color']) <= 7:
                            self.hue.state(device=device, bri=self.settings.PoseMapping['Idle']['Hue'][device]['Brightness'], col=self.settings.PoseMapping['Idle']['Hue'][device]['Color'])
                
                ## Reset Yeelight to Idle
                if 'Yeelight' in self.settings.PoseMapping['Idle']:
                    for device in self.settings.PoseMapping['Idle']['Yeelight']:
                        if 'Brightness' in self.settings.PoseMapping['Idle']['Yeelight'][device] and self.settings.PoseMapping['Idle']['Yeelight'][device]['Brightness'] >= 1 and 'Color' in self.settings.PoseMapping['Idle']['Yeelight'][device] and len(self.settings.PoseMapping['Idle']['Yeelight'][device]['Color']) >= 6 and len(self.settings.PoseMapping['Idle']['Yeelight'][device]['Color']) <= 7 and isinstance(self.settings.PoseMapping['Idle']['Yeelight'][device]['TransitionTime'], int):
                            self.yeelight.state(device=device, brightness=self.settings.PoseMapping['Idle']['Yeelight'][device]['Brightness'], color=self.settings.PoseMapping['Idle']['Yeelight'][device]['Color'], transition=self.settings.PoseMapping['Idle']['Yeelight'][device]['Transition'], transitionTime=self.settings.PoseMapping['Idle']['Yeelight'][device]['TransitionTime'])
            
            ## Send Idle payload
            jsonData = {
                "mascot": mascotIdleImage
            }
            self.Send(event="EVENT_WOOFERBOT", jsonData=jsonData, init=1)
        
        #
        # Overlay loop
        #
        pingSend = 0
        while True:
            pingSend = pingSend + 1
            ## Queue is not empty, process
            if self.sendQueue:
                jsonDataRaw = self.sendQueue
                try:
                    ## Process message
                    if 'message' in jsonDataRaw['data']:
                        ## Process inline randomizer
                        while jsonDataRaw['data']['message'].find("[") >= 0:
                            tmp = jsonDataRaw['data']['message'][slice(jsonDataRaw['data']['message'].find("[") + 1, jsonDataRaw['data']['message'].find("]"))]
                            jsonDataRaw['data']['message'] = jsonDataRaw['data']['message'][slice(0, jsonDataRaw['data']['message'].find("["))] + random.SystemRandom().choice(tmp.split(";")) + jsonDataRaw['data']['message'][slice(jsonDataRaw['data']['message'].find("]") + 1, 9999)]
                        
                        chatbotMsg = jsonDataRaw['data']['message']
                        ## Process substrings for chatbot
                        if chatbotMsg.find("{") >= 0:
                            while chatbotMsg.find("{") >= 0:
                                tmp = chatbotMsg[slice(chatbotMsg.find("{") + 1, chatbotMsg.find("}"))]
                                tmp2 = ""
                                if tmp in jsonDataRaw['data']:
                                    tmp2 = jsonDataRaw['data'][tmp]
                                
                                chatbotMsg = chatbotMsg[slice(0, chatbotMsg.find("{"))] + tmp2 + chatbotMsg[slice(chatbotMsg.find("}") + 1, 9999)]
                        
                        ## Send message to chat
                        self.chatbot.Send(chatbotMsg)
                    
                    ## Send message to overlay
                    await websocket.send(json.dumps(jsonDataRaw))
                except websockets.exceptions.ConnectionClosed:
                    ## Connection failed
                    print("Connection closed by overlay...")
                    self.active = self.active - 1
                    break
                else:
                    pingSend = 0
                    self.sendQueue = None
            ## Queue empty, send keepalive
            else:
                if pingSend >= 40:
                    jsonDataRaw = json.dumps({
                        "event": "EVENT_PING",
                        "data": ""
                    })
                    try:
                        await websocket.send(jsonDataRaw)
                    except websockets.exceptions.ConnectionClosed:
                        ## Connection failed
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
            css[".message|right"] = str(int(self.settings.mascotStyles["MascotMaxWidth"]) + 10) + "px"
            css[".message|left"] = "auto"
            css[".message|transform-origin"] = "100% 100%"
            css[".mainbox|text-align"] = "right"
            css[".message::after|display"] = "none"
            css[".message div:first-child|display"] = "none"
            css[".message::before|display"] = "block"
            css[".message div:last-child|display"] = "block"
        else:
            css[".mascot|left"] = "0"
            css[".mascot|right"] = "auto"
            css[".message|left"] = str(int(self.settings.mascotStyles["MascotMaxWidth"]) + 10) + "px"
            css[".message|right"] = "auto"
            css[".message|transform-origin"] = "0% 100%"
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
                    css[".message::after|border-right-color"] = "transparent"  # Not working
                    css[".message::before|border-right-color"] = "transparent"  # Not working
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
