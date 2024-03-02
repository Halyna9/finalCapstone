# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password


#=====importing libraries===========
import os
from datetime import datetime, date


#Global scope variables
DATETIME_STRING_FORMAT = "%Y-%m-%d"
TODAY = date.today()

# Functions

def ensure_file_exists(file_path):
    """ This function will create the file if it 
    doesn't exist 
    """
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding = "utf-8") as default_file:
            pass

def write_tasks_to_file(file_path, task_list):
    """This function allow user to write new and edited tasks to the text file"""
    
    with open(file_path, "w", encoding = "utf-8") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append("; ".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Your changes has been added to the file.\n")

def reg_user(username_password):
    '''Add a new user to the user.txt file'''

    # - Request input of a new username
    new_username = input("New Username: ")

    # - Make sure user name is not exist already
    while new_username in username_password.keys():
        print("This name is not available. Please use a different name") 
        new_username = input("New Username: ")

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")
     # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "w", encoding = "utf-8") as out_file:
                user_data = []
                for k in username_password:
                    user_data.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_data))

        # - Otherwise you present a relevant message.
    else:
         print("Passwords do no match")

def add_task():
    '''Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task.
            '''
    task_username = input("Name of person assigned to task: ")
    while task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": TODAY,
        "completed": False
    }

    task_list.append(new_task)
    write_tasks_to_file("tasks.txt", task_list)
    
def view_all():
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''
    task_num = 0
    for t in task_list:
        print("_" * 100)
        task_num += 1
        disp_str = f"Task {task_num}: \t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(task_list, curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    while True:
        # - extracted current user tasks and saved it in a list
        curr_user_tasks = [t for t in task_list if t.get('username') == curr_user]

        if len(curr_user_tasks) > 0:

            task_num = 0
            for task in curr_user_tasks:
                task_num += 1
                disp_task = f"-" * 100
                disp_task += f"\nTask {task_num}: \t {task['title']}\n"
                disp_task += f"Assigned to: \t {task['username']}\n"
                disp_task += f"Date Assigned: \t {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_task += f"Due Date: \t {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
                disp_task += f"Task Description: \n {task['description']}\n"
                print(disp_task)
            
            # - make sure the user provides a number as an input
            try:
                selected_task = int(input("If you would like to edit a task, please type a task number, or to exit type -1: "))
            except ValueError:
                print("Invalid input. Please enter a valid number")
                continue

            if selected_task == -1:
                break 

            # - make sure the user provides an existing task number
            if selected_task <= 0 or selected_task > len(curr_user_tasks):
                print("Sorry. we can't find task with this number")
                continue
        
            # checking if the user would like to mark the task as complete
            complete_task = input("Would you like to mark the task as complete? (Yes/No): ").lower()
            chosen_task = curr_user_tasks[selected_task -1] 
            if chosen_task["completed"]:
                    print("Sorry, you can't edit completed tasks")
                    continue
            
            elif complete_task == "yes":  
                chosen_task["completed"] = True
                print("\nYour task has been marked task as completed!\n")
                write_tasks_to_file("tasks.txt", task_list)

            elif complete_task == "no":
                    new_username = input("Reassigned this task to: ")
                    chosen_task["username"] = new_username
                    new_due_date = input("New due date of task (YYYY-MM-DD): ")
                    new_due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                    chosen_task["due_date"] = new_due_date_time
                    print(curr_user_tasks)

                     # write changes to the file
                    write_tasks_to_file("tasks.txt", task_list)
            else:
                print("Invalid input. Please enter 'yes' or 'no'")
                continue
        else:
            print("Sorry, you have no tasks yet.")
            break

def generate_reports(task_list):
    """ This function will create a detailed report about tasks and users. 
    It will also generate 2 text files with task overview and users overview accordingly. 
    """
    # calculating required data for task overview
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task["completed"] )
    unfinished_tasks = sum(1 for task in task_list if not task["completed"])
    overdue_tasks = sum(1 for task in task_list if task["due_date"].date() < TODAY)   
    unfinished_overdue_task = sum(1 for task in task_list if task["due_date"].date() < TODAY and not task["completed"])
    percent_unfinished_tasks = (unfinished_tasks * 100) / total_tasks
    percent_overdue_tasks = (overdue_tasks * 100) / total_tasks

    # Saving required data into a string to be able to print it into console
    task_overview_str = (f"""Task overview:
        1. Total number of tasks: {total_tasks}
        2. Completed tasks: {completed_tasks}
        3. Unfinished tasks: {unfinished_tasks}
        4. Overdue unfinished tasks: {unfinished_overdue_task}
        5. Percentage of unfinished tasks: {percent_unfinished_tasks}
        6. Percentage of overdue tasks: {percent_overdue_tasks}
""")
    print(task_overview_str)

    # saving report into a txt file
    ensure_file_exists("task_overview.txt")
    with open("task_overview.txt", "w", encoding = "utf-8") as task_overview_file:
        task_overview_file.write(task_overview_str)
    
    # Calculating required data for user overview
    total_users = len(username_password)
    user_overview_str = (f"""User overview:
            1. Total number of users: {total_users}
            2. Total number of tasks: {total_tasks}    
            """)

    for user in username_password:
        user_tasks = [task for task in task_list if task["username"] == user]
        if len(user_tasks) > 0:
            user_completed_tasks = sum(1 for task in user_tasks if task["completed"])
            user_unfinished_tasks = sum(1 for task in user_tasks if not task["completed"])
            user_overdue_tasks = sum(1 for task in user_tasks if task["due_date"].date() < TODAY)
            user_overdue_unfinished_tasks = sum(1 for task in user_tasks if task["due_date"].date() < TODAY and not task["completed"])

        
            # Calculate percentages for each user
            user_percent_of_total_tasks = (len(user_tasks) * 100) / total_tasks
            user_percent_completed_tasks = (user_completed_tasks * 100) / len(user_tasks)
            user_percent_unfinished_tasks = (user_unfinished_tasks * 100) / len(user_tasks)
            user_percent_overdue_unfinished_tasks = (user_overdue_unfinished_tasks * 100) / len(user_tasks)
        

            user_overview_str += (f"""    
                {user}:
            - Total number of tasks: {len(user_tasks)}
            - Percentage of the total number of tasks: {user_percent_of_total_tasks:.2f}%
            - Completed tasks: {user_completed_tasks} ({user_percent_completed_tasks:.2f}%)
            - Unfinished tasks: {user_unfinished_tasks} ({user_percent_unfinished_tasks:.2f}%)
            - Overdue unfinished tasks: {user_overdue_unfinished_tasks} ({user_percent_overdue_unfinished_tasks:.2f}%)\n""")
        
        else:
            zero_tasks_user = f"""
                {user}:
            - Total number of tasks: {len(user_tasks)}"""
            
    print(user_overview_str)
    print(zero_tasks_user)

    # saving report into a txt file
    ensure_file_exists("user_overview.txt")
    with open("user_overview.txt", "w", encoding = "utf-8") as user_overview_file:
        user_overview_file.write(user_overview_str)
        user_overview_file.write(zero_tasks_user)

