#python C:\Users\Zack\Everything\Documents\Postgrad\Coding\flying_to_fly.py

import os
import time
import datetime

class Traveler(object):
	def __init__(self, name, position, layovers):
		self.name = name
		self.position = position
		self.layovers = layovers
	def __repr__(self):
		return "Traveler" + str((self.name, self.position, self.layovers))
	
	def display_info(self):
		print self.name, self.position, self.layovers

class Layover(object):
	def __init__(self, airport, start_date, end_date):
		self.airport = airport
		self.start_date = start_date
		self.end_date = end_date
	def __repr__(self):
		return "Layover" + str((self.airport, self.start_date, self.end_date))

airport_dictionary = "C:/Users/Zack/Everything/Documents/Postgrad/Coding/airport_dictionary.txt"
my_file = open(airport_dictionary, "r")
read_airports = my_file.read()
exec read_airports
my_file.close()

""" above sets airports equal to dictionary of airports
with key = airport code 
	 val = [airport name, city, country] """

database = "C:/Users/Zack/Everything/Documents/Postgrad/Coding/database.txt"
my_file = open(database, "r")
read_users = my_file.read()
exec read_users
my_file.close()		


def check_date(test_date):
	test_date = test_date.split("/")
	if len(test_date) == 3:
		try:
			test_date = datetime.date(int(test_date[2]), int(test_date[0]), int(test_date[1]))
		except ValueError as e:
			print "Invalid date", e
			return False
		except TypeError:
			print "Date must contain only numbers"
			return False
	else:
		print "Date doesn't appear to be formatted correctly!"
		return False
	
	return True
	
def check_time(test_time):	
	test_time = test_time.split(":")
	if len(test_time) == 2:
		try:
			test_time = datetime.time(int(test_time[0]), int(test_time[1]))
		except ValueError as e:
			print "Invalid time", e
			return False
		except TypeError:
			print "Time must contain only numbers"
			return False
	else:
		print "Time doesn't appear to be formatted correctly!"
		return False
		
	return True

def get_date(test_date, test_time):
	test_date = test_date.split("/")
	for index in range(3):
		test_date[index] = int(test_date[index])
			
	test_time = test_time.split(":")
	for index in range(2):
		test_time[index] = int(test_time[index])
	if test_time[0] < 13 and test_time[0] > 0:
		while True:
			am_pm = str(raw_input("Is that time in AM or PM? "))
			if am_pm.upper() == "AM" or am_pm.upper() == "PM":
				break
			else:
				print "Input unclear, try again!"
		if am_pm.upper() == "AM" and test_time[0] == 12:
			test_time[0] = 0
		elif am_pm.upper() == "PM" and test_time[0] == 12:
			pass
		else:
			test_time[0] = (test_time[0] + 12)
	
	return datetime.datetime(test_date[2], test_date[0], test_date[1], test_time[0], test_time[1])
		
			

