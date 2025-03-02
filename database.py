import mysql.connector
import os
from dotenv import load_dotenv


# Load environment variables (for security)
load_dotenv()

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
    "Retrieve the most recent active workout (no end_time)." #TODO: remove simoultaneous workouts
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