# Create tasks.txt if it doesn't exist
ensure_file_exists("tasks.txt")

with open("tasks.txt", 'r', encoding = "utf-8") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for task_str in task_data:
    curr_task = {}

    # Split by semicolon and manually add each component
    task_components = task_str.split(";")
    curr_task['username'] = task_components[0]
    curr_task['title'] = task_components[1]
    curr_task['description'] = task_components[2]
    curr_task['due_date'] = datetime.strptime(task_components[3].strip(), DATETIME_STRING_FORMAT)
    curr_task['assigned_date'] = datetime.strptime(task_components[4].strip(), DATETIME_STRING_FORMAT)
    curr_task['completed'] = True if task_components[5].strip() == "Yes" else False

    task_list.append(curr_task)


#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
ensure_file_exists("user.txt")

# Read in user_data
with open("user.txt", 'r', encoding = "utf-8") as user_file:
    user_data = user_file.read().split("\n")
    
# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    '''Presenting the menu to the user and 
    making sure that the user input is converted to lower case. 
    '''
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine(task_list, curr_user)

    elif menu == 'gr':
        generate_reports(task_list)
                
    elif menu == 'ds' and curr_user == 'admin': 
        #If the user is an admin they can display statistics about number of users and tasks.
        
        ensure_file_exists("user.txt")
        with open("user.txt", "r", encoding = "utf-8") as user_file:
            user_data = user_file.read().split("\n")   
        num_users = len(user_data)

        ensure_file_exists("tasks.txt")
        with open("tasks.txt", "r", encoding = "utf-8") as task_file:
            task_data = task_file.read().split("\n")
        num_tasks = len(task_data)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")