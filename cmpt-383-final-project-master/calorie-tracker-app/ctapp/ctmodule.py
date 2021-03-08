import ctf
import requests
import sys
import datetime

ROOT_URL = 'http://localhost:8080/'

INVALID_INPUT_MSG = '\nInvalid option. Please type in only a number (Type "0" to select option (0), etc.).'
user_attr = ['password', 'first_name', 'last_name', 'age', 'gender', 'height', 'activity_level', 'goal']
food_attr = ['calories', 'serving_size']

'''
Tests connection to server at start up. Causes ctmain.py to cease execution if connection problem occurs
or if response text does not equal "secret message"
'''
def startup_test_conn():
	response = ""
	url = ROOT_URL + 'test'
	try:
		response = requests.get(url, timeout=10)
	except requests.exceptions.ConnectionError:
		print('Cannot connect to meal_server.js. Turn on node.js server first before running program.')
		sys.exit(0)
	if ctf.are_same_str(response.text, "secret message") == 0:
		print('Established connection but not test strings do not match. Check meal_server.js for more.')
		sys.exit(0)

'''
Makes string that shows selections for user interface. Based on current interface that user is in.
'''
def make_sels_str(options):
	s = 'Select '
	for i in range(len(options)):
		s += '(' + str(i) + ') ' + options[i] + ', '
	s += '(CTRL-C): Go back.'
	return s

'''
Used to validate user interface selections in 'make_sels_str' string.
'''
def user_interaction(sels_str, tot_sels):
	print(sels_str)
	inp = input('\nType here: ')
	if ctf.is_menu_option(inp, tot_sels) == 1:
		return inp
	else:
		return ""

'''
Guides user during login. Returns user JSON object if successful, otherwise returns emtpy JSON object.
'''
def login_attempt():
    u = input('Enter a username: ')
    pw = input('Enter a password: ')
    url = ROOT_URL + 'login?u=' + u + '&pw=' + pw
    response = requests.get(url)
    return response.json()

'''
Called after successful login. Makes sure today's weight and calorie count corresponds to current date.
'''
def update_user_at_login(user):
	curr_date = str(datetime.datetime.now().date())
	weight_hist = user['weight_history']
	if curr_date not in weight_hist:
		url = ROOT_URL + 'update/user/weight?val=' + str(0) + '&username=' + user['username'] + '&date=' + curr_date
		response = requests.post(url)
		user = response.json()
	cal_hist = user['cal_history']
	if curr_date not in cal_hist:
		url = ROOT_URL + 'update/user/cal?val=' + str(0) + '&username=' + user['username'] + '&date=' + curr_date
		response = requests.post(url)
		user = response.json()
	return user

'''
Guides user in creating/adding a new user. If confirmed by user, sends values to server to make user JSON object.
'''
def add_new_user():
	u = new_username()
	pw = input('Enter a password: ')
	fn = input('Enter your first name: ')
	ln = input('Enter your last name: ')
	age = new_age()
	gender = new_gender()
	h = new_height()
	act_lvl = new_act_lvl()
	goal = new_goal()
	if confirm_new_user(u, pw, fn, ln, age, gender, h, act_lvl, goal):
		url = ROOT_URL + 'add_user?username=' + u + '&pw=' + pw
		url += '&first_name=' + fn + '&last_name=' + ln
		url += '&age=' + age + '&gender=' + gender
		url += '&height=' + h + '&activity_level=' + act_lvl
		url += '&goal=' + goal
		response = requests.post(url)
		return True
	else:
		return False

'''
Asks user for valid username (one not already taken).
'''
def new_username():
	u = input('Enter a username: ')
	base_url = ROOT_URL + 'check_user?u='
	url = base_url + u
	response = requests.get(url)
	resp_code = response.text
	while ctf.are_same_str(resp_code, "1") == 1:
		u = input('Username already taken. Please enter another username: ')
		url = base_url + u
		response = requests.get(url)
		resp_code = response.text
	return u

'''
Asks user for valid age (must be a whole positive number).
'''
def new_age():
	age = input('Enter your age: ')
	while age.isnumeric() == False or int(age) < 0:
		print('Invalid age value. Type in a non-negative whole number only.')
		age = input('Enter your age: ')
	return age

