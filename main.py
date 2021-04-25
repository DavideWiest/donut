# Imports
import discord
from discord.ext import commands
from typing import Union
from typing import Optional
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import asyncio
from itertools import cycle
from datetime import datetime
from datetime import timedelta

info_color = discord.Color.dark_purple()

# Important Variables
TOKEN = "ODI1MDcwMDk3OTEwNzI2NjU3.YF4kaA.U9YxmzAPFJ_MvnywAgJGwDCpFtU"
STATUS = "-help | " + "4 the Art Garden" + " by .Daev#7540"


# Creating Bot instance with intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = commands.when_mentioned_or('-'), case_insensitive=True, intents=intents)

# Removing Base Command for custom Help-Command
bot.remove_command('help')

# Basic Embed to display Errors triggered
def embed_error(input1, input2=None):
    embed_error = discord.Embed(title=f'{input1}', color=discord.Color.red())
    if input2 != None:
        embed_error.add_field(name='\uFEFF', value=str(input2))
    return embed_error

# Function to evaluate the customizable Embed Color of the Bot
def get_custom_color():
    with open("donut/storage.json", "r") as f:
        file=json.load(f)

    color = eval(f"discord.Color.{'_'.join(file['special-color'].split(' '))}()")

    return color

#starting up
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=STATUS)) #<<<<------- 
    print("ready and good to go")

# Error Handler
@bot.event
async def on_command_error(ctx, error):

    # User has entered wrong Arguements (Arguement Sequence)
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.TooManyArguments):

        # User tests this Command to get Information about it
        if ctx.message.content in ['-' + ctx.command.name] + ['-' + i for i in ctx.command.aliases]:
            with open("donut/commands.json", "r") as f:
                file=json.load(f)
            await ctx.send(embed=discord.Embed(
                title=ctx.command.name + "  " + ctx.command.signature, 
                description=file[ctx.command.name]+ "\n\n" + f"Aliases: `{'`, `'.join(ctx.command.aliases) if ctx.command.aliases != [] else 'None'}`", 
                color=get_custom_color())
                )
        else:

            # User simply entered wrong Arguements
            await ctx.send(embed=embed_error(str(ctx.command.name) + "  " + str(ctx.command.signature), str(error)))

    # User uses Commands that need a Server to function in DMs
    elif isinstance(error, commands.NoPrivateMessage):
        await ctx.send(embed=embed_error("This command is only available in Servers. Sorry"))

    # User enters wrong Arguement Type
    elif isinstance(error, commands.BadArgument):
        await ctx.send(embed=embed_error('-' + str(ctx.command.name) + ' ' + str(ctx.command.signature), str(error)))

    # Bot cannot execute Command due to Missing Permissions in a Server (Moderation Commands)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(embed=embed_error("I'm missing Permissions to run this Command", str(error)))

    # User is not supposed to use Command  (Is missing Permissions himself)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=embed_error("Nice try. You do not have the Permissions to use this Command", str(error)))

    # Object of Arguement could not be found (Likely invalid or restricted)
    elif isinstance(error, commands.ChannelNotFound) or isinstance(error, commands.MessageNotFound) or isinstance(error, commands.RoleNotFound) or isinstance(error, commands.MemberNotFound):
        await ctx.send(embed=embed_error(str(error)))

    # No such Command found 
    elif isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(embed=embed_error(str(error)))

    # Else statement to catch all Errors of other Categories than the above ones
    else:
        if str(error).startswith("Command raised an exception: Forbidden: 403 Forbidden (error code: 50013)"):
            await ctx.send(embed=embed_error("I'm missing Permissions to run this Command", str(error)))
        else:
            await ctx.send(embed=embed_error(f"An Error occured within command {ctx.command.name}"))
            print(error)


# Adding Cogs to the Bot (Cogs make Code cleaner)
initial_extentsions = [
    'cogs.moderation',
    'cogs.levels',
    'cogs.starboard'
]

if __name__ == "__main__":
    for extension in initial_extentsions:
        bot.load_extension(extension)

guildid = 817239422881103893

#bumproleid = 763546928381820928
#bumpchannelid = 758389116047720459
#
#async def bumpreminder():
#    await asyncio.sleep(2)
#    await bot.wait_until_ready()
#
#    time = datetime.now()
#    if time.hour < 12:
#        start_time = datetime.now().replace(hour=12, minute=0, microsecond=0)
#    else:
#        start_time = datetime.now().replace(hour=12, minute=0, microsecond=0)
#        start_time = start_time + timedelta(days=1)
#
#    time_delta = (start_time - time).total_seconds()
#    print(str(time_delta) + '\n' + str(round(time_delta)))
#    await asyncio.sleep(round(time_delta))
#
#    while not bot.is_closed():
#        channel = bot.get_channel(bumpchannelid)
#        guild = bot.get_guild(guildid)
#        role = guild.get_role(bumproleid)
#
#        await channel.send(role.mention)
#
#        await channel.send(embed=discord.Embed(color=get_custom_color(), description=f"<:moon:787193302004924427> Time to bump the server with !d bump <:moon:787193302004924427> "))
#
#        await asyncio.sleep(60 * 60 * 2.1)

voteroleid = 828728856079761458
votechannelid = 825468696083562508

async def votereminder():
    await asyncio.sleep(2)
    await bot.wait_until_ready()

    time = datetime.now()
    if time.hour < 12:
        start_time = datetime.now().replace(hour=12, minute=0, microsecond=0)
    else:
        start_time = datetime.now().replace(hour=12, minute=0, microsecond=0)
        start_time = start_time + timedelta(days=1)

    time_delta = (start_time - time).total_seconds()
    print(str(time_delta) + '\n' + str(round(time_delta)))
    #await asyncio.sleep(round(time_delta))

    while not bot.is_closed():
        channel = bot.get_channel(votechannelid)
        guild = bot.get_guild(guildid)
        role = guild.get_role(voteroleid)

        await channel.send(str(role.mention))

        await channel.send(embed=discord.Embed(color=discord.Color.purple(), description=f"Please vote for us using this link: https://top.gg/servers/817239422881103893/vote To vote you simply need to tap the link to log in, then exit the tab. Then tap the link again and press the vote button!"))

        await asyncio.sleep(60 * 60 * 12.1)


#bot.loop.create_task(bumpreminder())
bot.loop.create_task(votereminder())

        
# Running the Bot after everything is set up
bot.run(TOKEN)
