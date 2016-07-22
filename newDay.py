import gspread
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *

clients=[fetchKey("sheetKey")]
worksheetName = dateNow()
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('data/auth.json',
                                                               scope)
for client in clients:
  gc = gspread.authorize(credentials)
  wks = gc.open_by_key(client)
  wks.add_worksheet(worksheetName, 500, 20)
  cs = wks.worksheet(worksheetName)
  cs.update_acell('A1', 'Twitch Username')
  cs.update_acell('B1', 'SteamID64')
  cs.update_acell('C1', 'Resub?')
  cs.update_acell('D1', 'Date+Time')
  cs.update_acell('G3', 'Subs Today:')
  cs.update_acell('H3', '=count(B2:B)')
with open('data/line.txt', 'w') as lineNum:
    lineNum.write('2')
