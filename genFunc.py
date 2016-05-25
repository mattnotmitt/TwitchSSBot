import re, time, socket, gspread, asyncio, argparse, json, os, random
from urllib.request import urlopen
from urllib.error import URLError
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg, con):
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
        if char == "!":
            break
        if char != ":":
            result = result + char
    url = 'https://api.twitch.tv/api/channels/' + result
    info = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
    return info["display_name"]


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
    coinChoices = ["100", "2", "0", "4", "5", "0", "1", "1", "0", "4", "2",
                   "0", "2", "5", "0", "1", "4", "50", "0", "1", "5", "0", "3",
                   "5", "0", "5", "5", "0", "25", "3", "0", "5", "10", "0",
                   "5", "3", "0", "3", "3", "10", "0", "5", "4", "0", "5", "2",
                   "4", "0", "2", "1"]
    coins = coinChoices[random.randint(0, 49)]
    return (coins)


def check_userID(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    url = 'https://api.twitch.tv/api/channels/' + user
    try:
        info = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
        return info['steam_id']
    except URLError as e:
        return 'User Not Found in Twitch Database'


def timeGet():
    os.environ['TZ'] = 'GB'
    time.tzset()
    timeRtNow = time.strftime('%X %Z %d/%m/%y')
    return timeRtNow


def dateNow():
    '''
    returns current date as a string
    '''
    now = date.today()
    full = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    return full


def checkCSGO(steamID):
    if steamID == 'User Not Found in Twitch Database' or steamID == None:
        return "Twitch and Steam not linked."
    try:
        info = json.loads(urlopen(
            "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001?key="+fetchKey("steamAPIKey")+"&steamid="
            + steamID,
            timeout=60).read().decode('utf-8'))
        csgoDict = (info['response'])['games']
        ownGame = (next(
            (item for item in csgoDict
             if item["appid"] == 730), "Doesn't Own"))
        if ownGame != "Doesn't Own":
            hoursPlayed = float((ownGame['playtime_forever']) / 60)
            if hoursPlayed >= 10:
                return ("Eligible for Roll.")
            else:
                return ("Does not have 10 hours in CSGO.")
        else:
            return ("Doesn't own CSGO.")
    except KeyError:
        return ("Private Profile/Family Shared CSGO.")
    except socket.timeout:
        return ("Steam Connection Timed Out.")


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def fetchKey(key):
    with open('data/login.json') as key_file:
        keys = json.loads(key_file.read())
    response = str(keys[key])
    return response


def check_user(user):
    """ returns 0: online, 1: offline, 2: not found, 3: error """
    url = 'https://api.twitch.tv/kraken/streams/' + user
    try:
        info = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
        if info['stream'] == None:
            status = 1
        else:
            status = 0
    except URLError as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            status = 2
        else:
            status = 3
    return status


def cmdSend(coins, twitchUser, fail, reason):
    con = socket.socket()
    con.connect(("irc.twitch.tv", 6667))
    send_pass(fetchKey("altTwitchOAuth"), con)
    send_nick(fetchKey("altTwitchUser"), con)
    join_channel("#onscoinbot", con)
    join_channel("#onscreenlol", con)
    if fail == False:
        send_message("#onscoinbot", ('!coins ' + coins + " " + twitchUser),
                     con)
        if check_user('onscreenlol') == 1:
            if coins != "0":
                send_message("#onscreenlol",
                             ("/me " + twitchUser + " won " + coins +
                              "k CSGODouble Coins."), con)
            else:
                send_message("#onscreenlol", "/me " + twitchUser + " won " +
                             coins + " CSGODouble Coins. FeelsBadMan", con)
    elif fail == True:
        send_message("#onscoinbot", '!fail ' + twitchUser + ' ' + reason, con)
        if check_user('onscreenlol') == 1:
            send_message("#onscreenlol",
                         ("/me" + twitchUser +
                          " does not qualify for CSGODouble coins. Reason: " +
                          reason), con)
    con.close()


def sheetAuth(sheet):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('auth.json',
                                                                   scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_key(fetchKey("sheetKey"))
    worksheet = wks.worksheet(sheet)
    return worksheet


def coinCheck(user, num="all"):
    i = 0
    wonList = []
    worksheet = sheetAuth("All subs")
    coinsWon = worksheet.findall(user)
    timesRolled = len(coinsWon) - 1
    if timesRolled < 0:
        coinsWon = worksheet.findall(user.lower())
        timesRolled = len(coinsWon) - 1
    if num == "all":
        while i <= timesRolled:
            won = worksheet.cell(coinsWon[i].row, 2).value
            if won != "N/A" and (
                    worksheet.acell('D' + str(coinsWon[i].row)).value) != "No":
                wonList.append(won)
            i += 1
    else:
        while i <= num:
            won = worksheet.cell((coinsWon[i].row), 2).value
            if won != "N/A" and worksheet.acell('D' + str(coinsWon[
                    i].row)).value != "No":
                wonList.append(won)
            i += 1
    if len(wonList) == 0:
        return "False"
    else:
        return wonList


def steamBefore(steam):
    steamFile = open("data/pastSteamIDs.txt", "r")
    pastSteamIDs = steamFile.readlines()
    steamFile.close()
    if steam + "\n" not in pastSteamIDs:
        return False
    else:
        return True
