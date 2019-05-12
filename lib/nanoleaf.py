##########################################################################
#
#    WooferBot, an interactive BrowserSource Bot for twitch.tv
#    Copyright (C) 2019  Tomaae
#    (https://github.com/tomaae/WooferBot)
#
#    This file is part of WooferBot.
#
#    WooferBot is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WooferBot is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WooferBot.  If not, see <https://www.gnu.org/licenses/>.
#
##########################################################################\

import socket
import requests
import json

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
		if not self.active:
			if not self.ip:
				ip_list = self.Scan()
			
				if len(ip_list) == 0:
					print("Nanoleaf not found")
					return
			
				self.ip = ip_list[0]
				settings.NanoleafIP = self.ip
			
		if self.token == "":
			if not self.Auth():
				return
			settings.NanoleafToken = self.token
			
		self.active = True

	#---------------------------
	#   Off
	#---------------------------
	def Off(self):
		if not self.active:
			return
			
		data = { 'on': { 'value': False } }
		self.put_request("state", data)
		return
		
	#---------------------------
	#   Scene
	#---------------------------
	def Scene(self, name):
		if not self.active:
			return
			
		data = { 'select': name } 
		self.put_request("effects", data)
		return
		
	#---------------------------
	#   Scene
	#---------------------------
	def put_request(self, endpoint, data: dict):
		url = "http://" + self.ip + ":16021/api/v1/" + self.token + "/" + endpoint
		
		try:
			result = requests.put(url, data = json.dumps(data), timeout = 1)
		except requests.exceptions.RequestException as e:
			print(e)
			return
		
		if result.status_code == 204:
			return
			
		if result.status_code == 403:
			print("Error 403, Bad request")
			return
			
		if result.status_code == 401:
			print("Error 401, Not authozed")
			return
			
		if result.status_code == 404:
			print("Error 404, Resource not found")
			return
			
		if result.status_code == 422:
			print("Error 422, Unprocessible entity")
			return
			
		if result.status_code == 500:
			print("Error 500, Internal error")
			return
			
		return
		
	#---------------------------
	#   Auth
	#---------------------------
	def Auth(self):
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
	#   Scan
	#---------------------------
	def Scan(self):
		print("Scanning the network...")
		
		ips = []
		local_ip = socket.gethostbyname(socket.gethostname())
		local_ip_arr = local_ip.split(".")
		local_nw = local_ip_arr[0] +  "." + local_ip_arr[1] +  "." + local_ip_arr[2] +  "."		
		
		socket.setdefaulttimeout(0.01)
		
		for ip_end in range(1, 255):
			ip = str(local_nw) + str(ip_end)
			socket_obj = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			if socket_obj.connect_ex((ip, 16021)) == 0:
				ips.append(ip)
			socket_obj.close()
			
		return ips
		
		