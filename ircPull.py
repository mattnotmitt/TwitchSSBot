#!/usr/bin/env python3

import re, time, socket, gspread, asyncio, argparse, json, time
from urllib.request import urlopen
from urllib.error import URLError
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from genFunc import *
# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"# Hostname of the IRC-Server in this case twitch's
PORT = 6667 # Default IRC-Port
CHAN = fetchKey("twitchChannel")
NICK = fetchKey("twitchUser")
PASS = fetchKey("twitchOAuth")
# --------------------------------------------- End Settings -------------------------------------------------------

con = socket.socket()
con.connect((HOST, PORT))
send_pass(PASS,con)
send_nick(NICK,con)
join_channel(CHAN,con)

data = ""

while True:
    try:
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()
        #print(data)
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)
            if line[0] == 'PING':
                send_pong(line[1],con)
            elif len(line) == 6 or len(line)== 11:
                if line[1] == 'PRIVMSG':
                    message = get_message(line)
                    if line[0] == ':twitchnotify!twitchnotify@twitchnotify.tmi.twitch.tv':
                        if is_number((line[3])[1:]) == False:
                            rawTwitchUser=line[3]
                            twitchUser=rawTwitchUser[1:]
                            with open('subs.txt', 'a') as subs:
                                subs.write(twitchUser+"\n")
    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")