##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for streamers
#    Copyright (C) 2020  Tomaae
#    (https://wooferbot.com/)
#
#    This file is part of WooferBot.
#
#    WooferBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
##########################################################################

from uuid import uuid4
from random import SystemRandom
from threading import Timer, Thread
from time import time, sleep
from os import path, system
from pynput.keyboard import Controller
from lib.helper import has_access_rights, KEYLIST
from lib.twitch import twitch_get_user, twitch_get_last_activity


# ---------------------------
#   Woofer logic
# ---------------------------
class Woofer:
    def __init__(self, settings, overlay, nanoleaf, hue, yeelight, chatbot, gui):
        self.settings = settings
        self.overlay = overlay
        self.nanoleaf = nanoleaf
        self.hue = hue
        self.yeelight = yeelight
        self.chatbot = chatbot
        self.gui = gui

        self.keyboard = Controller()

        self.queue = []
        self.queuePaused = False
        self.greetedUsers = []

        self.lurkingUsers = []
        self.unlurkingUsers = []
        self.hostingUsers = []
        self.shoutoutUsers = []
        self.commandsViewerOnce = {}
        self.commandsViewerTimeout = {}
        self.commandsGlobalTimeout = {}

        self.changedLightsNanoleaf = ""
        self.changedLightsHue = {}
        self.changedLightsYeelight = {}

        # Start timer for ScheduledMessages
        timer = Timer(300, self.woofer_timers)
        timer.daemon = True
        timer.start()

    # ---------------------------
    #   process_json
    # ---------------------------
    def process_json(self, json_data):
        #
        # Commands
        #
        if json_data["custom-tag"] == "command":
            # Shoutout
            if json_data["command"] in ["!so", "!shoutout"]:
                self.woofer_shoutout(json_data)

            # Lurk
            elif json_data["command"] == "!lurk":
                self.woofer_lurk(json_data)

            # Unlurk
            elif json_data["command"] in ["!unlurk", "!back"]:
                self.woofer_unlurk(json_data)

            # Custom commands
            elif json_data["command"] in self.settings.Commands:
                self.woofer_commands(json_data)

            # Search command aliases
            else:
                for action in self.settings.Commands:
                    if (
                        json_data["command"]
                        in self.settings.Commands[action]["Aliases"]
                    ):
                        json_data["command"] = action
                        self.woofer_commands(json_data)

        #
        # Messages
        #
        elif json_data["custom-tag"] == "message":
            common_bots = set(self.settings.commonBots)
            custom_bots = set(self.settings.Bots)

            # MinLines increase for timers
            self.settings.scheduleLines += 1

            # Alerts from chatbots
            if json_data["sender"] in common_bots or json_data["sender"] in custom_bots:
                # Follow
                if json_data["message"].find(self.settings.FollowMessage) > 0:
                    line = json_data["message"].split(" ")
                    json_data["display-name"] = line[0].rstrip(",")
                    json_data["custom-tag"] = "follow"
                    self.woofer_alert(json_data)

                return

            # Greeting
            if (
                json_data["sender"] not in common_bots
                and json_data["sender"] not in custom_bots
            ):
                self.woofer_greet(json_data)

            # Channel points default
            elif json_data["msg-id"] == "highlighted-message":
                self.settings.log(
                    "Channel points, claimed reward: Redeemed Highlight My Message"
                )

            # Channel points custom w/message
            elif json_data["custom-reward-id"]:
                self.settings.log(
                    "Channel points, claimed custom reward: {}".format(
                        json_data["custom-reward-id"]
                    )
                )

            # Bits
            elif (
                int(json_data["bits"]) > 0
                and int(json_data["bits"]) >= self.settings.MinBits
            ):
                json_data["custom-tag"] = "bits"
                self.woofer_alert(json_data)

        #
        # Standard alerts
        #
        elif json_data["custom-tag"] in [
            "new_chatter",
            "raid",
            "host",
            "autohost",
            "sub",
            "resub",
            "subgift",
            "anonsubgift",
        ]:
            self.woofer_alert(json_data)

    # ---------------------------
    #   woofer_queue
    # ---------------------------
    def woofer_queue(self, queue_id, json_data):
        #
        # Check if there is somethign in queue
        #
        if not self.queue:
            return

        #
        # Check if overlay is connected
        #
        if self.overlay.active < 1:
            self.settings.log("waiting for overlay")
            timer = Timer(3, self.woofer_queue, args=(queue_id, json_data))
            timer.daemon = True
            timer.start()
            return

        #
        # Check if queue is paused
        #
        if self.queuePaused:
            timer = Timer(1, self.woofer_queue, args=(queue_id, json_data))
            timer.daemon = True
            timer.start()
            return

        #
        # Check if our turn in queue
        #
        if self.queue[0] != queue_id:
            timer = Timer(0.5, self.woofer_queue, args=(queue_id, json_data))
            timer.daemon = True
            timer.start()
            return

        #
        # Send to overlay, retry later if overlay buffer is full
        #
        if self.overlay.send("EVENT_WOOFERBOT", json_data) == 1:
            timer = Timer(1, self.woofer_queue, args=(queue_id, json_data))
            timer.daemon = True
            timer.start()
            return

        #
        # Execute custom scripts
        #
        if "script" in json_data and json_data["script"] != "":
            system('"{}"'.format(json_data["script"]))

        #
        # Execute hotkey
        #
        if "hotkey" in json_data and json_data["hotkey"] != "":
            for key in json_data["hotkey"]:
                if key in KEYLIST:
                    try:
                        self.keyboard.press(KEYLIST[key])
                    except:
                        self.settings.log(
                            "Invalid hotkey in {}".format(json_data["id"])
                        )
                else:
                    try:
                        self.keyboard.press(key)
                    except:
                        self.settings.log(
                            "Invalid hotkey in {}".format(json_data["id"])
                        )

            sleep(0.05)

            for key in reversed(json_data["hotkey"]):
                if key in KEYLIST:
                    try:
                        self.keyboard.release(KEYLIST[key])
                    except:
                        self.settings.log(
                            "Invalid hotkey in {}".format(json_data["id"])
                        )
                else:
                    try:
                        self.keyboard.release(key)
                    except:
                        self.settings.log(
                            "Invalid hotkey in {}".format(json_data["id"])
                        )

        #
        # Turn on Nanoleaf
        #
        if "nanoleaf" in json_data and json_data["nanoleaf"] != "":
            self.nanoleaf.scene(json_data["nanoleaf"])
            if "nanoleafpersistent" in json_data and json_data["nanoleafpersistent"]:
                self.changedLightsNanoleaf = json_data["nanoleaf"]

        #
        # Turn on Hue
        #
        if "hue" in json_data:
            for device in json_data["hue"]:
                pose_light = json_data["hue"][device]
                if (
                    "Brightness" in pose_light
                    and pose_light["Brightness"] >= 1
                    and "Color" in pose_light
                    and 6 <= len(pose_light["Color"]) <= 7
                ):
                    self.hue.state(
                        device=device,
                        bri=pose_light["Brightness"],
                        col=pose_light["Color"],
                    )

            if "huepersistent" in json_data and json_data["huepersistent"]:
                self.changedLightsHue = json_data["hue"]

        #
        # Turn on Yeelight
        #
        if "yeelight" in json_data:
            for device in json_data["yeelight"]:
                pose_light = json_data["yeelight"][device]
                if (
                    "Brightness" in pose_light
                    and pose_light["Brightness"] >= 1
                    and "Color" in pose_light
                    and 6 <= len(pose_light["Color"]) <= 7
                ):
                    self.yeelight.state(
                        device=device,
                        brightness=pose_light["Brightness"],
                        color=pose_light["Color"],
                        transition=pose_light["Transition"],
                        transitionTime=pose_light["TransitionTime"],
                    )

            if "yeelightpersistent" in json_data and json_data["yeelightpersistent"]:
                self.changedLightsYeelight = json_data["yeelight"]

        #
        # Reset to default after X seconds
        #
        timer = Timer(
            json_data["time"] / 1000,
            self.woofer_queue_default,
            args=(queue_id, json_data),
        )
        timer.daemon = True
        timer.start()

    # ---------------------------
    #   woofer_queue_default
    # ---------------------------
    def woofer_queue_default(self, queue_id, old_json_data):
        #
        # Set default Idle image
        #
        mascot_idle_image = self.settings.mascotImages["Idle"]["Image"]
        if not path.isfile(mascot_idle_image):
            mascot_idle_image = ""

        #
        # Check mapping for custom Idle image
        #
        if (
            "Idle" in self.settings.PoseMapping
            and "Image" in self.settings.PoseMapping["Idle"]
            and self.settings.PoseMapping["Idle"]["Image"] in self.settings.mascotImages
        ):
            tmp = self.settings.mascotImages[
                self.settings.PoseMapping["Idle"]["Image"]
            ]["Image"]
            if path.isfile(tmp):
                mascot_idle_image = tmp

        #
        # Send to overlay, retry later if overlay buffer is full
        #
        json_data = {"mascot": mascot_idle_image}
        if self.overlay.send("EVENT_WOOFERBOT", json_data) == 1:
            timer = Timer(1, self.woofer_queue_default, args=(queue_id, old_json_data))
            timer.daemon = True
            timer.start()
            return

        #
        # Reset Nanoleaf to Idle
        #
        if "nanoleaf" in old_json_data and old_json_data["nanoleaf"]:
            # Reset to persistent lights
            if self.changedLightsNanoleaf:
                self.nanoleaf.scene(self.changedLightsNanoleaf)
            # Reset to Idle lights
            elif (
                "Idle" in self.settings.PoseMapping
                and "Nanoleaf" in self.settings.PoseMapping["Idle"]
            ):
                self.nanoleaf.scene(self.settings.PoseMapping["Idle"]["Nanoleaf"])
            # Turn off lights
            else:
                self.nanoleaf.scene()

        #
        # Reset Hue to Idle
        #
        if "hue" in old_json_data:
            # Reset to persistent lights
            if self.changedLightsHue:
                for device in self.changedLightsHue:
                    pose_light = self.changedLightsHue[device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                    ):
                        self.hue.state(
                            device=device,
                            bri=pose_light["Brightness"],
                            col=pose_light["Color"],
                        )

                for device in old_json_data["hue"]:
                    pose_light = old_json_data["hue"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                        and device not in self.changedLightsHue
                    ):
                        self.hue.state(device=device)

            # Reset to Idle lights
            elif (
                "Idle" in self.settings.PoseMapping
                and "Hue" in self.settings.PoseMapping["Idle"]
            ):
                for device in self.settings.PoseMapping["Idle"]["Hue"]:
                    pose_light = self.settings.PoseMapping["Idle"]["Hue"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                    ):
                        self.hue.state(
                            device=device,
                            bri=pose_light["Brightness"],
                            col=pose_light["Color"],
                        )

                for device in old_json_data["hue"]:
                    pose_light = old_json_data["hue"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                        and device not in self.settings.PoseMapping["Idle"]["Hue"]
                    ):
                        self.hue.state(device=device)

            # Turn off lights
            else:
                for device in old_json_data["hue"]:
                    pose_light = old_json_data["hue"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                    ):
                        self.hue.state(device=device)

        #
        # Reset Yeelight to Idle
        #
        if "yeelight" in old_json_data:
            # Reset to persistent lights
            if self.changedLightsYeelight:
                for device in self.changedLightsYeelight:
                    pose_light = self.changedLightsYeelight[device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                    ):
                        self.yeelight.state(
                            device=device,
                            brightness=pose_light["Brightness"],
                            color=pose_light["Color"],
                            transition=pose_light["Transition"],
                            transitionTime=pose_light["TransitionTime"],
                        )

                for device in old_json_data["yeelight"]:
                    pose_light = old_json_data["yeelight"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                        and device not in self.changedLightsYeelight
                    ):
                        self.yeelight.state(device=device)

            # Reset to Idle lights
            elif (
                "Idle" in self.settings.PoseMapping
                and "Yeelight" in self.settings.PoseMapping["Idle"]
            ):
                for device in self.settings.PoseMapping["Idle"]["Yeelight"]:
                    pose_light = self.settings.PoseMapping["Idle"]["Yeelight"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                    ):
                        self.yeelight.state(
                            device=device,
                            brightness=pose_light["Brightness"],
                            color=pose_light["Color"],
                            transition=pose_light["Transition"],
                            transitionTime=pose_light["TransitionTime"],
                        )

                for device in old_json_data["yeelight"]:
                    pose_light = old_json_data["yeelight"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                        and device not in self.settings.PoseMapping["Idle"]["Yeelight"]
                    ):
                        self.yeelight.state(device=device)

            # Turn off lights
            else:
                for device in old_json_data["yeelight"]:
                    pose_light = old_json_data["yeelight"][device]
                    if (
                        "Brightness" in pose_light
                        and pose_light["Brightness"] >= 1
                        and "Color" in pose_light
                        and 6 <= len(pose_light["Color"]) <= 7
                    ):
                        self.yeelight.state(device=device)

        #
        # Remove notification from queue
        #
        if self.queue:
            self.queue.remove(queue_id)

    # ---------------------------
    #   woofer_addtoqueue
    # ---------------------------
    def woofer_addtoqueue(self, json_response):
        self.settings.log("{}: {}".format(json_response["id"], json_response["sender"]))

        if "message" not in json_response or json_response["message"] == "":
            if json_response["id"] in self.settings.Messages:
                json_response["message"] = SystemRandom().choice(
                    self.settings.Messages[json_response["id"]]
                )
            else:
                json_response["message"] = ""

        json_response["mascot"] = self.mascot_images_file(json_response["id"])
        json_response["mascotmouth"] = self.mascot_images_mouth_height(
            json_response["id"]
        )
        json_response["time"] = self.mascot_images_time(json_response["id"])
        json_response["audio"] = self.mascot_audio_file(json_response["id"])
        json_response["volume"] = self.mascot_audio_volume(json_response["id"])
        json_response["nanoleaf"] = self.mascot_nanoleaf_scene(json_response["id"])
        json_response["nanoleafpersistent"] = self.mascot_nanoleaf_persistent(
            json_response["id"]
        )
        json_response["hue"] = self.mascot_hue_devices(json_response["id"])
        json_response["huepersistent"] = self.mascot_hue_persistent(json_response["id"])
        json_response["yeelight"] = self.mascot_yeelight_devices(json_response["id"])
        json_response["yeelightpersistent"] = self.mascot_yeelight_persistent(
            json_response["id"]
        )

        # Add to queue
        queue_id = uuid4()
        self.queue.append(queue_id)
        Thread(target=self.woofer_queue, args=(queue_id, json_response)).start()

    # ---------------------------
    #   woofer_alert
    # ---------------------------
    def woofer_alert(self, json_data):
        custom_id = json_data["custom-tag"]
        if not self.settings.Enabled[custom_id]:
            return

        json_feed = {"sender": json_data["display-name"]}

        #
        # sub/resub
        #
        if custom_id in ("sub", "resub"):
            for customObj in self.settings.CustomSubs:
                if customObj["Tier"] == "" and int(customObj["From"]) <= int(
                    json_data["months"]
                ) <= int(customObj["To"]):
                    custom_id = customObj["Name"]

            sub_tier = ""
            if json_data["sub_tier"] == "Tier 1":
                sub_tier = "1"
            if json_data["sub_tier"] == "Tier 2":
                sub_tier = "2"
            if json_data["sub_tier"] == "Tier 3":
                sub_tier = "3"
            if json_data["sub_tier"] == "Prime":
                sub_tier = "prime"

            for customObj in self.settings.CustomSubs:
                if sub_tier == customObj["Tier"] and int(customObj["From"]) <= int(
                    json_data["months"]
                ) <= int(customObj["To"]):
                    custom_id = customObj["Name"]

            json_feed["months"] = json_data["months"]
            json_feed["months_streak"] = json_data["months_streak"]
            json_feed["sub_tier"] = json_data["sub_tier"]

        #
        # subgift/anonsubgift
        #
        if custom_id in ("subgift", "anonsubgift"):
            if json_data["custom-tag"] == "anonsubgift":
                json_data["display-name"] = "anonymous"

            json_feed["recipient"] = json_data["msg-param-recipient-display-name"]
            json_feed["sub_tier"] = json_data["sub_tier"]

        #
        # bits
        #
        if custom_id == "bits":
            for customObj in self.settings.CustomBits:
                if (
                    int(customObj["From"])
                    <= int(json_data["bits"])
                    <= int(customObj["To"])
                ):
                    custom_id = customObj["Name"]

            json_feed["bits"] = json_data["bits"]

        #
        # host/raid
        #
        if custom_id in ("host", "raid"):
            # Check if user has already raided/hosted
            s = set(self.hostingUsers)
            if json_data["sender"] in s:
                return

            self.hostingUsers.append(json_data["sender"])

            if custom_id == "host":
                json_feed["sender"] = json_data["sender"]

            if custom_id == "raid":
                json_feed["viewers"] = json_data["viewers"]

        #
        # Send data
        #
        json_feed["id"] = custom_id
        self.woofer_addtoqueue(json_feed)

        # Trigger autoshoutout if enabled
        if custom_id in ("host", "raid") and self.settings.AutoShoutout:
            json_data["subscriber"] = "1"
            json_data["vip"] = "1"
            json_data["moderator"] = "1"
            json_data["broadcaster"] = "1"
            json_data["command_parameter"] = json_data["display-name"]
            json_data["custom-tag"] = "shoutout"
            timer = Timer(
                self.settings.AutoShoutoutTime, self.woofer_shoutout, args=[json_data]
            )
            timer.daemon = True
            timer.start()

    # ---------------------------
    #   woofer_timers
    # ---------------------------
    def woofer_timers(self):
        # Check if overlay is connected
        if self.overlay.active < 1:
            timer = Timer(30, self.woofer_timers)
            timer.daemon = True
            timer.start()
            return

        # Check if timer is enabled
        min_lines_timer = ""
        for action in self.settings.ScheduledMessages:
            if not action["Enabled"]:
                continue

            current_epoch = int(time())
            if (current_epoch - self.settings.scheduleTable[action["Name"]]) >= (
                action["Timer"] * 60
            ):

                # Timers without MinLines limits
                if action["MinLines"] == 0:
                    self.settings.scheduleTable[action["Name"]] = current_epoch

                    if "Command" in action:
                        self.woofer_commands(
                            {
                                "command": action["Command"],
                                "broadcaster": 1,
                                "sender": self.settings.TwitchChannel.lower(),
                                "display-name": self.settings.TwitchChannel,
                                "custom-tag": "command",
                            }
                        )
                    else:
                        self.woofer_addtoqueue(
                            {
                                "message": SystemRandom().choice(
                                    self.settings.Messages[action["Name"]]
                                ),
                                "image": "{}{}images{}{}".format(
                                    self.settings.pathRoot,
                                    self.settings.slash,
                                    self.settings.slash,
                                    action["Image"],
                                ),
                                "sender": "",
                                "customtag": "ScheduledMessage",
                                "id": action["Name"],
                            }
                        )

                # Check if timer with MinLines limits is executable
                elif action["MinLines"] > 0:
                    if self.settings.scheduleLines < action["MinLines"]:
                        continue

                    if (
                        min_lines_timer == ""
                        or self.settings.scheduleTable[action["Name"]]
                        < self.settings.scheduleTable[min_lines_timer]
                    ):
                        min_lines_timer = action["Name"]

        # Timers with MinLines limits
        if min_lines_timer != "":
            for action in self.settings.ScheduledMessages:
                if action["Name"] != min_lines_timer:
                    continue

                self.settings.scheduleLines = 0
                self.settings.scheduleTable[action["Name"]] = int(time())
                if "Command" in action:
                    self.woofer_commands(
                        {
                            "command": action["Command"],
                            "broadcaster": 1,
                            "sender": self.settings.TwitchChannel.lower(),
                            "display-name": self.settings.TwitchChannel,
                            "custom-tag": "command",
                        }
                    )
                else:
                    self.woofer_addtoqueue(
                        {
                            "message": SystemRandom().choice(
                                self.settings.Messages[action["Name"]]
                            ),
                            "image": "{}{}images{}{}".format(
                                self.settings.pathRoot,
                                self.settings.slash,
                                self.settings.slash,
                                action["Image"],
                            ),
                            "sender": "",
                            "customtag": "ScheduledMessage",
                            "id": action["Name"],
                        }
                    )

        # Reset to default after X seconds
        timer = Timer(30, self.woofer_timers)
        timer.daemon = True
        timer.start()

    # ---------------------------
    #   woofer_commands
    # ---------------------------
    def woofer_commands(self, json_data):
        #
        # Check if command is enabled
        #
        if not self.settings.Commands[json_data["command"]]["Enabled"]:
            return

        #
        # Check access rights
        #
        if self.settings.Commands[json_data["command"]][
            "Access"
        ] != "" and not has_access_rights(
            json_data, self.settings.Commands[json_data["command"]]["Access"]
        ):
            return

        #
        # ViewerOnce
        #
        if self.settings.Commands[json_data["command"]]["ViewerOnce"]:
            if (
                json_data["command"] in self.commandsViewerOnce
                and json_data["sender"] in self.commandsViewerOnce[json_data["command"]]
            ):
                return

            if json_data["command"] not in self.commandsViewerOnce:
                self.commandsViewerOnce[json_data["command"]] = []

            self.commandsViewerOnce[json_data["command"]].append(json_data["sender"])

        #
        # ViewerTimeout
        #
        if self.settings.Commands[json_data["command"]]["ViewerTimeout"] > 0:
            current_epoch = int(time())

            if (
                json_data["command"] in self.commandsViewerTimeout
                and json_data["sender"]
                in self.commandsViewerTimeout[json_data["command"]]
                and (
                    current_epoch
                    - self.commandsViewerTimeout[json_data["command"]][
                        json_data["sender"]
                    ]
                )
                < self.settings.Commands[json_data["command"]]["ViewerTimeout"]
            ):
                return

            if json_data["command"] not in self.commandsViewerTimeout:
                self.commandsViewerTimeout[json_data["command"]] = {}

            self.commandsViewerTimeout[json_data["command"]][
                json_data["sender"]
            ] = current_epoch

        #
        # GlobalTimeout
        #
        if self.settings.Commands[json_data["command"]]["GlobalTimeout"] > 0:
            current_epoch = int(time())
            if (
                json_data["command"] in self.commandsGlobalTimeout
                and (current_epoch - self.commandsGlobalTimeout[json_data["command"]])
                < self.settings.Commands[json_data["command"]]["GlobalTimeout"]
            ):
                return

            self.commandsGlobalTimeout[json_data["command"]] = current_epoch

        #
        # Check custom image
        #
        image = ""
        if self.settings.Commands[json_data["command"]]["Image"] != "":
            image = "{}{}images{}{}".format(
                self.settings.pathRoot,
                self.settings.slash,
                self.settings.slash,
                self.settings.Commands[json_data["command"]]["Image"],
            )
            if not path.isfile(image):
                image = ""

        #
        # Check custom script
        #
        script = ""
        if self.settings.Commands[json_data["command"]]["Script"] != "":
            script = "{}{}scripts{}{}".format(
                self.settings.pathRoot,
                self.settings.slash,
                self.settings.slash,
                self.settings.Commands[json_data["command"]]["Script"],
            )
            if not path.isfile(script):
                script = ""

        self.woofer_addtoqueue(
            {
                "image": image,
                "script": script,
                "hotkey": self.settings.Commands[json_data["command"]]["Hotkey"],
                "sender": json_data["display-name"],
                "id": json_data["command"],
            }
        )

    # ---------------------------
    #   woofer_greet
    # ---------------------------
    def woofer_greet(self, json_data):
        if not self.settings.Enabled["greet"]:
            return

        # Check if user was already greeted
        s = set(self.greetedUsers)
        if json_data["sender"] in s:
            return

        self.greetedUsers.append(json_data["sender"])

        # Check for custom greeting definitions
        custom_message = ""
        if "viewer_" + json_data["display-name"] in self.settings.Messages:
            custom_message = SystemRandom().choice(
                self.settings.Messages["viewer_" + json_data["display-name"]]
            )

        custom_id = "greet"
        if "viewer_" + json_data["display-name"] in self.settings.PoseMapping:
            custom_id = "viewer_" + json_data["display-name"]

        self.woofer_addtoqueue(
            {
                "message": custom_message,
                "sender": json_data["display-name"],
                "id": custom_id,
            }
        )

    # ---------------------------
    #   woofer_lurk
    # ---------------------------
    def woofer_lurk(self, json_data):
        if not self.settings.Enabled["lurk"]:
            return

        # Check if user was already lurking
        s = set(self.lurkingUsers)
        if json_data["sender"] in s:
            return

        self.lurkingUsers.append(json_data["sender"])

        self.woofer_addtoqueue({"sender": json_data["display-name"], "id": "lurk"})

    # ---------------------------
    #   woofer_unlurk
    # ---------------------------
    def woofer_unlurk(self, json_data):
        if not self.settings.Enabled["lurk"]:
            return

        # Check if user was already lurking
        s = set(self.lurkingUsers)
        if json_data["sender"] not in s:
            return

        # Check if user already used unlurk
        s = set(self.unlurkingUsers)
        if json_data["sender"] in s:
            return

        self.unlurkingUsers.append(json_data["sender"])

        self.woofer_addtoqueue({"sender": json_data["display-name"], "id": "unlurk"})

    # ---------------------------
    #   woofer_shoutout
    # ---------------------------
    def woofer_shoutout(self, json_data):
        if not self.settings.Enabled["shoutout"]:
            return
        #
        # Check access rights
        #
        if self.settings.ShoutoutAccess != "" and not has_access_rights(
            json_data, self.settings.ShoutoutAccess
        ):
            return

        #
        # Check if channel parameter was specified
        #
        if not json_data["command_parameter"]:
            return

        if json_data["command_parameter"].find("@") == 0:
            json_data["command_parameter"] = json_data["command_parameter"][1:]

        #
        # Get user info
        #
        so_id, so_name, so_pfp, result = twitch_get_user(
            self.settings.twitchoauth, self.settings.client_id, json_data["command_parameter"]
        )
        if result != 200:
            return

        s = set(self.shoutoutUsers)
        if so_name in s:
            return

        self.shoutoutUsers.append(so_name)

        #
        # Get channel last game
        #
        activity, result = twitch_get_last_activity(
            self.settings.twitchoauth, self.settings.client_id, so_id
        )

        if result != 200:
            return

        activity_text = ""
        if activity:
            if activity in self.settings.Activities:
                activity_text = SystemRandom().choice(
                    self.settings.Activities[activity]
                )
            else:
                activity_text = SystemRandom().choice(self.settings.Activities["Game"])

        self.woofer_addtoqueue(
            {
                "message": SystemRandom().choice(self.settings.Messages["shoutout"])
                + activity_text,
                "sender": json_data["display-name"],
                "recipient": so_name,
                "activity": activity,
                "image": so_pfp,
                "id": "shoutout",
            }
        )

    # ---------------------------
    #   mascotImagesFile
    # ---------------------------
    def mascot_images_file(self, action):
        pose = self.settings.PoseMapping
        if action in pose and pose[action]["Image"] in self.settings.mascotImages:
            tmp = self.settings.mascotImages[pose[action]["Image"]]["Image"]
            if path.isfile(tmp):
                return tmp

        return self.settings.mascotImages[pose["DEFAULT"]["Image"]]["Image"]

    # ---------------------------
    #   mascotImagesMouthHeight
    # ---------------------------
    def mascot_images_mouth_height(self, action):
        pose = self.settings.PoseMapping
        if (
            action in pose
            and pose[action]["Image"] in self.settings.mascotImages
            and "MouthHeight" in self.settings.mascotImages[pose[action]["Image"]]
        ):
            mouth_height = self.settings.mascotImages[pose[action]["Image"]][
                "MouthHeight"
            ]
            if mouth_height in ("", 0):
                return 80
            return mouth_height - 5

        return self.settings.mascotImages[pose["DEFAULT"]["Image"]]["MouthHeight"] - 5

    # ---------------------------
    #   mascotImagesTime
    # ---------------------------
    def mascot_images_time(self, action):
        pose = self.settings.PoseMapping
        if action in pose and pose[action]["Image"] in self.settings.mascotImages:
            return self.settings.mascotImages[pose[action]["Image"]]["Time"]

        return self.settings.mascotImages[pose["DEFAULT"]["Image"]]["Time"]

    # ---------------------------
    #   mascotAudioFile
    # ---------------------------
    def mascot_audio_file(self, action):
        pose = self.settings.PoseMapping
        if action in pose and pose[action]["Audio"] in self.settings.mascotAudio:
            tmp = SystemRandom().choice(
                self.settings.mascotAudio[pose[action]["Audio"]]["Audio"]
            )
            if path.isfile(tmp):
                return tmp

        elif pose["DEFAULT"]["Audio"] in self.settings.mascotAudio:
            return SystemRandom().choice(
                self.settings.mascotAudio[pose["DEFAULT"]["Audio"]]["Audio"]
            )

        return ""

    # ---------------------------
    #   mascotAudioVolume
    # ---------------------------
    def mascot_audio_volume(self, action):
        pose = self.settings.PoseMapping
        if action in pose and pose[action]["Audio"] in self.settings.mascotAudio:
            return self.settings.mascotAudio[pose[action]["Audio"]]["Volume"]

        return self.settings.GlobalVolume

    # ---------------------------
    #   mascotNanoleafScene
    # ---------------------------
    def mascot_nanoleaf_scene(self, action):
        pose = self.settings.PoseMapping
        if action in pose and "Nanoleaf" in pose[action]:
            return pose[action]["Nanoleaf"]

        if "Nanoleaf" in pose["DEFAULT"]:
            return pose["DEFAULT"]["Nanoleaf"]

        return ""

    # ---------------------------
    #   mascotNanoleafPersistent
    # ---------------------------
    def mascot_nanoleaf_persistent(self, action):
        pose = self.settings.PoseMapping
        if action in pose and "NanoleafPersistent" in pose[action]:
            return pose[action]["NanoleafPersistent"]

        if "NanoleafPersistent" in pose["DEFAULT"]:
            return pose["DEFAULT"]["NanoleafPersistent"]

        return ""

    # ---------------------------
    #   mascotHueDevices
    # ---------------------------
    def mascot_hue_devices(self, action):
        pose = self.settings.PoseMapping
        if action in pose and "Hue" in pose[action]:
            return pose[action]["Hue"]

        if "Hue" in pose["DEFAULT"]:
            return pose["DEFAULT"]["Hue"]

        return ""

    # ---------------------------
    #   mascotHuePersistent
    # ---------------------------
    def mascot_hue_persistent(self, action):
        pose = self.settings.PoseMapping
        if action in pose and "HuePersistent" in pose[action]:
            return pose[action]["HuePersistent"]

        if "HuePersistent" in pose["DEFAULT"]:
            return pose["DEFAULT"]["HuePersistent"]

        return ""

    # ---------------------------
    #   mascotYeelightDevices
    # ---------------------------
    def mascot_yeelight_devices(self, action):
        pose = self.settings.PoseMapping
        if action in pose and "Yeelight" in pose[action]:
            return pose[action]["Yeelight"]

        if "Yeelight" in pose["DEFAULT"]:
            return pose["DEFAULT"]["Yeelight"]

        return ""

    # ---------------------------
    #   mascotYeelightPersistent
    # ---------------------------
    def mascot_yeelight_persistent(self, action):
        pose = self.settings.PoseMapping
        if action in pose and "YeelightPersistent" in pose[action]:
            return pose[action]["YeelightPersistent"]

        if "YeelightPersistent" in pose["DEFAULT"]:
            return pose["DEFAULT"]["YeelightPersistent"]

        return ""
