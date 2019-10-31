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

from yeelight import discover_bulbs
from yeelight import Bulb
import msvcrt

#---------------------------
#   Yeelight Handling
#---------------------------
class Yeelight:
	
	def __init__(self, settings):
		self.settings = settings
		self.enabled = self.settings.YeelightEnabled
		self.active = False
		self.lights = {}
		
		if not self.enabled:
			return
		
		print("Initializing Yeelight...")
		while len(self.lights) == 0:
			self.detect_lights()
			if len(self.lights) == 0:
				print("Yeelight not found")
				print("Press C to cancel or any key to scan again")
				input_char = msvcrt.getch().decode("utf-8").upper()
				if input_char == 'C':
					return
		
		self.active = True
		return
	
	#---------------------------
	#   state
	#---------------------------
	def state(self, device, color = "", brightness = 100, effect = "smooth", duration = 1500):
		## Check if yeelight is active
		if not self.active:
			return
		
		## Check if light has been detected on startup
		if device not in self.lights:
			print("Yeelight Device \"" + device + "\" does not detected")
			return
		
		## Set light transition effect
		try:
			self.lights[device].effect = effect
			self.lights[device].duration = duration
		except:
			print("Communication failed with Yeelight " + device + ", light disabled")
			del self.lights[device]
			return
		
		## Turn light off
		if not color:
			try:
				self.lights[device].turn_off()
			except:
				print("Communication failed with Yeelight " + device + ", light disabled")
				del self.lights[device]
				return
			return
		
		if color:
			## Turn light on
			try:
				self.lights[device].turn_on()
				tmp = self.hex_to_rgb(color)
				self.lights[device].set_brightness(brightness)
				self.lights[device].set_rgb(tmp[0], tmp[1], tmp[2])
			except:
				print("Communication failed with Yeelight " + device + ", light disabled")
				del self.lights[device]
				return
		else:
			try:
				self.lights[device].set_brightness(brightness)
			except:
				print("Communication failed with Yeelight " + device + ", light disabled")
				del self.lights[device]
				return
		
		return
	
	#---------------------------
	#   detect_lights
	#---------------------------
	def detect_lights(self):
		discoveredLights = discover_bulbs()
		
		for light in discoveredLights:
			## Check light compatibility
			if 'capabilities' in light and 'model' in light['capabilities']:
				if light['capabilities']['model'] not in ['mono', 'color', 'stripe', 'bslamp', 'ceiling']:
					continue
			
			## Check reply consistency
			if 'ip' not in light:
				continue
			
			## Set device name
			device_name = light['capabilities']['name']
			
			## Check if device has a name
			if device_name == "":
				print("Name not defined for Yeelight " + light['capabilities']['model'] + ", ID: " + light['capabilities']['id'])
				
				## Identify light for user
				try:
					bulb = Bulb(light['ip'])
					bulb.turn_off()
					bulb.effect = "sudden"
					bulb.turn_on()
					bulb.set_brightness(100)
					bulb.set_rgb(0, 0, 255)
					bulb.effect = "smooth"
					bulb.duration = 10000
					bulb.set_rgb(255, 0, 0)
				except:
					print("Communication failed with Yeelight " + light['capabilities']['model'] + ", ID: " + light['capabilities']['id'])
					continue
				
				## Get user input for light name
				print("This device will change color from blue to red over 10 seconds.")
				print("Enter name for this device or press enter to skip it:")
				input_char = input()
				if input_char == '':
					try:
						bulb.turn_off()
					except:
						print("Communication failed with Yeelight " + light['capabilities']['model'] + ", ID: " + light['capabilities']['id'])
						continue
					continue
				
				## Set light name
				device_name = input_char
				try:
					bulb.set_name(device_name)
				except:
					print("Communication failed with Yeelight " + light['capabilities']['model'] + ", ID: " + light['capabilities']['id'])
					continue
			
			## Add usable light to list
			self.lights[device_name] = Bulb(light['ip'])
			
			## Turn off light
			try:
				self.lights[device_name].turn_off()
			except:
				print("Communication failed with Yeelight " + device_name + ", light disabled")
				del self.lights[device_name]
				continue
		
		return
	
	#---------------------------
	#   hex_to_rgb
	#---------------------------
	def hex_to_rgb(self,h):
		h = h.lstrip('#')
		r = int(h[0:2], 16)
		g = int(h[2:4], 16)
		b = int(h[4:6], 16)
		
		return r, g, b