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

from yeelight import discover_bulbs, Bulb
from lib.helper import hex_to_rgb


# ---------------------------
#   set_light_name
# ---------------------------
def set_light_name(ip, light_model, light_id):
    print("Name not defined for Yeelight {}, ID: {}".format(light_model, light_id))

    # Identify light for user
    try:
        bulb = Bulb(ip)
        bulb.turn_off()
        bulb.effect = "sudden"
        bulb.turn_on()
        bulb.set_brightness(100)
        bulb.set_rgb(0, 0, 255)
        bulb.effect = "smooth"
        bulb.duration = 10000
        bulb.set_rgb(255, 0, 0)
    except:
        print("Communication failed with Yeelight {}, ID: {}".format(light_model, light_id))
        return ""

    # Get user input for light name
    print("This device will change color from blue to red over 10 seconds.")
    print("Enter name for this device or press enter to skip it:")
    input_char = input()
    if input_char == '':
        try:
            bulb.turn_off()
        except:
            print("Communication failed with Yeelight {}, ID: {}".format(light_model, light_id))
            return ""
        return ""

    # Set light name
    device_name = input_char
    try:
        bulb.set_name(device_name)
    except:
        print("Communication failed with Yeelight {}, ID: {}".format(light_model, light_id))
        return ""

    return device_name


# ---------------------------
#   Yeelight Handling
# ---------------------------
class Yeelight:
    def __init__(self, settings):
        self.settings = settings
        self.enabled = self.settings.YeelightEnabled
        self.active = False
        self.lights = {}

        if not self.enabled:
            return

        if self.settings.os == 'win':
            from msvcrt import getch
        elif self.settings.os == 'lx':
            from getch import getch

        print("Initializing Yeelight...")
        while len(self.lights) == 0:
            self.detect_lights()
            if len(self.lights) == 0:
                print("Yeelight not found")
                print("Press C to cancel or any key to scan again")
                if self.settings.os == 'win':
                    input_char = getch().decode("utf-8").upper()
                elif self.settings.os == 'lx':
                    input_char = getch().upper()
                else:
                    input_char = "C"

                if input_char == 'C':
                    return

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
            if 'Yeelight' in self.settings.PoseMapping[action]:
                for light in self.settings.PoseMapping[action]['Yeelight']:
                    if light not in self.lights:
                        print("Error: Yeelight \"{}\" defined in PoseMapping \"{}\" has not been detected.".format(light, action))

    # ---------------------------
    #   state
    # ---------------------------
    def state(self, device, color="", brightness=100, transition=True, transition_time=1000):
        # Check if yeelight is active
        if not self.active:
            return

        # Check if light has been detected on startup
        if device not in self.lights:
            print("Yeelight Device \"{}\" does not detected".format(device))
            return

        # Set light transition transition
        try:
            if transition:
                self.lights[device].transition = "smooth"
                self.lights[device].duration = transition_time
            else:
                self.lights[device].effect = "sudden"

        except:
            print("Communication failed with Yeelight {}, light disabled".format(device))
            del self.lights[device]
            return

        # Turn light off
        if not color:
            try:
                self.lights[device].turn_off()
            except:
                print("Communication failed with Yeelight {}, light disabled".format(device))
                del self.lights[device]
                return
            return

        if color:
            # Turn light on
            try:
                self.lights[device].turn_on()
                tmp = hex_to_rgb(color)
                self.lights[device].set_brightness(brightness)
                self.lights[device].set_rgb(tmp[0], tmp[1], tmp[2])
            except:
                print("Communication failed with Yeelight {}, light disabled".format(device))
                del self.lights[device]
                return
        else:
            try:
                self.lights[device].set_brightness(brightness)
            except:
                print("Communication failed with Yeelight {}, light disabled".format(device))
                del self.lights[device]
                return

    # ---------------------------
    #   detect_lights
    # ---------------------------
    def detect_lights(self):
        discovered_lights = discover_bulbs()

        for light in discovered_lights:
            # Check light compatibility
            if 'capabilities' in light and 'model' in light['capabilities'] \
                    and light['capabilities']['model'] not in ['mono', 'color', 'stripe', 'bslamp', 'ceiling']:
                continue

            # Check reply consistency
            if 'ip' not in light:
                continue

            # Set device name
            device_name = light['capabilities']['name']

            # Check if device has a name
            if device_name == "":
                device_name = set_light_name(light['ip'], light['capabilities']['model'],
                                             light['capabilities']['id'])
                if device_name == "":
                    continue

            # Add usable light to list
            self.lights[device_name] = Bulb(light['ip'])

            # Turn off light
            try:
                self.lights[device_name].turn_off()
            except:
                print("Communication failed with Yeelight {}, light disabled".format(device_name))
                del self.lights[device_name]
                continue
