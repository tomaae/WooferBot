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
from idlelib.tooltip import Hovertip
from .const import (
    TWITCH,
    CHATBOT,
    OVERLAY,

    CONNECTING,
    CONNECTED,
    CONNECTION_FAILED,
    DISCONNECTED,
    DISABLED,
)


# ---------------------------
#   Gui Handling
# ---------------------------
class Gui:
    def __init__(self):
        print("Init gui...")
        self.settings = None
        self.woofer = None
        self.twitch = None
        self.chatbot = None

        # Root
        self.app = Tk()
        self.app.geometry("800x400")
        self.app.resizable(width=False, height=False)
        self.app.title("Wooferbot")
        self.app.iconbitmap("wooferbot.ico")

        # Tabs
        self.tab_control = ttk.Notebook(self.app)
        tab1 = Frame(self.tab_control)
        tab2 = Frame(self.tab_control)
        tab3 = Frame(self.tab_control)

        self.tab_control.add(tab1, text="Log")
        self.tab_control.add(tab2, text="Login")
        self.tab_control.add(tab3, text="General")
        self.tab_control.grid(row=0, column=0, columnspan=4, sticky="NSEW")
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        # Status bar
        statusbar_frame = Frame(self.app)
        statusbar_frame.grid(row=1, column=0, sticky=NSEW)
        statusbar_frame.grid_columnconfigure(3, weight=1)

        self.statusbar_twitch = Label(statusbar_frame, text="Twitch", bd=1, fg="GRAY", width=10, relief=SUNKEN, anchor=W, padx=1, pady=1)
        self.statusbar_twitch.tooltip = Hovertip(self.statusbar_twitch, "Twitch disabled", hover_delay=100)
        self.statusbar_twitch.grid(row=0, column=0, sticky=W)
        self.statusbar_chatbot = Label(statusbar_frame, text="Chatbot", bd=1, fg="GRAY", width=10, relief=SUNKEN, anchor=W, padx=1, pady=1)
        self.statusbar_chatbot.tooltip = Hovertip(self.statusbar_chatbot, "Chatbot disabled", hover_delay=100)
        self.statusbar_chatbot.grid(row=0, column=1, sticky=W)
        self.statusbar_overlay = Label(statusbar_frame, text="Overlay", bd=1, fg="GRAY", width=10, relief=SUNKEN, anchor=W, padx=1, pady=1)
        self.statusbar_overlay.tooltip = Hovertip(self.statusbar_overlay, "Overlay disabled", hover_delay=100)
        self.statusbar_overlay.grid(row=0, column=2, sticky=W)
        Label(statusbar_frame, bd=1, relief=SUNKEN, anchor=W, padx=1, pady=1).grid(row=0, column=3, sticky=EW)

        # [Tab] Log
        tab1.grid_columnconfigure([0], weight=1)
        tab1.grid_rowconfigure(0, weight=1)

        # [Tab] Log - Log Frame
        frame_log = LabelFrame(tab1, text="Log", padx=5, pady=5)
        frame_log.grid(row=0, column=0, padx=2, pady=2, sticky=["NSWE"])
        frame_log.grid_rowconfigure(0, weight=1)
        frame_log.grid_columnconfigure(0, weight=1)

        mls = Scrollbar(frame_log, orient="vertical")
        mls.grid(row=0, column=1, sticky=["N", "S", "E"])
        self.message_log = Listbox(frame_log, yscrollcommand=mls.set)
        mls.configure(command=self.message_log.yview)
        self.message_log.grid(row=0, column=0, sticky=["NSWE"])

        # [Tab] Log - Control Frame
        frame_control = LabelFrame(tab1, text="Controls", padx=5, pady=5)
        frame_control.grid(row=0, column=1, padx=2, pady=2, sticky=["N", "S", "E"])

        def test():
            self.message_log.insert(END, "1")
            self.message_log.insert(END, "2")
            self.message_log.insert(END, "3")
            self.message_log.insert(END, "4")
            self.message_log.insert(END, "5")
            self.message_log.yview(END)

        Button(frame_control, text="Clear queue", width=15, command=test).grid(row=0, column=0, sticky=E)
        Button(frame_control, text="Pause queue", width=15).grid(row=1, column=0, sticky=E)

    def start(self) -> None:
        print("Starting gui...")
        self.app.mainloop()

    # ---------------------------
    #   attach_settings
    # ---------------------------
    def attach_settings(self, settings) -> None:
        if not settings.GUIEnabled:
            return

        self.settings = settings

    # ---------------------------
    #   attach_chatbot
    # ---------------------------
    def attach_chatbot(self, chatbot) -> None:
        if not self.settings or not self.settings.GUIEnabled:
            return

        self.chatbot = chatbot

    # ---------------------------
    #   attach_woofer
    # ---------------------------
    def attach_woofer(self, woofer) -> None:
        if not self.settings or not self.settings.GUIEnabled:
            return

        self.woofer = woofer

    # ---------------------------
    #   attach_twitch
    # ---------------------------
    def attach_twitch(self, twitch) -> None:
        if not self.settings or not self.settings.GUIEnabled:
            return

        self.twitch = twitch

    # ---------------------------
    #   statusbar
    # ---------------------------
    def statusbar(self, key, status) -> None:
        color = "WHITE"
        tooltip = ""
        if status == CONNECTING:
            color = "ORANGE"
            tooltip = "connecting..."
        elif status == CONNECTED:
            color = "GREEN"
            tooltip = "connected"
        elif status == CONNECTION_FAILED:
            color = "RED"
            tooltip = "connection failed"
        elif status == DISCONNECTED:
            color = "WHITE"
            tooltip = "disconnected"
        elif status == DISABLED:
            color = "GRAY"
            tooltip = "disabled"

        if key == TWITCH:
            self.statusbar_twitch.tooltip.text = "Twitch " + tooltip
            self.statusbar_twitch.config(fg=color)
        elif key == CHATBOT:
            self.statusbar_chatbot.tooltip.text = "Web overlay " + tooltip
            self.statusbar_chatbot.config(fg=color)
        elif key == OVERLAY:
            self.statusbar_overlay.tooltip.text = "Web overlay " + tooltip
            self.statusbar_overlay.config(fg=color)

    # ---------------------------
    #   messagelog_add
    # ---------------------------
    def messagelog_add(self, text: str) -> None:
        self.message_log.insert(END, text)
        self.message_log.yview(END)
