# Imports
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import asyncio
import discord
from discord.ext import commands

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

# Function to check if a message meets the criteria to get into the starboard
def isvalid(message):
    isvalid = False
    if len(message.reactions) >= 1:
        for i in message.reactions:

            # Check if more than 5 people "upvoted" this message
            if str(i.emoji) in (':moon:', '<:moon:787193302004924427>'):
                if i.count == 1: #Change this later to 5 ------------------------------- done
                    isvalid = True
    return isvalid

# Function to evaluate the customizable Embed Color of the Bot
def get_custom_color():
    with open("donut/storage.json", "r") as f:
        file=json.load(f)

    color = eval(f"discord.Color.{'_'.join(file['special-color'].split(' '))}()")

    return color

# Actual Cog with Commands and Events
class Starboard(commands.Cog):

    # Mandatory Function to assign self.bot to the Bot instance of main.py
    def __init__(self, bot):
        self.bot = bot

    # Function to get the Message items and send them to the (customizable) starboard-channel
    async def starboard_send(self, message):
        channel_fetch = message.channel.id
        id_fetch = message.id

        # getting the starboard channel and setting an Embed up
        with open("donut/storage.json", "r") as f:
            file=json.load(f)
        starboard = self.bot.get_channel(file["starboard-channel"])
        embed_starboard = discord.Embed(color=get_custom_color(), description=message.content if message.content != None else '\uFEFF')
       
        # Customizing the Embed
        embed_starboard.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))
        embed_starboard.add_field(name="Jump to Original", value=f"[**Jump**]({message.jump_url})")
        
        #print(3)
        # Finding an Image, if it exists
        image = "None found"
        for i in message.attachments:
            try:
                # Checking if this Attachment has attrubutes of height or width (Which only images have)
                if hasattr(i, "width") or hasattr(i, "height"):
                    image = i.url
                    break
                else:

                    # Checking the filename extensions as other method to find an image
                    for ending in ['jpg', 'jpeg', 'png', 'tiff', 'gif', 'psg', 'pdf', 'eps', 'ai', 'raw', 'indd']:
                        if i.filename.lower().endswith(ending):
                            image = i.url
                            break
            
            # If something went wrong in the try part above, this would look for filename extensions again
            except:
                for ending in ['jpg', 'jpeg', 'png', 'tiff', 'gif', 'psg', 'pdf', 'eps', 'ai', 'raw', 'indd']:
                    if i.filename.lower().endswith(ending):
                        image = i.url
                        break

        # Adding an Image to the embed, if the image variable now represents an url
        if str(image) != "None found":
            embed_starboard.set_image(url=str(image))
        
        count = 0
        for i in message.reactions:
            if str(i.emoji) in (':moon:', '<:moon:787193302004924427>'):
                    count = i.count
        starmsg = await starboard.send(f"<:moon:787193302004924427> **{count}** {message.channel.mention} [{message.channel.id}]")
        await starboard.send(embed=embed_starboard)
        #print(4)
        channel_fetch2 = starmsg.channel.id
        id_fetch2 = starmsg.id

        # Periodiacally Updating the Star-Counter in intervals of 10 minutes (Updating it for 5hours)
        for x in range(720 * 2):
            await asyncio.sleep(60)
            message = self.bot.get_channel(channel_fetch)
            message = await message.fetch_message(id_fetch)
            for i in message.reactions:
                if str(i.emoji) in (':moon:', '<:moon:787193302004924427>') and i.count != count:
                    count = i.count
                    starmsg = self.bot.get_channel(channel_fetch2)
                    starmsg = await starmsg.fetch_message(id_fetch2)
                    await starmsg.edit(content=f"<:moon:787193302004924427> **{count}** {message.channel.mention} [{message.channel.id}]")
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        #print(1)
        if payload.guild_id != None:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            
            # Adding the blacklist for things that should not come to the starboard channel
            with open("donut/storage.json", "r") as f:
                file=json.load(f)
            if file["starboard-blacklist"] != None:
                blacklist_channels = list(file["starboard-blacklist"])
            else:
                blacklist_channels = []


            if message.channel.id not in blacklist_channels:

                if isvalid(message) == True:
                    #print(2)
                    await self.starboard_send(message)


    # Custom Command to set up the blacklisted Channels from Starboard
    @commands.command(aliases=["starboard-blacklist"])
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def starboardblacklist(self, ctx, add_or_remove, channel: discord.TextChannel):
        with open("donut/storage.json", "r") as f:
            file=json.load(f)
            
        if file["starboard-blacklist"] == None:
            file["starboard-blacklist"] = []
        
        # Adding a Channel to the Blacklist
        if add_or_remove == "add":
            file["starboard-blacklist"] = list(file["starboard-blacklist"]).append(channel.id)
            await ctx.send(embed=embed_success(f"{channel.name} was added to the Starboard-Blacklist", "It will now be ignored by the Starboard-System"))
        
        # Removing a Channel from the Blacklist
        elif add_or_remove == "remove": 
            file["starboard-blacklist"] = list(file["starboard-blacklist"]).remove(channel.id)
            await ctx.send(embed=embed_success(f"{channel.name} was removed from the Starboard-Blacklist", "It won't be ignored by the Starboard-System anymore"))
        
        # False Action-Parameter Handler
        else:
            await ctx.send(embed=embed_error(f"{add_or_remove} is not a valid Parameter for add_or_remove", "You (obviously) need to chose between `add` or `remove`"))

        # Saving all changes by overwriting the file with the changed one
        with open("donut/storage.json", "w") as f:
            json.dump(file, f)
    

    # ----------------------- FUNCTIONS -----------------------

# Adding the Cog Object
def setup(bot):
    bot.add_cog(Starboard(bot))