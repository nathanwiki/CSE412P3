import mysql.connector

# Function to create database
def create_database(database_name):
    mycursor = mydb.cursor()
    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    mycursor.close()

# Function to create table
def create_table():
    mycursor = mydb.cursor()
    mycursor.execute('''CREATE TABLE IF NOT EXISTS AppUser (
                    Username VARCHAR(255) NOT NULL,
                    Email VARCHAR(255) UNIQUE NOT NULL,
                    Password VARCHAR(255) NOT NULL,
                    FitnessLevel INT NOT NULL
                    );''')
    mycursor.execute('''CREATE TABLE IF NOT EXISTS Equipment (
                    EquipmentID INT PRIMARY KEY,
                    EquipmentName VARCHAR(255) NOT NULL
                    );''')
    mycursor.execute('''CREATE TABLE IF NOT EXISTS Workout (
                    WorkoutID INT PRIMARY KEY,
                    WorkoutName VARCHAR(255) NOT NULL,
                    Duration INT NOT NULL,
                    DifficultyLevel INT NOT NULL
                    );''')
    mycursor.execute('''CREATE TABLE IF NOT EXISTS Exercise (
                    ExerciseID INT PRIMARY KEY,
                    ExerciseName VARCHAR(255) NOT NULL,
                    Duration INT NOT NULL,
                    Repetitions INT NOT NULL
                    );''')
    mycursor.execute('''CREATE TABLE IF NOT EXISTS WorkoutPlan (
                    PlanID INT PRIMARY KEY,
                    UserID INT,
                    WorkoutID INT,
                    FOREIGN KEY (UserID) REFERENCES AppUser(UserID),
                    FOREIGN KEY (WorkoutID) REFERENCES Workout(WorkoutID)
                    );''')
    mycursor.execute('''CREATE TABLE IF NOT EXISTS WorkoutExercise (
                    WorkoutExerciseID INT PRIMARY KEY,
                    WorkoutID INT,
                    ExerciseID INT,
                    FOREIGN KEY (WorkoutID) REFERENCES Workout(WorkoutID),
                    FOREIGN KEY (ExerciseID) REFERENCES Exercise(ExerciseID)
                    );''')
    mycursor.execute('''CREATE TABLE IF NOT EXISTS EquipmentExercise (
                    EquipmentExerciseID INT PRIMARY KEY,
                    EquipmentID INT,
                    ExerciseID INT,
                    FOREIGN KEY (EquipmentID) REFERENCES Equipment(EquipmentID),
                    FOREIGN KEY (ExerciseID) REFERENCES Exercise(ExerciseID)
                    );''')
    mycursor.close()


# Add one user to the database
def add_user():
    try:
        cursor = mydb.cursor()
        # Get user input
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        fitness_level = int(input("Enter fitness level (1-5): "))
        # Insert data into the table
        sql = '''INSERT INTO AppUser (Username, Email, Password, FitnessLevel) VALUES (%s, %s, %s, %s)'''
        val = (username, email, password, fitness_level)
        cursor.execute(sql, val)
        mydb.commit()
        print("User added successfully!")
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# Add one equipment to database 
def add_equipment():
    try:
        cursor = mydb.cursor()
        # Get user input
        equipment_name = input("Enter equipment name: ")
        # Insert data into the table
        sql = '''INSERT INTO Equipment (EquipmentName) VALUES (%s)'''
        val = (equipment_name,)
        cursor.execute(sql, val)
        mydb.commit()
        print("Equipment added successfully!")
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# Add one workout to database 
def add_workout():
    try:
        cursor = mydb.cursor()
        # Get user input
        workout_name = input("Enter workout name: ")
        duration = int(input("Enter workout duration (minutes): "))
        difficulty = int(input("Enter workout difficulty level (1-5): "))
        # Insert data into the table
        sql = '''INSERT INTO Workout (WorkoutName, Duration, DifficultyLevel) VALUES (%s, %s, %s)'''
        val = (workout_name, duration, difficulty)
        cursor.execute(sql, val)
        mydb.commit()
        print("Workout added successfully!")
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# Add one exercise to database 
def add_exercise():
    try:
        cursor = mydb.cursor()
        # Get user input
        exercise_name = input("Enter exercise name: ")
        duration = int(input("Enter exercise duration (minutes): "))
        repetitions = int(input("Enter number of repetitions: "))
        # Insert data into the table
        sql = '''INSERT INTO Exercise (ExerciseName, Duration, Repetitions) VALUES (%s, %s, %s)'''
        val = (exercise_name, duration, repetitions)
        cursor.execute(sql, val)
        mydb.commit()
        print("Exercise added successfully!")
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# View all equipment 
def view_equipment():
    try:
        cursor = mydb.cursor()
        sql = '''SELECT * FROM Equipment'''
        cursor.execute(sql)
        data = cursor.fetchall()
        print("\nEquipment:")
        headers = cursor.column_names
        print(headers)
        for row in data: 
            print(row)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# View all workouts 
