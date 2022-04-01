import json, os, logging, time, re, string, os
from datetime import datetime

def checkfiles(guild):
    if os.path.isdir(f'./guildfiles/{guild}.json') == True:
        return
    else:
        joinguild(guild)
        return

def diff_dates(date1, date2):
    return abs(date2-date1).days

def firstrun():
    os.mkdir(os.path.join('./', 'guildfiles'))

def joinguild(guild):
    if os.path.exists(f'./guildfiles/{guild}.json') == True:
        return
    else:
        with open(f'./guildfiles/{guild}.json', 'w') as f:
            f.write(f"{{\"id\": {guild}, \"highscore\": 0, \"channel\": 0, \"currentnum\": 0, \"currentuser\": 0, \"date\": \"\"}}")
            return

def eval_expression(input_string):
    code = compile(input_string, "<string>", "eval")
    if code.co_names:
        raise NameError(f"Use of names not allowed")
    return eval(code, {"__builtins__": {}}, {})

def updatehighscore(score, guild):
    highscoredate(guild)
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        x.update({"highscore": score})
        y = json.dumps(x)
    with open(f'./guildfiles/{guild}.json', 'w') as f:
        f.write(y)

def highscoredate(guild):
    _today = datetime.today()
    _today= datetime.strftime(_today, '%b-%d-%Y')
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        x.update({"date": f"{_today}"})
        y = json.dumps(x)
    with open(f'./guildfiles/{guild}.json', 'w') as f:
        f.write(y)

def updatechannelid(channelid, guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        x.update({"channel": channelid})
        y = json.dumps(x)
    with open(f'./guildfiles/{guild}.json', 'w') as f:
        f.write(y)

def loaddate(guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        y = x["date"]
    if y == "":
        return "None"
    else:
        pass
    _today = datetime.today()
    hsdate = datetime.strptime(y, '%b-%d-%Y')
    date = datetime.strftime(hsdate, '%b-%d-%Y')
    days = diff_dates(_today, hsdate)
    if days == 0:
        z = f"Today"
    else:
        z = f"{days} days ago on {date}"
    return z

def loadnumber(guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        y = x["currentnum"]
        return y

def loaduser(guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        y = x["currentuser"]
        return y

def updatenumber(number, guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        x.update({"currentnum": number})
        y = json.dumps(x)
    with open(f'./guildfiles/{guild}.json', 'w') as f:
        f.write(y)

def updateuser(user, guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        x.update({"currentuser": user})
        y = json.dumps(x)
    with open(f'./guildfiles/{guild}.json', 'w') as f:
        f.write(y)

def getchannel(guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        y = x["channel"]
        return y


def getguild():
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        y = x["id"]
        return y