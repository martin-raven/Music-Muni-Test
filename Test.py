import os
import pickle
from googleapiclient import discovery

# Static Variables
spreadsheet_id="1A3Ph6mfzKO-Aollw8zCx86-PwCoI-wMJVf5hTtEb3bs"
range_one="Course"

# Initialize credentials
credentials = None
if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
else:
	print("Please run the InitialRun.py before this file")
	quit()

# Main Service initialized 
service = discovery.build('sheets', 'v4', credentials=credentials)

try:
	result = service.spreadsheets().values().get(
	    spreadsheetId=spreadsheet_id, range=range_one).execute()
	# Getting the values into the list
	if "values" in result and result["values"]!=[]:
		CourseData=result["values"][1:]
	# Incase the values is empty or error occurs while requesting
	else:
		print("No Courses found")
		quit()
	# print(CourseData)
	# Parsing the data into a JSON
	Courses=[]
	for Item in CourseData[1:]:
		# print(Item)
		Course={}
		try:
			for key,entry in zip(CourseData[0],Item):
				if entry!="":
					Course[key]=entry
					print(entry,key)
		except Exception as e:
			print(e)
		if Course!={}:
			Courses.append(Course)
	print(Courses)
except Exception as e:
	print(e)
	quit()
