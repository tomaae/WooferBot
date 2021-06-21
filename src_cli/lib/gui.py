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

from tkinter import *


# ---------------------------
#   Gui Handling
# ---------------------------
class Gui:
    def __init__(self, settings, woofer, twitch, chatbot):
        self.woofer = woofer
        self.settings = settings
        self.twitch = twitch
        self.chatbot = chatbot

    def start(self):
        print("Starting gui...")

        window = Tk()
        # Creates the window from the imported Tkinter module
        window.geometry("600x400")
        # Creates the size of the window
        window.title("Test :)")
        # Adds a title to the Windows GUI for the window
        window.mainloop()
        # Loops the window to prevent the window from just "flashing once"
