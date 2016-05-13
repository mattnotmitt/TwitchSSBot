import gspread, asyncio, json
from urllib.request import urlopen
from urllib.error import URLError
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *
banned = ['N/A', '0']
sheet = input("Which sheet?")
i = int(input("From what line?"))
double = input("Double commands?")
worksheet = sheetAuth(sheet)
print(worksheet.row_count)
while True:
    twitchCell = str('A' + str(i))
    steamCell = str('C' + str(i))
    coinCell = str('B' + str(i))
    completeCell = str('D' + str(i))
    commandCell = str('G' + str(i))
    user = worksheet.acell(twitchCell).value
    steam64 = worksheet.acell(steamCell).value
    print(user)
    if worksheet.acell(twitchCell).value != '':
        if worksheet.acell(coinCell).value in banned:
            worksheet.update_acell(steamCell, "N/A")
            worksheet.update_acell(completeCell, "N/A")
        else:
            if double.lower() == "true":
                if worksheet.acell(steamCell).value != 'None':
                    worksheet.update_acell(commandCell, str('/send ' + str(
                        steam64) + ' ' + str(worksheet.acell(coinCell).value)))
    else:
        break
    i = i + 1
print("Convert complete.")
