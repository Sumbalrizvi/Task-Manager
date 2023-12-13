#*****************COMPULSORY TASK 1 OF FOLDER SE T17**************** 

#******************MODIFIED TASK MANAGEMENT PROGRAM************************

#=====importing libraries==========
from datetime import date
import time

#=====Defining Functions===========

# Creating a function for user dictionary
def create_user_dict():
    # Creating the empty dictionary named user_info
    global user_info # making the user_info global to be used later in program
    user_info = {}
    
    # Reading the user.txt and assigning details to the dictionary
    with open("user.txt", "r", encoding="utf-8") as users:
        for line in users:
            # Splitting each line into a list of two items and removing \n from
            # each line
            list_line = line.strip("\n").split(", ")
            # Adding key:value pair to dictionary
            user_info[list_line[0]] = list_line[1]


# Creating a function for tasks dictionary
def create_task_dict():
    # Creating the empty tasks dictionary 
    global task_dict
    task_dict = {}
    # Opening tasks.txt here and adding each task to a dictionary with a number value as
    # key if it matches the username
    with open("tasks.txt", "r", encoding="utf-8") as tasks:
        for line in enumerate(tasks, 1):
            task_dict[line[0]] = line[1]

#=========TASK MANAGEMENT===========
#Present a menu to user of 4 options or to exit the program.
# Admin user gets a different menu with an extra option to view statistics about how many tasks and users are registered. 
# All other users get standard menu 
# Printing the regular menu:

def print_menu():
    print("""Select one of the following options below:
a -  Add a task
va - View all tasks
vm - View my tasks
e -  Exit
""")


# Printing the admin menu
def print_admin_menu():
    print("""Select one of the following options below:
r -  Register a new user
a -  Add a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
e -  Exit
""")


# Defining a function to register a user:
def reg_user():
    create_user_dict()
    # Checking that user is admin
    if username_attempt == "admin":
        # Asking user for a new username and password
        new_username = input("Please enter a new username:\n")
        # Checking if the user already exists and allows admin to try again if it
        # does
        while new_username in user_info:
            new_username = input("This user already exists. Please try again.\
\n")
        new_password = input("Please enter a new password for this user:\n")
        confirm_password = input("Please confirm your password:\n")
        # Checking both password entries to check they
        # are the same
        while new_password != confirm_password:
            new_password = input("Passwords were not the same. Please \
enter your new password again.\n")
            confirm_password = input("Please confirm your password:\n")
        # When the passwords match, writing new user info
        # to user.txt
        with open("user.txt", "a") as user:
            user.write(f"\n{new_username}, {new_password}")
            print("User has been added successfully.\n")
    # If user is not admin, printing an error message
    else:
        print("Sorry, only the admin can register a new user.\n")


# Defining a function to add a new task to tasks.txt:
def add_task():
    create_user_dict()
    # Prompting user for task data
    user_assigned = input("Who is this task assigned to?\n")
    # Checking that user is in user.txt
    while user_assigned not in user_info:
        user_assigned = input("Username not recognised. Please try \
again.\n")
    task_title = input("What is the title of this task?\n")
    task_description = input("Please enter a description for this task:\n")
    due_date = input("When is this task due? Please enter the full date with \
the shortened month (e.g. \"October\" as \"Oct\"):\n")
    # Getting current date 
    today_date = date.today().strftime("%d %b %Y")
    complete = "No"
    # Writing the task info to tasks.txt
    with open("tasks.txt", "a") as tasks:
        tasks.write(f"\n{user_assigned}, {task_title}, \
{task_description}, {today_date}, {due_date}, {complete}")
        print("Task has been added successfully.\n")


# Defining a function to view all tasks:
def view_all():
    create_task_dict()
    for tasknum, details in task_dict.items():
        details = str(details).split(", ")
        details[5] = details[5].strip("\n")  # Removing \n from end of line
        # Printing all tasks in an easy to read format
        print(f'''\
--------------------------------------------------------------------------------
Task Number:        {tasknum}
Task:               {details[1]}
Assigned to:        {details[0]}
Date assigned:      {details[3]}
Due date:           {details[4]}
Task complete?      {details[5]}
Task description:
{details[2]}
--------------------------------------------------------------------------------\
''')


