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

import codecs
import json
import os
import time
from sys import exit, platform
from lib.helper import get_var_default
from lib.dependencies import CheckSettingsDependencies
from lib.defaults import *


# ---------------------------
#   Settings Handling
# ---------------------------
class Settings:
    def __init__(self, pathRoot=None):
        self.encoding = "utf-8-sig"
        # Detect OS
        if platform.startswith('win'):
            self.os = 'win'
            self.slash = '\\'
        elif platform.startswith('freebsd') or platform.startswith('linux'):
            self.os = 'lx'
            self.slash = '/'
        elif platform.startswith('darwin'):
            self.os = 'osx'
            self.slash = '/'
        else:
            print("Failed to detect OS: {}".format(platform))
            exit(1)

        # Check paths
        self.pathRoot = pathRoot + self.slash
        self.configFile = self.pathRoot + "settings.json"
        if not os.path.isdir(self.pathRoot):
            print("Working directory not detected.")
            exit(1)
        if not os.path.isfile(self.pathRoot + "wooferbot.py") and not os.path.isfile(
                self.pathRoot + "wooferbot_cli.exe") and not os.path.isfile(self.pathRoot + "wooferbot_cli"):
            print("Working directory incorrect.")
            exit(1)
        if not os.path.isfile(self.configFile):
            print("Configuration file is missing, recreating with defaults.")

        self.Reload()
        self.ReloadMascot()

    # ---------------------------
    #   ReloadMascot
    # ---------------------------
    def ReloadMascot(self):
        print("Loading mascot settings...")
        self.mascotImages = {}
        self.mascotAudio = {}
        self.mascotStyles = {}

        # Load mascot config
        try:
            with codecs.open(self.pathRoot + "mascots" + self.slash + self.CurrentMascot + self.slash + "mascot.json",
                             encoding=self.encoding, mode="r") as f:
                data = json.load(f, encoding=self.encoding)
                for key, value in data.items():
                    self.__dict__[key] = value
        except:
            print("Unable to load mascot.json")
            exit(1)

        # Check mascot images
        for action in self.mascotImages:
            if 'Image' not in self.mascotImages[action]:
                print("Mascot Image variable is missing for action: {}".format(action))
                exit(1)

            self.mascotImages[action][
                'Image'] = self.pathRoot + "mascots" + self.slash + self.CurrentMascot + self.slash + "images" + self.slash + \
                           self.mascotImages[action]['Image']

        # Check mascot audio
        for action in self.mascotAudio:
            if not isinstance(self.mascotAudio[action]['Audio'], list):
                print("Mascot audio is not a list for action: {}".format(action))
                exit(1)

            for idx, val in enumerate(self.mascotAudio[action]['Audio']):
                self.mascotAudio[action]['Audio'][
                    idx] = self.pathRoot + "mascots" + self.slash + self.CurrentMascot + self.slash + "audio" + self.slash + \
                           self.mascotAudio[action]['Audio'][idx]

        CheckSettingsDependencies(self)

    # ---------------------------
    #   Reload
    # ---------------------------
    def Reload(self):
        print("Loading settings...")
        self.TwitchChannel = ""
        self.TwitchOAUTH = ""
        self.TwitchBotChannel = ""
        self.TwitchBotOAUTH = ""
        self.UseChatbot = False
        self.twitchClientID = "zpm94cuvrntu030mauvxvz9cv2ldja"
        self.Styles = {}
        self.Messages = {}
        self.Activities = {}
        self.Enabled = {}
        self.PoseMapping = {}
        self.CurrentMascot = ""
        self.AlignMascot = ""
        self.pathImages = self.pathRoot + "mascots" + self.slash + self.CurrentMascot + self.slash + "images" + self.slash
        self.pathAudio = self.pathRoot + "mascots" + self.slash + self.CurrentMascot + self.slash + "audio" + self.slash
        self.HostMessage = ""
        self.AutohostMessage = ""
        self.FollowMessage = ""
        self.GlobalVolume = 0.2
        self.MinBits = 0
        self.AutoShoutout = False
        self.AutoShoutoutTime = 10
        self.ShoutoutAccess = "mod"
        self.Bots = []
        self.commonBots = ["nightbot", "streamlabs", "streamelements", "stay_hydrated_bot", "botisimo", "wizebot",
                           "moobot"]
        self.ScheduledMessages = []
        self.scheduleTable = {}
        self.scheduleLines = 0
        self.CustomBits = []
        self.CustomSubs = []
        self.Commands = {}
        self.Watchdog = []

        self.NanoleafEnabled = False
        self.NanoleafIP = ""
        self.NanoleafToken = ""

        self.HueEnabled = False
        self.HueIP = ""
        self.HueToken = ""

        self.YeelightEnabled = False

        #
        # Load config
        #
        if os.path.isfile(self.configFile):
            try:
                with codecs.open(self.configFile, encoding=self.encoding, mode="r") as f:
                    data = json.load(f, encoding=self.encoding)
                    for key, value in data.items():
                        self.__dict__[key] = value

            except:
                print("Unable to load settings.json")
                exit(1)

            self.UpgradeSettingsFile()

        #
        # CONVERT
        #
        self.TwitchChannel = self.TwitchChannel.lower()
        self.TwitchBotChannel = self.TwitchBotChannel.lower()
        self.CurrentMascot = self.CurrentMascot.lower()
        if self.TwitchBotChannel and self.TwitchBotChannel not in self.Bots:
            self.Bots.append(self.TwitchBotChannel)
        self.Bots = [x.lower() for x in self.Bots]
        for action in self.Commands:
            self.Commands[action]['Hotkey'] = [key.lower() for key in self.Commands[action]['Hotkey']]

        #
        # Reset time on all ScheduledMessages
        #
        for action in self.ScheduledMessages:
            self.scheduleTable[action['Name']] = int(time.time())

        self.AutofillSettings()

        if not os.path.isfile(self.configFile):
            self.Save()
            print("Default configuration file has been created.")
            exit(0)

        self.VerifyLoginInformation()

    # ---------------------------
    #   SetVariables
    # ---------------------------
    @classmethod
    def SetVariables(self, cls, defaults_list):
        for var in defaults_list:
            var_found = True
            try:
                if type(cls) == dict:
                    tmp = cls[var]
                else:
                    tmp = getattr(cls, var)
            except:
                var_found = False
                tmp = get_var_default(defaults_list[var])

            if (type(defaults_list[var]) == str and type(tmp) != str) \
                    or (type(defaults_list[var]) in [int, float] and type(tmp) not in [int, float]) \
                    or (type(defaults_list[var]) == bool and type(tmp) != bool) \
                    or (type(defaults_list[var]) == list and type(tmp) != list) \
                    or not var_found:
                if type(cls) == dict:
                    cls[var] = defaults_list[var]
                else:
                    setattr(cls, var, defaults_list[var])

    # ---------------------------
    #   AutofillSettings
    # ---------------------------
    def AutofillSettings(self):
        self.SetVariables(self, defaults_root)
        self.SetVariables(self.Enabled, defaults_enabled)
        self.SetVariables(self.Styles, defaults_styles)
        self.SetVariables(self.Messages, defaults_messages)
        self.SetVariables(self.Activities, defaults_activities)
        for action in self.ScheduledMessages:
            self.SetVariables(action, defaults_scheduledmessages)

        for action in self.Commands:
            self.SetVariables(self.Commands[action], defaults_commands)

        for action in self.CustomBits:
            self.SetVariables(action, defaults_custombits)

        for action in self.CustomSubs:
            self.SetVariables(action, defaults_customsubs)

        if "DEFAULT" not in self.PoseMapping:
            self.PoseMapping['DEFAULT'] = {}
            self.PoseMapping['DEFAULT']['Image'] = 'Wave'
            self.PoseMapping['DEFAULT']['Audio'] = 'Wave'

        for action in self.PoseMapping:
            if 'Hue' in self.PoseMapping[action]:
                for light in self.PoseMapping[action]['Hue']:
                    self.SetVariables(self.PoseMapping[action]['Hue'][light], defaults_posemapping_hue)

            if 'Yeelight' in self.PoseMapping[action]:
                for light in self.PoseMapping[action]['Yeelight']:
                    self.SetVariables(self.PoseMapping[action]['Yeelight'][light], defaults_posemapping_yeelight)

    # ---------------------------
    #   UpgradeSettingsFile
    # ---------------------------
    def UpgradeSettingsFile(self):
        #
        # CurrectMascot fix v1.1
        #
        if hasattr(self, 'CurrectMascot'):
            self.CurrentMascot = self.CurrectMascot
            del self.CurrectMascot

        #
        # ScheduledMessages Messages and remove LastShown v1.2
        #
        for action in self.ScheduledMessages:
            if 'LastShown' in action:
                del action['LastShown']
            if 'Message' in action:
                if action['Name'] in self.Messages:
                    print("Upgrade: Cannot migrate message values from ScheduledMessages to Messages. {} already exists in Messages.".format(action['Name']))
                    exit(1)
                else:
                    self.Messages[action['Name']] = action['Message']
                    del action['Message']

        #
        # Commands Messages v1.2
        #
        for action in self.Commands:
            if 'Message' in self.Commands[action]:
                if action in self.Messages:
                    print("Upgrade: Cannot migrate message values from Commands to Messages. {} already exists in Messages.".format(action))
                    exit(1)
                else:
                    self.Messages[action] = self.Commands[action]['Message']
                    del self.Commands[action]['Message']

        #
        # CustomGreets v1.2
        #
        if hasattr(self, 'CustomGreets'):
            for action in self.CustomGreets:
                if action in self.Messages:
                    print("Upgrade: Cannot migrate CustomGreets to Messages. {} already exists in Messages.".format(action))
                    exit(1)

            for action in self.CustomGreets:
                self.Messages["viewer_" + action] = self.CustomGreets[action]

            del self.CustomGreets

    # ---------------------------
    #   Save
    # ---------------------------
    def Save(self):
        # Export config
        tmp = {}
        try:
            for key in self.__dict__:
                if key[:1].isupper():
                    tmp[key] = self.__dict__[key]
        except:
            print("Failed to export configuration")
            exit(1)

        # Save config
        try:
            with codecs.open(self.configFile, encoding=self.encoding, mode="w+") as f:
                json.dump(tmp, f, indent=4, ensure_ascii=False)
        except:
            print("Failed to save settings.json")
            exit(1)

        # Save config copy
        try:
            with codecs.open(self.pathRoot + "settings.bak", encoding=self.encoding, mode="w+") as f:
                json.dump(tmp, f, indent=4, ensure_ascii=False)
        except:
            print("Failed to save settings.bak")
            exit(1)

    # ---------------------------
    #   VerifyLoginInformation
    # ---------------------------
    def VerifyLoginInformation(self):
        code = 0
        # Check user name
        if len(self.TwitchChannel) < 1:
            print("Twitch channel not specified")
            code = 1

        # Check OAUTH
        if self.TwitchOAUTH.find('oauth:') != 0:
            print("Twitch OAUTH is invalid")
            code = 1

        # Check chatbot
        if self.UseChatbot and len(self.TwitchBotOAUTH) > 0 and self.TwitchBotOAUTH.find('oauth:') != 0:
            print("Twitch Bot OAUTH is invalid")
            code = 1

        # Check twitch client ID
        if len(self.twitchClientID) < 1:
            print("Twitch ClientID not specified. See https://dev.twitch.tv/docs/v5/#getting-a-client-id")
            code = 1

        if code:
            exit(code)
