#!/usr/bin/env python3

from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse    import Listener  as MouseListener
from os.path import expanduser
import threading
import time
import subprocess
import psutil
import logging
import dbus

class Main(object):
	"""docstring for Main
	main logging part of the program"""

	def __init__(self):
		while True:
			try:
				try:
					with open(f'{expanduser("~")}/app_data.log',"x") as file:
						file.write("DATE,TIME,APPLICATION\n")
				except:
					pass		
				logging.basicConfig(filename=f'{expanduser("~")}/app_data.log',level=logging.INFO,format='%(asctime)s,%(message)s',datefmt='%d-%m-%Y,%H:%M:%S')
				self.last_input_time=time.time()
				self.event = threading.Event()
				self.t1=threading.Thread(target=self.logger, args=(self.event,))
				self.t1.start()
				self.input_checker()
			except:
				self.__init__()

	def is_media_playing(self):
		"""this will check if the media file is playing or not and return true or false"""
		bus = dbus.SessionBus()
		for service in bus.list_names():
			if service.startswith('org.mpris.MediaPlayer2.'):
				player = dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')
				status = player.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus', dbus_interface='org.freedesktop.DBus.Properties')
				# print(status) #this will return Playing Paused Not playing
				if status == 'Playing':
					return True
		return False

	def movement(self,*args):
		"""This will put the last time of the user"""
		self.last_input_time=time.time()
		if not self.event.is_set():
			self.event.set()

	def input_checker(self):
		"""This will check the for the mouse and keyboard incteraction of the user"""
		with MouseListener(on_move=self.movement,on_click=self.movement, on_scroll=self.movement) as listener:
		    # with KeyboardListener(on_press=self.movement,on_release=self.movement) as listener: #you don't need on_release parameter i just kept it for future use and to remember the parameter in future
		    with KeyboardListener(on_press=self.movement) as listener:
		        listener.join()

	def logger(self,event):
		while True:
			pid = subprocess.check_output(["xdotool", "getactivewindow", "getwindowpid"]).decode("utf-8").strip()
			# print(pid,psutil.Process(int(pid)).name())
			logging.info(psutil.Process(int(pid)).name())
			if time.time()-self.last_input_time>180:
				if not self.is_media_playing():
					self.event.clear()  # clear event to pause the thread
					self.event.wait()  # wait for event to be set
			time.sleep(1)

if __name__ == '__main__':
	time.sleep(10)
	Main()