# Defining a function to view user tasks:
def view_mine():
    create_task_dict()
    # Checking if user has tasks assigned
    if username_attempt in str(task_dict):
        for tasknum, details in task_dict.items():
            details = str(details).split(", ")
            details[5] = details[5].strip("\n")  # Removing \n from end of line
            # Printing the task details for user
            if details[0] == username_attempt:
                print(f'''\
--------------------------------------------------------------------------------
Task Number:        {tasknum}
Task:               {details[1]}
Assigned to:        {details[0]}
Date assigned:      {details[3]}
Due date:           {details[4]}
Task complete?      {details[5]}
Task description:
{details[2]}
--------------------------------------------------------------------------------\
''')
        edit_task_menu()
    else:
        print("You currently have no tasks assigned.\n")


# Defining a function to edit task
def edit_task():
    # Checking if task is marked as complete
    if "Yes" in task_dict[edit_task_response]:
        print("Sorry, this task has already been marked as \
complete.\n")
    else:
        print("Would you like to change the user the task is assigned to \
(u) or the due date (d)?")
        username_or_date = input("Please enter your selection \
here:").lower().replace(" ", "")
        # If u selected, replacing username with a new username in
        # users.txt
        if username_or_date == "u":
            new_username = input("Please enter the new user you \
would like to assign this task to:")
            
            # Checking that user is in user.txt
            while new_username not in user_info:
                new_username = input("Username not recognised. \
Please try again.\n")
            # Find corresponding dictionary entry and changes
            # username to new user then rewrites tasks.txt
            # with the new info
            edited_task = task_dict[edit_task_response]
            edited_task = str(edited_task).split(", ")
            edited_task[0] = edited_task[0].replace(edited_task[0],
                                                    new_username)
            edited_task = ", ".join(edited_task)
            task_dict[edit_task_response] = edited_task
            with open("tasks.txt", "w", encoding="utf-8") as tasks:
                for tasknum, details in task_dict.items():
                    tasks.writelines(details)
                print("Username has been edited successfully.\n")
        # If the user selects d,
        elif username_or_date == "d":
            print("What date would you like to change the due date \
to? Please enter the full date with the shortened month (e.g. \"October\" \
as \"Oct\")")
            new_date = input("Enter your response here:")
            create_task_dict()
            # Replacing old due date with new due date and writing to
            # file
            edited_task = task_dict[edit_task_response]
            edited_task = str(edited_task).split(", ")
            edited_task[4] = edited_task[4].replace(edited_task[4],
                                                    new_date)
            edited_task = ", ".join(edited_task)
            task_dict[edit_task_response] = edited_task
            with open("tasks.txt", "w", encoding="utf-8") as tasks:
                for tasknum, details in task_dict.items():
                    tasks.writelines(details)
                print("Date has been edited successfully.\n")
        else:
            print("Input not recognised. Please try again.\n")


# Defininf a function to mark as complete
def mark_as_complete():
    # Checking if task is marked as complete
    if "Yes" in task_dict[edit_task_response]:
        print("This task is already complete!!!\n")
    else:
        # Replacing "No" with "Yes" and writes to file
        edited_task = task_dict[edit_task_response]
        edited_task = str(edited_task).replace("No", "Yes")
        task_dict[edit_task_response] = edited_task
        with open("tasks.txt", "w", encoding="utf-8") as tasks:
            for tasknum, details in task_dict.items():
                tasks.writelines(details)
            print("Task has been marked as complete.\n")