def add_layover(traveler):
	os.system("CLS")
	print "Hello", traveler.name, "let's try to find you an acrobuddy!"
	
	while True:
		airport_code = raw_input("Provide your 3 letter airport code: ").upper()
		if airport_code !="" and airport_code not in airports:
			os.system("CLS")
			print "Sorry, that doesn't seem to be a valid code"
		elif airport_code == "":
			os.system("CLS")
			print "Aborted!"
			return traveler
		else:
			break
	os.system("CLS")
	print "Great! Now let's get some info about the time of your trip!"
	
	while True:
		start_day = str(raw_input("When will you arrive? Enter as mm/dd/yyyy: "))
		if start_day != "" and not check_date(start_day):
			os.system("CLS")
			print "Try again!"
		elif start_day =="":
			os.system("CLS")
			print "Aborted!"
			return traveler
		else:
			os.system("CLS")
			start_time = str(raw_input("What time will you arrive? Enter as hh:mm "))
			if start_time != "" and not check_time(start_time):
				print "Try again!"
			elif start_time =="":
				print "Aborted!"
				return traveler
			else:
				trip_start = get_date(start_day, start_time)
				break
	os.system("CLS")			
	print "Finally, let's get some info about when you'll be available until."
	
	while True:
		end_day = str(raw_input("When will you depart? Enter as mm/dd/yyyy or, if the same date as departure, just type 'same': "))
		if end_day.lower() == "same":
			end_day = start_day
			
		if end_day != "" and not check_date(end_day):
			os.system("CLS")
			print "Try again!"
		elif end_day == "":
			os.system("CLS")
			print "Aborted!"
			return traveler
		elif get_date(end_day,"23:59") < datetime.datetime.now():
			os.system("CLS")
			print "Sorry, that date has already passed!"
		elif get_date(end_day,"23:59") < trip_start:
			os.system("CLS")
			print "That date is before your start date!!"
		else:
			os.system("CLS")
			end_time = str(raw_input("What time will you depart? Enter as hh:mm "))
			if end_time != "" and not check_time(end_time):
				print "Try again!"
			elif end_time == "":
				print "Aborted!"
				return traveler
			else:
				trip_end = get_date(end_day, end_time)
				if trip_end < datetime.datetime.now():
					print "Sorry, that date has already passed!"
				elif trip_end < trip_start:
					os.system("CLS")
					print "That date is before your start date!!"
				else:	
					traveler.layovers = traveler.layovers + [Layover(airport_code, trip_start, trip_end)]
					print "Mission accomplished!"
					return traveler
	
def save_data(user_list, profiles):
	my_file = open("C:/Users/Zack/Everything/Documents/Postgrad/Coding/database.txt", "w")
	my_file.truncate()
	
	my_file.write("user_list = ")
	my_file.write(str(user_list)) 
	my_file.write("\n")
	my_file.write("profiles = ")
	my_file.write(str(profiles))
	
	my_file.close()

def menu_select(menu):
	while True:
		for key in sorted(menu.keys()):
			print key, "-", menu[key][0]
		
		response = raw_input("Please Select an option: ")
		if response == "":
			return ""
		elif response in menu:
			return menu[response][1]
		else:
			print "Please select a valid choice."


def welcome(user_list,profiles):
	while True:
		os.system("CLS")
		print "Welcome to Flying to Fly, what would you like to do?"
		menu = {
				"1": ["Login","login(user_list,profiles)"],
				"2": ["Register","register('','',user_list,profiles)"],
				"3": ["Quit",""]
				}
		response = menu_select(menu)
		if response == "":
			print "Thanks for using Flying to Fly. See you next time!"
			return "Done"
		else:
			exec response

		
def login(user_list,profiles):
	os.system("CLS")
	
	while True:
		print "Please enter your username and password below"
		user = str(raw_input("User: "))
		if user == "":
			break
		elif user in user_list:
			password = str(raw_input("Password: "))
			if password == "":
				break	
			if user_list[user]==password:
				main_menu(user,profiles)
				save_data(user_list,profiles)
				break
			else:
				print "Incorrect password, try again",
		else:
				print "Username not recognized, register new username?"
				menu = {
						"1": ["Yes","register(user, password, user_list, profiles)"],
						"2": ["No","No"]
						}
				response = menu_select(menu)
				if response == "":
					break
				elif response == "No":
					continue
				else:
					password = str(raw_input("Password: "))
					if password == "":
						break	
					exec response
					
def register(user, password, user_list, profiles):
	if user == "" or password =="":
		while True:
			print "Please enter a username and password below"
			user = str(raw_input("user: "))
			if user in user_list:
				os.system("CLS")
				print "Username already taken, try again! \n"
				continue
			elif user == "":
				break
			
			password = str(raw_input("password: "))
			if password == "":
				break
			else:
				user_list[user] = password
				profiles[user] = create_profile(Traveler("","",[]))
				main_menu(user,profiles)
				save_data(user_list,profiles)
		welcome(user_list,profiles)
	else:
		user_list[user]=password
		profiles[user] = create_profile(Traveler("","",[]))
		main_menu(user,profiles)
		save_data(user_list,profiles)

