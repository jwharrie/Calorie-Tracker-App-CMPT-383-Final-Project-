# Project Goal

The project is a **calorie tracker** application. Calorie trackers help users reach body weight goals by allowing users to log in their body weight and calorie consumption. The app is great for helping people of all fitness levels control their body weight. Health and fitness will always be a relevant market. This makes a calorie tracker a relevant project for today and the future.

# Programming Languages

The following three programming languages were used for the project:

* **Python**: runs the main application `ctmain.py` that interacts with users. Codes module `ctmodule.py` that runs logic involving user interactions and sends HTTP requests to Node.js server. Python will store user information, which can vary based on the amount of weight and calorie entries they have. Calls C-implemented functions when required.
* **Javascript (Node.js)**: runs server `server.js` that receives requests from Python code and sends responses. Javascript is run under the **Node Express** framework for fast, asynchronous and event-driven performance. User and food data are stored in the **JSON** format, so Javascript is used to create/modify JSON objects read/write to `.json` files. 
* **C**: codes `ctf.c` functions that run simple but important operations needed by the main application. C is best suited for these calculations because it is statically-typed and statically-bound, therefore improving performance compared to dynamically-typed, dynamically-bound languages like Python.

# Cross-Language Communication

Python and Javacript code communicate together using RPC REST libraries in both languages. Python code is the client while Javascript code is the server.

Python communicates with C code using SWIG, an FFI.

# Commands to get project running

## Required

First run vagrant:
```
vagrant up
```
If you need to, use `provision` command:
```
vagrant provision
```
Execute `vagrant ssh`.

Navigate to the `calorie-tracker-app` directory:
```
cd project/calorie-tracker-app
```
Run the following command to keep Node.js server running in the background:
```
forever start ./ctserver/server.js
```
In case that the Express framework is not installed in `ctserver` directory, go into it and then run
```
npm install express --save
```
Finally, run the following command to start the application:
```
python3 ctapp/ctmain.py
```
## Optional

To check if the server is running, run the following command to list Node.js programs currently running:
```
forever list
```
To stop the server, run
```
forever stop 0
```
To rebuild the Python module containing C code, run `./build.sh` inside the `ctapp` directory.

# Project Features

The application uses a command-line user interface. Users interact with the command line when prompted to. The program will instruct users what to type in. The program will validate inputs to make sure instructions are followed. If invalid input is given, the application will keep asking for valid input until it is given.

The user can either cancel an action or navigate back to a previous interface using `CTRL-C`.

The user can shut down the program any time using `CTRL-D`.

## Start-up

This interface appears when you first run the calorie tracker. Here you can
* **log in**
* **create a new user**

At start-up, the app will automatically send a request to the server to test connectivity. The server should send back a *special string*. If the string is sent back, the user can continue to use the app. Otherwise a message pops up telling the user to run the server and then the app shuts down.

### Create a new user

The user will be asked for a
* *username*
* *password*
* *first name*
* *last name*
* *age*
* *gender*
* *height* (in centimetres)
* *activity level*, and
* *weight goal*

The user can then read a summary of their inputs and confirm them if they wish. The entries are then sent to the server to create a user JSON object and be written into `users.json`. The user will return to the start-up interface afterwards.

### Log in

The user will be asked for a *username* and *password*. The app will check with the server to see if the username-password combination matches. If they do, the server responds by sending back the user's JSON object containing the user's information. If not, the server sends back an empty JSON object, which the main application interprets as a failed login.

## Main Menu

Here a user can
* **log in today's weight**
* **update today's calories**
* enter the **food menu** interface
* list **user stats**
* **update user information**
* view the user's **weight history**
* view the user's **calorie consumption history**

It should be noted that each time a user logs in, the app will check if a weight or calorie record is recorded for today in the user's history. If not, then the user's weight and calorie record will be created for today and be each set to **0** and **None** respectively.

### Log in Today's Weight

The user will be asked to enter their weight for today in kilograms. The app will send the value to the server, where the server will update the user's weight record for today. The server will send back the updated user JSON object. The app will update the user information with the sent JSON object.

The user can update the weight for today as many times as they want.

### Update Today's Calories

The user will be asked to enter the *name* of a food item and the *number of servings* consumed of the food item. The user will be presented with a summary of the inputs to confirm. The user will also be presented with the new total calories for today. If confirmed the app will send the value to the server where the server will update the user's total calories for today. The server will send back the updated user JSON object. The app will update the user information with the sent JSON object.

### User Stats

The app will output the following information:

* first name
* last nameUsed to create a
* activity level
* today's logged weight, in kilograms and pounds
* body mass index (BMI)
* basal metabolic rate (BMR), the amount of calories required for the body at rest (with no physical activity at all) 
* user's weight goal
* calories required to maintain current weight
* calories required daily to reach goal
* calorie progress for today so far

### User Weight History

The app will output a list of all weight records by descending order of dates. The list will show the weight in both kg and lb.

### User Calorie History

Same as **User Weight History** except it outputs a record of total calories consumed for each day.

### Update User Information

The user will be asked to select any user attribute to change (except for *username*) and then select/enter a new value. The app will output a summary of the change, which the user can confirm. If confirmed, the value will be sent to the server. The server will update the user and then send back the updated user JSON object for the application.

## Food Menu

Here the user can
* **search** for a food item
* **add** a new food
* **update** information on a food
* **list all foods** in the system
* **delete** a food item

### Search for Food

The user will be asked to enter a food name. The query is then sent to the server and will check if the food exists. If it does the food JSON object will be sent back and the app will list the attributes of the food. Otherwise a message string will output about no results found. After either case the user will be asked to enter another query. This continues until the user exit the search with `CTRL-C`.

### Add New Food

The user will be asked for a
* *food name*
* *calorie amount*
* *serving size*

The user can then read a summary of their inputs and confirm them if they wish. The entries are then sent to the server to create a food JSON object and be written into `foods.json`.

### Update Food Item

It's the same as updating a user, except you can only update the calorie amount and the serving size.

### Delete Food Item

It's like updating a food item except you type in the name of an existing food item in the system and then confirm the deletion. Python should send in a delete request and then delete the entry in `foods.json`.

### About deleting users

It should be noted that the calorie tracker **cannot** delete users. I didn't want to give standard users that privilege.

## JSON Objects

### User

```
{
    'username': string,
	'password': string,
	'first_name': string,
	'last_name': string,
	'age': number,
	'gender': string,
	'height': number,
	'activity_level': string,
	'goal': string,
	'weight_history': JSON object containing Weight JSON objects,
	'cal_history': JSON object containing Calorie JSON objects,
	'weight_today': number,
	'cal_today': number
}
```
When stored in `users.json`, *username* is used as the object key.

### Food

```
{
    'name': string,
	'calories': number,
	'serving_size': number
}
```
When stored in `foods.json`, *name* is used as the object key.

For both User and Food objects, their keys are also stored in the objects for user output.

### Weight/Calorie
```
{
    'date': number
}
```

## Categories

### Activity Levels
* sedentary
* lightly active (light exercise/sports 1-3 days/week)
* moderatetely active (moderate exercise/sports 3-5 days/week)
* very active (hard exercise/sports 6-7 days a week) 
* extra active (very hard exercise/sports & physical job or 2x training)
### Weight Goals
* lose 1 kg per week
* lose 0.5 kg per week
* lose 0.25 kg per week
* maintain weight
* gain 0.25 kg per week
* gain 0.5 kg per week
* gain 1 kg per week