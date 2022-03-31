from dotenv import load_dotenv
import discord, json, os, logging, time, re, string, os.path
from discord.ext import commands, tasks
from progam_functions import *

#Program Variables
dir = os.path.dirname(__file__)

#Program Functions
load_dotenv(os.path.join(dir, ".env"))
if os.path.isdir('./guildfiles') == True:
    pass
else:
    firstrun()

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
    command_prefix="+",
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
#make sure it was sent by human
    if (message.author.bot):
        return
#check if it was sent in counting channel.
    _id = getchannel(message.guild.id)
    if message.channel.id != _id:
        return
#set vars
    channel = bot.get_channel(_id)
    msg = message.content
    msg = msg.split()
    msg = msg[0]
#fetch the current number
    currentnum = loadnumber(message.guild.id)
#try to eval the number
    try:
        num = eval_expression(msg)
    except:
        return
#check if it counting restarted
    if currentnum == 0 and num > 1 or num <= 0:
        await message.add_reaction('\N{WARNING SIGN}')
        await message.reply("First Number is 1", mention_author=False)
        return

#check if it is the right number
    if num == currentnum + 1:
        await message.add_reaction('✅')
    #update highscore if the number reached is bigger then the current highscore
        with open(f'./guildfiles/{message.guild.id}.json', 'r') as f:
            x = json.loads(f.read())
            y = x["highscore"]
            if y < currentnum + 1:
                updatehighscore(currentnum + 1, message.guild.id)
                updatenumber(currentnum + 1, message.guild.id)
            else:
                updatenumber(currentnum + 1, message.guild.id)
    #not the right number
    else:
    #update the number

        await message.add_reaction('❌')
        await channel.send(f"{message.author.mention} ruied it at {currentnum}.\n\nThe next number is 1.")

    #update highscore if the number reached is bigger then the current highscore
        with open(f'./guildfiles/{message.guild.id}.json', 'r') as f:
            x = json.loads(f.read())
            y = x["highscore"]
            if y < currentnum:
                updatehighscore(currentnum, message.guild.id)
                updatenumber(0, message.guild.id)
            else:
                updatenumber(0, message.guild.id)


#COMMANDS
#help command
@bot.command()
async def help(ctx):
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
    currentnum = loadnumber(ctx.guild.id)
    date = loaddate(ctx.guild.id)
    with open(f'./guildfiles/{ctx.guild.id}.json', 'r') as f:
        x = json.loads(f.read())
        highscore = x["highscore"]

    await ctx.send(content=None, embed=discord.Embed.from_dict(
    {
      "title": f"Guild Stats",
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
          "name": "Highest Count:",
          "value": f"{highscore}"
        },
                {
          "name": "Date Achieved:",
          "value": f"{date}"
        },
                {
          "name": "Current Count:",
          "value": f"{currentnum}"
        },        

      ]
    }
  ))

#Set counting channel command
@bot.command()
async def channel(ctx, channel: discord.TextChannel=None):
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