import gspread, asyncio, json, sys
from urllib.request import urlopen
from urllib.error import URLError
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *
from Naked.toolshed.shell import muterun_js
banned = ['N/A', '0']
steamFail = ['Not linked twitch and steam.', 'None']
sheet = input("Which sheet?")
i = int(input("From what line?"))
double = input("Double commands?")
worksheet = sheetAuth(sheet, fetchKey("sheetKey"))


def userSubbed(ttvUser):
    response = muterun_js('checksub.js', ttvUser.lower())
    if response.exitcode == 0:
        return (str(response.stdout[:-1])[2:-1])
    else:
        sys.stderr.write(response.stderr)


while True:
    twitchCell = str('A' + str(i))
    steamCell = str('C' + str(i))
    coinCell = str('B' + str(i))
    completeCell = str('D' + str(i))
    reasonCell = str("E" + str(i))
    commandCell = str('G' + str(i))
    subbedCell = str('H' + str(i))
    user = worksheet.acell(twitchCell).value
    steam64 = worksheet.acell(steamCell).value
    subbed = userSubbed(user)
    worksheet.update_acell(subbedCell, subbed)
    print(subbed)
    if subbed != "Yes":
        worksheet.update_acell(completeCell, "N/A")
        worksheet.update_acell(coinCell, "N/A")
        worksheet.update_acell(reasonCell, "Unsubbed.")
    print(user)
    if worksheet.acell(twitchCell).value != '':
        if worksheet.acell(coinCell).value in banned:
            worksheet.update_acell(steamCell, "N/A")
            worksheet.update_acell(completeCell, "N/A")
        else:
            if double.lower() == "true":
                if worksheet.acell(steamCell).value not in steamFail:
                    worksheet.update_acell(commandCell, str('/send ' + str(
                        steam64) + ' ' + str(worksheet.acell(coinCell).value)))
    else:
        break
    i = i + 1
print("Convert complete.")
