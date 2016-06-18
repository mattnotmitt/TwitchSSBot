import gspread, asyncio, json, sys, xml
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *
banned = ['N/A', '0', '']
steamFail = ['Not linked twitch and steam.', 'None', '']
sheet = input("")
i = int(input(""))
maxLine = int(input(""))
double = input("")
try:
    worksheet = sheetAuth(sheet, fetchKey("sheetKey"))
except gspread.WorksheetNotFound:
    print("ERROR: Sheet Not Found.")
    sys.exit()

try:
    while i <= maxLine:
        twitchCell = str('A' + str(i))
        steamCell = str('C' + str(i))
        coinCell = str('B' + str(i))
        completeCell = str('D' + str(i))
        reasonCell = str("E" + str(i))
        commandCell = str('G' + str(i))
        subbedCell = str('H' + str(i))
        user = worksheet.acell(twitchCell).value
        if worksheet.acell(steamCell).value in steamFail:
            steamID = check_userID(user)
            if steamID != None:
                worksheet.update_acell(steamCell, steamID)
            else:
                worksheet.update_acell(steamCell,
                                       'Not linked twitch and steam.')
        steamID = worksheet.acell(steamCell).value
        if worksheet.acell(coinCell).value in banned:
            worksheet.update_acell(steamCell, "N/A")
            worksheet.update_acell(completeCell, "N/A")
        elif steamID not in steamFail:
            steamID = worksheet.acell(steamCell).value
            if double.lower() == "true":
                if worksheet.acell(steamCell).value not in steamFail:
                    worksheet.update_acell(commandCell, str('/send ' + str(
                        steamID) + ' ' + str(worksheet.acell(coinCell).value)))
        i = i + 1
    print("Refresh of IDs complete.")
except gspread.exceptions.HTTPError:
    print("Google Sheets broke. Try again.")
except xml.etree.ElementTree.ParseError:
    print("Google Sheets broke. Try again.")
