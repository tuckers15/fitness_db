import discord
from discord.ext import commands
from config import TOKEN
import database as db


# Set up the bot with a prefix (e.g., "!log")
intents = discord.Intents.default()
intents.message_content = True  # Required for bot commands to work
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def join(ctx):
    discord_id = ctx.author.id
    discord_user = ctx.author.name

    user_id = db.insert_user(discord_id=discord_id, discord_user=discord_user)
    await ctx.send(f"User added! User ID: {user_id}")


@bot.command()
async def start_workout(ctx):
    discord_id = ctx.author.id
    user_db_id = db.get_user_id(discord_id)

    if user_db_id:
        workout_id = db.start_workout(user_db_id)
        await ctx.send(f"Workout started! ID: {workout_id}")
    else:
        await ctx.send("User not found. Please confirm registration status.")


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
    

bot.run(TOKEN)
