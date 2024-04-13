# Health-and-Fitness-Club-Management-System

---

## Overview

This repository contains SQL scripts to create and populate a database for a health and fitness club, as well as a Python script for managing various operations related to club members, trainers, administrative staff, and facilities.

### Files:

- `DDL.sql`: SQL script to create tables for members, fitness goals, health metrics, trainers, group classes, personal training sessions, rooms, equipment, and billing.
- `DML.sql`: SQL script to populate the tables with sample data.
- `health_club.py`: Python script to interact with the database and perform operations such as member registration, profile updates, setting fitness goals, logging health metrics, scheduling personal training sessions, registering for group classes, and administrative tasks like booking rooms, scheduling maintenance, updating class schedules, and processing payments.

---

## Getting Started

To set up the database and run the Python script, follow these steps:

1. **Database Setup**:
   - Execute the `DDL.sql` script to create the necessary tables.
   - Execute the `DML.sql` script to populate the tables with sample data.

2. **Python Environment**:
   - Ensure you have Python installed on your system.

3. **Install Dependencies**:
   - Install the `psycopg2` library using pip:
     ```
     pip install psycopg2
     ```

4. **Run the Script**:
   - Execute the `health_club.py` script to start interacting with the health and fitness club management system.

---

## Usage

Once the setup is complete, you can use the `health_club.py` script to perform various operations:

- **Member Functions**: Register member, update profile, set fitness goals, log health metrics, schedule personal training, register for group classes.
- **Trainer Functions**: Set trainer schedule, view member profile.
- **Administrative Staff Functions**: Book room, schedule equipment maintenance, update class schedule, process payment.

Follow the prompts in the script to navigate through different functionalities and perform desired operations.

---

## Additional Notes

- Ensure that your PostgreSQL database is running and accessible.
- Modify the database connection details in the Python script (`health_club.py`) to match your setup (host, database name, username, password).

---
