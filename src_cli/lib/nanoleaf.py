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

        if self.settings.os == 'win':
            from msvcrt import getch
        elif self.settings.os == 'lx':
            from getch import getch

        print("Initializing nanoleaf...")
        #
        # IP Not set
        #
        if not self.ip or not self.portup(self.ip, 16021):
            ip_list = []
            discovery_time = 5
            while len(ip_list) == 0:
                ip_list = self.ssdp_discovery(discovery_time)
                if len(ip_list) == 0:
                    print("Nanoleaf not found")
                    print("Press C to cancel or any key to scan again")
                    if self.settings.os == 'win':
                        input_char = getch().decode("utf-8").upper()
                    elif self.settings.os == 'lx':
                        input_char = getch().upper()

                    if discovery_time < 20:
                        discovery_time = discovery_time + 5

                    if input_char == 'C':
                        return

            self.ip = ip_list[0]
            settings.NanoleafIP = self.ip

        #
        # Token not set
        #
        result = self.put_request("state", {'on': {'value': False}})
        if self.token == "" or result.status_code == 401:
            while not self.auth():
                print("Press C to cancel or any key to try again")
                if self.settings.os == 'win':
                    input_char = getch().decode("utf-8").upper()
                elif self.settings.os == 'lx':
                    input_char = getch().upper()

                if input_char == 'C':
                    return

            settings.NanoleafToken = self.token

        self.active = True

    # ---------------------------
    #   ssdp_discovery
    # ---------------------------
    def ssdp_discovery(self, discovery_time: float = 5):
        devices = []

        #
        # Set request
        #
        ssdp_ip = "239.255.255.250"
        ssdp_port = 1900
        ssdp_mx = 10
        req = ['M-SEARCH * HTTP/1.1', 'HOST: ' + ssdp_ip + ':' + str(ssdp_port), 'MAN: "ssdp:discover"',
               'MX: ' + str(ssdp_mx), 'ST: ssdp:all']
        req = '\r\n'.join(req).encode('utf-8')

        #
        # Send broadcast
        #
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ssdp_mx)
        sock.bind((socket.gethostname(), 9090))
        sock.sendto(req, (ssdp_ip, ssdp_port))
        sock.setblocking(False)

        #
        # Detection loop
        #
        timeout = time.time() + discovery_time
        print("Starting Nanoleaf discovery.")
        while time.time() < timeout:
            try:
                # Get data from socket
                ready = select.select([sock], [], [], 5)
                if not ready[0]:
                    continue

                response = sock.recv(1024).decode("utf-8")
                # Process only a response from Nanoleaf
                if 'nanoleaf' not in response.lower():
                    continue

                # Parse IP from location entry
                for line in response.lower().split("\n"):
                    if "location:" in line:
                        ip = re.search(r'[0-9]+(?:\.[0-9]+){3}', line).group()
                        if ip not in devices and self.is_valid_ip_address(ip):
                            devices.append(ip)

            except socket.error as err:
                print("Socket error while discovering SSDP devices!")
                print(err)
                break

        sock.close()
        return devices

    # ---------------------------
    #   is_valid_ip_address
    # ---------------------------
    def is_valid_ip_address(self, ip):
        if self.is_valid_ipv4_address(ip) or self.is_valid_ipv6_address(ip):
            return True
        return False

    # ---------------------------
    #   is_valid_ipv4_address
    # ---------------------------
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

    # ---------------------------
    #   is_valid_ipv6_address
    # ---------------------------
    def is_valid_ipv6_address(self, address):
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True

    # ---------------------------
    #   scene
    # ---------------------------
    def scene(self, name=None):
        # Check if nanoleaf is active
        if not self.active:
            return

        if not name:
            # Turn nanoleaf off
            data = {'on': {'value': False}}
            result = self.put_request("state", data)
            return result

        # Set nanoleaf scene
        data = {'select': name}
        result = self.put_request("effects", data)
        return result

    # ---------------------------
    #   put_request
    # ---------------------------
    def put_request(self, endpoint, data: dict):
        url = "http://{}:16021/api/v1/{}/{}".format(self.ip, self.token, endpoint)
        try:
            result = requests.put(url, data=json.dumps(data), timeout=1)
        except requests.exceptions.RequestException as e:
            print(e)

        if result.status_code == 403:
            print("Error 403, Bad request")
        elif result.status_code == 401:
            print("Error 401, Not authorized")
        elif result.status_code == 404:
            print("Error 404, Resource not found")
        elif result.status_code == 422:
            print("Error 422, Unprocessible entity")
        elif result.status_code == 500:
            print("Error 500, Internal error")

        return result

    # ---------------------------
    #   auth
    # ---------------------------
    def auth(self):
        print("Auth with nanoleaf...")
        # Send API request
        url = "http://{}:16021/api/v1/new".format(self.ip)
        result = requests.post(url)

        # Authorization successful
        if result.status_code == 200:
            print("Authorized ok")
            self.token = result.json()['auth_token']
            return True

        # Authorization requires hardware confirmation
        if result.status_code == 403:
            print("Nanoleaf not in discovery mode.")
            print("Hold down power button for ~5 seconds until led starts blinking.")
            return False

    # ---------------------------
    #   portup
    # ---------------------------
    def portup(self, ip, port):
        # socket.setdefaulttimeout(0.01)
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if socket_obj.connect_ex((ip, port)) == 0:
            socket_obj.close()
            return True
        socket_obj.close()
        return False
