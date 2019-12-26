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

from json import dumps as json_dumps
from asyncio import get_event_loop as asyncio_get_event_loop, sleep as asyncio_sleep
from threading import Thread
from os import path
from random import SystemRandom
from websockets import serve, exceptions as websockets_exceptions


# ---------------------------
#   Overlay Handling
# ---------------------------
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

    # ---------------------------
    #   Start
    # ---------------------------
    def start(self):
        print("Starting overlay server...")
        self.serverSocket = serve(self.connection, self.bindIP, self.bindPort)
        print("Overlay server waiting for connection...")
        self.loop = asyncio_get_event_loop()
        self.loop.run_until_complete(self.serverSocket)
        self.loopThread = Thread(target=self.loop.run_forever)
        self.loopThread.daemon = True
        self.loopThread.start()

    # ---------------------------
    #   Stop
    # ---------------------------
    def stop(self):
        self.loop.stop()

    # ---------------------------
    #   Send
    # ---------------------------
    def send(self, event, json_data, init=0):
        if self.sendQueue:
            return 1

        # Check mascot image
        if 'mascot' in json_data:
            if path.isfile(json_data["mascot"]):
                json_data["mascot"] = f"file:///{json_data['mascot']}"
            else:
                json_data["mascot"] = ""

        # Check audio
        if 'audio' in json_data:
            if path.isfile(json_data["audio"]):
                json_data["audio"] = f"file:///{json_data['audio']}"
            else:
                json_data["audio"] = ""

        # Check speech bubble image
        if 'image' in json_data:
            if path.isfile(json_data["image"]):
                json_data["image"] = f"file:///{json_data['image']}"
            else:
                if json_data["image"].find('https://') != 0:
                    json_data["image"] = ""

        json_data_raw = {
            "event": event,
            "data": json_data
        }

        # Append styles on overlay initialization
        if init == 1:
            json_data_raw["styles"] = self.get_styles()

        self.sendQueue = json_data_raw
        return 0

    # ---------------------------
    #   Connection
    # ---------------------------
    async def connection(self, websocket, _):
        print("Initializing overlay...")
        self.active = self.active + 1

        #
        # Reset overlay to Idle on initialization
        #
        if not self.sendQueue:
            # Get default mascot image
            mascot_idle_image = self.settings.mascotImages['Idle']['Image']
            if not path.isfile(mascot_idle_image):
                mascot_idle_image = ""

            # Load Idle pose mapping if available
            if 'Idle' in self.settings.PoseMapping:
                # Reset Image to Idle
                if 'Image' in self.settings.PoseMapping['Idle'] and \
                        self.settings.PoseMapping['Idle']['Image'] in self.settings.mascotImages:
                    tmp = self.settings.mascotImages[self.settings.PoseMapping['Idle']['Image']]['Image']
                    if path.isfile(tmp):
                        mascot_idle_image = tmp

                # Reset Nanoleaf to Idle
                if 'Nanoleaf' in self.settings.PoseMapping['Idle']:
                    self.nanoleaf.scene(self.settings.PoseMapping['Idle']['Nanoleaf'])

                # Reset Hue to Idle
                if 'Hue' in self.settings.PoseMapping['Idle']:
                    for device in self.settings.PoseMapping['Idle']['Hue']:
                        pose_light = self.settings.PoseMapping['Idle']['Hue'][device]
                        if 'Brightness' in pose_light and \
                                pose_light['Brightness'] >= 1 and \
                                'Color' in pose_light and 6 <= len(pose_light['Color']) <= 7:
                            self.hue.state(device=device,
                                           bri=pose_light['Brightness'],
                                           col=pose_light['Color'])

                # Reset Yeelight to Idle
                if 'Yeelight' in self.settings.PoseMapping['Idle']:
                    for device in self.settings.PoseMapping['Idle']['Yeelight']:
                        pose_light = self.settings.PoseMapping['Idle']['Yeelight'][device]
                        if 'Brightness' in pose_light and \
                                pose_light['Brightness'] >= 1 and 'Color' in \
                                pose_light and 6 <= len(pose_light['Color']) <= 7 and \
                                isinstance(pose_light['TransitionTime'], int):
                            self.yeelight.state(device=device,
                                                brightness=pose_light['Brightness'],
                                                color=pose_light['Color'],
                                                transition=pose_light['Transition'],
                                                transitionTime=pose_light['TransitionTime'])

            # Send Idle payload
            json_data = {
                "mascot": mascot_idle_image
            }
            self.send(event="EVENT_WOOFERBOT", json_data=json_data, init=1)

        #
        # Overlay loop
        #
        ping_send = 0
        while True:
            ping_send = ping_send + 1
            # Queue is not empty, process
            if self.sendQueue:
                json_data_raw = self.sendQueue
                try:
                    # Process message
                    if 'message' in json_data_raw['data']:
                        # Process inline randomizer
                        while json_data_raw['data']['message'].find("[") >= 0:
                            tmp = json_data_raw['data']['message'][slice(json_data_raw['data']['message'].find("[") + 1,
                                                                         json_data_raw['data']['message'].find("]"))]
                            json_data_raw['data']['message'] = json_data_raw['data']['message'][slice(0, json_data_raw['data']['message'].find("["))] + \
                                                               SystemRandom().choice(tmp.split(";")) + \
                                                               json_data_raw['data']['message'][slice(json_data_raw['data']['message'].find("]") + 1, 9999)]

                        chatbot_msg = json_data_raw['data']['message']
                        # Process substrings for chatbot
                        if chatbot_msg.find("{") >= 0:
                            while chatbot_msg.find("{") >= 0:
                                tmp = chatbot_msg[slice(chatbot_msg.find("{") + 1, chatbot_msg.find("}"))]
                                tmp2 = ""
                                if tmp in json_data_raw['data']:
                                    tmp2 = json_data_raw['data'][tmp]

                                chatbot_msg = chatbot_msg[slice(0, chatbot_msg.find("{"))] + tmp2 + chatbot_msg[
                                    slice(chatbot_msg.find("}") + 1, 9999)]

                        # Send message to chat
                        self.chatbot.send(chatbot_msg)

                    # Send message to overlay
                    await websocket.send(json_dumps(json_data_raw))
                except websockets_exceptions.ConnectionClosed:
                    # Connection failed
                    print("Connection closed by overlay...")
                    self.active = self.active - 1
                    break
                else:
                    ping_send = 0
                    self.sendQueue = None
            # Queue empty, send keepalive
            else:
                if ping_send >= 40:
                    json_data_raw = json_dumps({
                        "event": "EVENT_PING",
                        "data": ""
                    })
                    try:
                        await websocket.send(json_data_raw)
                    except websockets_exceptions.ConnectionClosed:
                        # Connection failed
                        self.active = self.active - 1
                        if self.active == 0:
                            print("Connection closed by overlay...")
                        break
                    else:
                        ping_send = 0

            await asyncio_sleep(0.5)

    # ---------------------------
    #   get_styles
    # ---------------------------
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

        highlight_text_stroke_color = ""
        highlight_text_shadow_color = ""
        highlight_text_shadow_offset = ""
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
                    css[".message|box-shadow"] = "-1px -1px 0 " + val + \
                                                 ", 1px -1px 0 " + val + \
                                                 ", -1px 1px 0 " + val + \
                                                 ", 1px 1px 0 " + val
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
                highlight_text_stroke_color = val

            if style == "HighlightTextShadowColor":
                highlight_text_shadow_color = val

            if style == "HighlightTextShadowOffset":
                highlight_text_shadow_offset = val

            if highlight_text_stroke_color != "" and \
                    highlight_text_shadow_color != "" and \
                    highlight_text_shadow_offset != "":
                highlight_text_shadow_offset = str(highlight_text_shadow_offset)
                if highlight_text_shadow_offset != "0":
                    highlight_text_shadow_offset = highlight_text_shadow_offset + "px"
                css[".user|text-shadow"] = "-1px -1px 0 " + highlight_text_stroke_color + \
                                           ", 1px -1px 0 " + highlight_text_stroke_color + \
                                           ", -1px 0 0 " + highlight_text_stroke_color + \
                                           ", 1px 0 0 " + highlight_text_stroke_color + \
                                           ", -1px 1px 0 " + highlight_text_stroke_color + \
                                           ", 0 -1px 0 " + highlight_text_stroke_color + \
                                           ", 0 1px 0 " + highlight_text_stroke_color + \
                                           ", 1px 1px 0 " + highlight_text_stroke_color + \
                                           ", " + highlight_text_shadow_offset + \
                                           " " + highlight_text_shadow_offset + \
                                           " " + highlight_text_shadow_offset + \
                                           " " + highlight_text_shadow_color

        return css
