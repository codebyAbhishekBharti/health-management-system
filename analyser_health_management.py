#!/usr/bin/env python3

import pandas as pd
from os.path import expanduser
import time
from datetime import datetime,timedelta


class Main(object):
	"""docstring for Main"""
	def __init__(self):
		# self.path=f'{expanduser("~")}/app_data.log'
		# self.path='app_data.log'
		self.path='app_data_modified.log'
		self.log_time_diff=1
		self.time_format='%H:%M:%S'
		self.data_dict={'DATE':[],'START TIME':[],'END TIME':[],'USAGE':[],'APPLICATION':[]}

	def time_diff_finder(self,initial_time,final_time):
		t1 = datetime.strptime(initial_time, self.time_format)
		t2 = datetime.strptime(final_time, self.time_format)
		if t2 < t1:
		    t2 += timedelta(days=1)
		delta = t2 - t1
		return int(delta.total_seconds())

	def end_time_calc(self,time_data):
		epoch = int(time.mktime(time.strptime(time_data,self.time_format)))
		return str(time.ctime(epoch+1)).split(" ")[4]

	def data_appender(self,data):
		self.data_dict["DATE"].append(data[0])
		self.data_dict['START TIME'].append(data[1])
		self.data_dict['END TIME'].append(self.end_time_calc(data[1]))
		self.data_dict['USAGE'].append(self.log_time_diff)
		self.data_dict['APPLICATION'].append(data[2])

	def data_cleaner(self):
		"""Converting the data set into the fomat
		   DATE        START_TIME     END_TIME USAGE   APPLICATION
		   11-01-2022  11:49:42       11:50:33    52   thunar     """
		df=pd.read_csv(self.path)
		self.data_appender(df.iloc[0])
		for ind in df.index:
			try:
				if not df.iloc[ind,2]==df.iloc[ind+1,2] and self.time_diff_finder(df.iloc[ind,1],df.iloc[ind+1,1])==self.log_time_diff and df.iloc[ind,0]==df.iloc[ind+1,0]:
					self.data_dict['END TIME'][-1]=self.end_time_calc(df.iloc[ind,1])
					self.data_dict['USAGE'][-1]=self.time_diff_finder(self.data_dict['START TIME'][-1],self.data_dict['END TIME'][-1])
					self.data_appender(df.iloc[ind+1])
			except:
				pass
		# print(self.data_dict)
		# print(len(self.data_dict['DATE']))
		# print(len(self.data_dict['START TIME']))
		# print(len(self.data_dict['END TIME']))
		# print(len(self.data_dict['APPLICATION']))
		self.newdf=pd.DataFrame(self.data_dict)
		print(self.newdf)
		# self.newdf.to_csv("refined_data.csv",index=False)
		# print(newdf.loc[(newdf['APPLICATION']=="Thunar")&(newdf['DATE']=='11-01-2023')])
		# print(newdf.describe())
class Analyzer(Main):
	def __init__(self):
		self.path="refined_data.csv"
		
	def current_day_pie_chart(self):
		df=pd.read_csv(self.path)
		# print(df)
		today = datetime.now().strftime("%d-%m-%Y")
		# print(today)
		newdf=df.loc[(df['DATE']==today)]
		print(newdf)




if __name__ == '__main__':
	m=Main()
	# print(m.time_diff_finder('11:49:42','11:50:34'))
	# print(m.time_diff_finder('23:53:50','00:15:50'))
	# m.data_cleaner()
	analyzer=Analyzer()
	analyzer.current_day_pie_chart()

