from dotenv import load_dotenv
import discord, json, os, logging, time, re, string, os.path
from discord.ext import commands, tasks
from progam_functions import *
from leaderboard import *

#Program Variables
dir = os.path.dirname(__file__)

#Program Functions
load_dotenv(os.path.join(dir, ".env"))

if os.path.isdir('./guildfiles') != True:
    os.mkdir(os.path.join('./', 'guildfiles'))

elif os.path.isdir('./leaderboard.json') != True:
    with open(f'./leaderboard.json', 'w') as f:
        f.write("{}")
        
else:
    pass
# Discord Variables
activity = discord.Activity(type=discord.ActivityType.listening, name="+help")
author_id = "892999941146963969"
prefix = '+'

# Logger
logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)

# Bot info
bot = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    activity=activity,
    status=discord.Status.online
)
bot.author_id = author_id 
bot.remove_command("help") #For custom help command

#bot startup
@bot.event
async def on_ready():  # When the bot is ready
    print(f"{bot.user} Started.")


#EVENTS
#creates guild settings
@bot.event
async def on_guild_join(guild):
    joinguild(guild.id)
    return


#removes guild settings
@bot.event
async def on_guild_remove(guild):
    pass


#Message respond event
@bot.listen('on_message')
async def on_message(message):
    #set vars
    checkfiles(message.guild.id)
    currentnum = loadnumber(message.guild.id)
    _id = getchannel(message.guild.id)
    channel = bot.get_channel(_id)
    user = loaduser(message.guild.id)
    msg = message.content
    try:
        msg = msg.split()
        msg = msg[0]
    except:
        pass

    #1. Check to see if it was sent by a human.
    if (message.author.bot):
        return

    #2. Check to see if it was sent in the right channel
    if message.channel.id != _id:
        return

    #3. Check to see if it is a number
    try:
        num = eval_expression(msg)
    except:
        return

    #4. Check if the counting resarted
    #if they miscount at 0
    if currentnum == 0 and num != 1:
        await message.add_reaction('\N{WARNING SIGN}')
        await message.reply("First Number is 1", mention_author=False)
        return
    #if they correctly count at 0
    if currentnum == 0 and num == 1:
    #check if the number reached is bigger then the current highscore
        with open(f'./guildfiles/{message.guild.id}.json', 'r') as f:
            x = json.loads(f.read())
            y = x["highscore"]
            #update highscore and react yes
            if y < currentnum + 1:
                updatehighscore(currentnum + 1, message.guild.id)
                updatenumber(currentnum + 1, message.guild.id)
                updateuser(message.author.id, message.guild.id)
                await message.add_reaction('☑️')
                return
            #react yes
            else:
                updatenumber(currentnum + 1, message.guild.id)
                updateuser(message.author.id, message.guild.id)
                await message.add_reaction('✅')
                return

    #5. Check to see if it was sent by the same user as last time
    if message.author.id == user:
        if currentnum == 0:
            pass
        else:
            await message.add_reaction('❌')
            updateuser(0, message.guild.id)
            await channel.send(f"{message.author.mention} ruined it at {currentnum}! You can't count two numbers in a row! The next number is 1.")
            updatenumber(0, message.guild.id)
            return
    else:
        pass

    #6. Check to see if the number sent is 1 more then the current number
    if num == currentnum + 1:
    #check if the number reached is bigger then the current highscore
        with open(f'./guildfiles/{message.guild.id}.json', 'r') as f:
            x = json.loads(f.read())
            y = x["highscore"]
            #update highscore and react yes
            if y < currentnum + 1:
                updatehighscore(currentnum + 1, message.guild.id)
                updatenumber(currentnum + 1, message.guild.id)
                updateuser(message.author.id, message.guild.id)
                await message.add_reaction('☑️')
                return
            #react yes
            else:
                updatenumber(currentnum + 1, message.guild.id)
                updateuser(message.author.id, message.guild.id)
                await message.add_reaction('✅')
                return
    #not the right number
    else:
        updateuser(0, message.guild.id)
        await message.add_reaction('❌')
        updateuser(0, message.guild.id)
        await channel.send(f"{message.author.mention} ruined it at {currentnum}! WRONG NUMBER! The next number is 1.")
        updatenumber(0, message.guild.id)
        return


#Check if message was deleted
@bot.event
async def on_message_delete(message):
    checkfiles(message.guild.id)
    currentnum = loadnumber(message.guild.id)
    _id = getchannel(message.guild.id)
    channel = bot.get_channel(_id)
    user = loaduser(message.guild.id)
    msg = message.content
    msg = msg.split()
    msg = msg[0]

    if (message.author.bot):
        return

    if message.channel.id != _id:
        return

    try:
        num = eval_expression(msg)
    except:
        return

    channel = bot.get_channel(_id)
    msg = f'**{message.author.mention} deleted their count of {num}.**'
    await channel.send(content=msg, embed=discord.Embed.from_dict(
    {
      "title": "The next number is:",
      "color": 16777215,
      "description": f"```{currentnum + 1}```",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": []
    }
  ))

#COMMANDS
#help command
@bot.command()
async def help(ctx):
    checkfiles(ctx.guild.id)
    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Better Counting Bot Help",
      "color": 0,
      "description": "This is a list of commands and their descriptions.",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
        {
          "name": f"{prefix}help",
          "value": "Used to bring up this menu."
        },
        {
          "name": f"{prefix}channel",
          "value": "Used to set the channel to count in."
        },
        {
          "name": f"{prefix}stats",
          "value": "Used to view your guilds stats."
        }
      ]
    }
  ))

#highscore command
@bot.command()
async def stats(ctx):
    checkfiles(ctx.guild.id)
    currentnum = loadnumber(ctx.guild.id)
    user = loaduser(ctx.guild.id)
    date = loaddate(ctx.guild.id)
    with open(f'./guildfiles/{ctx.guild.id}.json', 'r') as f:
        x = json.loads(f.read())
        highscore = x["highscore"]

    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": f"Guild Stats for `{ctx.guild.name}`",
      "color": 0,
      "description": "",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": [
        {
          "name": "Current Count:",
          "value": f"{currentnum}"
        },        
                {
          "name": "Last Counted By:",
          "value": f"<@{user}>"
        }, 
        {
          "name": "Highest Count:",
          "value": f"{highscore}"
        },
                {
          "name": "Date Achieved:",
          "value": f"{date}"
        },
      ]
    }
  ))

#Set counting channel command
@bot.command()
async def channel(ctx, channel: discord.TextChannel=None):
    checkfiles(ctx.guild.id)
    if channel is None:
        updatechannelid(ctx.channel.id, ctx.guild.id)
        channel = ctx.channel.mention
    else:
        updatechannelid(channel.id, ctx.guild.id)
        channel = channel.mention

    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Updated Counting Channel",
      "color": 0,
      "description": f"Counting now happens in {channel}.",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": []
    }
  ))

@channel.error
async def channel_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": "Error: BadArgument",
      "color": 0,
      "description": "Command format is: +channel #<the channel you want to count in>",
      "timestamp": "",
      "author": {
        "name": "",
        "icon_url": ""
      },
      "image": {},
      "thumbnail": {},
      "footer": {},
      "fields": []
    }
  ))
 

#RUN
if __name__ == "__main__":
    bot.run(os.environ.get("KEY"))