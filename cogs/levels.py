# Imports
import discord
from discord import message
from discord.ext import commands
import json
from discord.utils import get
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import datetime
import asyncio
import random

level_list = {}

def create_level_list():
    num = 15
    prev_num = 15
    level_list[0] = 1
    for i in range(0, 100):
        level_list[num] = i + 2
        num = round(prev_num + prev_num * 0.075 + 100)
        prev_num = num

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
class Levels(commands.Cog):

    # Mandatory Function to assign self.bot to the Bot instance of main.py
    def __init__(self, bot):
        self.bot = bot

    # ----------------------- FUNCTIONS -----------------------

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel != None and message.author.bot == False:
            with open("levels.json", "r") as f:
                file = json.load(f)

            if str(message.author.id) in list(file):
                file[str(message.author.id)] += 1
            else:
                file[str(message.author.id)] = 1

            if level_list == {}:
                create_level_list()
            
            if file[str(message.author.id)] in list(level_list):
                level = level_list[file[str(message.author.id)]]
                channel = self.bot.get_channel(825210956145623080)
                await channel.send(f"Nice, {message.author.mention}, you just advanced to level {level}! \n Stay active and reach higher levels!")

            with open("levels.json", "w") as f2:
                json.dump(file, f2)

    @commands.command()
    async def rank(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author

        with open("levels.json", "r") as f:
            file = json.load(f)

        if str(member.id) not in list(file):
                file[str(member.id)] = 0

        if level_list == {}:
            create_level_list()

        prev_i = 0
        msgs_2 = 0
        counter = 0
        for i in list(level_list):
            if file[str(member.id)] > prev_i and file[str(member.id)] < i:
                counter = prev_i
                msgs_2 = i - file[str(member.id)]

            prev_i = i
        level = level_list[counter]

        grammarly_correct = " is " if member != ctx.author else ": You are "

        await ctx.send(embed=discord.Embed(color=get_custom_color(), description=f"{member.name}{grammarly_correct}currently on level **{level}** \n with **{file[str(member.id)]}** messages sent in total.\n\n About {round(msgs_2 / 10) * 10} Messages more for the next level. Happy talking!"))

    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx):
        with open("levels.json", "r") as f:
            file = json.load(f)

        if level_list == {}:
            create_level_list()
        
        list2 = []

        for i in list(file):
            try:
                m = ctx.guild.get_member(int(i))
                if m.bot == True:
                    continue
            except:
                pass
            
            prev_i = 0
            counter = 0
            for i2 in list(level_list):
                if file[str(i)] > prev_i and file[str(i)] < i2:
                    counter = prev_i

                prev_i = i2

            
            try:
                level = level_list[counter]
            except:
                level = 1
            
            name = str(ctx.guild.get_member(int(i)))
            
            list2.append([name, file[i], level])
            
        
        list2 = sorted(list2, key=lambda x: x[1], reverse=True)

        ranking_str = ["Rank; Level; Messages sent; Name"]
        counter = 0

        for i in list2:
            counter += 1

            if counter >= 16 and i[0] != str(ctx.author):
                continue

            for number in range(1, 6):
                if len(str(i[1])) < 6:
                    i[1] = str(i[1]) + " "

            for number in range(1, 3):
                if len(str(i[2])) < 3:
                    i[2] = str(i[2]) + " "
            
            if i[0] == str(ctx.author):
                ranking_str.append(f"**{counter}.   {i[2]}  {i[1]}  {i[0]}**")
            else:
                ranking_str.append(f"{counter}.   {i[2]}  {i[1]}  {i[0]}")

        ranking_str = "\n".join(ranking_str)

        await ctx.send(embed=discord.Embed(color=get_custom_color(), title="Art Garden's leaderboard", description=ranking_str))

    @commands.command(aliases=["blööm"])
    async def bloom(self, ctx):
        gif = random.choice([
            "https://tenor.com/view/floral-gif-7706411", 
            "https://tenor.com/view/relax-rain-anime-flower-gif-15454955", 
            "https://tenor.com/view/sarah-flower-gif-19730157", 
            "https://tenor.com/view/anime-anime-gif-flower-rain-gif-19978784", 
            "https://tenor.com/view/anime-flower-aesthetic-rose-gif-9490271", 
            "https://tenor.com/view/flowers-anime-anime-night-anime-flower-aesthetic-gif-20174502", 
            "https://tenor.com/view/flowers-flower-pretty-anime-aesthetic-gif-18783703",
            "https://tenor.com/view/flowers-anime-cute-kawaii-gif-9032319",
            "https://tenor.com/view/yellow-flower-rose-petals-gif-17032738",
            "https://tenor.com/view/blossom-flowers-cherry-blowers-bloom-gif-16747555",
            "https://tenor.com/view/flowers-bloom-blossom-flower-tree-gif-5509954",
            "https://tenor.com/view/anime-anime-gif-water-flower-gif-19978794",
            "https://tenor.com/view/kawaii-pink-anime-cherry-blossom-pastel-gif-20721840",
            "https://tenor.com/view/spring-fall-weather-peaceful-anime-gif-17094122",
            "https://tenor.com/view/rose-flower-dew-dripping-water-gif-8730197"])
        await ctx.send(gif)
        


    # Simple Command to inform People about Me (Daev) making Bots
    @commands.command(aliases=["daev", "dave", "bot"])
    async def custombot(self, ctx):
        embed_bot = discord.Embed(title=f"{self.bot.user.name} was created by Dæv•#7540", color=discord.Color.blurple(), description="""
If you spot a bug, typo or error, inform me or the staff

Contact me if you are interested in your own bot
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

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def vote(self, ctx):
        await ctx.send(embed=discord.Embed(color=discord.Color.green(), description="Click [here](https://top.gg/servers/817239422881103893/vote) to vote. Just click on the link, log into top.gg, and exit the link. Then click the link again, watch a 5 second add, and hit the vote button! Thank you!"))

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def voterole(self, ctx, member: discord.Member):
        role = ctx.guild.get_role(828728856079761458)
        await member.add_roles(role, reason=f"Action by {str(ctx.author)} \n Added the Voter-Role [{role.name}] to {str(member)} for 12h")

        await ctx.send(embed=embed_success(f"{member.name}, you now have the {role.name}-role for 12 Hours!"))
    
        await asyncio.sleep(12 * 60 * 60)

        await member.remove_roles(role, reason=f"Temporary Role-Ownership ({role.name}) by {str(ctx.author)} for 12h ended")
        
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def temprole(self, ctx, member: discord.Member, hours, *, role):
        try:
            role = self.bot.get_role(int(role[3:-1]))
        except:
            pass
        
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
        
        hours = int(hours.split("h")[0].split(" ")[0])
        await member.add_roles(role, reason=f"Action by {str(ctx.author)} \n Added the Voter-Role [{role.name}] to {str(member)} for {hours}h")

        await ctx.send(embed=embed_success(f"{member.name}, you now have the {role.name}-role for {hours} Hours!"))

        await asyncio.sleep(hours * 60 * 60)

        await member.remove_roles(role, reason=f"Temporary Role-Ownership ({role.name}) by {str(ctx.author)} for {hours}h ended")

    @commands.command(aliases=["nick"])
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, nickname):
        await member.edit(nick=str(nickname))

        await ctx.send(embed=embed_success(f"{member.name}'s new nickname is {nickname}"))

    @commands.command(aliases=["controversialtopic"])
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def controversial(self, ctx, category: str="all"):
        controversial_topics = {
            "law": 
                """1. Should abortion be legalized everywhere?
2. Should the sale of marijuana become legal?
3. Should the use of drones be regulated?
4. Should wage equality between women and men be stapled by law?
5. Should prostitution be made legal?
6. Should deceased organ donation be made mandatory by law?
7. Should the death penalty be abolished everywhere?
8. Should gun ownership by members of the public be banned?
9. Should parents be held legally responsible for crimes committed by their underaged children?
10. Should same-sex couples be allowed to wed in religious temples?
11. Is the assisted suicide of a terminally ill patient moral?
12. Have religious holidays been taken over by consumerism?
13. Does donating money to poor people make them even more dependent?
14. Do interreligious marriages help to bring people closer together?
15. Is there racism towards Caucasians?
16. Can torturing a person be justified if it could help to save others?
17. Should men be encouraged to become stay-at-home fathers?
18. Should parents exercise control over the relationships of their teenage children?
19. Is lying justified when it is meant to protect someone?
20. Can body shaming motivate people to lose weight?
21. Should there be separate public bathrooms for transgender people?""",
            "business": 
                """22. Do free trade deals benefit less well-off countries?
23. Are family-owned businesses more stable than public companies?
24. Is the state of the economy the main factor for the birth rate decline in most European countries?
25. Will an increase in the minimum wage make all people better-off?
26. Is the sharing economy a temporary phenomenon?
27. Can protectionism help to reduce unemployment permanently?
28. Is income equality beneficial for the economy?
29. Does the advancement of technology have a significant negative impact on jobs in the banking industry?
30. Should the minting of coins stop?
31. Will the European Union countries be better off out of the EU?
32. Does progressive tax improve income equality?""",
            "healthcare": 
                """33. Are alternative cancer treatments effective?
34. Is child vaccination good or bad?
35. Is forced feeding an effective treatment for anorexia?
36. Do cigarette label warnings help to reduce the incidences of lung cancer?
37. Do slim people really have a lower heart disease, all other things being equal?
38. Can moderate to severe depression be cured without antidepressants?
39. Should obesity be considered a disease?
40. Can virtual reality help hospital patients deal with isolation?
41. Are antibiotics used excessively for the treatment of disease?
42. Should birth control pills and devices be made free for women?""",
            "nutrition":
                """33. Are alternative cancer treatments effective?
34. Is child vaccination good or bad?
35. Is forced feeding an effective treatment for anorexia?
36. Do cigarette label warnings help to reduce the incidences of lung cancer?
37. Do slim people really have a lower heart disease, all other things being equal?
38. Can moderate to severe depression be cured without antidepressants?
39. Should obesity be considered a disease?
40. Can virtual reality help hospital patients deal with isolation?
41. Are antibiotics used excessively for the treatment of disease?
42. Should birth control pills and devices be made free for women?""",
            "politics": 
                """33. Are alternative cancer treatments effective?
34. Is child vaccination good or bad?
35. Is forced feeding an effective treatment for anorexia?
36. Do cigarette label warnings help to reduce the incidences of lung cancer?
37. Do slim people really have a lower heart disease, all other things being equal?
38. Can moderate to severe depression be cured without antidepressants?
39. Should obesity be considered a disease?
40. Can virtual reality help hospital patients deal with isolation?
41. Are antibiotics used excessively for the treatment of disease?
42. Should birth control pills and devices be made free for women?""",
            "technology":
                """33. Are alternative cancer treatments effective?
34. Is child vaccination good or bad?
35. Is forced feeding an effective treatment for anorexia?
36. Do cigarette label warnings help to reduce the incidences of lung cancer?
37. Do slim people really have a lower heart disease, all other things being equal?
38. Can moderate to severe depression be cured without antidepressants?
39. Should obesity be considered a disease?
40. Can virtual reality help hospital patients deal with isolation?
41. Are antibiotics used excessively for the treatment of disease?
42. Should birth control pills and devices be made free for women?""",
            "education": 
                """33. Are alternative cancer treatments effective?
34. Is child vaccination good or bad?
35. Is forced feeding an effective treatment for anorexia?
36. Do cigarette label warnings help to reduce the incidences of lung cancer?
37. Do slim people really have a lower heart disease, all other things being equal?
38. Can moderate to severe depression be cured without antidepressants?
39. Should obesity be considered a disease?
40. Can virtual reality help hospital patients deal with isolation?
41. Are antibiotics used excessively for the treatment of disease?
42. Should birth control pills and devices be made free for women?""",
            "media": 
                """83. Should video games with violence be banned?
84. Do social medial make people more obsessed with the lives of celebrities?
85. Do romantic movies make men more romantic?
86. Will TV channels become a thing of the past in 20 years?
87. Should newspapers offer more recreational content?
88. Are modern media completely unbiased?
89. Are space movies realistic?""",
            "sports": 
                """90. Should medals be withdrawn from the entire team if one member has broken the rules?
91. Do great players make great coaches?
92. Should athletes be forced to retire after a certain age?
93. Does the growing cost of participating in sports put children off?
94. Should athletes taking performance-enhancing drugs due to a medical condition be allowed to take part in the Olympics?
95. Do sports become overly commercialized?""",
            "miscellaneous": 
                """96. Is money the primary factor for measuring success?
97. Can winning the lottery bring you lasting happiness?
98. Is the simplest solution always the best?
99. Are more rational people more content with their life?
100. Should we always trust our instincts?"""
            
        }
        category = category.lower()

        if category not in list(controversial_topics) and category != "all":
            await ctx.send(embed=embed_error("Select a valid category", f"You can pick those categories (or enter none at all): {', '.join(list(controversial_topics))}"))
        elif category == "all":
            random_topic = random.choice(controversial_topics)
            random_topic = random.choice(controversial_topics[random_topic].split("\n"))
            await ctx.send(embed=discord.Embed(color=get_custom_color, title=f"{random_topic}"))
        elif category in list(controversial_topics):
            random_topic = category
            random_topic = random.choice(controversial_topics[random_topic].split("\n"))
            await ctx.send(embed=discord.Embed(color=get_custom_color, title=f"{random_topic}"))

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        with open("warnings.json", "r") as f:
            data=json.load(f)

        reason = f"Reason: {reason}" if reason != None else "No Reason was given"

        if str(member.id) not in list(data):
            data[str(member.id)] = 1
        else:
            data[str(member.id)] += 1

        with open("warnings.json", "w") as f:
            json.dump(data, f)
        
        await member.send(embed=embed_error(f"You have been warned [Art Garden]", f"Reason: `{reason}` \n\nCurrent total warnings: {data[str(member.id)]}"))
        
        await ctx.send(embed=embed_success(f"{str(member)} has been warned", f"Reason: `{reason}` \n\nCurrent total warnings: {data[str(member.id)]}"))

        channel = self.bot.get_channel(825206612196720640)
        crnt_time = datetime.datetime.now()
        crnt_time = crnt_time.strftime("%B %d, %X")
        await channel.send(embed=discord.Embed(color=discord.Color.red(), title=f"{str(member)} has been warned | Moderator: {str(ctx.author)}", description=f"{crnt_time} \n\nReason: `{reason}` \n\nCurrent total warnings: {data[str(member.id)]}"))

    @commands.command(aliases=["pardon"])
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def unwarn(self, ctx, member: discord.Member):
        with open("warnings.json", "r") as f:
            data=json.load(f)

        if str(member.id) not in list(data):
            data[str(member.id)] = 0

            await ctx.send(embed=embed_error(f"{str(member)} has no warnings"))
        else:
            data[str(member.id)] -= 1

            await ctx.send(embed=embed_success(f"{str(member)} was unwarned", f"Current total warnings: {data[str(member.id)]}"))

        with open("warnings.json", "w") as f:
            json.dump(data, f)
        

    @commands.command(aliases=["warnings"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def warns(self, ctx, member: discord.Member):
        with open("warnings.json", "r") as f:
            data=json.load(f)

        if str(member.id) in data:
            warns = data[str(member.id)]
        else:
            warns = 0

        await ctx.send(embed=embed_success(f"{str(member)} has {warns} Warnings"))
        
    # ----------------------- FUNCTIONS -----------------------

# Adding the Cog Object
def setup(bot):
    bot.add_cog(Levels(bot))
