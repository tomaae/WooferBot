##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for twitch.tv
#    Copyright (C) 2019  Tomaae
#    (https://github.com/tomaae/WooferBot)
#
#    This file is part of WooferBot.
#
#    WooferBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
##########################################################################

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

print('WooferBot  Copyright (C) 2019  Tomaae')
print('This program comes with ABSOLUTELY NO WARRANTY.')
print('This is free software, and you are welcome to redistribute it')
print('under certain conditions.')
print('')

# Initialize settings
settings = Settings(pathRoot=pathRoot)

# Initialize nanoleaf
nanoleaf = Nanoleaf(settings=settings)

settings.Save()

# Initialize overlay
overlay = Overlay(settings=settings)
overlay.Start()

# Initialize woofer
woofer = Woofer(settings=settings, overlay=overlay, nanoleaf=nanoleaf)

# Initialize twitch
twitch = Twitch(settings=settings, woofer=woofer)
twitch.Connect()

# Start CLI
cli = Cli(settings=settings, woofer=woofer)
cli.Start()

# Cleanup and exit
overlay.Stop()
exit(0)