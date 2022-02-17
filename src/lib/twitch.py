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

from socket import socket, error as socket_error, timeout as socket_timeout
from threading import Timer, Thread
from re import split as re_split
from time import time
from json import loads as json_loads
from requests import get as requests_get
from .const import (
    TWITCH,
    CHATBOT,
    CONNECTING,
    CONNECTED,
    CONNECTION_FAILED,
    DISCONNECTED,
    DISABLED,
)


# ---------------------------
#   twitch_validate_user
# ---------------------------
def twitch_validate_user(oauth: str):
    # Get user info from API
    headers = {
        "Authorization": f"Bearer {oauth}",
    }
    result = requests_get(
        "https://id.twitch.tv/oauth2/validate",
        headers=headers,
    )

    # Check encoding
    if result.encoding is None:
        result.encoding = "utf-8"

    # Check exit code
    if result.status_code != 200:
        return "", "", result.status_code

    json_result = json_loads(result.text)

    # User defined in result json
    if "client_id" not in json_result and not json_result["client_id"]:
        print("Unknown Twitch Username")
        return "", "", 900

    return json_result["client_id"], json_result["login"], result.status_code


# ---------------------------
#   twitch_get_user
# ---------------------------
def twitch_get_user(oauth: str, twitch_client_id: str, target_user: str):
    # Get user info from API
    headers = {
        "Client-Id": twitch_client_id,
        "Authorization": f"Bearer {oauth}",
    }
    result = requests_get(
        "https://api.twitch.tv/helix/users?login={0}".format(target_user.lower()),
        headers=headers,
    )

    # Check encoding
    if result.encoding is None:
        result.encoding = "utf-8"

    json_result = json_loads(result.text)

    # Check exit code
    if result.status_code != 200:
        return "", "", result.status_code

    # User defined in result json
    if "data" not in json_result and not json_result["data"]:
        print("Unknown Twitch Username")
        return "", "", result.status_code

    return (
        json_result["data"][0]["id"],
        json_result["data"][0]["display_name"],
        json_result["data"][0]["profile_image_url"],
        result.status_code,
    )


# ---------------------------
#   twitch_get_last_activity
# ---------------------------
def twitch_get_last_activity(oauth: str, twitch_client_id: str, user_id: int):
    # Get channel activity from API
    headers = {
        "Client-Id": twitch_client_id,
        "Authorization": f"Bearer {oauth}",
    }
    result = requests_get(
        "https://api.twitch.tv/helix/channels?broadcaster_id={}".format(user_id),
        headers=headers,
    )

    # Check encoding
    if result.encoding is None:
        result.encoding = "utf-8"

    json_result = json_loads(result.text)

    # Check exit code
    if result.status_code != 200:
        return "", result.status_code

    return json_result["data"][0]["game_name"], result.status_code


# ---------------------------
#   fill_tags
# ---------------------------
def fill_tags():
    result = {
        "vip": "0",
        "moderator": "0",
        "subscriber": "0",
        "broadcaster": "0",
        "bits_total": "0",
        "bits": "0",
        "sub_tier": "0",
        "months": "0",
        "months_streak": "0",
        "display-name": "",
        # Valid values: sub, resub, subgift, anonsubgift, raid, ritual.
        "msg-id": "",
        # (Sent only on raid) The number of viewers watching the source channel raiding this channel.
        "msg-param-viewerCount": "",
        # (Sent only on subgift, anonsubgift) The display name of the subscription gift recipient.
        "msg-param-recipient-display-name": "",
        # (Sent only on sub, resub, subgift, anonsubgift) The type of subscription plan being used.
        # Valid values: Prime, 1000, 2000, 3000. 1000, 2000, and 3000 refer to the first, second, and third levels
        # of paid subscriptions, respectively (currently $4.99, $9.99, and $24.99).
        "msg-param-sub-plan": "",
        # (Sent only on sub, resub) The total number of months the user has subscribed.
        "msg-param-cumulative-months": "",
        # (Sent only on sub, resub) The number of consecutive months the user has subscribed.
        # This is 0 if msg-param-should-share-streak is 0.
        "msg-param-streak-months": "",
        # (Sent only on ritual) The name of the ritual this notice is for. Valid value: new_chatter.
        "msg-param-ritual-name": "",
        "login": "",
        # <emote ID>:<first index>-<last index>,<another first index>-
        # <another last index>/<another emote ID>:<first index>-<last index>...
        "emotes": "",
        "command": "",
        "command_parameter": "",
        "sender": "",
        "message": "",
        "custom-tag": "",
        "custom-reward-id": "",
    }
    return result