def create_profile(profile):
	menu1 = {
			'1': ["Flyer", "position = 'Flyer'"],
			'2': ["Base", "position = 'Base'"],
			'3': ["Both", "position = 'Both'"]
	}
	
	menu2 = {
			'1': ["Yes", "profile = add_layover(profile)"],
			'2': ["No", ""],
	}
	
	menu3= {
			'1': ["Edit name", "name = raw_input('Your current name is %s, type your new name below, or press enter to keep it: ' % profile.name)"],
			'2': ["Edit preferred acro role", "position = raw_input('Your current role is %s, to change your role type 1, or press enter to keep it: ' % profile.position)"],
			'3': ["Save & Quit", ""]
	}
	os.system("CLS")
	
	print "Create/Edit Profile \n"
	if profile.name == "" and profile.position == "" and profile.layovers == []:
		name = raw_input("Welcome, please enter your name: ")
		if name == "":
			return profile
		
		print "What is your preferred acro role, %s?" % name
		response = menu_select(menu1)
		if response == "":
			return profile
		else:
			exec response
			profile.name = name
			profile.position = position 
		
		print "Do you have any upcoming trips you'd like to enter? \n"
		response = menu_select(menu2)
		if response == "":
			return profile
		else:
			exec response
			return profile
	
	else:
		name = ""
		position = ""
		print "Welcome, back", profile.name, "what would you like to do?"
		while True:
			response = menu_select(menu3)
			if response == "":
				return profile 
			else:
				exec response
			
				if name != "":
					profile.name = name
				if position == '1':
					response = menu_select(menu1)
					if response =="":
						print "Change aborted."
					else:
						exec response
						profile.position = position
						return profile
			
				
def match_traveler(user, profiles):
	os.system("CLS")
	matches = []
	traveler = profiles[user]
	for layover in traveler.layovers:
		for profile in profiles:
			for other_layover in profiles[profile].layovers:
				if (profile != user) and (other_layover.airport == layover.airport) and ((other_layover.end_date > layover.start_date and other_layover.end_date < layover.end_date) or (other_layover.start_date > layover.start_date and other_layover.start_date < layover.end_date)):
					matches = matches + [layover]
	if matches == []:
		print "no matches, sorry!"
	else:
		print "matches are as follows: "
		for match in matches:
			print match
	done = raw_input("Press enter to continue")


def view_profile(traveler):
	os.system("CLS")
	print "Here's what we have on you: "
	print "Name: %s \n" % traveler.name
	print "Preferred Acro Role: %s \n" % traveler.position
	print "Upcoming Trips: " 
	for trip_number in range(len(traveler.layovers)):
		trip = traveler.layovers[trip_number]
		print "%s - \n" % (trip_number + 1),
		print "Arriving at %s airport on %s at %s" % (trip.airport,trip.start_date.strftime("%m/%d/%Y") ,trip.start_date.strftime("%I:%M%p"))
		print "Staying until %s at %s \n" % (trip.end_date.strftime("%m/%d/%Y") ,trip.end_date.strftime("%I:%M%p"))
	raw_input("Press Enter to continue")	
def main_menu(user, profiles):
	profile = profiles[user]
	while True:
		os.system("CLS")
		menu={
			"1": ["View my profile","view_profile(profile)"],
			"2": ["Edit my profile","profile = create_profile(profile)"],
			"3": ["Add a trip","add_layover(profile)"],
			"4": ["Look for a match","match_traveler(user,profiles)"],
			"5": ["Logout",""]
			}
		
		print "Main Menu: "
		response = menu_select(menu)
		if response == "":
			break
		else:
			exec response
	profiles[user] = profile

welcome(user_list,profiles)
