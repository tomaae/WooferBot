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

from json import dumps as json_dumps
from requests import get as requests_get, put as requests_put, post as requests_post
from lib.helper import ssdp_discovery, hex_to_hue, portup


# ---------------------------
#   HUE Handling
# ---------------------------
class Hue:
    def __init__(self, settings):
        self.settings = settings
        self.enabled = self.settings.HueEnabled
        self.active = False
        self.ip = self.settings.HueIP
        self.token = self.settings.HueToken
        self.lights = {}

        if not self.enabled:
            return

        if self.settings.os == 'win':
            from msvcrt import getch
        elif self.settings.os == 'lx':
            from getch import getch

        print("Initializing Philips HUE...")
        #
        # IP Not set
        #
        if not self.ip or not portup(self.ip, 80):
            self.ip = self.detect_hue()
            settings.HueIP = self.ip

        #
        # Token not set
        #
        url = "http://{}:80/api/{}".format(self.ip, self.token)
        result = requests_get(url, data=json_dumps({'devicetype': 'wooferbot'}), timeout=5)
        output_json = result.json()
        if result.status_code != 200 or len(output_json) == 0:
            print("Philips HUE Bridge did not responding correctly")
            return

        if isinstance(output_json, list) and 'error' in output_json[0] and \
                'description' in output_json[0]['error'] and \
                (output_json[0]['error']['description'] == "unauthorized user"
                 or output_json[0]['error']['description'] == "method, GET, not available for resource, /"):
            while not self.auth():
                print("Press C to cancel or any key to try again")
                if self.settings.os == 'win':
                    input_char = getch().decode("utf-8").upper()
                elif self.settings.os == 'lx':
                    input_char = getch().upper()

                if input_char == 'C':
                    return

            settings.HueToken = self.token

        url = "http://{}:80/api/{}".format(self.ip, self.token)
        result = requests_get(url, data=json_dumps({'devicetype': 'wooferbot'}), timeout=5)
        output_json = result.json()
        if result.status_code == 200 and 'config' in output_json and 'bridgeid' in output_json['config'] and len(
                output_json['config']['bridgeid']) > 2:
            self.detect_lights()
            self.active = True
            self.check_mappings()

    # ---------------------------
    #   check_mappings
    # ---------------------------
    def check_mappings(self):
        # Check if hue is active
        if not self.active:
            return

        for action in self.settings.PoseMapping:
            if 'Hue' in self.settings.PoseMapping[action]:
                for light in self.settings.PoseMapping[action]['Hue']:
                    if light not in self.lights:
                        print(
                            "Error: Hue light \"{}\" defined in PoseMapping \"{}\" has not been detected.".format(
                                light, action))

    # ---------------------------
    #   state
    # ---------------------------
    def state(self, device, col="", bri=100):
        # Check if hue is active
        if not self.active:
            return

        # Check if light has been detected on startup
        if device not in self.lights:
            print("Philips HUE Device \"{}\" does not detected".format(device))
            return

        data = {}
        if col:
            # Turn hue light on
            data['on'] = True
            tmp = hex_to_hue(col)
            data['hue'] = tmp[0]
            data['sat'] = tmp[1]
        else:
            # Turn hue light off
            data['on'] = False

        if 'bri' in data:
            data['bri'] = round(bri * 2.54)

        # Send API request to Hue Bridge
        url = "http://{}:80/api/{}/lights/{}/state".format(self.ip, self.token, str(self.lights[device]))
        requests_put(url, data=json_dumps(data), timeout=5)

    # ---------------------------
    #   detect_lights
    # ---------------------------
    def detect_lights(self):
        url = "http://{}:80/api/{}/lights".format(self.ip, self.token)
        result = requests_get(url, timeout=5)

        if result.status_code == 200:
            output_json = result.json()

            i = -1
            for items in output_json:
                i = i + 1
                if 'error' in items and output_json[i]['error']['type'] == 1:
                    print("Philips HUE: Unauthorized user")
                    return False

                if not output_json[items]['state']['reachable']:
                    continue

                if len(output_json[items]['name']) > 0:
                    self.lights[output_json[items]['name']] = items

    # ---------------------------
    #   auth
    # ---------------------------
    def auth(self):
        print("Registering HueBridge...")
        # Send API request
        data = {'devicetype': 'wooferbot'}
        url = "http://{}:80/api".format(self.ip)
        result = requests_post(url, data=json_dumps(data), timeout=5)

        if result.status_code == 200:
            output_json = result.json()
            i = -1
            for items in output_json:
                i = i + 1
                # Authorization requires hardware confirmation
                if 'error' in items:
                    error_type = output_json[i]['error']['type']
                    if error_type == 101:
                        print("Error: Press link button and try again")
                        return False

                # Authorization successful
                if 'success' in items:
                    self.token = output_json[i]['success']['username']
                    print("Authorized successfully")
                    return True

        # General error
        print("Error connecting")
        return False

    # ---------------------------
    #   detect_hue
    # ---------------------------
    def detect_hue(self):
        if self.settings.os == 'win':
            from msvcrt import getch
        elif self.settings.os == 'lx':
            from getch import getch

        ip_list = []
        discovery_time = 5
        while len(ip_list) == 0:
            print("Starting Hue Bridge discovery.")
            ip_list = ssdp_discovery(searchstr="ipbridge", discovery_time=discovery_time)
            if len(ip_list) == 0:
                print("Philips HUE Bridge not found")
                print("Press C to cancel or any key to scan again")
                if self.settings.os == 'win':
                    input_char = getch().decode("utf-8").upper()
                elif self.settings.os == 'lx':
                    input_char = getch().upper()

                if discovery_time < 20:
                    discovery_time = discovery_time + 5

                if input_char == 'C':
                    return

        return ip_list[0]