# ---------------------------
#   parse_tags
# ---------------------------
def parse_tags(json_data, msg):
    tags = msg.split(";")
    for tag in tags:
        tag = tag.split("=")
        # "@badges": "", # Comma-separated list of chat badges and the version of each badge
        # (each in the format <badge>/<version>.
        # Valid badge values: admin, bits, broadcaster, global_mod, moderator, subscriber, vip, staff, turbo.
        if tag[0] == "badges":
            badges = tag[1].split(",")
            for badge in badges:
                badge = badge.split("/")
                if badge[0] in ["broadcaster", "moderator", "subscriber", "vip"]:
                    json_data[badge[0]] = badge[1]

                if badge[0] == "bits":
                    json_data["bits_total"] = badge[1]
        else:
            if tag[0] in json_data:
                json_data[tag[0]] = tag[1]

    if json_data["broadcaster"] == 1:
        json_data["moderator"] = "1"

    return json_data


# ---------------------------
#   get_sender
# ---------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break

        if char != ":":
            result += char

    return result


# ---------------------------
#   get_message
# ---------------------------
def get_message(msg):
    result = ""
    i = 4
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1

    result = result.lstrip(":")
    result = result.strip()
    return result


# ---------------------------
#   remove_emotes
# ---------------------------
def remove_emotes(msg, emotes):
    if not emotes:
        return msg

    emotes = emotes.replace("/", ",")
    emotes = emotes.split(",")
    for emote in reversed(emotes):
        if emote.find(":") >= 0:
            emote = emote.split(":")[1]

        emote = emote.split("-")
        msg = msg[: int(emote[0])] + msg[int(emote[1]) + 1 :]

    # print(msg)
    return msg


