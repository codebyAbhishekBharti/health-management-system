from pynput.keyboard import Listener  as KeyboardListener
from pynput.mouse    import Listener  as MouseListener
import threading
import time
import subprocess
import psutil
import logging
import dbus

class Main(object):
	"""docstring for Main
	main logging part of the program"""
	last_input_time=time.time()
	logging.basicConfig(filename='app_data.log',level=logging.INFO,format='%(asctime)s:%(message)s')

	def __init__(self):
		self.event = threading.Event()
		self.t1=threading.Thread(target=self.logger, args=(self.event,))
		self.t2=threading.Thread(target=self.input_checker)
		self.t1.start()
		self.t2.start()

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
		print(self.last_input_time)
		if not self.event.is_set():
			self.event.set()

	def input_checker(self):
		"""This will check the for the mouse and keyboard incteraction of the user"""
		with MouseListener(on_move=self.movement,on_click=self.movement, on_scroll=self.movement) as listener:
		    # with KeyboardListener(on_press=self.movement,on_release=self.movement) as listener: #you don't need on_release parameter i just kept it for future use and to remember the parameter in future
		    with KeyboardListener(on_press=self.movement) as listener:
		        listener.join()

	def logger(self,event):
		check_pid=''
		while True:
			pid = subprocess.check_output(["xdotool", "getactivewindow", "getwindowpid"]).decode("utf-8").strip()
			print(pid,psutil.Process(int(pid)).name())
			logging.info(psutil.Process(int(pid)).name())
			if time.time()-self.last_input_time>2:
				if not self.is_media_playing():
					self.event.clear()  # clear event to pause the thread
					self.event.wait()  # wait for event to be set
			check_pid=pid
			time.sleep(1)

if __name__ == '__main__':
	main=Main()
