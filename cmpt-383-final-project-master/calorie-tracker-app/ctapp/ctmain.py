import ctmodule

INVALID_INPUT_MSG = '\nInvalid option. Please type in only a number (Type "0" to select option (0), etc.).'
STARTUP_HEADER = '\n*** Start-Up Menu ***'
MAIN_MENU_HEADER = '\n*** Main Menu ***'
FOOD_MENU_HEADER = '\n*** Food Menu ***'

startup_sels = ['Login', 'Add New User']
main_sels = ['Log in Today\'s Weight', 'Update Today\'s Calories', 'Food Menu', 'User Stats', 'Update User Info', 'User Weight History', 'User Calorie History']
food_sels = ['Search for Food', 'Add New food', 'Update Food Item', 'List All Foods', 'Delete a Food Item']

def startup_interface():
    print('*** CMPT 383 Final Project: Calorie Tracker App (Summer 2020) ***')
    print('***             Author: Jacob Wharrie (301220132)             ***')
    print(STARTUP_HEADER)
    startup_sels_str = ctmodule.make_sels_str(startup_sels)
    while(True):
        try:
            si = ctmodule.user_interaction(startup_sels_str, len(startup_sels))
        except KeyboardInterrupt:
            print('\nShutting down...')
            return
        if si== "0":
            login_interface()
        elif si == "1":
            add_new_user_interface()
        else:
            print(INVALID_INPUT_MSG)

def add_new_user_interface():
    print('\n*** User Creation')
    try:
        new_user_created = ctmodule.add_new_user()
        if not new_user_created:
            print('\nUser creation halted.')
            print(STARTUP_HEADER)
            return
    except KeyboardInterrupt:
        print('\nUser creation halted.')
        print(STARTUP_HEADER)
        return
    print('\nUser creation completed. Log in to access your new account.')
    print(STARTUP_HEADER)

def login_interface():
    print('\n*** Login Menu ***')
    while(True):
        try:
            user = ctmodule.login_attempt()
        except KeyboardInterrupt:
            print(STARTUP_HEADER)
            return
        if not bool(user):
            print('Incorrect username and/or password. Please try again.')
        else:
            print('Success. Logging in as ' + user['username'] + '...')
            user = ctmodule.update_user_at_login(user)
            main_interface(user)

def main_interface(user):
    print(MAIN_MENU_HEADER)
    main_sels_str = ctmodule.make_sels_str(main_sels)
    while(True):
        try:
            mi = ctmodule.user_interaction(main_sels_str, len(main_sels))
        except KeyboardInterrupt:
            print('\nLogging out...')
            return
        if mi == "0":
            try:
                user = ctmodule.log_weight_today(user)
                print('\nWeight logged successfully.')
                print(MAIN_MENU_HEADER)
            except KeyboardInterrupt:
                print('\nLogging weight cancelled.')
                print(MAIN_MENU_HEADER)
        elif mi == "1":
            try:
                user = ctmodule.update_calories(user)
                print(MAIN_MENU_HEADER)
            except KeyboardInterrupt:
                print('\nCalories update cancelled.')
                print(MAIN_MENU_HEADER)
        elif mi == "2":
            food_interface()
        elif mi == "3":
            ctmodule.display_user_stats(user)
            print(MAIN_MENU_HEADER)
        elif mi == "4":
            try:
                print('\n*** Updating User Info')
                user = ctmodule.update_user(user)
            except KeyboardInterrupt:
                print('\nUser update cancelled.')
                print(MAIN_MENU_HEADER)
        elif mi == "5":
            ctmodule.list_weight_history(user)
            print(MAIN_MENU_HEADER)
        elif mi == "6":
            ctmodule.list_cal_history(user)
            print(MAIN_MENU_HEADER)
        else:
            print(INVALID_INPUT_MSG)

def food_interface():
    print(FOOD_MENU_HEADER)
    food_sels_str = ctmodule.make_sels_str(food_sels)
    while(True):
        try:
            fi = ctmodule.user_interaction(food_sels_str, len(food_sels))
        except KeyboardInterrupt:
            print(MAIN_MENU_HEADER)
            return
        if fi == "0":
            food_search_interface()
        elif fi == "1":
            add_food_interface()
        elif fi == "2":
            update_food_interface()
        elif fi == "3":
            ctmodule.list_all_foods()
        elif fi == "4":
            delete_food_interface()
        else:
            print(INVALID_INPUT_MSG)

def food_search_interface():
    print('\n*** Food Search')
    while(True):
        try:
            ctmodule.search_food()
        except KeyboardInterrupt:
            print('\nFood search ended.')
            print(FOOD_MENU_HEADER)
            return

def add_food_interface():
    print('\n*** Adding Food')
    try:
        new_food_added = ctmodule.add_food()
        if not new_food_added:
            print('\nAdding food halted.')
            print(FOOD_MENU_HEADER)
            return
    except KeyboardInterrupt:
        print('\nAdding food halted.')
        print(FOOD_MENU_HEADER)
        return
    print('\nNew food item added.')
    print(FOOD_MENU_HEADER)

def update_food_interface():
    print('\n*** Updating Food')
    try:
        food_updated = ctmodule.update_food()
        if not food_updated:
            print('\nFood update cancelled.')
            print(FOOD_MENU_HEADER)
            return
    except KeyboardInterrupt:
        print('\nFood update cancelled.')
        print(FOOD_MENU_HEADER)
        return
    print('\nFood item updated.')
    print(FOOD_MENU_HEADER)

def delete_food_interface():
    print('\n*** Deleting Food')
    try:
        food_updated = ctmodule.delete_food()
        if not food_updated:
            print('\nFood deletion cancelled.')
            print(FOOD_MENU_HEADER)
            return
    except KeyboardInterrupt:
        print('\nFood deletion cancelled.')
        print(FOOD_MENU_HEADER)
        return
    print('\nFood item successfully deleted.')
    print(FOOD_MENU_HEADER)

def main():
    ctmodule.startup_test_conn()
    try:
        startup_interface()
    except EOFError:
        print('\nShutting down...')

if __name__ == "__main__":
    main()
