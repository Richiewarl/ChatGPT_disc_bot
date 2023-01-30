import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os
from controller import apiCalls 

# loading .env file
load_dotenv()

# init command object
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

# setup apiCalls commands
asyncio.run(bot.add_cog(apiCalls(bot)))

# register on start
@bot.event
async def on_ready():
    print("Hi! We've logged in as {0.user}".format(bot))

# exe
bot.run(os.getenv('BOT_TOKEN'))