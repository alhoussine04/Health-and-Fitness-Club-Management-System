# health_club.py

import psycopg2
from datetime import datetime

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="health_club",
    user="postgres",
    password="*******"
)

# Create a cursor object
cur = conn.cursor()

# Member Functions
def register_member(first_name, last_name, email, password, date_of_birth, gender, phone=None):
    query = "INSERT INTO members (first_name, last_name, email, password, date_of_birth, gender, phone) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING member_id"
    values = (first_name, last_name, email, password, date_of_birth, gender, phone)
    cur.execute(query, values)
    member_id = cur.fetchone()[0]
    conn.commit()
    return member_id

def update_profile(member_id, first_name=None, last_name=None, email=None, password=None,gender=None, phone=None):
    query = "UPDATE members SET "
    values = []
    if first_name:
        query += "first_name = %s, "
        values.append(first_name)
    if last_name:
        query += "last_name = %s, "
        values.append(last_name)
    if email:
        query += "email = %s, "
        values.append(email)
    if password:
        query += "password = %s, "
        values.append(password)
    if gender:
        query += "gender = %s, "
        values.append(gender)
    if phone:
        query += "phone = %s, "
        values.append(phone)
    query = query.rstrip(", ") + " WHERE member_id = %s"
    values.append(member_id)
    cur.execute(query, values)
    conn.commit()

def set_fitness_goal(member_id, goal_type, target_value, metric_type, target_date):
    query = "INSERT INTO fitness_goals (member_id, goal_type, target_value, metric_type, target_date) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (member_id, goal_type) DO UPDATE SET target_value = %s, target_date = %s"
    values = (member_id, goal_type, target_value, target_date, metric_type, target_value, target_date)
    cur.execute(query, values)
    conn.commit()

def log_health_metric(member_id, metric_type, metric_value, metric_date=None):
    if not metric_date:
        metric_date = datetime.now().date()
    query = "INSERT INTO health_metrics (member_id, metric_type, metric_value, metric_date) VALUES (%s, %s, %s, %s)"
    values = (member_id, metric_type, metric_value, metric_date)
    cur.execute(query, values)
    conn.commit()

def schedule_personal_training(member_id, trainer_id, start_time, end_time, date):
    if check_trainer_schedule_conflict(trainer_id, start_time, end_time, date):
        print("Error: Trainer schedule conflict. Unable to add personal training session.")
        return None
    
    query = "INSERT INTO personal_training_sessions (member_id, trainer_id, start_time, end_time, date) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"
    values = (member_id, trainer_id, start_time, end_time, date)
    cur.execute(query, values)
    
    query = "INSERT INTO trainer_schedule (trainer_id, start_time, end_time, date) VALUES (%s, %s, %s, %s) ON CONFLICT (trainer_id, start_time, end_time, date) DO NOTHING"
    values = (trainer_id, start_time, end_time, date)
    cur.execute(query, values)
    conn.commit()

def register_group_class(member_id, class_id):
    query = "INSERT INTO class_registrations (member_id, class_id) VALUES (%s, %s) ON CONFLICT DO NOTHING"
    values = (member_id, class_id)
    cur.execute(query, values)
    conn.commit()


# Trainer Functions
def set_trainer_schedule(trainer_id, start_time, end_time, date):
    query = "INSERT INTO trainer_schedule (trainer_id, start_time, end_time, date) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"
    values = (trainer_id, start_time, end_time, date)
    cur.execute(query, values)
    conn.commit()

def get_member_profile(member_id):
    query = "SELECT * FROM members WHERE member_id = %s"
    value = (member_id)
    cur.execute(query, value)
    member_profile = cur.fetchone()
    return member_profile

# Administrative Staff Functions
def book_room(class_name, class_description, room_id, instructor, start_time, end_time, date):
    if check_trainer_schedule_conflict(instructor, start_time, end_time, date):
        print("Error: Trainer schedule conflict. Unable to add personal training session.")
        return None
    query = "SELECT * FROM group_classes WHERE room_id = %s AND instructor = %s AND date = %s AND (start_time >= %s AND start_time < %s OR end_time > %s AND end_time <= %s)"
    values = (room_id, instructor, date, start_time, end_time, start_time, end_time)
    cur.execute(query, values)
    if cur.fetchone():
        return False
    else:
        query = "INSERT INTO group_classes (class_name, class_description, instructor_id, start_time, end_time, date, room_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (class_name, class_description, instructor, start_time, end_time, date, room_id)
        cur.execute(query, values)
        conn.commit()
        return True

def schedule_maintenance(equipment_id, maintenance_date):
    query = "UPDATE equipment SET maintenance_schedule = %s + INTERVAL '1 year' WHERE equipment_id = %s"
    values = (maintenance_date, equipment_id)
    cur.execute(query, values)
    conn.commit()

def update_class_schedule(class_id, instructor, new_start_time, new_end_time, new_date, new_room_id):
    query = "UPDATE group_classes SET start_time = %s, instructor = %s, end_time = %s, date = %s, room_id = %s WHERE class_id = %s"
    values = (new_start_time, instructor, new_end_time, new_date, new_room_id, class_id)
    cur.execute(query, values)
    conn.commit()

