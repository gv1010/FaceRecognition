import os
import time
import pandas as pd
import csv
from datetime import date, datetime

class Attendence:
	
	def __init__(self):
		self.cwd = os.getcwd()
		
	def mark(self):
	
		"""
		When this function is called, it scans through the record folder in every user folder in the dataset,
		searches for the csv file in the record folder having a csv file with current date as the name.
		When it finds this file in the subfolder of userid, it records in the markattendece csv with userid, 
		name and True, else if the csv file is missing, it will mark as False.
		Args:		
					None
		Return: 	
					None
		"""
		dirList = os.listdir('dataset')
		for x in dirList:
			path_ = os.path.join('dataset', x + "\\record")
			if os.path.exists(os.path.join(path_, str(date.today().day)+ str(date.today().month)+ str(date.today().year)+".csv")):
				with open(self.cwd + "\\mark attendence\\Mark Attendence.csv", "a") as f:
					write = csv.writer(f)
					now = datetime.now()
					date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
					#print(date_time)
					write.writerow([x, date_time, "True"])
			else:
				with open(self.cwd + "\\mark attendence\\Mark Attendence.csv", "a") as f:
					write = csv.writer(f)
					now = datetime.now()
					date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
					#print(date_time)
					write.writerow([x, date_time, "False"])
					
					
a = Attendence()
a.mark()
			