# Defining a function to Edit task menu
def edit_task_menu():
    print("Would you like to edit a task? Press the corresponding task number \
or \"-1\" to return to the main menu.")
    global edit_task_response
    edit_task_response = int(input("Please enter your selection here:"))
    create_task_dict()
    create_user_dict()
    try:
        task_dict[edit_task_response]
        if edit_task_response == -1:
            return  # Returning user to main menu
        else:
            print("Would you like to edit the task (e) or mark as complete \
(mc)?")
            edit_or_complete = input("Enter your selection here:")\
                .lower().replace(" ", "")
            if edit_or_complete == "e":
                edit_task()
            elif edit_or_complete == "mc":
                mark_as_complete()
            else:
                print("Input not recognised. Please try again.")
    # Printing an error message if the task number is not in dictionary
    except KeyError as key:
        print(f"Task number {key} was out of range, please try \
again.\n")


# \defining a function to display statistics
def display_stats():
    create_task_dict()
    create_user_dict()
    # Checking that user is admin
    if username_attempt == "admin":
        print("Would you like display the user overview (u) or task overview \
(t)")
        task_or_user = input("Enter you selection here:")\
            .lower().replace(" ", "")
        if task_or_user == "u":
            # Generating user report for reading if not already generated
            generate_user_overview()
            with open("user_overview.txt", "r", encoding="utf-8") as \
                    user_overview:
                for line in user_overview:
                    print(line)
        elif task_or_user == "t":
            # Generating task report if not already there
            generate_task_overview()
            with open("task_overview.txt", "r", encoding="utf-8") as \
                    task_overview:
                for line in task_overview:
                    print(line)
        else:
            print("Input not recognised. Please try again.")
    # If user is not admin, printing an error message
    else:
        print("Nice try finding this option but only the admin can display \
statistics!\n")


# Defining a function to generate task overview report
def generate_task_overview():
    create_task_dict()
    # Creating and casting 'today_date' to date to compare with due date
    today_date = date.today().strftime("%d %b %Y")
    today_date = time.strptime(today_date, "%d %b %Y")
    # Creates counts
    completed = 0
    uncompleted = 0
    overdue = 0
    for tasknum, details in task_dict.items():
        if "Yes" in details:
            completed += 1
        elif "No" in details:
            uncompleted += 1
            # Creating sub-count for uncompleted and overdue
            details = str(details).split(", ")
            due_date = details[3]
            due_date = time.strptime(due_date, "%d %b %Y")
            if today_date > due_date:
                overdue += 1
    # Writing task overview info to file 'task_overview.txt'
    task_overview = f"""\
--------------------------------------------------------------------------------
Task Overview
--------------------------------------------------------------------------------
Total number of tasks generated:  {len(task_dict)}
Total number of completed tasks:  {completed}
Total number of uncompleted tasks: {uncompleted}
Total number of tasks that are uncompleted and overdue: {overdue}
Percentage of tasks that are incomplete: {uncompleted/len(task_dict)*100}%
Percentage of tasks that are overdue:   \
{overdue/len(task_dict)*100}%
--------------------------------------------------------------------------------\
"""
    with open("task_overview.txt", "w", encoding="utf-8") as\
            task_overview_text:
        task_overview_text.write(task_overview)