# ---------------------------
#   Twitch API
# ---------------------------
class Twitch:
    def __init__(self, settings, woofer, gui, bot=False):
        self.bot = bot
        self.settings = settings
        self.woofer = woofer
        self.gui = gui
        self.host = "irc.twitch.tv"  # Hostname of the IRC-Server in this case twitch's
        self.port = 6667  # Default IRC-Port
        self.chrset = "UTF-8"
        self.loopThread = None
        self.con = socket()
        self.conCheckTimer = Timer(30, self.connection_checker)
        self.lastPing = 0
        self.connected = False
        self.linkTwitch = False
        self.TwitchLogin = ""
        self.TwitchOAUTH = ""

    # ---------------------------
    #   connect
    # ---------------------------
    def connect(self):
        self.loopThread = Thread(target=self.connection)
        self.loopThread.daemon = True
        self.loopThread.start()

    # ---------------------------
    #   disconnect
    # ---------------------------
    def disconnect(self):
        self.connected = False
        if self.conCheckTimer.is_alive():
            self.conCheckTimer.cancel()
        self.con.close()

    # ---------------------------
    #   connection_checker
    # ---------------------------
    def connection_checker(self):
        if not self.connected:
            return

        if int(time()) > (self.lastPing + 400):
            if self.bot:
                self.gui.statusbar(CHATBOT, CONNECTION_FAILED)
            else:
                self.gui.statusbar(TWITCH, CONNECTION_FAILED)

            self.settings.log(
                "Connection {} to Twitch not responding, reconnecting...".format(
                    self.TwitchLogin
                )
            )
            self.connected = False
            self.disconnect()
            return

        self.conCheckTimer = Timer(30, self.connection_checker)
        self.conCheckTimer.start()

    # ---------------------------
    #   link_account
    # ---------------------------
    def link_account(self, account):
        self.linkTwitch = account

    # ---------------------------
    #   send
    # ---------------------------
    def send(self, message):
        # Send over linked account in set
        if self.linkTwitch:
            self.linkTwitch.send(message)

        # Do nothing if not connected
        if not self.connected:
            return False

        # Send message to chat
        self.con.send(
            bytes(
                "PRIVMSG #{} :{}\r\n".format(self.settings.twitchchannel, message),
                self.chrset,
            )
        )
        return True

    # ---------------------------
    #   Connection
    # ---------------------------
    def connection(self):
        # Set login
        if self.bot:
            self.TwitchOAUTH = self.settings.TwitchBotOAUTH
            if self.TwitchOAUTH.startswith("oauth:"):
                self.TwitchOAUTH = self.TwitchOAUTH[6:]

            self.settings.client_id, self.TwitchLogin, result = twitch_validate_user(
                self.TwitchOAUTH
            )
            if result != 200:
                self.settings.log(
                    "Unable to connect bot {} to Twitch...".format(self.TwitchLogin)
                )
                self.connected = False
                self.gui.statusbar(CHATBOT, CONNECTION_FAILED)
                return 1

            self.settings.twitchbotlogin = self.TwitchLogin
            self.gui.statusbar(CHATBOT, CONNECTING)
        else:
            self.TwitchOAUTH = self.settings.TwitchOAUTH
            if self.TwitchOAUTH.startswith("oauth:"):
                self.TwitchOAUTH = self.TwitchOAUTH[6:]

            self.settings.client_id, self.TwitchLogin, result = twitch_validate_user(
                self.TwitchOAUTH
            )
            if result != 200:
                self.settings.log(
                    "Unable to connect {} to Twitch...".format(self.TwitchLogin)
                )
                self.connected = False
                self.gui.statusbar(TWITCH, CONNECTION_FAILED)
                return 1

            self.settings.twitchoauth = self.TwitchOAUTH
            self.settings.twitchchannel = self.TwitchLogin
            if self.TwitchLogin not in self.woofer.greetedUsers:
                self.woofer.greetedUsers.append(self.TwitchLogin)
                self.woofer.greetedUsers.append(self.TwitchLogin + "bot")

            if (
                self.settings.twitchbotlogin
                and self.settings.twitchbotlogin not in self.woofer.greetedUsers
            ):
                self.woofer.greetedUsers.append(self.settings.twitchbotlogin)

            self.gui.statusbar(TWITCH, CONNECTING)

        self.settings.log("Connecting {} to Twitch...".format(self.TwitchLogin))

        #
        # Log in
        #
        try:
            self.con = socket()
            self.con.connect((self.host, self.port))
            self.con.send(bytes("PASS oauth:%s\r\n" % self.TwitchOAUTH, self.chrset))
            self.con.send(bytes("NICK %s\r\n" % self.TwitchLogin, self.chrset))
            self.con.send(
                bytes("JOIN #%s\r\n" % self.settings.twitchchannel, self.chrset)
            )
            if not self.bot:
                self.con.send(
                    bytes("CAP REQ :twitch.tv/tags twitch.tv/commands\r\n", self.chrset)
                )

        except:
            self.settings.log(
                "Unable to connect {} to Twitch...".format(self.TwitchLogin)
            )
            self.connected = False
            if self.bot:
                self.gui.statusbar(CHATBOT, CONNECTION_FAILED)
            else:
                self.gui.statusbar(TWITCH, CONNECTION_FAILED)

            return 1

        if self.bot:
            self.gui.statusbar(CHATBOT, CONNECTED)
        else:
            self.gui.statusbar(TWITCH, CONNECTED)

        self.settings.log("Connected {} to Twitch...".format(self.TwitchLogin))
        self.connected = True
        self.lastPing = int(time())
        if self.conCheckTimer.is_alive():
            self.conCheckTimer.cancel()

        self.conCheckTimer = Timer(30, self.connection_checker)
        self.conCheckTimer.start()

        #
        # Twitch loop
        #
        data = ""
        while True:
            try:
                data = data + self.con.recv(1024).decode(self.chrset)
                data_split = re_split(r"[~\r\n]+", data)
                data = data_split.pop()
                Thread(target=self.process_data, args=(data_split,)).start()
            except socket_error:
                if self.bot:
                    self.gui.statusbar(CHATBOT, CONNECTION_FAILED)
                else:
                    self.gui.statusbar(TWITCH, CONNECTION_FAILED)
                self.settings.log("Twitch {} socket error".format(self.TwitchLogin))
                self.connected = False
                self.connect()
                break
            except socket_timeout:
                if self.bot:
                    self.gui.statusbar(CHATBOT, CONNECTION_FAILED)
                else:
                    self.gui.statusbar(TWITCH, CONNECTION_FAILED)
                self.settings.log("Twitch {} socket timeout".format(self.TwitchLogin))
                self.connected = False
                self.connect()
                break

        self.disconnect()

    # ---------------------------
    #   ProcessData
    # ---------------------------
    def process_data(self, data):
        for line in data:
            line = line.strip()
            # print(self.TwitchLogin + "!" + line)

            if line.find("Login authentication failed") > 0:
                self.settings.log("Twitch login authentication failed")
                if self.bot:
                    self.gui.statusbar(CHATBOT, CONNECTION_FAILED)
                else:
                    self.gui.statusbar(TWITCH, CONNECTION_FAILED)
                return

            line = line.split(" ")

            if len(line) >= 1:
                #
                # PING
                #
                if line[0] == "PING":
                    self.lastPing = int(time())
                    self.con.send(bytes("PONG %s\r\n" % line[1], self.chrset))
                    continue

                # Bot check
                if self.bot:
                    continue
                # print(line)

                json_data = fill_tags()
                #
                # DM
                #
                if len(line) >= 2 and line[1] == "PRIVMSG":
                    json_data["sender"] = get_sender(line[3])
                    json_data["message"] = get_message(line)

                    # HOST
                    if json_data["message"].find(self.settings.HostMessage) == 0:
                        json_data["custom-tag"] = "host"
                        self.woofer.process_json(json_data)

                    # AUTOHOST
                    elif json_data["message"].find(self.settings.AutohostMessage) == 0:
                        json_data["custom-tag"] = "autohost"
                        self.woofer.process_json(json_data)

                #
                # CHAT
                #
                elif len(line) >= 3 and line[2] == "PRIVMSG":
                    json_data = parse_tags(json_data, line[0])
                    json_data["sender"] = get_sender(line[1])
                    json_data["message"] = get_message(line)
                    # json_data["message"] = self.remove_emotes(json_data["message"], json_data["emotes"])

                    # COMMAND
                    if json_data["message"].find("!") == 0:
                        val = json_data["message"].split(" ", 1)
                        json_data["command"] = val[0]
                        if len(val) >= 2:
                            json_data["command_parameter"] = val[1]
                        json_data["custom-tag"] = "command"
                        self.woofer.process_json(json_data)
                    else:
                        # NORMAL MESSAGE
                        json_data["custom-tag"] = "message"
                        self.woofer.process_json(json_data)

                #
                # USERNOTICE
                #
                elif len(line) >= 3 and line[2] == "USERNOTICE":
                    if line[0].find("@") == 0:
                        json_data = parse_tags(json_data, line[0])

                    # RAID
                    if json_data["msg-id"] == "raid":
                        json_data["custom-tag"] = "raid"
                        json_data["viewers"] = ""
                        if "msg-param-viewerCount" in json_data:
                            json_data["viewers"] = json_data["msg-param-viewerCount"]
                        self.woofer.process_json(json_data)

                    # SUB
                    elif json_data["msg-id"] in [
                        "sub",
                        "resub",
                        "subgift",
                        "anonsubgift",
                    ]:
                        json_data["custom-tag"] = json_data["msg-id"]

                        if json_data["msg-param-sub-plan"] == "Prime":
                            json_data["sub_tier"] = "Prime"
                        elif json_data["msg-param-sub-plan"] == "1000":
                            json_data["sub_tier"] = "Tier 1"
                        elif json_data["msg-param-sub-plan"] == "2000":
                            json_data["sub_tier"] = "Tier 2"
                        elif json_data["msg-param-sub-plan"] == "3000":
                            json_data["sub_tier"] = "Tier 3"

                        if json_data["msg-id"] in ["sub", "resub"]:
                            if json_data["msg-param-cumulative-months"]:
                                json_data["months"] = json_data[
                                    "msg-param-cumulative-months"
                                ]
                            if json_data["msg-param-streak-months"]:
                                json_data["months_streak"] = json_data[
                                    "msg-param-streak-months"
                                ]

                        self.woofer.process_json(json_data)

                    # MASS SUBGIFT
                    elif json_data["msg-id"] == "submysterygift":
                        json_data["custom-tag"] = "submysterygift"
                        # TODO: Mass gift subs
                        # self.woofer.ProcessJson(json_data)

                    # RITUAL NEW CHATTER
                    elif (
                        json_data["msg-id"] == "ritual"
                        and json_data["msg-param-ritual-name"] == "new_chatter"
                    ):
                        json_data["sender"] = json_data["display-name"]
                        json_data["message"] = get_message(line)
                        json_data["custom-tag"] = "new_chatter"
                        self.woofer.process_json(json_data)
