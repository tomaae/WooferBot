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

import tkinter as tk
from tkinter import *
from tkinter import ttk


# ---------------------------
#   Gui Handling
# ---------------------------
class Gui:
    def __init__(self, settings):
        print("Init gui...")
        self.settings = settings
        self.woofer = None
        self.twitch = None
        self.chatbot = None

        self.app = Tk()
        self.app.geometry("800x400")
        self.app.resizable(width=False, height=False)
        self.app.title("Wooferbot")
        self.app.iconbitmap("wooferbot.ico")

        self.tab_control = ttk.Notebook(self.app)
        tab1 = Frame(self.tab_control)
        tab2 = Frame(self.tab_control)
        tab3 = Frame(self.tab_control)

        self.tab_control.add(tab1, text="Log", compound=TOP)
        self.tab_control.add(tab2, text="Login")
        self.tab_control.add(tab3, text="General")
        self.tab_control.pack(fill=BOTH, expand=True)

        self.status_bar_twitch = Label(self.app, text="Twitch", bd=1, fg="RED", width=10, relief=SUNKEN, anchor=W)
        self.status_bar_twitch.pack(side=LEFT)
        self.status_bar_chatbot = Label(self.app, text="Chatbot", bd=1, fg="RED", width=10, relief=SUNKEN, anchor=W)
        self.status_bar_chatbot.pack(side=LEFT)
        self.status_bar_overlay = Label(self.app, text="Overlay", bd=1, fg="RED", width=10, relief=SUNKEN, anchor=W)
        self.status_bar_overlay.pack(side=LEFT)
        Label(self.app, text="", bd=1, relief=SUNKEN, anchor=W).pack(fill=BOTH, side=LEFT, expand=True)

        # my_button = Button(tab1, text="test", command=self.testcmd).pack()

    def start(self):
        print("Starting gui...")
        self.app.mainloop()

    def attach_chatbot(self, chatbot):
        self.chatbot = chatbot

    def attach_woofer(self, woofer):
        self.woofer = woofer

    def attach_twitch(self, twitch):
        self.twitch = twitch

    def connected_twitch(self, status):
        if status:
            self.status_bar_twitch.config(fg="GREEN")
        else:
            self.status_bar_twitch.config(fg="RED")

    def connected_chatbot(self, status):
        if status:
            self.status_bar_chatbot.config(fg="GREEN")
        else:
            self.status_bar_chatbot.config(fg="RED")

    def connected_overlay(self, status):
        if status:
            self.status_bar_overlay.config(fg="GREEN")
        else:
            self.status_bar_overlay.config(fg="RED")

