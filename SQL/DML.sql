-- sample_data.sql

-- Insert sample members
INSERT INTO members (first_name, last_name, email, password, date_of_birth, gender, phone)
VALUES
    ('John', 'Doe', 'john.doe@example.com', 'password123', '1990-05-15', 'Male', '1234567890'),
    ('Jane', 'Smith', 'jane.smith@example.com', 'password456', '1985-11-22', 'Female', '9876543210'),
    ('Michael', 'Johnson', 'michael.johnson@example.com', 'password789', '1988-07-20', 'Male', '1122334455'),
    ('Sarah', 'Williams', 'sarah.williams@example.com', 'passwordxyz', '1995-03-12', 'Female', '9988776655');

-- Insert sample rooms
INSERT INTO rooms (room_name, room_description, capacity)
VALUES
    ('Studio A', 'Main fitness studio', 30),
    ('Yoga Room', 'Dedicated yoga and pilates room', 20),
    ('Cycling Studio', 'Studio equipped for indoor cycling classes', 15),
    ('Weightlifting Area', 'Dedicated space for weightlifting workouts', 20);

-- Insert sample fitness goals
INSERT INTO fitness_goals (member_id, goal_type, target_value, metric_type, target_date)
VALUES
    (1, 'Weight Loss', 75.0, 'kg', '2024-06-30'),
    (2, 'Running Distance', 10.0, 'km','2024-09-30'),
    (3, 'Muscle Gain', 80.0, 'kg', '2024-08-31'),
    (4, 'Flexibility', NULL, NULL, '2024-10-31');

-- Insert sample health metrics
INSERT INTO health_metrics (member_id, metric_type, metric_value)
VALUES
    (1, 'Weight', 85.0),
    (2, 'Weight', 62.0),
    (1, 'Blood Pressure', 120.0),
    (2, 'Blood Pressure', 115.0),
    (3, 'Weight', 78.0),
    (4, 'Blood Pressure', 122.0),
    (3, 'Body Fat Percentage', 20.0);

-- Insert sample trainers
INSERT INTO trainers (first_name, last_name, email, password, expertise, bio)
VALUES
    ('Alex', 'Brown', 'alex.brown@example.com', 'password789', 'Strength Training', 'Certified personal trainer with 5 years of experience.'),
    ('Emily', 'Wilson', 'emily.wilson@example.com', 'passwordabc', 'Yoga and Pilates', 'Yoga and Pilates instructor with 8 years of experience.'),
    ('Jessica', 'Miller', 'jessica.miller@example.com', 'password123', 'Cardio and Endurance', 'Specializes in cardio workouts for endurance improvement.'),
    ('David', 'Wilson', 'david.wilson@example.com', 'password456', 'Weightlifting', 'Experienced weightlifting coach with a focus on form and technique.');


-- Insert sample trainer schedules
INSERT INTO trainer_schedule (trainer_id, start_time, end_time, date)
VALUES
    (1, '09:00', '12:00', '2024-04-12'),
    (1, '14:00', '17:00', '2024-04-12'),
    (2, '10:00', '13:00', '2024-04-12'),
    (2, '16:00', '19:00', '2024-04-12');

-- Insert sample group classes
INSERT INTO group_classes (class_name, class_description, instructor_id, start_time, end_time, date, room_id)
VALUES
    ('Bootcamp', 'High-intensity full-body workout', 1, '08:00', '09:00', '2024-04-13', 1),
    ('Yoga Flow', 'Vinyasa yoga for all levels', 2, '18:00', '19:30', '2024-04-13', 2),
    ('Zumba', 'High-energy dance fitness class', 3, '10:00', '11:00', '2024-04-15', 1),
    ('Powerlifting', 'Focus on heavy lifting and strength development', 4, '17:00', '18:30', '2024-04-15', 1);


-- Insert sample class registrations
INSERT INTO class_registrations (member_id, class_id)
VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4);

-- Insert sample personal training sessions
INSERT INTO personal_training_sessions (member_id, trainer_id, start_time, end_time, date)
VALUES
    (1, 1, '10:00', '11:00', '2024-04-14'),
    (2, 2, '16:00', '17:00', '2024-04-14'),
    (3, 3, '09:00', '10:00', '2024-04-16'),
    (4, 4, '15:00', '16:00', '2024-04-16');


-- Insert sample equipment
INSERT INTO equipment (equipment_name, equipment_description, room_id, maintenance_schedule)
VALUES
    ('Treadmills', 'Cardiovascular training equipment', 1, INTERVAL '6 months'),
    ('Free Weights', 'Dumbbells and barbells for strength training', 1, INTERVAL '1 year'),
    ('Stationary Bikes', 'Indoor cycling equipment', 3, INTERVAL '6 months'),
    ('Bench Press', 'Weightlifting bench with barbells and plates', 4, INTERVAL '1 year');

-- Insert sample billing records
INSERT INTO billing (member_id, amount, payment_type)
VALUES
    (1, 50.0, 'Credit Card'),
    (2, 60.0, 'Bank Transfer'),
    (3, 70.0, 'PayPal'),
    (4, 80.0, 'Cash');
