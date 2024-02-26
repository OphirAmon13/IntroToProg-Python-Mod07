# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: Ophir Amon, 2/19/2024
# ------------------------------------------------------------------------------------------ #

# Import necessary functions
from sys import exit
import json
from json.decoder import JSONDecodeError

# Define the Data Variables and constants
MENU: str = '''
    ---- Course Registration Program ----
    Select from the following menu:  
        1. Register a Student for a Course.
        2. Show current data.  
        3. Save data to a file.
        4. Exit the program.
    ----------------------------------------- 
    '''
FILE_NAME: str = "Enrollments.json"
menu_choice: str = "" # Hold the choice made by the user.
students: list = []  # A table of student data

# Define the classes to organize code

class Person: # Creates the Person object

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def __str__(self):
        return f"{self.first_name,self.last_name}"

    @property
    def first_name(self):
        return self.__first_name.title()
    
    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha():
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")
        
    @property
    def last_name(self):
        return self.__last_name.title()
    
    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha():
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

class Student(Person): # Creates the Student object that inherits properties from the Person class
    def __init__(self, first_name: str = "", last_name: str = "", course_name: str = ""):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    def __str__(self):
        return f"{self.first_name,self.last_name,self.course_name}"
    
    def __repr__(self):
        return self.__str__()

    @property
    def course_name(self):
        return self.__course_name
    
    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value


class FileProcessor: # Stores all functions that have to do with .json files
    
    # Function that reads and prints the data from a file
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        try:
            with open(file_name, "r") as file:
                print("First Name \tLast Name \tCourse Name")
                loaded_student_table = json.load(file)
                for item in loaded_student_table:
                        new_student = Student(item["first_name"], item["last_name"], item["course_name"])
                        student_data.append(new_student)
                        print(f"{new_student.first_name} \t\t{new_student.last_name} \t\t{new_student.course_name}")
        except FileNotFoundError as error_message:
            IO.output_error_messages(f"There was an error finding the {file_name} file!", error_message)
        except JSONDecodeError as error_message:
            IO.output_error_messages(f"There was an error reading the data from the {file_name} file!", error_message)
        except Exception as error_message:
            IO.output_error_messages(f"There was an error reading the data from the {file_name} file!", error_message)
    
    # Function that saves data to a file
    @staticmethod
    def write_data_to_file(file_name: str, student_data: list): # Saves all information to JSON file
        try:
            list_of_students: list = []
            for student in student_data:
                student_dict: dict = {
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "course_name": student.course_name,
                    }
                list_of_students.append(student_dict)

            with open(file_name, "w") as file:
                json.dump(list_of_students, file)
                for student in list_of_students:
                    print(f"You have registered {student['first_name']} {student['last_name']} for {student['course_name']}.")
        except Exception as error_message:
            IO.output_error_messages(f"There was an error saving the data to the {file_name} file!", error_message)
        
class IO:

    # Function to output error message whereever needed
    @staticmethod
    def output_error_messages(message: str, error: Exception = None): 
        print(message)
        print(f"Error detail: {error}")

    # Function that prints the menu options
    @staticmethod
    def output_menu(menu: str): # Prints the menu of options
        print(menu)

    # Function that stores the user's menu choice 
    @staticmethod
    def input_menu_choice(): # 
        return input("Please enter a menu option (1-4): ")

    # Function that allows user to add students to the data
    @staticmethod
    def input_student_data(student_data: list): # Adds user to database
        
        try:
            student_first_name = input("Enter the student's first name: ")
            student_last_name = input("Enter the student's last name: ")
            course_name = input("Please enter the name of the course: ")
            new_student = Student(student_first_name, student_last_name, course_name)
        except ValueError as error_message:
            IO.output_error_messages("Only use names without numbers", error_message)
            return
        except Exception as error_message:
            IO.output_error_messages("There was a non-specific error when adding data!", error_message)
            return
            
        student_data.append(new_student) # Adds student to list of all student data
        print(student_data)

    # Function that prints out the current data
    @staticmethod
    def output_student_courses(student_data: list): # Presents all information to the user
        print("First Name \tLast Name \tCourse Name")
        for student in student_data:
            print(f"{student.first_name} \t\t{student.last_name} \t\t{student.course_name}")

    # Function that ends the program
    @staticmethod
    def quit_program(): # Ends the program
        exit()

if __name__ == "__main__":

    FileProcessor.read_data_from_file(FILE_NAME, students)


    while True:
        # Present the menu of choices
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()
           
        # Checks the user's menu choice against different cases           
        match menu_choice:
            case "1":
                IO.input_student_data(students)
            case "2":
                IO.output_student_courses(students)     
            case "3":
                FileProcessor.write_data_to_file(FILE_NAME, students)
            case "4":
                IO.quit_program()
            case _:
                print("ERROR: Please select a valid option")