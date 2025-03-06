import discord
from discord.ext import commands
from config import TOKEN
import database as db
import re


# Set up the bot with a prefix (e.g., "!log")
intents = discord.Intents.default()
intents.message_content = True  # Required for bot commands to work
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def end_workout(ctx):
    discord_id = ctx.author.id
    user_db_id = db.get_user_id(discord_id)

    if user_db_id:
        workout_id = db.get_active_workout(user_db_id)
        if workout_id:
            db.end_workout(workout_id)
            await ctx.send(f"Workout {workout_id} ended")
        else:
            await ctx.send("No active workout found. Start one with '!start_workout'.")
    else:
        await ctx.send("User not recognized. Please confirm registration status.")

@bot.command()
async def join(ctx):
    discord_id = ctx.author.id
    discord_user = ctx.author.name

    # Check if the user already exists in the database
    user_exists = db.check_user_exists(discord_id)

    if user_exists:
        await ctx.send(f"User {discord_user} already exists!")
    else:
        # If the user does not exist, insert them
        user_id = db.insert_user(discord_id=discord_id, discord_user=discord_user)
        await ctx.send(f"User added! User ID: {user_id}")

@bot.command()
async def log(ctx, exercise: str, sets_reps: str, weight: str):
    """Parses exercise logs, supporting both '4x8' and '4 8' formats for sets/reps."""

    #Check that exercise exists
    #exercise_exists = db.check_exercise_exists(exercise_name=exercise)

    exercise_id = db.get_exercise_id(exercise_name=exercise)
    
    if exercise_id:
        #exercise_id = db.get_exercise_id(exercise_name=exercise)
        await ctx.send(f"Logging {exercise}")
    else:
        exercise_id = db.add_exercise(exercise_name=exercise)
        await ctx.send(f"Added new exercise \n{exercise} at id: {exercise_id}")

    # Check if sets and reps are given in "NxM" format (e.g., "4x8")
    match = re.match(r"(\d+)x(\d+)", sets_reps)
    if match:
        sets, reps = match.groups()
    else:
        # Try to split normally (if user entered separate values)
        try:
            sets, reps = sets_reps.split()
        except ValueError:
            await ctx.send("Invalid format! Use `!log exercise setsxreps weight` (e.g., `!log bbBenchPress 4x8 120lbs`).")
            return

    # Extract numeric weight (remove "lbs", "kg", etc.)
    weight_value = re.sub(r"[^\d.]", "", weight)

    if not weight_value:
        await ctx.send("Invalid weight format! Please enter a valid number (e.g., '120lbs' or '120').")
        return
    

    #Get user and workout id
    discord_id = ctx.author.id
    user_db_id = db.get_user_id(discord_id=discord_id)

    workout_id = db.get_active_workout(user_db_id)

    exercise_data = {
        "workout_id": workout_id,
        "exercise": exercise_id,
        "weight": float(weight_value),
        "reps": int(reps),
        "sets": int(sets)
    }
    
    db.log_exercise(exercise_data)

    await ctx.send(f"Exercise: {exercise}\nSets: {sets}\nReps: {reps}\nWeight: {weight_value} lbs")


@bot.command()
async def my_workouts(ctx):
    discord_id = ctx.author.id

    output = db.get_workouts_from_user(discord_id)# TODO: digest this output

    for workout in output:

        length = workout[4] - workout[3]

        await ctx.send(f"ID: {workout[0]} Date: {workout[2]} Duration: {length}\n")

@bot.command()
async def show_workout(ctx, workout_id: int):
    """Gets and outputs the individual exercises of a workout"""

    output = db.get_workout_details(workout_id)

    print(output)

    await ctx.send(f"User: {output[0][0]} \nDate: {output[0][1]} \nExercises: {output[0][2]}")


@bot.command()
async def start_workout(ctx):
    discord_id = ctx.author.id
    user_db_id = db.get_user_id(discord_id)

    active_workout = db.get_active_workout(user_db_id)

    if user_db_id:
        if active_workout:
            await ctx.send(f"Workout already in session with ID:{active_workout}.")
            await ctx.send("Please end current workout with '!end_workout' before starting another.")
        else:
            workout_id = db.start_workout(user_db_id)
            await ctx.send(f"Workout started! ID: {workout_id}")
    else:
        await ctx.send("User not found. Please confirm registration status.")



bot.run(TOKEN)
