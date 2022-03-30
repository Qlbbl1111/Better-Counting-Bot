from dotenv import load_dotenv
import discord, json, os, logging, time, re, string
from discord.ext import commands, tasks
from make_files import firstrun, joinguild

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

'''
#removes guild settings
@bot.event
async def on_guild_remove(guild):
    pass
'''

#Message respond event
@bot.event
async def on_message(message):
    msg = message.content
    if (message.author.bot):
        return
    if isinstance(message.channel, discord.channel.DMChannel):
        return
        

        await message.reply(r, mention_author=False)
    else:


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
          "name": f"{prefix}highscore",
          "value": "Used to view your guilds highest count."
        }
      ]
    }
  ))

#highscore command
@bot.command()
async def highscore(ctx):
    pass
#Set counting channel command
@bot.command()
async def channel(ctx, channel: discord.TextChannel):
    pass


#RUN
if __name__ == "__main__":
    bot.run(os.environ.get("KEY"))