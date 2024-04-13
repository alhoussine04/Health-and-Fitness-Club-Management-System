CREATE TABLE members (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    phone VARCHAR(20),
    join_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE rooms (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    room_description TEXT,
    capacity INTEGER NOT NULL
);

CREATE TABLE fitness_goals (
    goal_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(member_id),
    goal_type VARCHAR(50) NOT NULL,
    target_value NUMERIC,
    metric_type VARCHAR(50),
    target_date DATE NOT NULL,
    UNIQUE (member_id, goal_type)
);

CREATE TABLE health_metrics (
    metric_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(member_id),
    metric_type VARCHAR(50) NOT NULL,
    metric_value NUMERIC NOT NULL,
    metric_date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE trainers (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    expertise VARCHAR(100) NOT NULL,
    bio TEXT
);

CREATE TABLE trainer_schedule (
    schedule_id SERIAL PRIMARY KEY,
    trainer_id INTEGER NOT NULL REFERENCES trainers(trainer_id),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    date DATE NOT NULL,
    UNIQUE (trainer_id, start_time, end_time, date)
);

CREATE TABLE group_classes (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    class_description TEXT,
    instructor_id INTEGER NOT NULL REFERENCES trainers(trainer_id),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    date DATE NOT NULL,
    room_id INTEGER NOT NULL REFERENCES rooms(room_id),
    UNIQUE (start_time, end_time, date, room_id)
);

CREATE TABLE class_registrations (
    registration_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(member_id),
    class_id INTEGER NOT NULL REFERENCES group_classes(class_id),
    UNIQUE (member_id, class_id)
);

CREATE TABLE personal_training_sessions (
    session_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(member_id),
    trainer_id INTEGER NOT NULL REFERENCES trainers(trainer_id),
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    date DATE NOT NULL,
    UNIQUE (member_id, trainer_id, start_time, end_time, date)
);


CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    equipment_description TEXT,
    room_id INTEGER NOT NULL REFERENCES rooms(room_id),
    maintenance_schedule INTERVAL NOT NULL
);

CREATE TABLE billing (
    billing_id SERIAL PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES members(member_id),
    amount NUMERIC NOT NULL,
    payment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    payment_type VARCHAR(50) NOT NULL
); 
