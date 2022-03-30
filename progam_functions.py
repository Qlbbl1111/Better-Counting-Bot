import json, os, logging, time, re, string, os.path


def firstrun():
    os.mkdir(os.path.join('./', 'guildfiles'))


def joinguild(guild):
    if os.path.exists(f'./guildfiles/{guild}.json') == True:
        return
    else:
        with open(f'./guildfiles/{guild}.json', 'w') as f:
            f.write(f"{{\"id\": {guild}, \"highscore\": 0, \"channel\": 0, \"currentnum\": 0}}")
            print('ran')
            return


def eval_expression(input_string):
    code = compile(input_string, "<string>", "eval")
    if code.co_names:
        raise NameError(f"Use of names not allowed")
    return eval(code, {"__builtins__": {}}, {})


def updatehighscore(score, guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        x.update({"highscore": score})
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


def loadnumber(guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        y = x["currentnum"]
        return y


def updatenumber(number, guild):
    with open(f'./guildfiles/{guild}.json', 'r') as f:
        x = json.loads(f.read())
        x.update({"currentnum": number})
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