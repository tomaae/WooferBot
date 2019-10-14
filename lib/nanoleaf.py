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
import requests
import time
import select
import re
import json
import msvcrt

#---------------------------
#   Nanoleaf Handling
#---------------------------
class Nanoleaf:
	
	def __init__(self, settings):
		self.settings = settings
		
		self.enabled = self.settings.NanoleafEnabled
		self.active = False
		
		self.ip = self.settings.NanoleafIP
		self.token = self.settings.NanoleafToken
		
		if not self.enabled:
			return
			
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
					input_char = msvcrt.getch().decode("utf-8").upper()
					if discovery_time < 20:
						discovery_time = discovery_time + 5
					if input_char == 'C':
						return
						
			self.ip = ip_list[0]
			settings.NanoleafIP = self.ip
		
		#
		# Token not set
		#
		result = self.put_request("state", { 'on': { 'value': False } })
		if self.token == "" or result.status_code == 401:
			while not self.auth():
				print("Press C to cancel or any key to try again")
				input_char = msvcrt.getch().decode("utf-8").upper()
				if input_char == 'C':
					return
			
			settings.NanoleafToken = self.token
		
		
		self.active = True

	#---------------------------
	#   ssdp_discovery
	#---------------------------
	def ssdp_discovery(self, discovery_time: float = 5):
		SSDP_IP = "239.255.255.250"
		SSDP_PORT = 1900
		SSDP_MX = 10
		
		devices = []

		req = ['M-SEARCH * HTTP/1.1',
		'HOST: ' + SSDP_IP + ':' + str(SSDP_PORT),
		'MAN: "ssdp:discover"',
		'MX: ' + str(SSDP_MX),
		'ST: ssdp:all']
		req = '\r\n'.join(req).encode('utf-8')

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, SSDP_MX)
		sock.bind((socket.gethostname(), 9090))
		sock.sendto(req, (SSDP_IP, SSDP_PORT))
		sock.setblocking(False)


		timeout = time.time() + discovery_time
		print("Starting Nanoleaf discovery.")
		while time.time() < timeout:
			try:
				ready = select.select([sock], [], [], 5)
				if ready[0]:
					response = sock.recv(1024).decode("utf-8")
					if 'nanoleaf' not in response:
						continue

					ip = ""
					for line in response.lower().split("\n"):
						if "location:" in line:
							ip = re.search( r'[0-9]+(?:\.[0-9]+){3}', line).group()

							if ip not in devices and (self.is_valid_ipv4_address(ip) or self.is_valid_ipv6_address(ip)):
								devices.append(ip)
					
			except socket.error as err:
				print("Socket error while discovering SSDP devices!")
				print(err)
				sock.close()
				break
				
		sock.close()
		return devices

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
	#   Scene
	#---------------------------
	def Scene(self, name = None):
		if not self.active:
			return
			
		if not name:
			data = { 'on': { 'value': False } }
			result = self.put_request("state", data)
			return result
			
		data = { 'select': name } 
		result = self.put_request("effects", data)
		return result
		
	#---------------------------
	#   put_request
	#---------------------------
	def put_request(self, endpoint, data: dict):
		url = "http://" + self.ip + ":16021/api/v1/" + self.token + "/" + endpoint
		
		try:
			result = requests.put(url, data = json.dumps(data), timeout = 1)
		except requests.exceptions.RequestException as e:
			print(e)
			return result
		
		if result.status_code == 204:
			return result
			
		if result.status_code == 403:
			print("Error 403, Bad request")
			return result
			
		if result.status_code == 401:
			print("Error 401, Not authorized")
			return result
			
		if result.status_code == 404:
			print("Error 404, Resource not found")
			return result
			
		if result.status_code == 422:
			print("Error 422, Unprocessible entity")
			return result
			
		if result.status_code == 500:
			print("Error 500, Internal error")
			return result
			
		return result
		
	#---------------------------
	#   auth
	#---------------------------
	def auth(self):
		print("Auth with nanoleaf...")
		
		url = "http://" + self.ip + ":16021/api/v1/new"
		result = requests.post(url)
		
		if result.status_code == 200:
			print("Authorized ok")
			self.token = result.json()['auth_token']
			return True
			
		if result.status_code == 403:
			print("Nanoleaf not in discovery mode.")	
			print("Hold down power button for ~5 seconds until led starts blinking.")	
			return False

		return

	#---------------------------
	#   portup
	#---------------------------
	def portup(self, ip, port):
		#socket.setdefaulttimeout(0.01)
		socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		if socket_obj.connect_ex((ip, port)) == 0:
			socket_obj.close()
			return True
		socket_obj.close()
		return False
		