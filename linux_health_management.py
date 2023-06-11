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
	"""Created class main where we are going to put all the methods of this class to logged the record to the log file"""

	def __init__(self):
		while True:
			try:   
				"""Combining above while loop and this try except makes sure that the program recover from any mishappening and completely restarts the code"""
				logging.basicConfig(filename=f'{expanduser("~")}/app_data.log',level=logging.INFO,format='%(asctime)s,%(message)s',datefmt='%d-%m-%Y,%H:%M:%S')  #sets the basic configuration for the logger file
				self.last_input_time=time.time()     #stores the data for last input time
				self.event = threading.Event()       #creates threading event
				self.t1=threading.Thread(target=self.logger, args=(self.event,))   #creating thread 1
				self.t1.start()                      #starting thread 1
				self.input_checker()                 #this function will check if user in working on this laptop or not 
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
		"""This will check the for the mouse and keyboard incteraction of the user
			if mouse or keyboard interaction is detected then it will call movement funcation to change the last interaction time for the user"""
		with MouseListener(on_move=self.movement,on_click=self.movement, on_scroll=self.movement) as listener:
		    # with KeyboardListener
		    # (on_press=self.movement,on_release=self.movement) as
		    # listener: #you don't need on_release parameter i just kept it
		    # for future use and to remember the parameter in future
		    with KeyboardListener(on_press=self.movement) as listener:
		        listener.join()

	def logger(self,event):
		"""this funcation checks the which application is running on the screen and requests to log the data"""
		while True:  #it ensures the stores data until system is shutdown
			try:
				pid = subprocess.check_output(["xdotool", "getactivewindow", "getwindowpid"]).decode("utf-8").strip() #this will get the process Id of the current application on the screen
			except Exception as e:
				"""this will handle the expection like this program works on x11 interface but in case of wayland program won't run to handle this we'll use this and like some time there is no application on screen so we don't get any process id this exception block will take care of it """
				logging.info(e)
				continue
			
			# print(pid,psutil.Process(int(pid)).name())
			logging.info(psutil.Process(int(pid)).name())  #stores the data to the log file
			if time.time()-self.last_input_time>180:   #ensures the system is not inactive for more than 3 minutes
				if not self.is_media_playing(): #if the system is inactive, check if user is playing is media file or not. if media file is playing don't pause the thread else pause the thread and wait until it is set by the movement funcation operated by input check function.
					self.event.clear()  # clear event to pause the thread
					self.event.wait()  # wait for event to be set
			time.sleep(1)

if __name__ == '__main__':
	time.sleep(5)  #initial time gap to make sure the program will perfectly
	Main()    #calling main class