# Defining a function to generate user overview report
def generate_user_overview():
    create_task_dict()
    create_user_dict()
    # Finding total number of users and tasks and adding to a string
    total_users = len(user_info)
    total_tasks = len(task_dict)
    user_overview = f"""\
--------------------------------------------------------------------------------
User Overview
Total number of users:  {total_users}
Total number of tasks:  {total_tasks}"""
    # Getting today's date and converting it to date format to match due date
    today_date = date.today().strftime("%d %b %Y")
    today_date = time.strptime(today_date, "%d %b %Y")
    # Creating empty dictionaries for different categories
    task_count_dict = {}
    user_uncompleted = {}
    user_overdue = {}
    user_completed = {}
    # For every username, counting the number of tasks assigned to them and adding
    # to a new dictionary
    for username, password in user_info.items():
        task_count = 0
        uncompleted_count = 0
        overdue_count = 0
        for tasknum, details in task_dict.items():
            details = str(details).strip("\n").split(", ")
            if details[0] == username:
                task_count += 1
                # Creating a sub-count for uncompleted by that user
                if details[5] == "No":
                    uncompleted_count += 1
                    due_date = details[3]
                    due_date = time.strptime(due_date, "%d %b %Y")
                    # Creating another sub-count for overdue
                    if due_date < today_date:
                        overdue_count += 1
        completed_count = task_count - uncompleted_count
        # Updating the dictionaries with the info for each user
        task_count_dict.update({username: task_count})
        user_uncompleted.update({username: uncompleted_count})
        user_completed.update({username: completed_count})
        user_overdue.update({username: overdue_count})
        # Adding info to 'user_overview' string checking that task number is
        # greater than zero to avoid error
        if task_count > 0:
            user_overview += f"""\

--------------------------------------------------------------------------------
User: {username}
--------------------------------------------------------------------------------
Total number of tasks assigned to user: {task_count_dict[username]}
Percentage of tasks assigned to user:   \
{task_count_dict[username]/total_tasks*100}%
Percentage of tasks completed by user:  \
{user_completed[username]/task_count_dict[username]*100}%
Percentage of tasks still to be completed by user:  \
{user_uncompleted[username]/task_count_dict[username]*100}%
Percentage of tasks that are overdue:   \
{user_overdue[username]/task_count_dict[username]*100}%
--------------------------------------------------------------------------------\
"""
        else:
            user_overview += f"""\

--------------------------------------------------------------------------------
User: {username}
--------------------------------------------------------------------------------
Total number of tasks assigned to user: {task_count_dict[username]}
Percentage of tasks assigned to user:   NA
Percentage of tasks completed by user:  NA
Percentage of tasks still to be completed by user: NA
Percentage of tasks that are overdue:  NA
--------------------------------------------------------------------------------\
"""
# Writing string to user_overview.txt
    with open("user_overview.txt", "w", encoding="utf-8") \
            as user_overview_text:
        user_overview_text.write(user_overview)


# Defining a function to generate reports
def generate_reports():
    
    # Checks if user is admin before generating reports
    if username_attempt == "admin":
        generate_task_overview()
        generate_user_overview()
        print("Reports have been generated.\n")
    else:
        print("Sorry, only the admin can generate reports.\n")

# ------------------------------------------------------------------------------


# ====Login Section====

create_user_dict()

# Asking user to input their username and checking it against the dictionary
username_attempt = input("Please enter your username:\n")
while username_attempt not in user_info:
    username_attempt = input("Username not found. Please try again.\n")

# Asking the user for their password and checking it against the corresponding
# password value for their username key
password_attempt = input("Please enter your password:\n")
while password_attempt != user_info[username_attempt]:
    password_attempt = input("Incorrect password. Please try again.\n")


# ====Menu Selection====

while True:
    # If the user is admin, displaying a different menu
    if username_attempt == "admin":
        print_admin_menu()
    # Otherwise, displaying the regular menu
    else:
        print_menu()
    # Asking user for their input, making sure input is lowercase and whitespace
    # is removed
    menu = input("Please enter your selection here:").lower().replace(" ", "")
    # Registering a new user
    if menu == 'r':
        reg_user()
    # Adding a task to tasks.txt
    elif menu == 'a':
        add_task()
    # Reading tasks.txt and outputs them in a user friendly manner
    elif menu == 'va':
        view_all()
    # Only printing tasks if username is the same as the team member assigned
    elif menu == 'vm':
        view_mine()
    # Generating reports
    elif menu == 'gr':
        generate_reports()
    # Displaying statistics
    elif menu == 'ds':
        display_stats()
    # Exiting the program
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    # If the user does not enter one of the options, displaying an error message
    else:
        print("You have made a wrong choice, please try again.")

# ------------------------------------------------------------------------------
# References
# ------------------------------------------------------------------------------
# (1) Used info from here to understand functions:
# https://docs.python.org/3/library/functions.html#open
#
# (2) Used info from here for use of the datetime module:
# https://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/

# (3) Used info from here to understand how to generate reports by using user and tasks dictionaries:
# https://github.com/tnaccarato/hyperion-dev-L1-capstone-II/blob/main/task_manager.py