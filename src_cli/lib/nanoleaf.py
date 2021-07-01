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

from json import dumps as json_dumps
from requests import (
    put as requests_put,
    post as requests_post,
    exceptions as requests_exceptions,
)
from lib.helper import portup, ssdp_discovery


# ---------------------------
#   Nanoleaf Handling
# ---------------------------
class Nanoleaf:
    def __init__(self, settings):
        self.settings = settings
        self.enabled = self.settings.NanoleafEnabled
        self.active = False
        self.ip = self.settings.NanoleafIP
        self.token = self.settings.NanoleafToken

        if not self.enabled:
            return

        if self.settings.os == "win":
            from msvcrt import getch
        elif self.settings.os == "lx":
            from getch import getch

        self.settings.log("Initializing nanoleaf...")
        #
        # IP Not set
        #
        if not self.ip or not portup(self.ip, 16021):
            ip_list = []
            discovery_time = 5
            while len(ip_list) == 0:
                self.settings.log("Starting Nanoleaf discovery.")
                ip_list = ssdp_discovery(
                    searchstr="nanoleaf", discovery_time=discovery_time
                )
                if len(ip_list) == 0:
                    self.settings.log("Nanoleaf not found")
                    self.settings.log("Press C to cancel or any key to scan again")
                    if self.settings.os == "win":
                        input_char = getch().decode("utf-8").upper()
                    elif self.settings.os == "lx":
                        input_char = getch().upper()

                    if discovery_time < 20:
                        discovery_time = discovery_time + 5

                    if input_char == "C":
                        return

            self.ip = ip_list[0]
            settings.NanoleafIP = self.ip

        #
        # Token not set
        #
        result = self.put_request("state", {"on": {"value": False}})
        if self.token == "" or result.status_code == 401:
            while not self.auth():
                self.settings.log("Press C to cancel or any key to try again")
                if self.settings.os == "win":
                    input_char = getch().decode("utf-8").upper()
                elif self.settings.os == "lx":
                    input_char = getch().upper()

                if input_char == "C":
                    return

            settings.NanoleafToken = self.token

        self.active = True

    # ---------------------------
    #   scene
    # ---------------------------
    def scene(self, name=None):
        # Check if nanoleaf is active
        if not self.active:
            return

        if not name:
            # Turn nanoleaf off
            data = {"on": {"value": False}}
            result = self.put_request("state", data)
            return result

        # Set nanoleaf scene
        data = {"select": name}
        result = self.put_request("effects", data)
        return result

    # ---------------------------
    #   put_request
    # ---------------------------
    def put_request(self, endpoint, data: dict):
        url = "http://{}:16021/api/v1/{}/{}".format(self.ip, self.token, endpoint)
        try:
            result = requests_put(url, data=json_dumps(data), timeout=1)
        except requests_exceptions.RequestException as e:
            self.settings.log(e)

        if result.status_code == 403:
            self.settings.log("Error 403, Bad request")
        elif result.status_code == 401:
            self.settings.log("Error 401, Not authorized")
        elif result.status_code == 404:
            self.settings.log("Error 404, Resource not found")
        elif result.status_code == 422:
            self.settings.log("Error 422, Unprocessible entity")
        elif result.status_code == 500:
            self.settings.log("Error 500, Internal error")

        return result

    # ---------------------------
    #   auth
    # ---------------------------
    def auth(self):
        self.settings.log("Auth with nanoleaf...")
        # Send API request
        url = "http://{}:16021/api/v1/new".format(self.ip)
        result = requests_post(url)

        # Authorization successful
        if result.status_code == 200:
            self.settings.log("Authorized ok")
            self.token = result.json()["auth_token"]
            return True

        # Authorization requires hardware confirmation
        if result.status_code == 403:
            self.settings.log("Nanoleaf not in discovery mode.")
            self.settings.log(
                "Hold down power button for ~5 seconds until led starts blinking."
            )
            return False