'''
Prompts user to type in either 'm' or 'f'.
'''
def new_gender():
	g = input('Enter your gender (enter \'m\' for male or \'f\' for female): ')
	while ctf.are_same_str(g,"m") == 0 and ctf.are_same_str(g,"f") == 0 :
		g = input('Incorrect input. Enter either \'m\' for male or \'f\' for female): ')
	return g

'''
Asks user for valid height (must be a positive number).
'''
def new_height():
	h = input('Enter your height in centimetres (cm): ')
	while(True):
		try:
			test = float(h)
			if test < 0:
				print('Invalid height value. Type in a positive number only.')
				h = input('Enter your height in centimetres (cm): ')
				continue
			break
		except ValueError:
			print('Invalid age value. Type in a valid number only.')
			h = input('Enter your height in centimetres (cm): ')
	return h

'''
Prompts user to type in a number from 0 to 4.
'''
def new_act_lvl():
	explain_act_levels()
	act_lvl = input('Select an above activity levels that best describes you: ')
	while ctf.is_menu_option(act_lvl, 5) == 0:
		print(INVALID_INPUT_MSG)
		explain_act_levels()
		act_lvl = input('Select an above activity levels that best describes you: ')
	return act_lvl

'''
Prints strings explaining each activity level selection.
'''
def explain_act_levels():
	print('\nActivity levels:')
	print('(0)', ctf.explain_activity_level("0"))
	print('(1)', ctf.explain_activity_level("1"))
	print('(2)', ctf.explain_activity_level("2"))
	print('(3)', ctf.explain_activity_level("3"))
	print('(4)', ctf.explain_activity_level("4"), '\n')
	return

'''
Prompts user to type in a number from 0 to 6.
'''
def new_goal():
	explain_goals()
	goal = input('Select a weight goal: ')
	while ctf.is_menu_option(goal, 7) == 0:
		print(INVALID_INPUT_MSG)
		explain_goals()
		goal = input('Select a weight goal: ')
	return goal

'''
Prints strings explaining each weight goal selection.
'''
def explain_goals():
	print('\nWeight goals:')
	print('(0)', ctf.explain_goal("0"))
	print('(1)', ctf.explain_goal("1"))
	print('(2)', ctf.explain_goal("2"))
	print('(3)', ctf.explain_goal("3"))
	print('(4)', ctf.explain_goal("4"))
	print('(5)', ctf.explain_goal("5"))
	print('(6)', ctf.explain_goal("6"), '\n')
	return

'''
Prints summary of new user attributes and asks user for confirmation.
'''
def confirm_new_user(u, pw, first_name, last_name, age, gender, h, act_lvl, goal):
	print('\nNew user summary:')
	print('Username:', u)
	print('Password:', pw)
	print('First name:', first_name)
	print('Last name:', last_name)
	print('Age:', age)
	print('Gender:', ctf.get_gender_str(gender))
	print('Height:',h, 'cm')
	print('Activity level:', ctf.explain_activity_level(act_lvl))
	print('Weight goal:', ctf.explain_goal(goal))
	inp = input('\nConfirm user (y/n)?: ')
	while ctf.are_same_str(inp,"y") == 0 and ctf.are_same_str(inp,"n") == 0:
		print('Invalid input. Type in either \'y\' or \'n\'.')
		inp = input('Confirm user (y/n)?: ')
	if inp == "y":
		return True
	else:
		return False

'''
Prints out user stats.
'''
def display_user_stats(user):
	print('\n*** General Information -->', user['username'])

	print('First name:', user['first_name'])

	print('Last name:', user['last_name'])

	age = user['age']
	print('Age:', str(age))

	gender = user['gender']
	print('Gender:', ctf.get_gender_str(gender))

	height = user['height']
	feet = '(' + '{:.2f}'.format(ctf.cm_to_ft(height)) + ' ft)' 
	print('Height:', '{:.2f}'.format(height), 'cm', feet)

	print('\n*** Health Information')

	level = user['activity_level']
	print('Activity level:', ctf.explain_activity_level(level))

	weight = user['weight_today']
	pounds = '(' + '{:.2f}'.format(ctf.kg_to_lb(weight)) + ' lb)' 
	print('Today\'s weight:', '{:.2f}'.format(weight), 'kg', pounds)

	bmi = ctf.bmi(weight, height)
	print('BMI:', '{:.2f}'.format(bmi))

	bmr = ctf.bmr(weight, height, age, gender)
	print('Basal metabolic rate (BMR):', '{:.2f}'.format(bmr))

	print('\n*** Calorie Goal Information')

	goal = user['goal']
	print('Weight goal:', ctf.explain_goal(goal))

	basal_cal = ctf.basal_cal(bmr, level)
	print('Daily calories required to maintain weight:', '{:.2f}'.format(basal_cal))

	cal_goal = ctf.cal_goal(basal_cal, goal)
	print('Daily calories required to reach goal:', '{:.2f}'.format(cal_goal))

	print('Calories consumed so far today:', '{:.2f}'.format(user['cal_today']), '/', '{:.2f}'.format(cal_goal))

