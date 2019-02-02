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

import sys
import os

pathRoot = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(pathRoot, "lib")) #point at lib folder for classes / references

from settings import Settings
from overlay import Overlay
from woofer import Woofer
from twitch import Twitch

#---------------------------
#   Main
#---------------------------

print('WooferBot  Copyright (C) 2018  Tomaae')
print('This program comes with ABSOLUTELY NO WARRANTY.')
print('This is free software, and you are welcome to redistribute it')
print('under certain conditions.')
print('')

# Initialize settings
settings = Settings(pathRoot=pathRoot)
settings.Save()

# Initialize overlay
overlay = Overlay(settings=settings)
overlay.Start()

# Initialize woofer
woofer = Woofer(settings=settings, overlay=overlay)

# Initialize twitch
twitch = Twitch(settings=settings, woofer=woofer)
twitch.Connect()

print("Started...")
while True:
	input("")

exit(0)