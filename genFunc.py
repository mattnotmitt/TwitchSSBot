import re, time, socket, gspread, asyncio, argparse, json, os
from urllib.request import urlopen
from urllib.error import URLError
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg,con):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg, con):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick, con):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password, con):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan, con):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan, con):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        print(char)
        if char == "!":
            break
        if char != ":":
            result = result + char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result        

# --------------------------------------------- End Helper Functions -----------------------------------------------
# --------------------------------------------- Main Functions -----------------------------------------------------
def roll_coins():
  coinChoices=["100k","2k","0","4k","5k","0","1k","1k","0","4k","2k","0","2k","5k","0","1k","4k","50k","0","1k","5k","0","3k","5k","0","5k","5k","0","25k","3k","0","5k","10k","0","5k","3k","0","3k","3k","10k","0","5k","4k","0","5k","2k","4k","0","2k","1k"]
  coins=coinChoices[random.randint(0,49)]
  return(coins)

def check_userID(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    url = 'https://api.twitch.tv/api/channels/' + user
    try:
        info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
        return info['steam_id']
    except URLError as e:
        return 'User Not Found in Twitch Database'
        
def timeGet():
    os.environ['TZ'] = 'GB'
    time.tzset()
    timeRtNow = time.strftime('%X %x %Z')
    return timeRtNow
  
def dateNow():
    '''
    returns current date as a string
    '''
    now = date.today()
    full = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    return full

def checkCSGO(steamID):
    info = json.loads(urlopen("http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001?key=E6B9BEF1975FF027CD07A6BBE9C04D7B&steamid="+steamID, timeout=15).read().decode('utf-8'))
    try:
        csgoDict=(info['response'])['games']
        ownGame = (next((item for item in csgoDict if item["appid"] == 730), "Doesn't Own"))
        if ownGame!="Doesn't Own":
            hoursPlayed=float((ownGame['playtime_forever'])/60)
            if hoursPlayed >= 10:
                return("Eligible for Roll.")
            else:
                return("Does not have 10 hours in CSGO.")
        else:
            return("Doesn't own CSGO.")
    except KeyError:
        return("Private Profile/Family Shared CSGO.")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
      
def fetchKey(key):
  with open('login.json') as key_file:    
    keys = json.loads(key_file.read())
  response = str(keys[key])
  print(response)
  return response