'''
Logs user weight for current date in kilograms.
'''
def log_weight_today(user):
	curr_date = str(datetime.datetime.now().date())
	w = ask_for_weight()
	url = ROOT_URL + 'update/user/weight?val=' + w + '&username=' + user['username'] + '&date=' + curr_date
	response = requests.post(url)
	return response.json()

'''
Asks user for valid weight (must be a positive number).
'''
def ask_for_weight():
	size = input('Enter your current weight (in kg): ')
	while(True):
		try:
			test = float(size)
			if test < 0:
				print('Invalid weight value. Type in a positive number only.')
				size = input('Enter your current weight (in kg): ')
				continue
			break
		except ValueError:
			print('Invalid weight value. Type in a valid number only.')
			size = input('Enter your current weight (in kg): ')
	return size

'''
Adds to current calorie amount of current date.
'''
def update_calories(user):
	curr_date = str(datetime.datetime.now().date())
	base_url = url = ROOT_URL + 'get_food?q='
	q = input('\nEnter a food you consumed today: ')
	url = base_url + q
	response = requests.get(url)
	food = response.json()
	while not(food):
		print('\nFood does not exist. Either retype the food\'s name again or register the food in the Food Menu.')
		q = input('\nEnter a food you consumed today: ')
		url = base_url + q
		response = requests.get(url)
		food = response.json()
	
	servings = ask_for_serving_amount()
	cal_amt = ctf.cal_eaten(food['calories'], float(servings))
	if confirm_calorie_update(user, food, servings, cal_amt):
		url = ROOT_URL + 'update/user/cal?val=' + '{:.2f}'.format(cal_amt) + '&username=' + user['username'] + '&date=' + curr_date
		response = requests.post(url)
		return response.json()
	else:
		return user

'''
Outputs summary of calorie count change and asks for confirmation.
'''
def confirm_calorie_update(user, food, servings, cal_amt):
	print('Food entered:', food['name'])
	print('Servings entered:', servings)
	print('Current calories consumed today:', '{:.2f}'.format(user['cal_today']))
	print('New calories consumed:', '{:.2f}'.format(cal_amt))
	print('New calorie total:', '{:.2f}'.format(user['cal_today'] + cal_amt))
	inp = input('\nConfirm calorie update (y/n)?: ')
	while ctf.are_same_str(inp,"y") == 0 and ctf.are_same_str(inp,"n") == 0:
		print('Invalid input. Type in either \'y\' or \'n\'.')
		inp = input('Confirm user (y/n)?: ')
	if inp == "y":
		return True
	else:
		return False

'''
Guides user in creating/adding a new food item. If confirmed by user, sends values to server to make food JSON object.
'''
def add_food():
	name = new_food_name()
	cal = new_food_cal()
	size = new_serving()
	if confirm_new_food(name, cal, size):
		url = ROOT_URL + 'add_food?name=' + name + '&cal=' + cal + '&serving_size=' + size
		response = requests.post(url)
		return True
	else:
		return False

'''
Asks user for name of a food.
'''
def new_food_name():
	name = input('Enter the name of the food item: ')
	base_url = ROOT_URL + 'check_food?f='
	url = base_url + name
	response = requests.get(url)
	resp_code = response.text
	while ctf.are_same_str(resp_code, "1") == 1:
		name = input('Food already exists in server. Please enter another food item: ')
		url = base_url + name
		response = requests.get(url)
		resp_code = response.text
	return name

