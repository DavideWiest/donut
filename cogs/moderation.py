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
    with open("donut/storage.json", "r") as f:
        file=json.load(f)

    color = eval(f"discord.Color.{'_'.join(file['special-color'].split(' '))}()")

    return color

# Actual Cog with Commands and Events
class Moderation(commands.Cog):

    # Mandatory Function to assign self.bot to the Bot instance of main.py
    def __init__(self, bot):
        self.bot = bot
    
    # ----------------------- FUNCTIONS -----------------------

    # Command to delete roles
    @commands.command(aliases=['delete-role', 'del-role'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def delrole(self, ctx, *, role):

        rolegot = False

        # Check if the role Arguement isnt already a Role (@Rolename etc.) but a String ("Rolename" or just Rolename)
        # The code inside the if statement will find a Role from a string, so it needs to be skipped if the arguement is already a role object
        if not isinstance(role, discord.Role):

            # Iteratinng through all roles of the server to check
            for i in ctx.guild.roles:
                
                # Looking if the role name starts/ends with the role parameter, or is equal to it
                if i.name.lower().startswith(role.lower()) or i.name.lower().endswith(role.lower()) or i.name.lower() == role.lower() or str(i.id) == str(role[3:-1]):
                    rolegot = True
                    role = i
                    break
            
            # Look if the code above didnt already find a role
            if rolegot == False:

                # Running the code finder again if the statement above triggered
                for i in ctx.guild.roles:
                    
                    # Looking if the role name starts/ends with the role parameter, or is equal to it, Or if the role parameter is one item of the single parts of the role inside the iteration
                    if role.lower() in i.name.split(" ") or i.name.lower().startswith(role.lower()) or i.name.lower().endswith(role.lower()) or i.name.lower() == role.lower() or str(i.id) == str(role[3:-1]):
                        rolegot = True
                        role = i
                        break
        
        # Deleting the Role (with Passing the Comitter inside the reason) & sending a response
        await role.delete(reason=f"Action by {str(ctx.author)} [{str(ctx.author.id)}]")
        await ctx.send(embed=embed_success(f"Deleted the Role \'{role.name}\'"))

    # Command to remove a role from a specific Member
    @commands.command(aliases=['remrole', 'remove-role'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def removerole(self, ctx, member: discord.Member=None, *, role):
        await ctx.trigger_typing()
        
        if member == None:
            member = ctx.author

        rolegot = False

        # Trying to get role object by mentioned string
        try:
            role = self.bot.get_role(int(role[3:-1]))
        except:
            pass
        
        # Check if the role Arguement isnt already a Role (@Rolename etc.) but a String ("Rolename" or just Rolename)
        # The code inside the if statement will find a Role from a string, so it needs to be skipped if the arguement is already a role object
        if not isinstance(role, discord.Role):

            # Iteratinng through all roles of the server to check
            for i in ctx.guild.roles:
                
                # Looking if the role name starts/ends with the role parameter, or is equal to it
                if i.name.lower().startswith(role.lower()) or i.name.lower().endswith(role.lower()) or i.name.lower() == role.lower() or str(i.id) == str(role[3:-1]):
                    rolegot = True
                    role = i
                    break
            
            # Look if the code above didnt already find a role
            if rolegot == False:

                # Running the code finder again if the statement above triggered
                for i in ctx.guild.roles:
                    
                    # Looking if the role name starts/ends with the role parameter, or is equal to it, Or if the role parameter is one item of the single parts of the role inside the iteration
                    if role.lower() in i.name.split(" ") or i.name.lower().startswith(role.lower()) or i.name.lower().endswith(role.lower()) or i.name.lower() == role.lower() or str(i.id) == str(role[3:-1]):
                        rolegot = True
                        role = i
                        break
        
        # Removing the Role from a Member (with Passing the Comitter inside the reason) & sending a response
        await member.remove_roles(role, reason=f"Action by {str(ctx.author)} [{str(ctx.author.id)}] \n ")
        await ctx.send(embed=embed_success(f'Remove \'{role.name}\' from {member.name}\'s Roles.'))

    # Command to give a Role to a specific Member
    @commands.command(aliases=['grantrole', 'give-role', 'giverole'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member=None, *, role):
        await ctx.trigger_typing()
        
        if member == None:
            member = ctx.author 
        
        rolegot = False

        # Check if the role Arguement isnt already a Role (@Rolename etc.) but a String ("Rolename" or just Rolename)
        # The code inside the if statement will find a Role from a string, so it needs to be skipped if the arguement is already a role object
        if not isinstance(role, discord.Role):
            
            # Iteratinng through all roles of the server to check
            for i in ctx.guild.roles:
                
                # Looking if the role name starts/ends with the role parameter, or is equal to it
                if i.name.lower().startswith(role.lower()) or i.name.lower().endswith(role.lower()) or i.name.lower() == role.lower() or str(i.id) == str(role[3:-1]):
                    rolegot = True
                    role = i
                    
                    break
            
            # Look if the code above didnt already find a role
            if rolegot == False:

                # Running the code finder again if the statement above triggered
                for i in ctx.guild.roles:
                    
                    # Looking if the role name starts/ends with the role parameter, or is equal to it, Or if the role parameter is one item of the single parts of the role inside the iteration
                    if role.lower() in i.name.split(" ") or i.name.lower().startswith(role.lower()) or i.name.lower().endswith(role.lower()) or i.name.lower() == role.lower() or str(i.id) == str(role[3:-1]):
                        rolegot = True
                        role = i
                        break
            
        # Adding the Role to Someone (with Passing the Comitter inside the reason) & sending a response
        await member.add_roles(role, reason=f"Action by {str(ctx.author)} [{str(ctx.author.id)}] \n ")
        await ctx.send(embed=embed_success(f'Added \'{role}\' to {member.name}\'s roles.'))

    # This Command will create a new Role with custom Color
    @commands.command(aliases=['createrole'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def newrole(self, ctx, *, name_and_color_seperated):
        
        # Seperating the Name and Color
        try:
            name, color = name_and_color_seperated.split(', ')

        # If this does not work, the color will be defaulted
        except:
            name = name_and_color_seperated
            color = "default"

        # Creating the Role & sending a response
        try:
            await ctx.guild.create_role(name=name, colour=eval(f"discord.Color.{'_'.join(color.lower().split(' '))}()"))
            await ctx.send(embed=embed_success(f'Added {name} to roles.', f'Color: {color}'))

        # Catching Errors when used inappropriately
        except:
            await ctx.send(embed=embed_error("Please use the command like this", "-newrole Name, color (blue, green, yellow, blurple etc.) or -newrole Name (color then defaulted)"))

    # Will Kick a Member
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member , *, reason=None):

        # Setting up reason-string
        reason = f"Reason: {reason}" if reason != None else "No Reason was given"

        # Informing the kicked Member
        await member.send(embed=embed_error(f'You have been kicked \n From: **{str(ctx.guild)}** \n By: **{str(ctx.author)}**', f'`{reason}`'))

        # Kicking him
        await member.kick(reason=f"Action by {str(ctx.author)} [{str(ctx.author.id)}] \n {reason}")

        # sending responses
        await ctx.send(embed=embed_success(f'**{str(member)}** was kicked by **{str(ctx.author)}**', f'`{reason}`'))
        
    # Will ban a Member
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):

        # Setting up reason-string
        reason = f"Reason: {reason}" if reason != None else "No Reason was given"

        # Informing the banned Member
        await member.send(embed=embed_error(f'You have been banned \n From: **{str(ctx.guild)}** \n By: **{str(ctx.author)}**', f'`{reason}`'))

        # Kicking him
        await member.ban(reason=f"Action by {str(ctx.author)} [{str(ctx.author.id)}] \n {reason}")

        # sending responses
        await ctx.send(embed=embed_success(f'**{str(member)}** was banned by **{str(ctx.author)}**', f'`{reason}`'))


    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def unban(self, ctx, member: str, *, reason=None):

        bannedmembers = await ctx.guild.bans()
        try:
            member_name, member_disc = member.split('#')
        except:
            member_name = member
            member_disc = member

        # finding the banned person and unbanned it
        for ban_entry in bannedmembers:
            user = ban_entry.user
            
            #print(user)
            #print(str(user.id))
            #print(str(member))
            #print(member)
            if (user.name, user.discriminator) == (member_name, member_disc) or str(user.id) == member:
                await ctx.guild.unban(user, reason=f"Action by {str(ctx.author)} [{str(ctx.author.id)}] \n {reason}")
            

        # Setting up reason-string
        reason = f"Reason: {reason}" if reason != None else "No Reason was given"

        # sendng responses
        await ctx.send(embed=embed_success(f'**{str(member)}** was unbanned by **{str(ctx.author)}**', f'`{reason}`'))

    # Muting a Member until he will be unmuted
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member, reason=None):
        mutedworked = False

        # Setting up reason-string
        reason = f"Reason: {reason}" if reason != None else "No Reason was given"

        # Finding the needed Role and granting it the Member so he will be Muted
        for role in ctx.guild.roles:
            if role.name == 'Muted':
                await member.add_roles(role)

                await ctx.send(embed=embed_success(f'**{str(member)}** has been muted \n By: **{str(ctx.author)}**', f'`{reason}`'))
                
                mutedworked = True
                break
            
        # muting the Member with a new Role if there is none
        if mutedworked == False:
                
            # process of creating the Muted role
            overwrite = discord.PermissionOverwrite(send_messages=False)
            newrole = await ctx.guild.create_role(name='Muted')

            # Overwriting the Permissions to make the Muted role do its job
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(newrole, overwrite=overwrite)

            await member.add_roles(newrole)

            await ctx.send(embed=embed_success(f'**{str(member)}** has been muted \n By: **{str(ctx.author)}**', f'`{reason}`'))
            
    # Command to mute someone for a specified time
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def tempmute(self, ctx, member: discord.Member, time, *, reason=None):
        mutedworked = False

        # Setting up reason-string
        reason = f"Reason: {reason}" if reason != None else "No Reason was given"

        # Finding the needed Role and granting it the Member so he will be Muted
        for role in ctx.guild.roles:
            if role.name == 'Muted':
                await member.add_roles(role)

                await ctx.send(embed=embed_success(f'**{str(member)}** has been muted \n By: **{str(ctx.author)}**', f'`{reason}`'))
                
                mutedworked = True
                break
            
        # muting the Member with a new Role if there is none
        if mutedworked == False:

            # process of creating the Muted role
            overwrite = discord.PermissionOverwrite(send_messages=False)
            newrole = await ctx.guild.create_role(name='Muted')

            # Overwriting the Permissions to make the Muted role do its job
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(newrole, overwrite=overwrite)

            await member.add_roles(newrole)

            await ctx.send(embed=embed_success(f'**{str(member)}** has been muted \n By: **{str(ctx.author)}**', f'`{reason}`'))
            
        # Setting up the muted time
        time = time.split(" ")
        muted_for = 0
        for i in time:

            # looking which category the parts of time belong to and adding them to the muted_for variable (by removing the last item it will be a number)
            if i.endswith("d"):
                muted_for += int(i[:-1]) * 60 * 60 * 24
            elif i.endswith("h"):
                muted_for += int(i[:-1]) * 60 * 60
            elif i.endswith("m"):
                muted_for += int(i[:-1]) * 60
            elif i.endswith("s"):
                muted_for += int(i[:-1])

        # Waiting until the time dued
        await asyncio.sleep(muted_for)
            
        # Finding and removing the 'Muted' role
        for role in ctx.guild.roles:
            if role.name == 'Muted':
                        
                await member.remove_roles(role, reason=f"Temporary Mute by {str(ctx.author)} finished  [{muted_for / 60} Minutes]")

    # For unmuting someone
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member):
        umuteworked = False

        # Finding and Removing the role
        for role in ctx.guild.roles:
            if role.name == 'Muted':
                await member.remove_roles(role)
                await ctx.send(embed=embed_success(f'{member.name} has been unmuted'))
                umuteworked = True
                break
        
        # Error catched if the Member was not muted
        if not umuteworked:
            await ctx.send(embed=embed_error(f'{str(member)} was not muted'))
    
    # Delete an amount of Messages from a Channel
    @commands.command(aliases=['purge', 'prune'])
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):

        # Deleting the Messages (amount + 1 will delete the amount with respect to the command triggering it)
        if  amount > 0:

            # Setting Maximum of Deleted Messages to 200

            await ctx.channel.purge(limit=amount+1)
            
            await ctx.send(embed=embed_success(f"{str(amount)} Messages have been deleted", f"By {str(ctx.author)}"), delete_after=8)

        # Catching Logical-Error
        else:
            await ctx.send(embed=embed_error(f"Please choose a number above 0"), delete_after=8)

    # Advanced Poll command
    @commands.command(aliases=["poll2"])
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def multipoll(self, ctx, *, args):
        if ctx.guild != None:
            await ctx.channel.purge(limit=1)
        
        # Extracting the optional value when the poll ends
        try:
            args, stats = args.split("end=")
        except:
            stats = None
        
        # Extracting the optional value which color the poll embed should have
        try:
            args, color = args.split("color=")
        except:
            color = get_custom_color()
        
        # Setting up the avaialble options and a title
        questionlist = args.split(";")
        if len(questionlist) >= 3:
            title = questionlist[0]
            questionlist = list(questionlist[1:])
        else:
            title = "A new Poll appeared"
        
        # setting up a dict to take the place of questionlist
        questiondict = {}
        for counter, item in enumerate(questionlist[1:]):
            questiondict[counter + 1] = item
        
        # Enumerating options
        questionlist = []
        for i in questiondict:
            questionlist.append(f"{str(i)}. {questiondict[i]}")

        # Setting up the Embed
        embed_poll = discord.Embed(color=eval(f"discord.Color.{color}()"), title=title, description="\n".join(questionlist))
        embed_poll.set_author(name=ctx.author.name, icon_url=str(ctx.author.avatar_url))
        msg = await ctx.send(embed=embed_poll)
        
        # Adding the Reactions (No, i cant to it that much simpler, the enterpreter would throw me an Unicode Error)
        for counter, item in enumerate(questionlist):
            
            if counter < 9:
                if counter == 0:
                    await msg.add_reaction("1\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 1:
                    await msg.add_reaction("2\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 2:
                    await msg.add_reaction("3\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 3:
                    await msg.add_reaction("4\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 4:
                    await msg.add_reaction("5\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 5:
                    await msg.add_reaction("6\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 6:
                    await msg.add_reaction("7\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 7:
                    await msg.add_reaction("8\N{variation selector-16}\N{combining enclosing keycap}")
                if counter == 8:
                    await msg.add_reaction("9\N{variation selector-16}\N{combining enclosing keycap}")
            else:
                
                # Emoji for 10
                await msg.add_reaction("\N{keycap ten}")
                break
        

        msg_id = msg.id
        
        # Poll Ending Part
        if stats != None:
            
            # Waiting until the time in minutes elapsed or sleeping for 12 h as default value
            try: 
                await asyncio.sleep(int(round(float(stats))) * 60)
            except:
                await asyncio.sleep(86400 / 2)

            # Fetching the Message to get the updated version
            msg = await ctx.fetch_message(int(msg_id))
            
            optionlist = []
            
            # appending emojies
            for i in msg.reactions:
                if i.count-1 >= 1:
                    optionlist.append([str(i.emoji), int(i.count -1)])
            
            # sorting them to make a winner
            optionstr = []
            optionsorted = sorted(optionlist, reverse=True, key=lambda x: x[1])
            
            optionstr.append("Ranking Option ---- Votes")
            counter = 0
            
            # Data put into a string
            for i in optionsorted:
                counter += 1
                optionstr.append(f"{counter}.        {i[0]} ––– {i[1]}")
            
            # wontwork there to look if there is only one option
            wontwork=False
            try:
                optionsorted[0]
                optionsorted[1]
            except:
                wontwork=True
            
            # evaluating Winner (and Term)
            if not wontwork:
                if optionsorted[0][1] != optionsorted[1][1]:
                    result = f"Option {optionsorted[0][0]} wins Mayority"
                    
                else:
                    result = f"Tie Between Option {optionsorted[0][0]} and {optionsorted[1][0]}"
            else:
                try:
                    result = f"Option {optionsorted[0][0]} wins Mayority"
                except:
                    result = "No Votes"
        
            # Sending the Poll Results
            final = '\n'.join(optionstr)
            
            embed_results=discord.Embed(title=f"Results: {result}", description=f"{final}", color=eval(f"discord.Color.{color}()"))
            
            await ctx.send(embed=embed_results)
            
            # Ending the Poll
            for i in msg.reactions:
                await i.clear()
            
            embed_poll.title = "Poll Ended"
            await msg.edit(embed=embed_poll)

            


    # Simple Poll Command
    @commands.command(aliases=["create-poll"])
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def poll(self, ctx, *, question):
        await ctx.channel.purge(limit=1)

        # Setting up and Sending Embed
        embed_poll = discord.Embed(color=get_custom_color(), title=str(question))
        embed_poll.set_footer(text="Support, Disagree or stay neutral?")
        embed_poll.set_author(name=ctx.author.name, icon_url=str(ctx.author.avatar_url))
        msg = await ctx.send(embed=embed_poll)

        # Adding Reactions (ThumbsUp, ThumbsDown, N for Neutral or No Answer)
        await msg.add_reaction("\U0001f44d")
        await msg.add_reaction("\U0001f44e")
        await msg.add_reaction("\U0001f1f3")

    # Customization Command
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set(self, ctx, parameter, *, new_value):
        if "to" in new_value.split(" "):
            new_value = new_value.split("to ")[1]

        parameter = parameter.lower()

        # If a channel was given, the new value will be its id since it is stored that way
        if isinstance(new_value, discord.TextChannel) or parameter in ("message-channel" , "starboard-channel"):
            try:
                parameter = parameter.id
            except:
                try:
                    parameter = self.bot.get_channel(parameter[3:-1]).id
                except:
                    try:
                        for i in ctx.guild.channels:
                            if i.name == parameter:
                                parameter = i.id
                    except:
                        await ctx.send(embed=embed_error("Select a channel for this customization parameter", "You should fix this by doing #joining-and-leaving-logs or mentioning the wanted channel"))

        # manipulating new value for the level-schema
        if parameter == "level-schema":
            try:
                new_value = [float(new_value.split(", ")[0]), float(new_value.split(", ")[1])]
            except:
                await ctx.send(embed=embed_error("Your Input was invalid", "Please reset it to `[12, 0.7]` or chose different values"))

        # will set the None value (to deactivate auto-messages) to an integer so other functions can work with it better
        if parameter in ("message-channel" , "starboard-channel") and new_value == "None":
            new_value = 0

        with open("donut/storage.json", "r") as f:
            file = json.load(f)

        # Checks if the parameter is actually a valid parameter
        if parameter in list(file):
            file[parameter] = new_value

            with open("donut/storage.json", "w") as f:
                json.dump(file, f)

            await ctx.send(embed=embed_success(f"Set {parameter} to {new_value}"))
        
        # Catching invalid Parameter Error
        else:
            await ctx.send(embed=embed_error(f"Parameter {parameter} is not customizable", f"Choose from: \n{', '.join(list(file))}"))


    # Help Command for a specific or all commands
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, command=None):

        # Help for a specific Command
        if command != None:
            with open("donut/commands.json", "r") as f:
                file=json.load(f)

            # Validating if the given command is a name or Alias of a Command
            if command.lower() not in [a.name for a in self.bot.commands] + [a.aliases for a in self.bot.commands]:
                await ctx.send(embed=embed_error("Did not find this Command", "Do -help to see all commands"))
            else:

                # getting the Command object from the given name/alias
                command = self.bot.get_command(command.lower())

                # setting up information and putting it into an embed
                signature = command.signature
                description = file[command.name]
                embed_help = discord.Embed(color=get_custom_color(), title=command.name + "  " + signature, description=description + "\n\n" + f"Aliases: `{'`, `'.join(command.aliases) if command.aliases != [] else 'None'}`")
                await ctx.send(embed=embed_help)
        
        # Help generally (no command given)
        else:
            with open("donut/commands.json", "r") as f:
                file=json.load(f)

            # setting up the Embed
            embed_help = discord.Embed(title=f"{self.bot.user.name}'s Commands", color=get_custom_color())

            # Putting the pieces of information into an Embed like above
            for command in self.bot.commands:
                signature = command.signature
                description = file[command.name]
                embed_help.add_field(name=command.name + "  " + signature, value='\uFEFF', inline=False) #, value=description + "\n\n" + f"Aliases: `{'`, `'.join(command.aliases) if command.aliases != [] else 'None'}`"
            
            embed_help.add_field(name='\uFEFF', value="**Make sure to check on commands closer with `-help <command>`**")

            # Sending Responses
            await ctx.author.send(embed=embed_help)
            await ctx.send(embed=embed_success("Done, check your DMs"))
    
    # Mini Command for simple testing
    @commands.command()
    async def test(self, ctx):
        gif = random.choice(["https://tenor.com/view/star-wars-han-solo-dont-do-it-no-dont-test-me-gif-12870482", "https://tenor.com/view/pedro-monkey-puppet-meme-awkward-gif-15268759", "https://tenor.com/view/yes-girl-yas-confetti-glitters-gif-6021125"])
        await ctx.send(gif)

    # Command to view setup/customization
    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def setup(self, ctx, parameter=None):
        with open("donut/storage.json", "r") as f:
            file=json.load(f)
        
        # Code to display the whole customization
        if parameter == None:
            customizationlist = []
            for i in file:

                # Normal Cases
                if i != "starboard-blacklist":

                    # Checking if i isnt an id of a text channel
                    if not isinstance(file[i], int):
                        customizationlist.append([i, file[i]])

                    # Handling text channels (getting their name or "Channel Not Found")
                    else:
                        try:
                            customizationlist.append([i, '#' + self.bot.get_channel(int(file[i])).name])
                        except:
                            customizationlist.append(i, "`Channel Not Found`")

                # Handling the special case of starboard-blacklist
                else:
                    if file[i] != [] and file[i] != None:
                        list_ = ['#' + self.bot.get_channel(int(a)).name for a in file[i]]
                        customizationlist.append([i, ', '.join(list_)])
                    else:
                        customizationlist.append([i, 'None'])
            
            # Sending the Customization in an embed (Fields for each value)
            embed_customization = discord.Embed(color=get_custom_color(), title="Customization")
            for i in customizationlist:
                embed_customization.add_field(name=i[0], value=i[1], inline=False)

            await ctx.author.send(embed=embed_customization)
            await ctx.send(embed=embed_success("Done, check your DMs"))

        # code to display a specific parameter
        else:
            if parameter in list(file):
                customizationlist = []
                i = parameter
                embed_customization = discord.Embed(color=get_custom_color(), title=f"Customization {parameter}")
                if parameter != "starboard-blacklist":
                    if not isinstance(file[parameter], int):
                        customizationlist.append([parameter, file[parameter]])
                    else:
                        try:
                            customizationlist.append([parameter, '#' + self.bot.get_channel(int(file[parameter])).name])
                        except:
                            customizationlist.append(parameter, "`Channel Not Found`")
                    
                else:
                    if file[parameter] != [] and file[parameter] != None:
                        list_ = ['#' + self.bot.get_channel(int(a)).name for a in file[parameter]]
                        customizationlist.append([parameter, ', '.join(list_)])
                    else:
                        customizationlist.append([parameter, 'None'])

                embed_customization.add_field(name=customizationlist[0][0], value=customizationlist[0][1])
                await ctx.author.send(embed=embed_customization)
                await ctx.send(embed=embed_success("Done, check your DMs"))
            else:
                await ctx.send(embed=embed_error(f"Could not find Parameter {parameter}, Sorry.", f"Parameters: {', '.join(list(file))}"))

    # Informational Command that shows you what parameters are customizable and gives further info on them
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def customizationhelp(self, ctx):

        # setting the Embed up, sending it later
        embed_customizationsheet = discord.Embed(
            title=f"{self.bot.user.name} Customization Sheet",
            color=get_custom_color(),
            description="""
**-->** `level-message` 
The message a user will receive upon leveling up 
Example: "Very nice, {}, you advanced to Level {}" (The first '{}' will always be the member, the second the level)

**-->** `level-schema`
The Mathematical Schema how many messages a Member needs to get to the next Level
Only Informed and Experienced should experiment with this
Example: [12, 0.7] Schema: [ 1) Number-Multiplied with Level Number, 2) Number added to 1) Muliplied with Previous Level]
Level 2 =  1) 12 * 2 + 2) 12 * 1 * 0.7

**-->** `welcoming-message`
The Welcoming Message when a Member joins
Example: "Welcome to {s}, {m}! Have a good time!" (The first '{s}' will always be the Server Name, the second the Member Name)

**-->** `leaving-message`
The leaving Message when a Member leaves
Example: "Bye, {m}. :/" (Here the '{m}' will represent the Member Name)

**-->** `message-channel`
The Channel where Member-Leaves and Joins are logged. Set to `None` to block it.
Example: #join-and-leave-logs

**-->** `starboard-channel`
The Channel where popular Messages/Images are posted to (Starboard-System)
Example: #starboard

**-->** `special-color`
The Bots Special Color (Simple Inputs like blue, green, red, grey, greyple, purple, default = black, yellow ...)

**-->** `starboard-blacklist`
The Channels that are ignored by the Starboard-System (Blacklisted)
Use Special Command `-starboard-blacklist add/remove *channel*` to configurate this List
            """
        )
        await ctx.author.send(embed=embed_customizationsheet)
        await ctx.send(embed=embed_success("Done, check your DMs"))

    # Mini Command to check the Latency
    @commands.command(aliases=["ping"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def latency(self, ctx):
        await ctx.send(embed=embed_success(f"Here 4 You in {round(self.bot.latency * 1000)}ms :D"))



    # ----------------------- FUNCTIONS -----------------------

# Adding the Cog Object
def setup(bot):
    bot.add_cog(Moderation(bot))
