import discord
from dotenv import load_dotenv
import os

# loading .env file
load_dotenv()

# discord object
intents = discord.Intents.all()
client = discord.Client(command_prefix='~', intents=intents)

# events
@client.event
async def on_ready():
  print("Hi! We've logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  # ignore own messages
  if (message.author == client.user):
    return

  if message.content.startswith('ask'):
    await message.channel.send("SUCCESS")

# exe
client.run(os.getenv('BOT_TOKEN'))