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
wooferbotVersion = 'v1.1.0'

import sys
import os

pathRoot = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(pathRoot, "lib")) #point at lib folder for classes / references

from settings import Settings
from overlay import Overlay
from woofer import Woofer
from twitch import Twitch
from cli import Cli
from nanoleaf import Nanoleaf

#---------------------------
#   Main
#---------------------------

print('WooferBot ' + wooferbotVersion + '  Copyright (C) 2019  Tomaae')
print('This program comes with ABSOLUTELY NO WARRANTY.')
print('This is free software, and you are welcome to redistribute it')
print('under certain conditions.')
print('By using this program, you accept the terms of the software license agreement.')
print('')

# Initialize settings
settings = Settings(pathRoot=pathRoot)

# Initialize nanoleaf
nanoleaf = Nanoleaf(settings=settings)

settings.Save()

# Initialize twitch chatbot
twitchBot = Twitch(settings=settings, woofer=None, bot = True)
if settings.UseChatbot and len(settings.TwitchBotChannel) > 0 and settings.TwitchBotOAUTH.find('oauth:') == 0:
	twitchBot.Connect()

# Initialize overlay
overlay = Overlay(settings=settings, chatbot=twitchBot)
overlay.Start()


# Initialize woofer
woofer = Woofer(settings=settings, overlay=overlay, nanoleaf=nanoleaf, chatbot=twitchBot)

# Initialize twitch
twitch = Twitch(settings=settings, woofer=woofer)
twitch.Connect()
if settings.UseChatbot and len(settings.TwitchBotChannel) < 1 and settings.TwitchBotOAUTH.find('oauth:') != 0:
	twitchBot.LinkTwitch(twitch)

# Start CLI
cli = Cli(settings=settings, woofer=woofer)
cli.Start()

# Cleanup and exit
overlay.Stop()
exit(0)