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
from tkinter import messagebox
from tkinter import colorchooser
from tkinter import font
import webbrowser
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
        self.app.geometry("800x450")
        self.app.resizable(width=False, height=False)
        self.app.title("Wooferbot")
        self.app.iconbitmap("wooferbot.ico")

        # ---------------------------
        # Tabs
        # ---------------------------
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)
        self.tab_control = ttk.Notebook(self.app)
        self.tab_control.grid(row=0, column=0, columnspan=4, sticky="NSEW")
        tab1 = Frame(self.tab_control)

        self.tab_control.add(tab1, text="Log")

        # ---------------------------
        # Status bar
        # ---------------------------
        self.statusbar_frame = Frame(self.app)
        self.statusbar_frame.grid(row=1, column=0, sticky=NSEW)
        self.statusbar_frame.grid_columnconfigure(3, weight=1)

        self.statusbar_twitch = Label(self.statusbar_frame, text="Twitch", bd=1, fg="GRAY", width=10, relief=SUNKEN,
                                      anchor=W, padx=1, pady=1)
        self.statusbar_twitch.tooltip = Hovertip(self.statusbar_twitch, "Twitch disabled", hover_delay=100)
        self.statusbar_twitch.grid(row=0, column=0, sticky=W)
        self.statusbar_chatbot = Label(self.statusbar_frame, text="Chatbot", bd=1, fg="GRAY", width=10, relief=SUNKEN,
                                       anchor=W, padx=1, pady=1)
        self.statusbar_chatbot.tooltip = Hovertip(self.statusbar_chatbot, "Chatbot disabled", hover_delay=100)
        self.statusbar_chatbot.grid(row=0, column=1, sticky=W)
        self.statusbar_overlay = Label(self.statusbar_frame, text="Overlay", bd=1, fg="GRAY", width=10, relief=SUNKEN,
                                       anchor=W, padx=1, pady=1)
        self.statusbar_overlay.tooltip = Hovertip(self.statusbar_overlay, "Overlay disabled", hover_delay=100)
        self.statusbar_overlay.grid(row=0, column=2, sticky=W)
        Label(self.statusbar_frame, bd=1, relief=SUNKEN, anchor=W, padx=1, pady=1).grid(row=0, column=3, sticky=EW)

        # ---------------------------
        # [Tab] Log
        # ---------------------------
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
        self.frame_control = LabelFrame(tab1, text="Controls", padx=5, pady=5)
        self.frame_control.grid(row=0, column=1, padx=2, pady=2, sticky=["N", "S", "E"])

        def cmd_clear_notifications():
            self.woofer.queue.clear()

        def cmd_pause_notifications():
            self.woofer.queuePaused = True
            self.pause_notifications['text'] = "Resume notifications"
            self.pause_notifications['command'] = cmd_resume_notifications

        def cmd_resume_notifications():
            self.woofer.queuePaused = False
            self.pause_notifications['text'] = "Pause notifications"
            self.pause_notifications['command'] = cmd_pause_notifications

        def cmd_reconnect_twitch_accounts():
            if hasattr(self.twitch, 'connected') and self.twitch.connected:
                self.twitch.disconnect()
            if hasattr(self.chatbot, 'connected') and self.chatbot.connected:
                self.chatbot.disconnect()

        clear_notifications = Button(self.frame_control, text="Clear notifications", width=15,
                                     command=cmd_clear_notifications)
        clear_notifications.tooltip = Hovertip(clear_notifications, "Clear all waiting notifications", hover_delay=100)
        clear_notifications.grid(row=0, column=0, sticky=E)
        self.pause_notifications = Button(self.frame_control, text="Pause notifications", width=15,
                                          command=cmd_pause_notifications)
        self.pause_notifications.tooltip = Hovertip(self.pause_notifications, "Pause notifications", hover_delay=100)
        self.pause_notifications.grid(row=1, column=0, sticky=E)
        reconnect_twitch = Button(self.frame_control, text="Reconnect Twitch", width=15,
                                  command=cmd_reconnect_twitch_accounts)
        reconnect_twitch.tooltip = Hovertip(reconnect_twitch, "Reconnect all connections to Twitch", hover_delay=100)
        reconnect_twitch.grid(row=2, column=0, sticky=E)

        self.app.update_idletasks()
        self.app.update()

    # ---------------------------
    #   attach_settings
    # ---------------------------
    def attach_settings(self, settings) -> None:
        if not settings.GUIEnabled:
            return

        self.settings = settings

        # ---------------------------
        # Tabs
        # ---------------------------
        tab2 = Frame(self.tab_control)
        tab3 = Frame(self.tab_control)
        tab4 = Frame(self.tab_control)
        tab5 = Frame(self.tab_control)

        self.tab_control.add(tab2, text="Login")
        self.tab_control.add(tab3, text="General")
        self.tab_control.add(tab4, text="Mascot")
        self.tab_control.add(tab5, text="Hardware")

        # ---------------------------
        # [Tab] Login
        # ---------------------------
        def cmd_reconnect_broadcaster():
            if hasattr(self.twitch, 'connected') and self.twitch.connected:
                self.twitch.disconnect()

        def cmd_reconnect_chatbot():
            if hasattr(self.chatbot, 'connected') and self.chatbot.connected:
                self.chatbot.disconnect()

        def cmd_save_broadcaster():
            tmp_name = broadcaster_name_var.get()
            if len(tmp_name) < 1:
                messagebox.showerror(title="Error", message="Name empty")
                return 1

            tmp_oauth = broadcaster_oauth_var.get()
            if tmp_oauth.find('oauth:') != 0:
                messagebox.showerror(title="Error", message="OAUTH is invalid")
                return 1

            self.settings.TwitchChannel = tmp_name
            self.settings.TwitchOAUTH = tmp_oauth
            self.settings.save()

        def cmd_save_chatbot():
            tmp_name = broadcaster_name_var.get()
            if len(tmp_name) < 1:
                messagebox.showerror(title="Error", message="Name empty")
                return 1

            tmp_oauth = broadcaster_oauth.get()
            if tmp_oauth.find('oauth:') != 0:
                messagebox.showerror(title="Error", message="OAUTH is invalid")
                return 1

            self.settings.TwitchBotChannel = tmp_name
            self.settings.TwitchBotOAUTH = tmp_oauth
            self.settings.save()

        # [Tab] Login - Broadcaster
        frame_twitch = LabelFrame(tab2, text="Twitch account", padx=5, pady=5)
        frame_twitch.grid(row=0, column=0, padx=2, pady=2, sticky=["NSWE"])
        tab2.grid_rowconfigure(0, weight=1)
        tab2.grid_columnconfigure([0, 1], weight=1)

        Label(frame_twitch, text="Channel name").grid(row=0, column=0, sticky=E)
        Label(frame_twitch, text="OAUTH").grid(row=1, column=0, sticky=E)

        broadcaster_name_var = tk.StringVar()
        broadcaster_name_var.set(self.settings.TwitchChannel)
        broadcaster_name = Entry(frame_twitch, textvariable=broadcaster_name_var, width=30)
        broadcaster_name.grid(row=0, column=1)

        broadcaster_oauth_var = tk.StringVar()
        broadcaster_oauth_var.set(self.settings.TwitchOAUTH)
        broadcaster_oauth = Entry(frame_twitch, textvariable=broadcaster_oauth_var, show='*', width=30)
        broadcaster_oauth.grid(row=1, column=1)

        broadcaster_save = Button(frame_twitch, text="Save", width=15, command=cmd_save_broadcaster)
        broadcaster_save.grid(row=2, column=1, sticky=E)

        broadcaster_reconnect = Button(frame_twitch, text="Reconnect Twitch", width=15,
                                       command=cmd_reconnect_broadcaster)
        broadcaster_reconnect.tooltip = Hovertip(frame_twitch, "Reconnect broadcaster twitch account", hover_delay=100)
        broadcaster_reconnect.grid(row=10, column=1, sticky=E, pady=15)

        # [Tab] Login - chatbot
        frame_chatbotbot = LabelFrame(tab2, text="Chatbot account", padx=5, pady=5)
        frame_chatbotbot.grid(row=0, column=1, padx=2, pady=2, sticky=["NSWE"])

        Label(frame_chatbotbot, text="Chatbot name").grid(row=0, column=0, sticky=E)
        Label(frame_chatbotbot, text="OAUTH").grid(row=1, column=0, sticky=E)

        chatbot_name_var = tk.StringVar()
        chatbot_name_var.set(self.settings.TwitchBotChannel)
        chatbot_name = Entry(frame_chatbotbot, textvariable=chatbot_name_var, width=30)
        chatbot_name.grid(row=0, column=1)

        chatbot_oauth_var = tk.StringVar()
        chatbot_oauth_var.set(self.settings.TwitchBotOAUTH)
        chatbot_oauth = Entry(frame_chatbotbot, textvariable=chatbot_oauth_var, show='*', width=30)
        chatbot_oauth.grid(row=1, column=1)

        chatbot_save = Button(frame_chatbotbot, text="Save", width=15, command=cmd_save_chatbot)
        chatbot_save.grid(row=2, column=1, sticky=E)

        chatbot_reconnect = Button(frame_chatbotbot, text="Reconnect Chatbot", width=15, command=cmd_reconnect_chatbot)
        chatbot_reconnect.tooltip = Hovertip(frame_chatbotbot, "Reconnect chatbot twitch account", hover_delay=100)
        chatbot_reconnect.grid(row=10, column=1, sticky=E, pady=15)

        # ---------------------------
        # [Tab] Mascot
        # ---------------------------
        frame_mascot = LabelFrame(tab4, text="Speech bubble styles", padx=5, pady=5)
        frame_mascot.grid(row=0, column=0, padx=2, pady=2, sticky=["NSWE"])
        tab2.grid_rowconfigure(0, weight=1)
        tab2.grid_columnconfigure([0, 1], weight=1)

        def cmd_colorpicker(var, field):
            color_code = colorchooser.askcolor(title="Choose color")[1]
            var.set(color_code)
            field.configure(bg=str(var.get()))

        Label(frame_mascot, text="Background Color").grid(row=0, column=0, sticky=E)
        styles_backgroundcolor_var = tk.StringVar()
        styles_backgroundcolor_var.set(self.settings.Styles["BackgroundColor"])
        styles_backgroundcolor = Entry(frame_mascot, textvariable=styles_backgroundcolor_var, width=30)
        styles_backgroundcolor.grid(row=0, column=1)
        styles_backgroundcolor.configure(bg=str(styles_backgroundcolor_var.get()))
        Button(frame_mascot, text="Pick",
               command=lambda: cmd_colorpicker(styles_backgroundcolor_var, styles_backgroundcolor)).grid(row=0,
                                                                                                         column=2,
                                                                                                         sticky=E)

        Label(frame_mascot, text="Border Color").grid(row=1, column=0, sticky=E)
        styles_bordercolor_var = tk.StringVar()
        styles_bordercolor_var.set(self.settings.Styles["BorderColor"])
        styles_bordercolor = Entry(frame_mascot, textvariable=styles_bordercolor_var, width=30)
        styles_bordercolor.grid(row=1, column=1)
        styles_bordercolor.configure(bg=str(styles_bordercolor_var.get()))
        Button(frame_mascot, text="Pick",
               command=lambda: cmd_colorpicker(styles_bordercolor_var, styles_bordercolor)).grid(row=1,
                                                                                                 column=2,
                                                                                                 sticky=E)

        Label(frame_mascot, text="Border Width").grid(row=2, column=0, sticky=E)
        styles_borderwidth_var = IntVar()
        styles_borderwidth_var.set(self.settings.Styles["BorderWidth"])
        styles_borderwidth = Spinbox(frame_mascot, textvariable=styles_borderwidth_var, width=28, from_=0, to=20)
        styles_borderwidth.grid(row=2, column=1)

        Label(frame_mascot, text="Border Radius").grid(row=3, column=0, sticky=E)
        styles_borderradius_var = IntVar()
        styles_borderradius_var.set(self.settings.Styles["BorderRadius"])
        styles_borderradius = Spinbox(frame_mascot, textvariable=styles_borderradius_var, width=28, from_=0, to=50)
        styles_borderradius.grid(row=3, column=1)

        Label(frame_mascot, text="Border Stroke Color").grid(row=4, column=0, sticky=E)
        styles_borderstrokecolor_var = tk.StringVar()
        styles_borderstrokecolor_var.set(self.settings.Styles["BorderStrokeColor"])
        styles_borderstrokecolor = Entry(frame_mascot, textvariable=styles_borderstrokecolor_var, width=30)
        styles_borderstrokecolor.grid(row=4, column=1)
        styles_borderstrokecolor.configure(bg=str(styles_borderstrokecolor_var.get()))
        Button(frame_mascot, text="Pick",
               command=lambda: cmd_colorpicker(styles_borderstrokecolor_var, styles_borderstrokecolor)).grid(row=4,
                                                                                                             column=2,
                                                                                                             sticky=E)

        Label(frame_mascot, text="Text Font Family").grid(row=5, column=0, sticky=E)
        font_list = []
        i_n = -1
        for i in font.families():
            i_n = i_n + 1
            font_list.append(i)
            if i == self.settings.Styles["TextFontFamily"]:
                font_list_textfontfamily = i_n

        styles_textfontfamily = ttk.Combobox(frame_mascot, values=font_list, width=26)
        styles_textfontfamily.grid(row=5, column=1, sticky=W)
        styles_textfontfamily.current(font_list_textfontfamily)

        Label(frame_mascot, text="Text Size").grid(row=6, column=0, sticky=E)
        styles_textsize_var = IntVar()
        styles_textsize_var.set(self.settings.Styles["TextSize"])
        styles_textsize = Spinbox(frame_mascot, textvariable=styles_textsize_var, width=28, from_=8, to=60)
        styles_textsize.grid(row=6, column=1)

        Label(frame_mascot, text="Text Weight").grid(row=7, column=0, sticky=E)
        styles_textweight_var = IntVar()
        styles_textweight_var.set(self.settings.Styles["TextWeight"])
        styles_textweight = Spinbox(frame_mascot, textvariable=styles_textweight_var, width=28, from_=1, to=1000)
        styles_textweight.grid(row=7, column=1)

        Label(frame_mascot, text="Text Color").grid(row=8, column=0, sticky=E)
        styles_textcolor_var = tk.StringVar()
        styles_textcolor_var.set(self.settings.Styles["TextColor"])
        styles_textcolor = Entry(frame_mascot, textvariable=styles_textcolor_var, width=30)
        styles_textcolor.grid(row=8, column=1)
        styles_textcolor.configure(bg=str(styles_textcolor_var.get()))
        Button(frame_mascot, text="Pick",
               command=lambda: cmd_colorpicker(styles_textcolor_var, styles_textcolor)).grid(row=8,
                                                                                             column=2,
                                                                                             sticky=E)

        Label(frame_mascot, text="Highlight Text Size").grid(row=9, column=0, sticky=E)
        styles_highlighttextsize_var = IntVar()
        styles_highlighttextsize_var.set(self.settings.Styles["HighlightTextSize"])
        styles_highlighttextsize = Spinbox(frame_mascot, textvariable=styles_highlighttextsize_var, width=28, from_=8,
                                           to=60)
        styles_highlighttextsize.grid(row=9, column=1)

        Label(frame_mascot, text="Highlight Text Spacing").grid(row=10, column=0, sticky=E)
        styles_highlighttextspacing_var = IntVar()
        styles_highlighttextspacing_var.set(self.settings.Styles["HighlightTextSpacing"])
        styles_highlighttextspacing = Spinbox(frame_mascot, textvariable=styles_highlighttextspacing_var, width=28,
                                              from_=0, to=10)
        styles_highlighttextspacing.grid(row=10, column=1)

        Label(frame_mascot, text="Highlight Text Color").grid(row=11, column=0, sticky=E)
        highlighttextcolor_var = tk.StringVar()
        highlighttextcolor_var.set(self.settings.Styles["HighlightTextColor"])
        highlighttextcolor = Entry(frame_mascot, textvariable=highlighttextcolor_var, width=30)
        highlighttextcolor.grid(row=11, column=1)
        highlighttextcolor.configure(bg=str(highlighttextcolor_var.get()))
        Button(frame_mascot, text="Pick",
               command=lambda: cmd_colorpicker(highlighttextcolor_var, highlighttextcolor)).grid(row=11,
                                                                                                 column=2,
                                                                                                 sticky=E)

        Label(frame_mascot, text="Highlight Text Stroke Color").grid(row=12, column=0, sticky=E)
        highlighttextstrokecolor_var = tk.StringVar()
        highlighttextstrokecolor_var.set(self.settings.Styles["HighlightTextStrokeColor"])
        highlighttextstrokecolor = Entry(frame_mascot, textvariable=highlighttextstrokecolor_var, width=30)
        highlighttextstrokecolor.grid(row=12, column=1)
        highlighttextstrokecolor.configure(bg=str(highlighttextstrokecolor_var.get()))
        Button(frame_mascot, text="Pick",
               command=lambda: cmd_colorpicker(highlighttextstrokecolor_var, highlighttextstrokecolor)).grid(row=12,
                                                                                                             column=2,
                                                                                                             sticky=E)

        Label(frame_mascot, text="Highlight Text Shadow Color").grid(row=13, column=0, sticky=E)
        highlighttextshadowcolor_var = tk.StringVar()
        highlighttextshadowcolor_var.set(self.settings.Styles["HighlightTextShadowColor"])
        highlighttextshadowcolor = Entry(frame_mascot, textvariable=highlighttextshadowcolor_var, width=30)
        highlighttextshadowcolor.grid(row=13, column=1)
        highlighttextshadowcolor.configure(bg=str(highlighttextshadowcolor_var.get()))
        Button(frame_mascot, text="Pick",
               command=lambda: cmd_colorpicker(highlighttextshadowcolor_var, highlighttextshadowcolor)).grid(row=13,
                                                                                                             column=2,
                                                                                                             sticky=E)

        Label(frame_mascot, text="Highlight Text Shadow Offset").grid(row=14, column=0, sticky=E)
        styles_highlighttextshadowoffset_var = IntVar()
        styles_highlighttextshadowoffset_var.set(self.settings.Styles["HighlightTextShadowOffset"])
        styles_highlighttextshadowoffset = Spinbox(frame_mascot, textvariable=styles_highlighttextshadowoffset_var, width=28, from_=0, to=20)
        styles_highlighttextshadowoffset.grid(row=14, column=1)

    # ---------------------------
    #   start
    # ---------------------------
    def start(self) -> None:
        print("Starting gui...")
        self.app.mainloop()

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