def view_workout():
    try:
        cursor = mydb.cursor()
        sql = '''SELECT * FROM Workout'''
        cursor.execute(sql)
        data = cursor.fetchall()
        print("\nWorkouts:")
        headers = cursor.column_names
        print(headers)
        for row in data: 
            print(row)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()

# View all exercises 
def view_exercise():
    try:
        cursor = mydb.cursor()
        sql = '''SELECT * FROM Exercise'''
        cursor.execute(sql)
        data = cursor.fetchall()
        print("\nExercises:")
        headers = cursor.column_names
        print(headers)
        for row in data: 
            print(row)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# View exercises available based on current equipment 
def view_exercises_available():
    try:
        cursor = mydb.cursor()
        sql = '''SELECT c.ExerciseName 
                FROM Equipment a
                LEFT JOIN EquipmentExercise  b ON a.EquipmentID = b.EquipmentID
                LEFT JOIN Exercise c ON b.ExerciseID = c.ExerciseID
                WHERE c.ExerciseName IS NOT NULL;'''
        cursor.execute(sql)
        data = cursor.fetchall()
        print("Exercises:")
        headers = cursor.column_names
        print(headers)
        for row in data: 
            print(row)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# Link equipment to exercise 
def link_equipment_exercise():
    try: 
        cursor = mydb.cursor()
        # Display all exercises (so user can choose one to link equipment to)
        view_exercise()
        # Display all equipment 
        view_equipment()
        # Ask user to choose an exercise to add to 
        exercise_id = input("Which exercise would you like to link? Type in exercise ID\n")
        equipment_id = input("Which equipment would you like to add to this exercise? Type in equipment ID\n")
        # Insert data into the table
        sql = '''INSERT INTO EquipmentExercise (EquipmentID, ExerciseID) VALUES (%s, %s)'''
        val = (equipment_id, exercise_id)
        cursor.execute(sql, val)
        mydb.commit()
        print("Equipment added to exercise successfully!")
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()


# Link exercise to workout 
def link_exercise_workout():
    try: 
        cursor = mydb.cursor()
        # Display all workouts (so user can choose one to link exercise to)
        view_workout()
        # Display all exercises 
        view_exercise()
        # Ask user to choose a workout to add to 
        workout_id = input("Which workout would you like to link? Type in workout ID\n")
        exercise_id = input("Which exercise would you like to add to this workout? Type in exercise ID\n")
        # Insert data into the table
        sql = '''INSERT INTO WorkoutExercise (WorkoutID, ExerciseID) VALUES (%s, %s)'''
        val = (workout_id, exercise_id)
        cursor.execute(sql, val)
        mydb.commit()
        print("Exercise added to workout successfully!")
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()

# View all exercises pertaining to a specific workout 
def view_workout_exercises():
    try:
        cursor = mydb.cursor()
        # Display all workouts to choose from 
        view_workout()
        workout_id = input("\nWhich workout would you like to view exercises for? Type in workout ID\n")
        sql = '''SELECT c.* 
                FROM WorkoutExercise a
                JOIN Workout b ON a.WorkoutID = b.WorkoutID
                JOIN Exercise c ON a.ExerciseID = c.ExerciseID
                WHERE a.WorkoutID = %s'''
        cursor.execute(sql, (workout_id,))
        data = cursor.fetchall()
        print("Exercises:")
        headers = cursor.column_names
        print(headers)
        for row in data: 
            print(row)
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()



# Establish MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    database="412DB",
    user="root",  # Replace with your MySQL username
    password=""  # Replace with your MySQL password
)

if mydb:
    try:
        database_name = input("Enter database name: ")
        create_database(database_name)
        mydb.database = "412DB"
        create_table()
        add_user()
        action = input('''\nWhat would you like to do?
                           1: Add equipment
                           2: Add workout
                           3: Add exercise
                           4: Add equipment to exercise
                           5: Add exercise to workout
                           6: View all equipment
                           7: View all workouts
                           8: View all exercises
                           9: View exercises available
                           10: View workout exercises
                           0: Quit\n''')
        while(action != '0'):
            if(action == '1'):
                view_equipment()
                add_equipment()
            elif(action == '2'): 
                view_workout()
                add_workout()
            elif(action == '3'): 
                view_exercise()
                add_exercise()
            elif(action == '4'): 
                link_equipment_exercise()
            elif(action == '5'): 
                link_exercise_workout()
            elif(action == '6'): 
                view_equipment()
            elif(action == '7'): 
                view_workout()
            elif(action == '8'): 
                view_exercise()
            elif(action == '9'): 
                view_exercises_available()
            elif(action == '10'): 
                view_workout_exercises()
            elif(action == '0'):
                break
            else: 
                print("Action not recognized!\n")
            action = input('''\nWhat would you like to do?
                           1: Add equipment
                           2: Add workout
                           3: Add exercise
                           4: Add equipment to exercise
                           5: Add exercise to workout
                           6: View all equipment
                           7: View all workouts
                           8: View all exercises
                           9: View exercises available
                           10: View workout exercises
                           0: Quit\n''')
    except mysql.connector.Error as e:
        print(e)
    finally:
        mydb.close()
else:
    print("Unable to establish a connection to the database.")