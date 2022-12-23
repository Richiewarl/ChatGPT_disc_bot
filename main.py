import discord
from discord.ext import commands
import openai
from dotenv import load_dotenv
import os

# loading .env file
load_dotenv()

# discord objects
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='~', intents=intents)

# openai objects
openai.api_key = os.getenv('OPENAI_TOKEN')

# test outputs


# register on start
@bot.event
async def on_ready():
    print("Hi! We've logged in as {0.user}".format(bot))

# commands
@bot.command()
async def ping(ctx):
    await ctx.channel.send("pong :ping_pong:")

@bot.command()
async def models(ctx):
    await ctx.channel.send(f" \
        The OpenAI API currently has {len(openai.Model.list().data)} available model from the GPT-3, Codex and Content Filter family. They each have their own capabilities and strengths. I primarily use models from the GPT-3 family for natural language processing which allows me to answer your questions. The main GPT-3 models are: \n \t1. Davinci - <https://beta.openai.com/docs/models/davinci> \n \t2. Curie - <https://beta.openai.com/docs/models/curie> \n \t3. Babbage - <https://beta.openai.com/docs/models/babbage> \n \t4. Ada - <https://beta.openai.com/docs/models/ada> \n To learn more, visit https://beta.openai.com/docs/models/overview. \
        ")

@bot.command()
async def completion(ctx, arg):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=arg,
        max_tokens=3900,
        temperature=1
        )
    print(response)
    await ctx.channel.send(response.choices[0].text)


# exe
bot.run(os.getenv('BOT_TOKEN'))