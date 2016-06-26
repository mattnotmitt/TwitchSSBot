import socket, gspread, time, random, xml
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
while True:
    try:
        if newRun == True:
            loops = 0
            newRun = False
        with open('data/line.txt', 'r') as lineNum:
            i = int(lineNum.read(10))
        gc = gspread.authorize(credentials)
        #print("Connecting!")
        wks = gc.open_by_key(fetchKey("sheetKey"))
        worksheet = wks.worksheet(dateNow())
        #worksheet = wks.worksheet('Auto Subs')
        lastSub = ''
        while loops < 100:
            with open("data/subs.txt", "r") as f:
                readLines = f.readlines()
            with open("data/subs.txt", "w") as f:
                f.write("")
            lines.extend(readLines)
            while len(lines) > 0:
                print(lines)
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
                if steamUser == None:
                    worksheet.update_acell(steamUserCell,
                                           "Not linked twitch and steam.")
                else:
                    worksheet.update_acell(steamUserCell, steamUser)
                coinGen = hottedRoll_coins()
                cmdSend(coinGen, twitchUser, 'False', "n/a", ((fetchKey("twitchChannel"))[0]))
                if coinGen == "0":
                    worksheet.update_acell(coinCell, coinGen)
                    worksheet.update_acell(sentCell, "N/A")
                else:
                    worksheet.update_acell(coinCell, coinGen + "000")
                time.sleep(20)
                lines.pop(0)
                i = i + 1
                with open('data/line.txt', 'w') as lineNum:
                    lineNum.write(str(i))
            loops = loops + 1
            time.sleep(1)
            if loops == 100:
                newRun = True
    except gspread.exceptions.HTTPError:
        print("Google Sheets broke. Try again.")
    except gspread.exceptions.WorksheetNotFound:
        print("Cannot find today's sheet.")
    except xml.etree.ElementTree.ParseError:
        print("Google Sheets broke. Try again.")
