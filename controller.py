import discord
from discord.ext import commands
import openai

from dotenv import load_dotenv
import os

class apiCalls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # init openai 
        openai.api_key = os.getenv('OPENAI_TOKEN')
    

    # helper functions
    def setEmbedAuthor(embedIn): 
        embedIn = embedIn.set_author(
            name="OpenAI", 
            url="https://beta.openai.com/docs/api-reference/images/create", 
            icon_url="https://pbs.twimg.com/profile_images/1603113436757389313/wpYDqrIf_400x400.jpg")

        return embedIn


    # api call commands
    @commands.command(
        help = "Pings the discord servers to check if the bot is online. A reply with Pong indicates it's online.",
        brief = "Checks if bot is online."
    )
    async def ping(self, ctx):
        await ctx.channel.send("pong :ping_pong:")

    @commands.command(
        help = "Displays the number of available models by the OpenAI API and the main GPT-3 models. Relevant links to the documentation and models are provided. ",
        brief = "Displays a list of popular GPT-3 models and relevant links."
    )
    async def models(self, ctx):
        embed = discord.Embed(
            title="Main GPT-3 Models",
            description="GPT-3 models can understand and generate natural language. OpenAI offers four main models with different levels of power suitable for different tasks.",
            colour=discord.Color.from_rgb(255,255,255)  # white
            )
        embed = setEmbedAuthor(embed)
        embed.add_field(name="text-davinci-003", value="[Click Here](https://beta.openai.com/docs/models/davinci)")
        embed.add_field(name="text-curie-001", value="[Click Here](https://beta.openai.com/docs/models/curie)")
        embed.add_field(name="text-babbage-001", value="[Click Here](https://beta.openai.com/docs/models/babbage)")
        embed.add_field(name="text-ada-001", value="[Click Here](https://beta.openai.com/docs/models/ada)")

        await ctx.channel.send(f" \
            The OpenAI API currently has {len(openai.Model.list().data)} available model from the GPT-3, Codex and Content Filter family. They each have their own capabilities and strengths. To learn more, visit https://beta.openai.com/docs/models/overview. \
            ", embed=embed)

    @commands.command(
        name="ask",
        help="Given a prompt, GPT will answer you. Each prompt and reply is currently limited to 2000 words respectively. https://beta.openai.com/docs/guides/completion",
        brief="Ask GPT a question and it shall answer."
        )
    async def completion(self, ctx, *, arg, temp=1):
        # TODO: allow user to temp appropriately
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=arg,
            max_tokens=2000,
            temperature=temp
            )

        print("Completion:", response, "\n")
        await ctx.channel.send(response.choices[0].text)

    @commands.command(
        name="fix",
        help="Given a sentence, GPT will fix the spelling mistakes.",
        brief="GPT fixes the spelling mistakes in your sentence."
        )
    # TODO: allow user to temp appropriately
    async def edit(self, ctx, *, arg, temp=0):
        print(ctx)
        response = openai.Edit.create(
            model="text-davinci-edit-001",
            input=arg,
            instruction="Please fix the grammer and spelling mistakes.",
            temperature=temp
            )

        print("Edit:", response, "\n")
        await ctx.channel.send(response.choices[0].text)

    @commands.command(
        name="img",
        help="Give a promt/description, GPT will generate a 1024x1024 image based on it.",
        brief="Turns a description into an image."
        )
    async def images_generation(self, ctx, *, arg):
        # TODO: Allow user to select number of imges (n) and resolution. multiple imgs support is there, just selection from user.
        resolution = ["256x256", "512x512", "1024x1024"]  # available res
        response = openai.Image.create(
            prompt=arg,
            n=1,
            size="1024x1024",
            response_format="url"
            )
        urls = response.data
        print("images_generation:", response, "\n")

        # create embed
        icons = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:", ":keycap_ten:"]
        embed = discord.Embed(
            title="AI Generated Pictures" if len(urls) > 1 else "AI Generated Picture",
            description=arg,
            colour=discord.Color.from_rgb(255,255,255)
            )
        embed = setEmbedAuthor(embed)
        embed.set_thumbnail(url=urls[0].url)
        for i in range(len(urls)):
            embed.add_field(
                name=":frame_photo:" if (len(urls) == 1) else icons[i] + " :frame_photo:",
                value="[Click Here](" + urls[i].url + ")")
        
        await ctx.channel.send(embed=embed)
