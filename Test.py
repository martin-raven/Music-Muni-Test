import os
import pickle
from googleapiclient import discovery

					# Static Variables
spreadsheet_id="1A3Ph6mfzKO-Aollw8zCx86-PwCoI-wMJVf5hTtEb3bs"
range_one="Course"
range_two="module"


# Handling Network retrivals
def retrive(range):
	try:

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
		result = service.spreadsheets().values().get(
		    spreadsheetId=spreadsheet_id, range=range).execute()
						# Getting the values into the list
		if "values" in result and result["values"]!=[]:
			Data=result["values"][1:]
						# Incase the values is empty or error occurs while requesting
		else:
			print("No Courses found")
			quit()
		return Data
	except Exception as e:
		print("Exception in retrival : ",e)
		quit()

# Function to parse modules into Courses
def ParseModules(range,Courses):
	modulesData=retrive(range)
	print(modulesData)

					# Function to parse Courses
def ParseCourse(range):
	CourseData=retrive(range)
	Courses=[]
	for Item in CourseData[1:]:
		# print(Item)
		Course={}
		try:
			for key,entry in zip(CourseData[0],Item):
				if entry!="":
					Course[key]=entry
					# print(entry,key)
		except Exception as e:
			print("Unable to add ",Item," because ",e)
		if Course!={}:
			Courses.append(Course)
	return Courses 
					#Main Function 
def main():


		# print(CourseData)
						# Parsing the data into a JSON
		Courses=ParseCourse(range_one)
		print(Courses)
						# Parsing module data into Courses
		Courses=ParseModules(range_two,Courses)
	
if __name__ == '__main__':
    main()