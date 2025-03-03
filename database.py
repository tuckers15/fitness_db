import mysql.connector
import os
from dotenv import load_dotenv


# Load environment variables (for security)
load_dotenv()

def check_user_exists(discord_id):
    """Check if the user already exists in the users table."""
    db = get_db_connection()
    cursor = db.cursor()
    
    query = "SELECT 1 FROM users WHERE discord_id = %s"
    cursor.execute(query, (discord_id,))
    
    # If a row is returned, the user exists
    result = cursor.fetchone()
    
    db.close()
    return result is not None

def check_exercise_exists(exercise_name):
    "Check that a exercise exists before inserting"
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("Select * FROM exercises WHERE name = %s", exercise_name)

    result = cursor.fetchone()

    db.close()
    return result is not None

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def insert_user(discord_id, discord_user):
    "Inserting a discord usert into database !join"
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(          
        "INSERT INTO users (discord_id, discord_user) VALUES (%s, %s)", (discord_id, discord_user)
    )
    db.commit()
    user_id = cursor.lastrowid
    db.close()
    return user_id

def get_user_id(discord_id):
    "Retrieving database user id (primary key) from discord id"
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id FROM users WHERE discord_id = %s", (discord_id,)
    )
    result = cursor.fetchone()
    db.close()
    return result[0] if result else None

def get_exercise_id(exercise_name):
    "Getting exercise id"
    db = get_db_connection()
    cursor = db.cursor()
   
    query = "SELECT id FROM exercises WHERE name = %s"
    
    # Use a tuple to pass the parameter
    cursor.execute(query, (exercise_name,))

    result = cursor.fetchone()
    db.close()
    return result[0] if result else None

def start_workout(user_db_id):
    "Workout entry"
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO workouts (user_id, start_time) VALUES (%s, NOW())",
        (user_db_id,)
    )
    db.commit()
    workout_id = cursor.lastrowid
    db.close()
    return workout_id

def get_active_workout(user_db_id):
    "Retrieve the most recent active workout (no end_time)."
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id FROM workouts WHERE user_id = %s AND end_time IS NULL ORDER BY start_time DESC LIMIT 1",
        (user_db_id,)
    )
    result = cursor.fetchone()
    db.close()
    return result[0] if result else None

def end_workout(workout_id):
    "Mark a workout as ended by setting the end_time."
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE workouts SET end_time = NOW() WHERE id = %s", (workout_id,))
    db.commit()
    db.close()

def log_exercise(exercise_data):
    """Add an exercise to the current workout."""
    db = get_db_connection()
    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO workouts_exercises (workout_id, exercise_id, weight_load, reps, set_count)
            VALUES (%s, %s, %s, %s, %s)
            """,(
            exercise_data['workout_id'], 
            exercise_data['exercise'], 
            exercise_data['weight'],
            exercise_data['reps'], 
            exercise_data['sets']
            )
        )
        db.commit()
    except Exception as e:
        print(f"Database error: {e}")  # Print or log the error
    finally:
        db.close()  # Ensure the database connection is closed
    

def add_exercise(exercise_name):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute(          
        "INSERT INTO exercises (name) VALUES (%s)", (exercise_name,)
    )
    db.commit()
    exercise_id = cursor.lastrowid
    db.close()
    return exercise_id




