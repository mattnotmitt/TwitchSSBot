import socket, gspread, time
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *
# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"# Hostname of the IRC-Server in this case twitch's
PORT = 6667 # Default IRC-Port
CHAN = fetchKey("twitchChannel")
NICK = fetchKey("altTwitchUser")
PASS = fetchKey("altTwitchOAuth")
# --------------------------------------------- End Settings -------------------------------------------------------

'''
con = socket.socket()
con.connect((HOST, PORT))
send_pass(PASS,con)
send_nick(NICK,con)
join_channel(CHAN,con)
'''
print("Credentials being auth")
loops=0
scope = ['https://spreadsheets.google.com/feeds']
newRun=False
credentials = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
steamFile = open("pastSteamIDs.txt","r")
pastSteamIDs = steamFile.readlines()
steamFile.close()
while True:    
    if newRun == True:
        loops=0
        newRun=False
    with open('line.txt', 'r') as lineNum:
        i=int(lineNum.read(10))
    gc = gspread.authorize(credentials)
    print("Connecting!")
    wks = gc.open_by_key(fetchKey("sheetKey"))
    worksheet = wks.worksheet(dateNow())
    lastSub=''
    while loops<100:
        twitchUserCell=str("A"+str(i))
        steamUserCell=str("C"+str(i))
        coinCell=str("B"+str(i))
        timeCell=str("F"+str(i))
        sentCell=str("D"+str(i))
        reasonCell=str("E"+str(i))
        f = open("subs.txt","r")
        lines = f.readlines()
        f.close()
        while len(lines)>0:
            rawTwitchUser = lines[0]
            twitchUser = rawTwitchUser[:-1]
            worksheet.update_acell(twitchUserCell, twitchUser)
            worksheet.update_acell(timeCell,timeGet())
            steamUser=check_userID(twitchUser)
            if steamUser=='User Not Found in Twitch Database':
              break
            elif steamUser!=None:
              rawSteamUser=steamUser+"\n"
              if rawSteamUser not in pastSteamIDs:
                worksheet.update_acell(steamUserCell, steamUser)
                csgoCheck=checkCSGO(steamUser)
                pastSteamIDs.append(rawSteamUser)
                with open("pastSteamIDs.txt", 'a') as pastIDs:
                  pastIDs.write(rawSteamUser)
                if csgoCheck != "Eligible for Roll.":
                  worksheet.update_acell(sentCell, "No")
                  worksheet.update_acell(reasonCell, csgoCheck)
                  worksheet.update_acell(coinCell, "N/A")
                """else:
                  coinGen=roll_coins()
                  send_message(CHAN,('/w onscreenbot !coins'+coinGen+" "+twitchUser),con)
                  worksheet.update_acell(coinCell,coinGen)
                  """
              else:
                worksheet.update_acell(sentCell, "No")
                worksheet.update_acell(reasonCell, "Steam account used before.")
                worksheet.update_acell(coinCell, "N/A")
                worksheet.update_acell(steamUserCell, steamUser)
            else:
              worksheet.update_acell(steamUserCell, 'Steam not linked.')
              worksheet.update_acell(coinCell, 'N/A')
              worksheet.update_acell(sentCell, 'No')
              worksheet.update_acell(reasonCell, 'Steam and Twitch not linked.')
            i=i+1
            with open('line.txt', 'w') as lineNum:
                lineNum.write(str(i))
            f = open("subs.txt","w")
            for updateLine in lines:
              if updateLine!=rawTwitchUser:
                f.write(updateLine)
            f.close()
            lines.pop(0)
        loops=loops+1
        time.sleep(2)
        if loops==100:
            newRun=True
        