def process_payment(member_id, amount, payment_type):
    query = "INSERT INTO billing (member_id, amount, payment_type) VALUES (%s, %s, %s)"
    values = (member_id, amount, payment_type)
    cur.execute(query, values)
    conn.commit()

# Display Functions
def display_members():
    query = "SELECT member_id, first_name, last_name FROM members"
    cur.execute(query)
    members = cur.fetchall()

    print("\nMembers:")
    for member in members:
        print(f"ID: {member[0]}, Name: {member[1]} {member[2]}")

def display_trainers():
    query = "SELECT trainer_id, first_name, last_name, email, expertise FROM trainers"
    cur.execute(query)
    trainers = cur.fetchall()

    print("\nTrainers:")
    for trainer in trainers:
        print(f"ID: {trainer[0]}, Name: {trainer[1]} {trainer[2]}, Email: {trainer[3]}, Expertise: {trainer[4]}")

def display_trainer_schedule(trainer):
    query = "SELECT * FROM trainer_schedule WHERE trainer_id = %s;"
    cur.execute(query, (trainer,))
    trainers = cur.fetchall()

    print("\nTrainers:")
    for trainer in trainers:
        print(f"Schedule ID: {trainer[0]}, Start:{trainer[2]}, End:{trainer[3]}, Date:{trainer[4]}")

def display_group_classes():
    query = """
        SELECT c.class_id, c.class_name, c.instructor, c.start_time, c.end_time, c.date, r.room_name
        FROM group_classes c
        JOIN rooms r ON c.room_id = r.room_id
    """
    cur.execute(query)
    classes = cur.fetchall()

    print("\nGroup Classes:")
    for class_info in classes:
        print(f"ID: {class_info[0]}, Name: {class_info[1]}, Instructor: {class_info[2]}, Time: {class_info[3]} - {class_info[4]}, Date: {class_info[5]}, Room: {class_info[6]}")
#

# Helper Functions
def check_trainer_schedule_conflict(trainer_id, start_time, end_time, date):
    # Check if the proposed time slot conflicts with the trainer's existing schedule
    query = """
        SELECT COUNT(*) FROM trainer_schedule
        WHERE trainer_id = %s
          AND date = %s
          AND (
            (start_time >= %s AND start_time < %s)
            OR (end_time > %s AND end_time <= %s)
            OR (start_time <= %s AND end_time >= %s)
          )
    """
    values = (trainer_id, date, start_time, end_time, start_time, end_time, start_time, end_time)
    cur.execute(query, values)
    count = cur.fetchone()[0]
    return count > 0

# Main Function
def main():
    print("Welcome to the Health and Fitness Club Management System!")
    print("Please select an option:")
    print("1. Member Functions")
    print("2. Trainer Functions")
    print("3. Administrative Staff Functions")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        member_functions()
    elif choice == "2":
        trainer_functions()
    elif choice == "3":
        admin_functions()
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main()

# Member Functions
def member_functions():
    display_members()
    print("\nMember Functions")
    print("1. Register Member")
    print("2. Update Profile")
    print("3. Set Fitness Goal")
    print("4. Log Health Metric")
    print("5. Schedule Personal Training")
    print("6. Register for Group Class")
    print("7. Go Back")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        register_member_prompt()
    elif choice == "2":
        update_profile_prompt()
    elif choice == "3":
        set_fitness_goal_prompt()
    elif choice == "4":
        log_health_metric_prompt()
    elif choice == "5":
        schedule_personal_training_prompt()
    elif choice == "6":
        register_group_class_prompt()
    elif choice == "7":
        main()
    else:
        print("Invalid choice. Please try again.")
        member_functions()

def register_member_prompt():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    date_of_birth = input("Enter date of birth (YYYY-MM-DD): ")
    gender = input("Enter gender: ")
    phone = input("Enter phone (optional): ")

    member_id = register_member(first_name, last_name, email, password, date_of_birth, gender, phone)
    print(f"Member registered successfully with ID: {member_id}")

    member_functions()

def update_profile_prompt():
    member_id = int(input("Enter member ID: "))
    first_name = input("Enter new first name (leave blank if no change): ")
    last_name = input("Enter new last name (leave blank if no change): ")
    email = input("Enter new email (leave blank if no change): ")
    password = input("Enter new password (leave blank if no change): ")
    gender = input("Enter new gender (leave blank if no change): ")
    phone = input("Enter new phone (leave blank if no change): ")

    update_profile(member_id, first_name, last_name, email, password, gender, phone)
    print("Profile updated successfully.")

    member_functions()

def set_fitness_goal_prompt():
    member_id = int(input("Enter member ID: "))
    goal_type = input("Enter goal type (e.g., Weight Loss, Running Distance): ")
    target_value = float(input("Enter target value (kg, km): "))
    metric_type = input("Enter metric type (e.g., kg, km): ")
    target_date = input("Enter target date (YYYY-MM-DD): ")

    set_fitness_goal(member_id, goal_type, target_value, metric_type, target_date)
    print("Fitness goal set successfully.")

    member_functions()

