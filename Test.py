import os
import pickle
from googleapiclient import discovery

					# Static Variables
spreadsheet_id="1A3Ph6mfzKO-Aollw8zCx86-PwCoI-wMJVf5hTtEb3bs"
range_one="Course"
range_two="Module"
range_three="Lesson"
range_four="media"


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


# Function to parse Media into Lessons
def ParseMedias(range,Courses):
	MediasData=retrive(range)
	# print(modulesData)
	Medias={}
	for Item in MediasData[1:]:
		# print(Item)
		Media={}
		try:
			for key,entry in zip(MediasData[0],Item):
				if entry!="":
					Media[key]=entry.rstrip('\n')
					# print(entry,key)
		except Exception as e:
			print("Unable to add ",Item," because ",e)
		if Media!={}:
			Medias[Media["UID"].rstrip('\n')]=Media
	# print(Medias)
	UnusedMedias=list(Medias.keys())
	for Course in Courses:
		for Module in Course["modules"]:
			# print(Module)
			for Lesson in Module["lessons"]:
				Lesson["medias"]=Lesson["medias"].split(",")
				for LessonMedia in Lesson["medias"]:
					# print(LessonMedia)
					try:
						if(LessonMedia=="ram_bhajan_1_17_Cs3_audio"):
							print("Debug",Lesson["medias"],LessonMedia)
						Lesson["medias"][Lesson["medias"].index(LessonMedia)]=Medias[LessonMedia]
						UnusedMedias.remove(LessonMedia)
					except Exception as e:
						print(e," media mensioned in ",Lesson," is missing")
	print(Courses)
	if UnusedMedias!=[]:
		print("The following medias have no parent: ",UnusedMedias)
	return Courses

# Function to parse Lessons into Modules
def ParseLessons(range,Courses):
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
			Lessons[Lesson["UID"]]=Lesson
	# print(Lessons)
	UnusedLessons=list(Lessons.keys())
	for Course in Courses:
		for Module in Course["modules"]:
			# print(Module)
			Module["lessons"]=Module["lessons"].split(",")
			for ModuleLesson in Module["lessons"]:
				print(ModuleLesson)
				try:
					Module["lessons"][Module["lessons"].index(ModuleLesson)]=Lessons[ModuleLesson]
					UnusedLessons.remove(ModuleLesson)
				except Exception as e:
					print(e," lesson is missing !!")
	# print(Courses)
	if UnusedLessons!=[]:
		print("The following lessons have no parent: ",UnusedLessons)
	return Courses



# Function to parse Modules into Courses
def ParseModules(range,Courses):
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
			Modules[Module["UID"]]=Module
	# print(Modules)
	UnusedModules=list(Modules.keys())
	for Course in Courses:
		Course["modules"]=Course["modules"].split(',')
		for CourseModule in Course["modules"]:
			# print(CourseModule)
			try:
				Course["modules"][Course["modules"].index(CourseModule)]=Modules[CourseModule]
				UnusedModules.remove(CourseModule)
			except Exception as e:
				print(e," module is missing !!")
	# print(Courses)
	if UnusedModules!=[]:
		print("The following modules have no parent: ",UnusedModules)
	return Courses


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
		# print(Courses)
						# Parsing module data into Courses
		Courses=ParseModules(range_two,Courses)
						# Parsing lessons data into Modules
		Courses=ParseLessons(range_three,Courses)
		# print(Courses)
						# Parsing medias data into Lessons
		Courses=ParseMedias(range_four,Courses)

	
if __name__ == '__main__':
    main()