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

from os import path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ---------------------------
#   _WatchdogCustomHandler
# ---------------------------
class _WatchdogCustomHandler(FileSystemEventHandler):
    def __init__(self, settings, woofer, watchdog_name):
        self.settings = settings
        self.woofer = woofer
        self.filename = ""
        self.watchdog_name = watchdog_name

        for action in self.settings.Watchdog:
            if action['Name'] != self.watchdog_name:
                continue

            self.filename = action['Filename']

    # ---------------------------
    #   on_created
    # ---------------------------
    def on_created(self, event):
        self._check_modification(event.src_path)

    # ---------------------------
    #   on_modified
    # ---------------------------
    def on_modified(self, event):
        self._check_modification(event.src_path)

    # ---------------------------
    #   _check_modification
    # ---------------------------
    def _check_modification(self, filename):
        if self.filename == filename:
            for action in self.settings.Watchdog:
                if action['Name'] == self.watchdog_name:
                    f = open(self.filename, "r")

                    if 'Command' in action:
                        self.woofer.woofer_commands({
                            "command": action['Command'],
                            "broadcaster": 1,
                            "sender": action['Name'],
                            "display-name": action['Name'],
                            "custom-tag": 'watchdog'
                        })
                    else:
                        self.woofer.woofer_addtoqueue({
                            "image": action['Image'],
                            "message": action['Message'] + f.read(),
                            "sender": action['Name'],
                            "id": "watchdog"
                        })


# ---------------------------
#   Watchdog
# ---------------------------
class Watchdog:
    def __init__(self, settings, woofer):
        self.settings = settings
        self.woofer = woofer
        self.watchdogs = {}

        for action in self.settings.Watchdog:
            if not action['Enabled']:
                continue

            filepath, filename = path.split(action['Filename'])
            self.watchdogs[action['Name']] = Observer()
            self.watchdogs[action['Name']].schedule(_WatchdogCustomHandler(settings, woofer, action['Name']), filepath,
                                                    recursive=False)
            self.watchdogs[action['Name']].start()

    # ---------------------------
    #   stop
    # ---------------------------
    def stop(self):
        for action in self.watchdogs:
            action.stop()

        for action in self.watchdogs:
            action.join()
