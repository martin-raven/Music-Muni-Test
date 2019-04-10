import os
import pickle
from googleapiclient import discovery
import time
import json

					# Static Variables
spreadsheet_id="1A3Ph6mfzKO-Aollw8zCx86-PwCoI-wMJVf5hTtEb3bs"
range_one="Course"
range_two="Module"
range_three="Lesson"
range_four="media"


# Handling Network retrivals
def retrive(range):
	print("Retriving ",range+"s"," from Sheets")
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


# Function to parse Media into Lessons
def ParseMedias(range,Courses):
	print("Parsing Media into JSON....")
	MediasData=retrive(range)
	# print(modulesData)
	Medias={}
	for Item in MediasData[1:]:
		# print(Item)
		Media={}
		try:
			for key,entry in zip(MediasData[0],Item):
				if entry!="":
					Media[key]=entry
					# print(entry,key)
		except Exception as e:
			print("Unable to add ",Item," because ",e)
		if Media!={}:
			Medias[Media["UID"]]=Media
	# print(Medias)
	UnusedMedias=list(Medias.keys())
	for Course in Courses:
		for Module in Course["modules"].keys():
			# print(Module)
			for Lesson in Course["modules"][Module]["lessons"].keys():
				MediaList=Course["modules"][Module]["lessons"][Lesson]["medias"].split(",")
				Course["modules"][Module]["lessons"][Lesson]["medias"]={}
				for LessonMedia in MediaList:
					# print(LessonMedia)
					try:
						Course["modules"][Module]["lessons"][Lesson]["medias"][LessonMedia]=Medias[LessonMedia]
						UnusedMedias.remove(LessonMedia)
					except Exception as e:
						print(e," media mensioned in ",Lesson," is missing")
						# Course["modules"][Module][Lesson]["medias"].remove(LessonMedia)
	# print(Courses)
	if UnusedMedias!=[]:
		print("The following medias have no parent: ",UnusedMedias)
	print("Parsing Media into JSON completed.\n")
	# print(Courses)
	return Courses

# Function to parse Lessons into Modules
def ParseLessons(range,Courses):
	print("Parsing Lessons into JSON....")
	LessonsData=retrive(range)
	# print(modulesData)
	Lessons={}
	for Item in LessonsData[1:]:
		# print(Item)
		Lesson={}
		try:
			for key,entry in zip(LessonsData[0],Item):
				if entry!="":
					Lesson[key]=entry.rstrip('\n')
					# print(entry,key)
		except Exception as e:
			print("Unable to add ",Item," because ",e)
		if Lesson!={}:
			Lessons[Lesson["UID"].rstrip('\n')]=Lesson
	# print(Lessons)
	UnusedLessons=list(Lessons.keys())
	for Course in Courses:
		for Module in Course["modules"].keys():
			# print(Module)
			LessonList=Course["modules"][Module]["lessons"].split(",")
			Course["modules"][Module]["lessons"]={}
			for ModuleLesson in LessonList:
				# print(ModuleLesson)
				try:
					Course["modules"][Module]["lessons"][ModuleLesson]=Lessons[ModuleLesson]
					UnusedLessons.remove(ModuleLesson)
				except Exception as e:
					print(e,ModuleLesson," is missing !!")
					# Module["lessons"].remove(ModuleLesson)
	# print(Courses)
	if UnusedLessons!=[]:
		print("The following lessons have no parent: ",UnusedLessons)
	print("Parsing Lessons into JSON completed.\n")
	# print(Courses)
	return Courses



# Function to parse Modules into Courses
def ParseModules(range,Courses):
	print("Parsing Modules into JSON....")
	modulesData=retrive(range)
	# print(modulesData)
	Modules={}
	for Item in modulesData[1:]:
		# print(Item)
		Module={}
		try:
			for key,entry in zip(modulesData[0],Item):
				if entry!="":
					Module[key]=entry.rstrip('\n')
					# print(entry,key)
		except Exception as e:
			print("Unable to add ",Item," because ",e)
		if Module!={}:
			Modules[Module["UID"].rstrip('\n')]=Module
	# print(Modules)
	UnusedModules=list(Modules.keys())
	for Course in Courses:
		ModuleList=Course["modules"].split(',')
		Course["modules"]={}
		for CourseModule in ModuleList:
			# print(CourseModule)
			try:
				Course["modules"][CourseModule]=Modules[CourseModule]
				UnusedModules.remove(CourseModule)
			except Exception as e:
				print(e,CourseModule," module is missing !!")
				# Course["modules"][CourseModule].remove(CourseModule)
	if UnusedModules!=[]:
		print("The following modules have no parent: ",UnusedModules)
	print("Parsing Modules into JSON completed.\n")
	# print(Courses)
	return Courses


					# Function to parse Courses
def ParseCourse(range):
	print("\nParsing Courses into JSON....")
	CourseData=retrive(range)
	Courses=[]
	for Item in CourseData[1:]:
		# print(Item)
		Course={}
		try:
			for key,entry in zip(CourseData[0],Item):
				if entry!="":
					Course[key]=entry.rstrip('\n')
					# print(entry,key)
		except Exception as e:
			print("Unable to add ",Item," because ",e)
		if Course!={}:
			Courses.append(Course)
	print("Parsing Courses into JSON completed.\n")
	return Courses 
					#Main Function 
def main():

		startTime=time.time()
		# print(CourseData)
						# Parsing the data into a JSON
		Courses=ParseCourse(range_one)
		# print(Courses)
						# Parsing module data into Courses
		Courses=ParseModules(range_two,Courses)
						# Parsing lessons data into Modules
		Courses=ParseLessons(range_three,Courses)
		# print(Courses)
						# Parsing medias data into Lessons
		Courses=ParseMedias(range_four,Courses)
		# print(Courses)
		with open('Data.json', 'w') as outputfile:
			json.dump(Courses, outputfile)
		print("\nCompleted the parsing of the data, check the Data.json file.\n")

		endTime=time.time()
		print("Execution took",int(endTime)-int(startTime),"seconds")

	
if __name__ == '__main__':
    main()