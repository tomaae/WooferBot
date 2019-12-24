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

import socket
import time
import select
import re
import json
import requests


#---------------------------
#   HUE Handling
#---------------------------
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
            import msvcrt
        elif self.settings.os == 'lx':
            import getch
        
        print("Initializing Philips HUE...")
        #
        # IP Not set
        #
        if not self.ip or not self.portup(self.ip, 80):
            ip_list = []
            discovery_time = 5
            while len(ip_list) == 0:
                ip_list = self.ssdp_discovery(discovery_time)
                if len(ip_list) == 0:
                    print("Philips HUE Bridge not found")
                    print("Press C to cancel or any key to scan again")
                    if self.settings.os == 'win':
                        input_char = msvcrt.getch().decode("utf-8").upper()
                    elif self.settings.os == 'lx':
                        input_char = getch.getch().upper()
                    
                    if discovery_time < 20:
                        discovery_time = discovery_time + 5
                    if input_char == 'C':
                        return
            
            self.ip = ip_list[0]
            settings.HueIP = self.ip
        
        #
        # Token not set
        #
        url = "http://" + self.ip + ":80/api/" + self.token
        result = requests.get(url, data=json.dumps({'devicetype': 'wooferbot'}), timeout=5)
        output_json = result.json()
        if result.status_code != 200 or len(output_json) == 0:
            print("Philips HUE Bridge did not responding correctly")
            return
        
        if isinstance(output_json, list) and 'error' in output_json[0] and 'description' in output_json[0]['error']:
            if output_json[0]['error']['description'] == "unauthorized user" or output_json[0]['error']['description'] == "method, GET, not available for resource, /":
                while not self.auth():
                    print("Press C to cancel or any key to try again")
                    input_char = msvcrt.getch().decode("utf-8").upper()
                    if input_char == 'C':
                        return
                
                settings.HueToken = self.token
        
        url = "http://" + self.ip + ":80/api/" + self.token
        result = requests.get(url, data=json.dumps({'devicetype': 'wooferbot'}), timeout=5)
        output_json = result.json()
        if result.status_code == 200 and 'config' in output_json and 'bridgeid' in output_json['config'] and len(output_json['config']['bridgeid']) > 2:
            self.detect_lights()
            self.active = True
            self.check_mappings()
        
        return
        
    #---------------------------
    #   check_mappings
    #---------------------------
    def check_mappings(self):
        ## Check if hue is active
        if not self.active:
            return
        
        for action in self.settings.PoseMapping:
            if 'Hue' in self.settings.PoseMapping[action]:
                for light in self.settings.PoseMapping[action]['Hue']:
                    if light not in self.lights:
                        print("Error: Philips Hue light \"" + light + "\" defined in PoseMapping \"" + action + "\" has not been detected.")
        
        return
        
    #---------------------------
    #   state
    #---------------------------
    def state(self, device, col="", bri=100):
        ## Check if hue is active
        if not self.active:
            return
        
        ## Check if light has been detected on startup
        if device not in self.lights:
            print("Philips HUE Device \"" + device + "\" does not detected")
            return
        
        data = {}
        if col:
            ## Turn hue light on
            data['on'] = True
            tmp = self.hex_to_hue(col)
            data['hue'] = tmp[0]
            data['sat'] = tmp[1]
        else:
            ## Turn hue light off
            data['on'] = False
        
        if 'bri' in data:
            data['bri'] = round(bri * 2.54)
        
        ## Send API request to Hue Bridge
        url = "http://" + self.ip + ":80/api/" + self.token + "/lights/" + str(self.lights[device]) + "/state"
        requests.put(url, data=json.dumps(data), timeout=5)
        return
        
    #---------------------------
    #   detect_lights
    #---------------------------
    def detect_lights(self):
        url = "http://" + self.ip + ":80/api/" + self.token + "/lights"
        result = requests.get(url, timeout=5)
        
        if result.status_code == 200:
            output_json = result.json()
            
            i = -1
            for items in output_json:
                i = i + 1
                
                if 'error' in items:
                    error_type = output_json[i]['error']['type']
                    if error_type == 1:
                        print("Philips HUE: Unauthorized user")
                        return False
                
                if not output_json[items]['state']['reachable']:
                    continue
                
                if len(output_json[items]['name']) > 0:
                    self.lights[output_json[items]['name']] = items
        
        return
        
    #---------------------------
    #   ssdp_discovery
    #---------------------------
    def ssdp_discovery(self, discovery_time: float = 5):
        devices = []
        
        #
        # Set request
        #
        SSDP_IP = "239.255.255.250"
        SSDP_PORT = 1900
        SSDP_MX = 10
        req = ['M-SEARCH * HTTP/1.1', 'HOST: ' + SSDP_IP + ':' + str(SSDP_PORT), 'MAN: "ssdp:discover"', 'MX: ' + str(SSDP_MX), 'ST: ssdp:all']
        req = '\r\n'.join(req).encode('utf-8')
        
        #
        # Send broadcast
        #
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, SSDP_MX)
        sock.bind((socket.gethostname(), 9090))
        sock.sendto(req, (SSDP_IP, SSDP_PORT))
        sock.setblocking(False)
        
        #
        # Detection loop
        #
        timeout = time.time() + discovery_time
        print("Starting HUE discovery.")
        while time.time() < timeout:
            try:
                ## Get data from socket
                ready = select.select([sock], [], [], 5)
                if ready[0]:
                    response = sock.recv(1024).decode("utf-8")
                    ## Process only a response from Hue Bridge
                    if 'ipbridge' not in response.lower():
                        continue
                    
                    ## Parse IP from location entry
                    ip = ""
                    for line in response.lower().split("\n"):
                        if "location:" in line:
                            ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', line).group()
                            if ip not in devices and (self.is_valid_ipv4_address(ip) or self.is_valid_ipv6_address(ip)):
                                devices.append(ip)
            
            except socket.error as err:
                print("Socket error while discovering SSDP devices!")
                print(err)
                break
        
        sock.close()
        return devices
        
    #---------------------------
    #   auth
    #---------------------------
    def auth(self):
        print("Registering HueBridge...")
        ## Send API request
        data = {'devicetype': 'wooferbot'}
        url = "http://" + self.ip + ":80/api"
        result = requests.post(url, data=json.dumps(data), timeout=5)
        
        if result.status_code == 200:
            output_json = result.json()
            i = -1
            for items in output_json:
                i = i + 1
                ## Authorization requires hardware confirmation
                if 'error' in items:
                    error_type = output_json[i]['error']['type']
                    if error_type == 101:
                        print("Error: Press link button and try again")
                        return False
                
                ## Authorization successful
                if 'success' in items:
                    self.token = output_json[i]['success']['username']
                    print("Authorized successfully")
                    return True
        
        ## General error
        print("Error connecting")
        return False
        
    #---------------------------
    #   is_valid_ipv4_address
    #---------------------------
    def is_valid_ipv4_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True
        
    #---------------------------
    #   is_valid_ipv6_address
    #---------------------------
    def is_valid_ipv6_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True
        
    #---------------------------
    #   portup
    #---------------------------
    def portup(self, ip, port):
        #socket.setdefaulttimeout(0.01)
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if socket_obj.connect_ex((ip, port)) == 0:
            socket_obj.close()
            return True
        socket_obj.close()
        return False
        
    #---------------------------
    #   hex_to_hue
    #---------------------------
    def hex_to_hue(self, h):
        h = h.lstrip('#')
        r = int(h[0:2], 16)
        g = int(h[2:4], 16)
        b = int(h[4:6], 16)
        
        r = r / 255
        g = g / 255
        b = b / 255
        high = max(r, g, b)
        low = min(r, g, b)
        h, s, l = ((high + low) / 2,) * 3
        if max == min:
            h = 0.0
            s = 0.0
        else:
            d = high - low
            s = d / (2 - high - low) if l > 0.5 else d / (high + low)
            h = {
                r: (g - b) / d + (6 if g < b else 0),
                g: (b - r) / d + 2,
                b: (r - g) / d + 4,
            }[high]
            h /= 6
        
        h = round(h * 65535)
        s = round(s * 254)
        return h, s
