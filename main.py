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

@bot.command(name="ask")
async def completion(ctx, *, arg, temp=1):
    # TODO: allow user to temp appropriately
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=arg,
        max_tokens=3900,
        temperature=temp
        )

    print("Completion:", response, "\n")
    await ctx.channel.send(response.choices[0].text)

@bot.command(name="fix")
# TODO: allow user to temp appropriately
async def edit(ctx, *, arg, temp=0):
    print(ctx)
    response = openai.Edit.create(
        model="text-davinci-edit-001",
        input=arg,
        instruction="Please fix the grammer and spelling mistakes.",
        temperature=temp
        )

    print("Edit:", response, "\n")
    await ctx.channel.send(response.choices[0].text)

@bot.command(name="img")
async def images_generation(ctx, *, arg):
    # TODO: Allow user to select number of imges and resolution. multiple imgs support is there, just selection from user.
    resolution = ["256x256", "512x512", "1024x1024"]  # available res
    response = openai.Image.create(
        prompt=arg,
        n=2,
        size="1024x1024",
        response_format="url"
        )
    urls = response.data
    print("images_generation:", response, "\n")

    # create embed
    icons = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
    embed = discord.Embed(
        title="Generated Pictures" if len(urls) > 1 else "Generated Picture",
        description=arg,
        colour=discord.Color.purple()
        )
    embed.set_author(
        name="OpenAI",
        url="https://beta.openai.com/docs/api-reference/images/create",
        icon_url="https://pbs.twimg.com/profile_images/1603113436757389313/wpYDqrIf_400x400.jpg")
    embed.set_thumbnail(url=urls[0].url)
    for i in range(len(urls)):
        embed.add_field(name=icons[i] + " :frame_photo:", value="[Click Here](" + urls[i].url + ")")
    
    await ctx.channel.send(embed=embed)

# exe
bot.run(os.getenv('BOT_TOKEN'))