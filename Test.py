from pprint import pprint
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
service = discovery.build('sheets', 'v4', credentials=credentials)

try:
	result = service.spreadsheets().values().get(
	    spreadsheetId=spreadsheet_id, range=range_one).execute()
	# Getting the values into the list
	if "values" in result and result["values"]!=[]:
		CourseData=result["values"][1:]

	else:
		print("No Courses found")
		quit()
	# 
	print(CourseData)
except Exception as e:
	print(e)
	quit()
# numRows = result.get('values') if result.get('values')is not None else 0
# print('{0} rows retrieved.'.format(numRows))
