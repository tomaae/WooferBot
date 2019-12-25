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
from socket import socket, gethostname, inet_aton, inet_pton, error as socket_error, AF_INET, SOCK_STREAM, SOCK_DGRAM, IPPROTO_IP, IP_MULTICAST_TTL, AF_INET6
from re import search as re_search
from select import select
from time import time


# ---------------------------
#   hex_to_rgb
# ---------------------------
def hex_to_rgb(h):
    h = h.lstrip('#')
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)

    return r, g, b


# ---------------------------
#   hex_to_hue
# ---------------------------
def hex_to_hue(h):
    h = h.lstrip('#')
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)

    r = r / 255
    g = g / 255
    b = b / 255
    high = max(r, g, b)
    low = min(r, g, b)
    h, s, x = ((high + low) / 2,) * 3
    if max == min:
        h = 0.0
        s = 0.0
    else:
        d = high - low
        s = d / (2 - high - low) if x > 0.5 else d / (high + low)
        h = {
            r: (g - b) / d + (6 if g < b else 0),
            g: (b - r) / d + 2,
            b: (r - g) / d + 4,
        }[high]
        h /= 6

    h = round(h * 65535)
    s = round(s * 254)
    return h, s


# ---------------------------
#   portup
# ---------------------------
def portup(ip, port):
    # socket.setdefaulttimeout(0.01)
    socket_obj = socket(AF_INET, SOCK_STREAM)
    if socket_obj.connect_ex((ip, port)) == 0:
        socket_obj.close()
        return True
    socket_obj.close()
    return False


# ---------------------------
#   ssdp_discovery
# ---------------------------
def ssdp_discovery(searchstr="", discovery_time: float = 5):
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
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, ssdp_mx)
    sock.bind((gethostname(), 9090))
    sock.sendto(req, (ssdp_ip, ssdp_port))
    sock.setblocking(False)

    #
    # Detection loop
    #
    timeout = time() + discovery_time
    while time() < timeout:
        try:
            # Get data from socket
            ready = select([sock], [], [], 5)
            if not ready[0]:
                continue

            response = sock.recv(1024).decode("utf-8")
            # Process only a response from Nanoleaf
            if searchstr not in response.lower():
                continue

            # Parse IP from location entry
            for line in response.lower().split("\n"):
                if "location:" in line:
                    ip = re_search(r'[0-9]+(?:\.[0-9]+){3}', line).group()
                    if ip not in devices and is_valid_ip_address(ip):
                        devices.append(ip)

        except socket_error as err:
            print("Socket error while discovering SSDP devices!")
            print(err)
            break

    sock.close()
    return devices


# ---------------------------
#   is_valid_ip_address
# ---------------------------
def is_valid_ip_address(ip):
    if is_valid_ipv4_address(ip) or is_valid_ipv6_address(ip):
        return True
    return False


# ---------------------------
#   is_valid_ipv4_address
# ---------------------------
def is_valid_ipv4_address(address):
    try:
        inet_pton(AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            inet_aton(address)
        except socket_error:
            return False
        return address.count('.') == 3
    except socket_error:  # not a valid address
        return False
    return True


# ---------------------------
#   is_valid_ipv6_address
# ---------------------------
def is_valid_ipv6_address(address):
    try:
        inet_pton(AF_INET6, address)
    except socket_error:  # not a valid address
        return False
    return True


# ---------------------------
#   get_var_default
# ---------------------------
def get_var_default(vartype):
    if isinstance(vartype, str):
        tmp = ""
    elif type(vartype) == int or type(vartype) == float:
        tmp = 0
    elif type(vartype) == bool:
        tmp = False
    elif type(vartype) == list:
        tmp = []

    return tmp
