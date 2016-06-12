import socket, gspread, time, random
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *
import datetime
mydate = datetime.datetime.now()
print("Credentials being auth")
loops = 0
lines = []
scope = ['https://spreadsheets.google.com/feeds']
newRun = False
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'data/auth.json', scope)
pastUsers = {}
with open("data/pastSteamIDs.txt") as f:
    for line in f:
        #print(line)
        lineArr = line.split(' ')
        pastUsers[lineArr[1][0:-1]] = lineArr[0]

while True:
    try:
        if newRun == True:
            loops = 0
            newRun = False
        with open('data/line.txt', 'r') as lineNum:
            i = int(lineNum.read(10))
        gc = gspread.authorize(credentials)
        print("Connecting!")
        wks = gc.open_by_key(fetchKey("sheetKey"))
        worksheet = wks.worksheet(dateNow())
        #worksheet = wks.worksheet('Insert Key Here')
        lastSub = ''
        while loops < 100:
            with open("data/onscreenlolsubs.txt", "r") as f:
                readLines = f.readlines()
            with open("data/onscreenlolsubs.txt", "w") as f:
                f.write("")
            lines.extend(readLines)
            while len(lines) > 0:
                print(lines)
                print(i)
                i = i + 1
                with open('data/line.txt', 'w') as lineNum:
                    lineNum.write(str(i))
                twitchUserCell = str("A" + str(i))
                steamUserCell = str("C" + str(i))
                coinCell = str("B" + str(i))
                timeCell = str("F" + str(i))
                sentCell = str("D" + str(i))
                reasonCell = str("E" + str(i))
                rawTwitchUser = lines[0]
                twitchUser = rawTwitchUser[:-1]
                worksheet.update_acell(twitchUserCell, twitchUser)
                worksheet.update_acell(timeCell, timeGet())
                steamUser = check_userID(twitchUser)
                if steamUser == 'User Not Found in Twitch Database':
                    break
                elif steamUser != None:
                    rawSteamUser = steamUser + "\n"
                    if steamUser not in pastUsers:
                        worksheet.update_acell(steamUserCell, steamUser)
                        csgoCheck = checkCSGO(steamUser)
                        if csgoCheck != "Eligible for Roll.":
                            worksheet.update_acell(sentCell, "No")
                            worksheet.update_acell(reasonCell, csgoCheck)
                            worksheet.update_acell(coinCell, "N/A")
                            coinGen = roll_coins()
                            cmdSend("n/a", twitchUser, 'True', csgoCheck)
                            time.sleep(10)
                        else:
                            coinGen = roll_coins()
                            cmdSend(coinGen, twitchUser, 'False', "n/a")
                            if coinGen == "0":
                                worksheet.update_acell(coinCell, coinGen)
                                worksheet.update_acell(sentCell, "N/A")
                            else:
                                worksheet.update_acell(coinCell,
                                                       coinGen + "000")
                            pastUsers[steamUser] = twitchUser
                            with open("data/pastSteamIDs.txt", 'a') as pastIDs:
                                pastIDs.write(twitchUser + " " + rawSteamUser)
                            time.sleep(20)
                    else:
                        worksheet.update_acell(sentCell, "No")
                        worksheet.update_acell(
                            reasonCell, "Steam account used since 1st " +
                            mydate.strftime("%B") + " by account '" +
                            pastUsers[steamUser] + "'.")
                        worksheet.update_acell(coinCell, "N/A")
                        worksheet.update_acell(steamUserCell, steamUser)
                        cmdSend("n/a", twitchUser, 'True',
                                "Steam account used since 1st " +
                                mydate.strftime("%B") + " by account '" +
                                pastUsers[steamUser] + "'.")
                        time.sleep(10)
                else:
                    worksheet.update_acell(steamUserCell, 'Steam not linked.')
                    worksheet.update_acell(coinCell, 'N/A')
                    worksheet.update_acell(sentCell, 'No')
                    worksheet.update_acell(reasonCell,
                                           'Steam and Twitch not linked.')
                    cmdSend("n/a", twitchUser, 'True',
                            'Steam and Twitch not linked.')
                    time.sleep(10)
                lines.pop(0)
            loops = loops + 1
            time.sleep(1)
            if loops == 100:
                newRun = True
    except gspread.exceptions.HTTPError:
        print("Google Sheets broke. Try again.")
    except xml.etree.ElementTree.ParseError:
        print("Google Sheets broke. Try again.")