'''
Asks for valid calorie amount (must be a positive number).
'''
def new_food_cal():
	cal = input('Enter the total calories in the food: ')
	while(True):
		try:
			test = float(cal)
			if test < 0:
				print('Invalid calorie value. Type in a positive number only.')
				cal = input('Enter the total calories in the food: ')
				continue
			break
		except ValueError:
			print('Invalid calorie value. Type in a valid number only.')
			cal = input('Enter the total calories in the food: ')
	return cal

'''
Asks for valid serving amount (must be a positive number).
'''
def new_serving():
	size = input('Enter serving size (in grams): ')
	while(True):
		try:
			test = float(size)
			if test < 0:
				print('Invalid serving size value. Type in a positive number only.')
				size = input('Enter serving size (in grams): ')
				continue
			break
		except ValueError:
			print('Invalid serving size value. Type in a valid number only.')
			size = input('Enter serving size (in grams): ')
	return size

'''
Asks users for number of servings consumed (must be a positive number).
'''
def ask_for_serving_amount():
	size = input('Enter number of servings consumed: ')
	while(True):
		try:
			test = float(size)
			if test < 0:
				print('Invalid serving amount. Type in a positive number only.')
				size = input('Enter number of servings consumed: ')
				continue
			break
		except ValueError:
			print('Invalid serving amount. Type in a valid number only.')
			size = input('Enter number of servings consumed: ')
	return size

'''
Outputs summary of food to be added. Asks user for confirmation.
'''
def confirm_new_food(name, cal, size):
	print('\nNew food summary:')
	print('Name:', name)
	print('Total calories:', cal)
	print('Serving size:', size, 'g')
	inp = input('\nConfirm food (y/n)?: ')
	while ctf.are_same_str(inp,"y") == 0 and ctf.are_same_str(inp,"n") == 0:
		print('Invalid input. Type in either \'y\' or \'n\'.')
		inp = input('Confirm user (y/n)?: ')
	if inp == "y":
		return True
	else:
		return False

'''
Asks for a food name as a query and prints out food info if match found.
'''
def search_food():
	q = input('\nEnter a food name: ')
	url = ROOT_URL + 'get_food?q=' + q
	response = requests.get(url)
	food = response.json()
	if bool(food):
		print('\nResult:')
		print('Name:', food['name'])
		print('Total calories:', food['calories'])
		print('Serving size:', str(food['serving_size']), 'g')
	else:
		print('\nNo results found.')

'''
Lists all food names in foods.json.
'''
def list_all_foods():
	url = ROOT_URL + 'get_all_foods'
	response = requests.get(url)
	foods = response.json()
	if not bool(foods):
		print('List is empty. Please add in some food items.')
		return
	print('\n*** Food List ***')
	for f in foods:
		print(f)
	print('\nEnd of list...\n')

'''
Conducts update on a user attribute. Asks for attribute to change and then asks
for input based on attribute.
'''
def update_user(user):
	user_attr_sel_str = make_sels_str(user_attr)

	sel = user_interaction(user_attr_sel_str, len(user_attr))
	while ctf.are_same_str(sel, "") == 1:
		print(INVALID_INPUT_MSG)
		sel = user_interaction(user_attr_sel_str, len(user_attr))
	attr_str = user_attr[int(sel)]

	val = ''
	if ctf.are_same_str(attr_str, 'password') == 1:
		val = input('Enter a password: ')
	elif ctf.are_same_str(attr_str, 'first_name') == 1:
		val = input('Enter your first name: ')
	elif ctf.are_same_str(attr_str, 'last_name') == 1:
		val = input('Enter your last name: ')
	elif ctf.are_same_str(attr_str, 'age') == 1:
		val = new_age()
	elif ctf.are_same_str(attr_str, 'gender') == 1:
		val = new_gender()
	elif ctf.are_same_str(attr_str, 'height') == 1:
		val = new_height()
	elif ctf.are_same_str(attr_str, 'activity_level') == 1:
		val = new_act_lvl()
	else:
		val = new_goal()

	if confirm_user_update(attr_str, val):
		url = ROOT_URL + 'update/user/' + attr_str + '?username=' + user['username'] + '&val=' + val
		response = requests.post(url)
		print('\nUpdate successful')
		return response.json()
	else:
		print('\nUser update cancelled.')
		return user

