import discord
import mysql.connector
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables (for security)
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")


# Connect to MySQL
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()


# Set up the bot with a prefix (e.g., "!log")
intents = discord.Intents.default()
intents.message_content = True  # Required for bot commands to work
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Command to start a workout session
@bot.command()
async def join(ctx):
    discord_id = ctx.author.id
    discord_user = ctx.author.name

    cursor.execute(          
        "INSERT INTO users (discord_id, discord_user) VALUES (%s, %s)", (discord_id, discord_user)
    )

    db.commit()
    await ctx.send(f"User made! User ID: {cursor.lastrowid}")


#Starting a workout
@bot.command()
async def start_workout(ctx):
    discord_id = ctx.author.id

    # Get the user's ID from the users table using their discord_id
    cursor.execute("SELECT id FROM users WHERE discord_id = %s", (discord_id,))
    result = cursor.fetchone()

    if result:
        user_db_id = result[0]

        cursor.execute(
            "INSERT INTO workouts (user_id, start_time) VALUES (%s, NOW())",
            (user_db_id,)
        )
        db.commit()
        workout_id = cursor.lastrowid
        await ctx.send(f"Workout started! ID: {workout_id}")
    else:
        await ctx.send("User not found in the database. Please register your Discord ID first.")

@bot.command()
async def end_workout(ctx):
    user_id = ctx.author.id  # Discord user ID

    # Get the user's ID from the users table
    cursor.execute("SELECT id FROM users WHERE discord_id = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        user_db_id = result[0]  # Get the user's ID from the users table
        
        # Find the most recent workout for that user that doesn't have an end_time
        cursor.execute(
            "SELECT id FROM workouts WHERE user_id = %s AND end_time IS NULL ORDER BY start_time DESC LIMIT 1",
            (user_db_id,)
        )
        workout = cursor.fetchone()

        if workout:
            workout_id = workout[0]
            
            # Update the workout with the end_time
            cursor.execute(
                "UPDATE workouts SET end_time = NOW() WHERE id = %s",
                (workout_id,)
            )
            db.commit()
            await ctx.send(f"Workout {workout_id} ended!")
        else:
            await ctx.send("No active workout found. Start a new one with !start_workout.")
    else:
        await ctx.send("User not found in the database. Please register your Discord ID first.")


bot.run(TOKEN)
