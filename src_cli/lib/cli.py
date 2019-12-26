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


# ---------------------------
#   CLI Handling
# ---------------------------
class Cli:
    def __init__(self, settings, woofer, twitch, chatbot):
        self.woofer = woofer
        self.settings = settings
        self.twitch = twitch
        self.chatbot = chatbot

    def start(self):
        print("Starting cli...")
        while True:
            cmd = input("")

            if cmd == "x":
                break
            elif cmd == "h":
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
                print("11 - Subgift")
                print("r  - Reconnect to twitch")
                print("x  - Exit")

            #
            # Start
            #
            elif cmd == "0":
                self.woofer.woofer_commands({
                    "display-name": "testname",
                    "sender": "testname",
                    "broadcaster": 1,
                    "command": "!start",
                    "custom-tag": "!start"
                })

            #
            # Follow
            #
            elif cmd == "1":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "custom-tag": "follow"
                })

            #
            # Greet
            #
            elif cmd == "2":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "sender": "testname",
                    "custom-tag": "greet"
                })

            #
            # Shoutout
            #
            elif cmd == "3":
                self.woofer.woofer_shoutout({
                    "subscriber": "1",
                    "vip": "1",
                    "moderator": "1",
                    "broadcaster": "1",
                    "display-name": "testname",
                    "sender": "testname",
                    "command_parameter": "testname",
                    "custom-tag": "shoutout"
                })

            #
            # Lurk
            #
            elif cmd == "4":
                self.woofer.woofer_lurk({
                    "display-name": "testname",
                    "sender": "testname",
                    "custom-tag": "lurk"
                })

            #
            # Bits
            #
            elif cmd == "5":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "bits": "1000",
                    "custom-tag": "bits"
                })

            #
            # New chatter
            #
            elif cmd == "6":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "sender": "testname",
                    "custom-tag": "new_chatter"
                })

            #
            # Raid
            #
            elif cmd == "7":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "sender": "testname",
                    "viewers": "1",
                    "custom-tag": "raid"
                })

            #
            # Host
            #
            elif cmd == "8":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "sender": "testname",
                    "custom-tag": "host"
                })

            #
            # Sub
            #
            elif cmd == "9":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "sender": "testname",
                    "sub_tier": "Tier 2",
                    "months": "4",
                    "months_streak": "4",
                    "custom-tag": "sub"
                })

            #
            # Resub
            #
            elif cmd == "10":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "sender": "testname",
                    "sub_tier": "Tier 3",
                    "months": "4",
                    "months_streak": "4",
                    "custom-tag": "resub"
                })

            #
            # Subgift
            #
            elif cmd == "11":
                self.woofer.woofer_alert({
                    "display-name": "testname",
                    "sender": "testname",
                    "sub_tier": "Tier 2",
                    "msg-param-recipient-display-name": "testname2",
                    "custom-tag": "subgift"
                })

            #
            # Reconnect to twitch
            #
            elif cmd == "r":
                if self.twitch.connected:
                    self.twitch.disconnect()
                if self.chatbot.connected:
                    self.chatbot.disconnect()

            # print(cmd)