def log_health_metric_prompt():
    member_id = int(input("Enter member ID: "))
    metric_type = input("Enter metric type (e.g., Weight, Blood Pressure): ")
    metric_value = float(input("Enter metric value: "))
    metric_date_str = input("Enter metric date (YYYY-MM-DD) (leave blank for today): ")
    metric_date = None if not metric_date_str else datetime.strptime(metric_date_str, "%Y-%m-%d").date()

    log_health_metric(member_id, metric_type, metric_value, metric_date)
    print("Health metric logged successfully.")

    member_functions()

def schedule_personal_training_prompt():
    member_id = int(input("Enter member ID: "))
    display_trainers()
    trainer_id = int(input("Enter trainer ID: "))
    display_trainer_schedule(trainer_id)
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")
    date_str = input("Enter date (YYYY-MM-DD): ")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    schedule_personal_training(member_id, trainer_id, start_time, end_time, date)
    print("Personal training session scheduled successfully.")

    member_functions()

def register_group_class_prompt():
    member_id = int(input("Enter member ID: "))
    display_group_classes()
    class_id = int(input("Enter class ID: "))

    register_group_class(member_id, class_id)
    print("Group class registration successful.")

    member_functions()

# Trainer Functions
def trainer_functions():
    display_trainers()
    print("\nTrainer Functions")
    print("1. Set Trainer Schedule")
    print("2. View Member Profile")
    print("3. Go Back")

    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        set_trainer_schedule_prompt()
    elif choice == "2":
        get_member_profile_prompt()
    elif choice == "3":
        main()
    else:
        print("Invalid choice. Please try again.")
        trainer_functions()

def set_trainer_schedule_prompt():
    trainer_id = int(input("Enter trainer ID: "))
    display_trainer_schedule(trainer_id)
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")
    date = input("Enter date (YYYY-MM-DD): ")

    set_trainer_schedule(trainer_id, start_time, end_time, date)
    print("Trainer schedule set successfully.")

    trainer_functions()

def get_member_profile_prompt():
    display_members()
    member_id = input("Enter member ID: ")
    member_profile = get_member_profile(member_id)

    if member_profile:
        print(f"Member Profile: {member_profile}")
    else:
        print("Member not found.")

    trainer_functions()

# Administrative Staff Functions
def admin_functions():
    print("\nAdministrative Staff Functions")
    print("1. Book Room")
    print("2. Schedule Equipment Maintenance")
    print("3. Update Class Schedule")
    print("4. Process Payment")
    print("5. Go Back")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        book_room_prompt()
    elif choice == "2":
        schedule_maintenance_prompt()
    elif choice == "3":
        update_class_schedule_prompt()
    elif choice == "4":
        process_payment_prompt()
    elif choice == "5":
        main()
    else:
        print("Invalid choice. Please try again.")
        admin_functions()

def book_room_prompt():
    class_name = input("Enter class name: ")
    class_discription = input("Enter class discription)): ")
    room_id = int(input("Enter room ID: "))
    instructor = int(input("Enter instructor ID: "))
    start_time = input("Enter start time (HH:MM): ")
    end_time = input("Enter end time (HH:MM): ")
    date_str = input("Enter date (YYYY-MM-DD): ")
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    booking_success = book_room(class_name, class_discription, room_id, instructor, start_time, end_time, date)
    if booking_success:
        print("Room booked successfully.")
    else:
        print("Room booking failed. Room already booked for the specified time.")

    admin_functions()

def schedule_maintenance_prompt():
    equipment_id = int(input("Enter equipment ID: "))
    maintenance_date_str = input("Enter maintenance date (YYYY-MM-DD): ")
    maintenance_date = datetime.strptime(maintenance_date_str, "%Y-%m-%d").date()

    schedule_maintenance(equipment_id, maintenance_date)
    print("Maintenance scheduled successfully.")

    admin_functions()

def update_class_schedule_prompt():
    display_trainers()
    class_id = int(input("Enter class ID: "))
    instructor = int(input("Enter instructor ID: "))
    new_start_time = input("Enter new start time (HH:MM): ")
    new_end_time = input("Enter new end time (HH:MM): ")
    new_date_str = input("Enter new date (YYYY-MM-DD): ")
    new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
    new_room_id = int(input("Enter new room ID: "))

    update_class_schedule(class_id, instructor, new_start_time, new_end_time, new_date, new_room_id)
    print("Class schedule updated successfully.")

    admin_functions()

def process_payment_prompt():
    member_id = int(input("Enter member ID: "))
    amount = float(input("Enter payment amount: "))
    payment_type = input("Enter payment type (e.g., Credit Card, Bank Transfer): ")

    process_payment(member_id, amount, payment_type)
    print("Payment processed successfully.")

    admin_functions()

if __name__ == "__main__":
    main()

# Close the database connection
conn.close() 
