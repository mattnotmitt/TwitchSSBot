import re, time, socket, gspread, asyncio, argparse, json, os, random
from urllib.request import urlopen
from urllib.error import URLError
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date, timedelta


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
    roll = random.uniform(0, 100)
    with open('data/rolls.txt', 'a') as rolls:
        rolls.write(str(roll) + "\n")
    if 0 <= roll < 10:
        return ('0')
    elif 10 <= roll < 20:
        return ('1')
    elif 20 <= roll < 40:
        return ('2')
    elif 40 <= roll < 70:
        return ('3')
    elif 70 <= roll < 90:
        return ('5')
    elif 90 <= roll < 99:
        return ('10')
    elif 99 <= roll < 99.5:
        return ('50')
    elif 99.5 <= roll < 100:
        return ('100')

# Fetches a user's steam ID
def check_userID(user):
    url = 'https://api.twitch.tv/api/channels/' + user
    try:
        info = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
        return info['steam_id']
    except URLError as e:
        return 'User Not Found in Twitch Database'

# Checks if a twitch account is 30 days old
def acctAge(user):
    url = 'https://api.twitch.tv/kraken/users/' + user
    info = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
    created = datetime.strptime(info['created_at'][0:10], "%Y-%m-%d")
    present = datetime.today() - timedelta(days=30)
    return present > created

# Gets current time and date
def timeGet():
    timeRtNow = time.strftime('%X %Z %d/%m/%y')
    return timeRtNow

# Gets current date
def dateNow():
    '''
    returns current date as a string
    '''
    timeRtNow = time.strftime('%-d/%-m/%Y')
    return timeRtNow

# Checks if a user owns CSGO and has 100 hrs in it
def checkCSGO(steamID):
    if steamID == 'User Not Found in Twitch Database' or steamID == None:
        return "Twitch and Steam not linked."
    try:
        info = json.loads(urlopen(
            "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001?key="
            + fetchKey("steamAPIKey") + "&steamid=" + steamID,
            timeout=60).read().decode('utf-8'))
        csgoDict = (info['response'])['games']
        ownGame = (next(
            (item for item in csgoDict
             if item["appid"] == 730), "Doesn't Own"))
        if ownGame != "Doesn't Own":
            hoursPlayed = float((ownGame['playtime_forever']) / 60)
            if hoursPlayed >= 100:
                return ("Eligible for Roll.")
            else:
                return ("Does not have 100 hours in CSGO.")
        else:
            return ("Doesn't own CSGO.")
    except KeyError:
        return ("Private Profile/Family Shared CSGO.")
    except socket.timeout:
        return ("Steam Connection Timed Out.")

# Checks if a string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Fetches a key from the login.json file
def fetchKey(key):
    with open('data/login.json') as key_file:
        keys = json.loads(key_file.read())
    response = str(keys[key])
    return response

# Checks stream status
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

# Sends the command to the bot and the twitch chat
def cmdSend(coins, twitchUser, fail, reason, streamer):
    con = socket.socket()
    con.connect(("irc.twitch.tv", 6667))
    send_pass(fetchKey("twitchOAuth"), con)
    send_nick(fetchKey("twitchUser"), con)
    join_channel("# "+fetchKey("twitchUser"), con)
    join_channel(streamer, con)
    if fail == 'False':
        send_message("#onscoinbot",
                     ('!' + streamer + 'coins ' + coins + " " + twitchUser),
                     con)
        if check_user(streamer[1:]) == 1:
            if coins != "0":
                send_message(streamer, ("/me " + twitchUser + " won " + coins +
                                        "k CSGODouble Coins."), con)
            else:
                send_message(streamer, "/me " + twitchUser + " won " + coins +
                             " CSGODouble Coins. FeelsBadMan", con)
    elif fail == 'True':
        send_message("# "+fetchKey("twitchUser"),
                     '!' + streamer + 'fail ' + twitchUser + ' ' + reason, con)
        if check_user(streamer[1:]) == 1:
            print('stream offline')
            send_message("# "+fetchKey("twitchUser"), (
                "/me " + twitchUser +
                " does not qualify for CSGODouble coins. Reason: " + reason),
                         con)
    con.close()

# Authorises the sheet
def sheetAuth(sheet, sheetKey):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'data/auth.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open_by_key(sheetKey)
    worksheet = wks.worksheet(sheet)
    return worksheet

# Check coins won in the past
def coinCheck(user, num="all"):
    i = 0
    wonList = []
    worksheet = sheetAuth("All subs", fetchKey("sheetKey"))
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