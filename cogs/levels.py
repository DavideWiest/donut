# Imports
import discord
from discord.ext import commands
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import asyncio
import random

# Basic Embed to display Errors triggered
def embed_error(input1, input2=None):
    embed_error = discord.Embed(title=f'{input1}', color=discord.Color.red())
    if input2 != None:
        embed_error.add_field(name='\uFEFF', value=str(input2))
    return embed_error

# Basic Embed to display a successful Action
def embed_success(input1, input2=None):
    embed_success = discord.Embed(title = f'{input1}', color = discord.Color.green())
    if input2 != None:
        embed_success.add_field(name='\uFEFF', value=str(input2))
    return embed_success

# Function to evaluate the customizable Embed Color of the Bot
def get_custom_color():
    with open("storage.json", "r") as f:
        file=json.load(f)

    color = eval(f"discord.Color.{'_'.join(file['special-color'].split(' '))}()")

    return color

# Actual Cog with Commands and Events
class Levels(commands.Cog):

    # Mandatory Function to assign self.bot to the Bot instance of main.py
    def __init__(self, bot):
        self.bot = bot

    # ----------------------- FUNCTIONS -----------------------

    # On-Message Event for Leveling
    @commands.Cog.listener()
    async def on_message(self, message):
        return
        # Chcking if this Message was not sent in DMs
        if message.guild != None:

            # Logging that an User (message.author) sent a Message
            with open("levels.json", "r") as f:
                file=json.load(f)

            if str(message.author.id) not in list(file[str(message.guild.id)]):
                file[str(message.guild.id)][str(message.author.id)] = 1
            else:
                file[str(message.guild.id)][str(message.author.id)] += 1

            with open("levels.json", "w") as f:
                json.dump(file, f)

            # Creating the Leveling-Map (To know which Message-Counter corresponds to which Level)
            with open("storage.json", "r") as f:
                lvling=json.load(f)
                base_msgs, factor_msgs = lvling["level-schema"]
                req_msgs = {}

                # Iterating/Making the Leveling Map up to Level 100
                for i in range(101):
                    req_msgs[round(i * base_msgs + (i-1) * base_msgs * factor_msgs)] = i

    # Simple Command to inform People about Me (Daev) making Bots
    @commands.command(aliases=["bot-maker", "daev", "dave", "bot"])
    async def custombot(self, ctx):
        embed_bot = discord.Embed(title=f"{self.bot.user.name} was created by Dæv•#7540", color=discord.Color.blurple(), description="""
**Want your own custom bot?
tell that Dæv•#7540**
- experienced Coder 
- Verified Bot-Developer by Discord

- high-quality Discord-Bot made with Love :heart:
- :level_slider: custom commands and design
- highly customizable afterwards
- reliable, Hosting is also my job
- <:emoji_48:789910396962078760> fast Support
- Price-Worthy starting at around 10€

        """)
        await ctx.send(embed=embed_bot)

    # Mini Command for simple testing
    @commands.command()
    async def bake(self, ctx):
        gif = random.choice(["https://tenor.com/view/tim-hortons-cookies-delicious-yummy-national-cookie-day-gif-16659532", "https://tenor.com/view/missallthingsawesome-awesomelystudio-pink-pink-queen-queen-of-pink-gif-16432520", "https://tenor.com/view/how-is-eating-it-pusheen-bake-cookies-gif-16199799", "https://tenor.com/view/pusheen-bake-baking-cat-gif-6080184", "https://tenor.com/view/e22-macaron-macarons-macaroon-macaroons-gif-19095594", "https://tenor.com/view/chocolate-charlotte-cake-cake-delicious-dessert-sweet-gif-17857749", "https://tenor.com/view/cangrejo-perreador-dance-croissant-gif-8133122"])
        await ctx.send(gif)
        
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reminder(self, ctx, *, time_and_msg):
        try:
            time, message = time_and_msg.split(" -- ")
        except:
            time = time_and_msg.split(" ")[0]
            message = " ".join(time_and_msg.split(" ")[1:])

        time = time.split(" ")
        muted_for = 0
        for i in time:

            if i.endswith("d"):
                muted_for += int(i[:-1]) * 60 * 60 * 24
            elif i.endswith("h"):
                muted_for += int(i[:-1]) * 60 * 60
            elif i.endswith("m"):
                muted_for += int(i[:-1]) * 60
            elif i.endswith("s"):
                muted_for += int(i[:-1])

        await ctx.send(embed=embed_success(f"Set a reminder [{message}]"))

        # Waiting until the time dued
        await asyncio.sleep(muted_for)

        await ctx.send(f"{ctx.author.mention}")
            
        await ctx.send(embed=discord.Embed(color=get_custom_color(), description="Reminder: \n" + message))



    # ----------------------- FUNCTIONS -----------------------

# Adding the Cog Object
def setup(bot):
    bot.add_cog(Levels(bot))