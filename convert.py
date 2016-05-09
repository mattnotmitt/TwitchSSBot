import gspread, asyncio, json
from urllib.request import urlopen
from urllib.error import URLError
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *
banned=['N/A','0']
sheet=input("Which sheet?")
i=int(input("From what line?"))
double=input("Double commands?")
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('auth.json', scope)
gc = gspread.authorize(credentials)
print("Connecting!")
wks = gc.open_by_key(fetchKey("sheetKey"))
worksheet = wks.worksheet(sheet)
print("Connected")
print(worksheet.row_count)
while True:
    twitchCell=str('A' + str(i))
    steamCell=str('C'+ str(i))
    coinCell=str('B'+str(i))
    completeCell=str('D' + str(i))
    commandCell=str('G' + str(i))
    user=worksheet.acell(twitchCell).value
    steam64=check_userID(user)
    print(user)
    if worksheet.acell(twitchCell).value != '':
        if worksheet.acell(coinCell).value not in banned:
            """
            if worksheet.acell(steamCell).value == '' or worksheet.acell(steamCell).value == 'None':
                if steam64=='Null':
                    print("Account not linked")
                    worksheet.update_acell(steamCell, "Account not linked")
                elif steam64=='User Not Found in Twitch Database':
                    print("User not in Twitch database")
                    worksheet.update_acell(steamCell, "User not in Twitch database")
                else:
                    print(steam64)
                    worksheet.update_acell(steamCell, steam64)
            steam64=worksheet.acell(steamCell).value
            """
            if double.lower()=="true":
              if worksheet.acell(steamCell).value != 'None':
                worksheet.update_acell(commandCell, str('/send '+str(steam64)+' '+str(worksheet.acell(coinCell).value)))
        else:
            worksheet.update_acell(steamCell, "N/A")
            worksheet.update_acell(completeCell, "N/A")
    else:
        break
    i=i+1
print("Convert complete.")
