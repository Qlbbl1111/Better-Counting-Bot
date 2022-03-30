import json, os

def firstrun():
    os.mkdir(os.path.join('./', 'guildfiles'))

def joinguild(guild):
    with open(f'{guild}.json', 'w') as f:
        f.write('{"guilds": [{ "id": "", "highscore": 0, "channel": ""}]}')
