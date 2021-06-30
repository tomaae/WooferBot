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

from json import load as json_load, dump as json_dump
from codecs import open
from os import path
from time import time
from sys import exit, platform
from lib.helper import get_var_default
from lib.dependencies import CheckSettingsDependencies
from lib.defaults import *


# ---------------------------
#   Settings Handling
# ---------------------------
class Settings:
    def __init__(self, gui, path_root=None):
        self.gui = gui

        self.TwitchChannel = ""
        self.TwitchOAUTH = ""
        self.TwitchBotChannel = ""
        self.TwitchBotOAUTH = ""
        self.UseChatbot = False
        self.CurrentMascot = ""
        self.AlignMascot = ""
        self.HostMessage = ""
        self.AutohostMessage = ""
        self.FollowMessage = ""
        self.MinBits = 0
        self.AutoShoutout = False
        self.AutoShoutoutTime = 10
        self.ShoutoutAccess = "mod"
        self.GlobalVolume = 0.2
        self.NanoleafEnabled = False
        self.NanoleafIP = ""
        self.NanoleafToken = ""
        self.HueEnabled = False
        self.HueIP = ""
        self.HueToken = ""
        self.YeelightEnabled = False
        self.GUIEnabled = True

        self.Styles = {}
        self.Activities = {}
        self.Enabled = {}
        self.Commands = {}
        self.Messages = {}
        self.PoseMapping = {}
        self.Bots = []
        self.ScheduledMessages = []
        self.CustomBits = []
        self.CustomSubs = []
        self.Watchdog = []
        self.scheduleTable = {}
        self.scheduleLines = 0

        self.mascotImages = {}
        self.mascotAudio = {}
        self.mascotStyles = {}

        self.twitch_client_id = "zpm94cuvrntu030mauvxvz9cv2ldja"
        self.commonBots = ["nightbot", "streamlabs", "streamelements", "stay_hydrated_bot", "botisimo", "wizebot",
                           "moobot"]
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
            self.log("Failed to detect OS: {}".format(platform), error=True)

        # Check paths
        self.pathRoot = path_root + self.slash
        self.configFile = self.pathRoot + "settings.json"
        if not path.isdir(self.pathRoot):
            self.log("Working directory not detected.", error=True)
        if not path.isfile(self.pathRoot + "wooferbot.py") and not path.isfile(
                self.pathRoot + "wooferbot_cli.exe") and not path.isfile(self.pathRoot + "wooferbot_cli"):
            self.log("Working directory incorrect.", error=True)
        if not path.isfile(self.configFile):
            self.log("Configuration file is missing, recreating with defaults.")

        self.reload()
        self.reload_mascot()

    # ---------------------------
    #   log
    # ---------------------------
    def log(self, message: str, error=False):
        print(message)

        self.gui.messagelog_add(message)

        self.gui.app.update_idletasks()
        self.gui.app.update()

        if error:
            print("WooferBot initialization failed.")
            self.gui.messagelog_add("WooferBot initialization failed.")
            self.gui.frame_control.grid_forget()
            self.gui.start()
            exit(1)

    # ---------------------------
    #   reload_mascot
    # ---------------------------
    def reload_mascot(self):
        self.log("Loading mascot settings...")
        self.mascotImages = {}
        self.mascotAudio = {}
        self.mascotStyles = {}

        # Load mascot config
        try:
            with open(self.pathRoot + "mascots" + self.slash + self.CurrentMascot + self.slash + "mascot.json",
                      encoding=self.encoding, mode="r") as f:
                data = json_load(f, encoding=self.encoding)
                for key, value in data.items():
                    self.__dict__[key] = value
        except:
            self.log("Unable to load mascot.json", error=True)

        # Check mascot images
        for action in self.mascotImages:
            if 'Image' not in self.mascotImages[action]:
                self.log("Mascot Image variable is missing for action: {}".format(action), error=True)

            self.mascotImages[action]['Image'] = "{}mascots{}{}{}images{}{}".format(self.pathRoot,
                                                                                    self.slash,
                                                                                    self.CurrentMascot,
                                                                                    self.slash,
                                                                                    self.slash,
                                                                                    self.mascotImages[action]['Image'])

        # Check mascot audio
        for action in self.mascotAudio:
            if not isinstance(self.mascotAudio[action]['Audio'], list):
                self.log("Mascot audio is not a list for action: {}".format(action), error=True)

            for idx, val in enumerate(self.mascotAudio[action]['Audio']):
                self.mascotAudio[action]['Audio'][idx] = "{}mascots{}{}{}audio{}{}".format(self.pathRoot,
                                                                                           self.slash,
                                                                                           self.CurrentMascot,
                                                                                           self.slash,
                                                                                           self.slash,
                                                                                           self.mascotAudio[action]['Audio'][idx])

        CheckSettingsDependencies(self)

    # ---------------------------
    #   Reload
    # ---------------------------
    def reload(self):
        self.log("Loading settings...")
        self.set_variables_defaults(self, defaults_root)

        self.Styles = {}
        self.Activities = {}
        self.Enabled = {}
        self.Commands = {}
        self.Messages = {}
        self.PoseMapping = {}
        self.Bots = []
        self.ScheduledMessages = []
        self.CustomBits = []
        self.CustomSubs = []
        self.Watchdog = []

        self.scheduleTable = {}
        self.scheduleLines = 0

        #
        # Load config
        #
        if path.isfile(self.configFile):
            try:
                with open(self.configFile, encoding=self.encoding, mode="r") as f:
                    data = json_load(f, encoding=self.encoding)
                    for key, value in data.items():
                        self.__dict__[key] = value

            except:
                self.log("Unable to load settings.json", error=True)

            self.upgrade_settings_file()

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
            self.scheduleTable[action['Name']] = int(time())

        self.autofill_settings()

        if not path.isfile(self.configFile):
            self.save()
            self.log("Default configuration file has been created.")

        self.verify_login_information()

    # ---------------------------
    #   set_variables_defaults
    # ---------------------------
    @classmethod
    def set_variables_defaults(self, cls, defaults_list):
        for var in defaults_list:
            if type(cls) == dict:
                cls[var] = get_var_default(defaults_list[var])
            else:
                setattr(cls, var, get_var_default(defaults_list[var]))

    # ---------------------------
    #   set_variables
    # ---------------------------
    @classmethod
    def set_variables(self, cls, defaults_list):
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
    def autofill_settings(self):
        self.set_variables(self, defaults_root)
        self.set_variables(self.Enabled, defaults_enabled)
        self.set_variables(self.Styles, defaults_styles)
        self.set_variables(self.Messages, defaults_messages)
        self.set_variables(self.Activities, defaults_activities)
        for action in self.ScheduledMessages:
            self.set_variables(action, defaults_scheduledmessages)

        for action in self.Commands:
            self.set_variables(self.Commands[action], defaults_commands)

        for action in self.CustomBits:
            self.set_variables(action, defaults_custombits)

        for action in self.CustomSubs:
            self.set_variables(action, defaults_customsubs)

        if "DEFAULT" not in self.PoseMapping:
            self.PoseMapping['DEFAULT'] = {}
            self.PoseMapping['DEFAULT']['Image'] = 'Wave'
            self.PoseMapping['DEFAULT']['Audio'] = 'Wave'

        for action in self.PoseMapping:
            if 'Hue' in self.PoseMapping[action]:
                for light in self.PoseMapping[action]['Hue']:
                    self.set_variables(self.PoseMapping[action]['Hue'][light], defaults_posemapping_hue)

            if 'Yeelight' in self.PoseMapping[action]:
                for light in self.PoseMapping[action]['Yeelight']:
                    self.set_variables(self.PoseMapping[action]['Yeelight'][light], defaults_posemapping_yeelight)

    # ---------------------------
    #   Save
    # ---------------------------
    def save(self):
        # Export config
        tmp = {}
        try:
            for key in self.__dict__:
                if key[:1].isupper():
                    tmp[key] = self.__dict__[key]
        except:
            self.log("Failed to export configuration", error=True)

        # Save config
        try:
            with open(self.configFile, encoding=self.encoding, mode="w+") as f:
                json_dump(tmp, f, indent=4, ensure_ascii=False)
        except:
            self.log("Failed to save settings.json", error=True)

        # Save config copy
        try:
            with open(self.pathRoot + "settings.bak", encoding=self.encoding, mode="w+") as f:
                json_dump(tmp, f, indent=4, ensure_ascii=False)
        except:
            self.log("Failed to save settings.bak", error=True)

    # ---------------------------
    #   VerifyLoginInformation
    # ---------------------------
    def verify_login_information(self):
        code = 0
        # Check user name
        if len(self.TwitchChannel) < 1:
            self.log("Twitch channel not specified")
            code = 1

        # Check OAUTH
        if self.TwitchOAUTH.find('oauth:') != 0:
            self.log("Twitch OAUTH is invalid")
            code = 1

        # Check chatbot
        if self.UseChatbot and len(self.TwitchBotOAUTH) > 0 and self.TwitchBotOAUTH.find('oauth:') != 0:
            self.log("Twitch Bot OAUTH is invalid")
            code = 1

        # Check twitch client ID
        if len(self.twitch_client_id) < 1:
            self.log("Twitch ClientID not specified. See https://dev.twitch.tv/docs/v5/#getting-a-client-id")
            code = 1

        if code:
            exit(code)

    # ---------------------------
    #   UpgradeSettingsFile
    # ---------------------------
    def upgrade_settings_file(self):
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
                    self.log("Upgrade: Cannot migrate message values from ScheduledMessages to Messages. {} already exists in Messages.".format(action['Name']), error=True)
                else:
                    self.Messages[action['Name']] = action['Message']
                    del action['Message']

        #
        # Commands Messages v1.2
        #
        for action in self.Commands:
            if 'Message' in self.Commands[action]:
                if action in self.Messages:
                    self.log("Upgrade: Cannot migrate message values from Commands to Messages. {} already exists in Messages.".format(action), error=True)
                else:
                    self.Messages[action] = self.Commands[action]['Message']
                    del self.Commands[action]['Message']

        #
        # CustomGreets v1.2
        #
        if hasattr(self, 'CustomGreets'):
            for action in self.CustomGreets:
                if action in self.Messages:
                    self.log("Upgrade: Cannot migrate CustomGreets to Messages. {} already exists in Messages.".format(action), error=True)

            for action in self.CustomGreets:
                self.Messages["viewer_" + action] = self.CustomGreets[action]

            del self.CustomGreets