'''
Asks user to confirm user attribute update.
'''
def confirm_user_update(attr, val):
	print('\nUser update summary:')
	print('Attribute to update:', attr)
	print('New value:', val)
	inp = input('\nConfirm change (y/n)?: ')
	while ctf.are_same_str(inp,"y") == 0 and ctf.are_same_str(inp,"n") == 0:
		print('Invalid input. Type in either \'y\' or \'n\'.')
		inp = input('Confirm user (y/n)?: ')
	if inp == "y":
		return True
	else:
		return False

'''
Conducts update on a food attribute. Asks for attribute to change and then asks
for input based on attribute.
'''
def update_food():
	name = validate_food_name()

	food_attr_sel_str = make_sels_str(food_attr)

	sel = user_interaction(food_attr_sel_str, len(food_attr))
	while ctf.are_same_str(sel,"") == 1:
		print(INVALID_INPUT_MSG)
		sel = user_interaction(food_attr_sel_str, len(food_attr))
	attr_str = food_attr[int(sel)]

	val = ''
	if ctf.are_same_str(attr_str, 'calories') == 1:
		val = new_food_cal()
	else:
		val = new_serving()

	if confirm_food_update(name, attr_str, val):
		url = ROOT_URL + 'update/food/' + attr_str + '?name=' + name + '&val=' + val
		response = requests.post(url)
		return True
	else:
		return False

'''
Asks for name of food and then checks if food exists in foods.json.
'''
def validate_food_name():
	name = input('Enter name of food to update: ')
	base_url = ROOT_URL + 'check_food?f='
	url = base_url + name
	response = requests.get(url)
	resp_code = response.text
	while ctf.are_same_str(resp_code, "0") == 1:
		name = input('Food item cannot be found. Please enter the name of the food properly: ')
		url = base_url + name
		response = requests.get(url)
		resp_code = response.text
	return name

'''
Guides user in deleting food item.
'''
def delete_food():
	name = validate_food_name_delete()
	inp = input('\nAre you sure you want to delete food item (y/n)?: ')
	while ctf.are_same_str(inp,"y") == 0 and ctf.are_same_str(inp,"n") == 0:
		print('Invalid input. Type in either \'y\' or \'n\'.')
		inp = input('\nAre you sure you want to delete food item (y/n)?: ')
	if inp == "y":
		url = ROOT_URL + 'delete_food?f=' + name
		response = requests.delete(url)
		return True
	else:
		return False

'''
Asks user for existing food item to delete.
'''
def validate_food_name_delete():
	name = input('Enter name of food to delete: ')
	base_url = ROOT_URL + 'check_food?f='
	url = base_url + name
	response = requests.get(url)
	resp_code = response.text
	while ctf.are_same_str(resp_code, "0") == 1:
		name = input('Food item cannot be found. Please enter the name of the food properly: ')
		url = base_url + name
		response = requests.get(url)
		resp_code = response.text
	return name

'''
Asks user to confirm food attribute update.
'''
def confirm_food_update(name, attr, val):
	print('\nFood update summary:')
	print('Food to update:', name)
	print('Attribute to update:', attr)
	print('New value:', val)
	inp = input('\nConfirm change (y/n)?: ')
	while ctf.are_same_str(inp,"y") == 0 and ctf.are_same_str(inp,"n") == 0:
		print('Invalid input. Type in either \'y\' or \'n\'.')
		inp = input('Confirm user (y/n)?: ')
	if inp == "y":
		return True
	else:
		return False

'''
Lists user's weight entries by date in descending order.
'''
def list_weight_history(user):
	print('\nUser Weight History:')
	hist = user['weight_history']
	dates = []
	for i in hist:
		dates.append(i)
	dates.sort(reverse=True)
	for d in dates:
		w = hist[d]
		pounds = '(' + '{:.2f}'.format(ctf.kg_to_lb(w)) + ' lb)' 
		print(d, '-->', '{:.2f}'.format(w), 'kg', pounds)

'''
Lists user's calorie entries by date in descending order.
'''
def list_cal_history(user):
	print('\nUser Calorie History:')
	hist = user['cal_history']
	dates = []
	for i in hist:
		dates.append(i)
	dates.sort(reverse=True)
	for d in dates:
		print(d, '-->', str(hist[d]), 'cal')
