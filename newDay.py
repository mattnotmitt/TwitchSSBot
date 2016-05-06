import gspread
from oauth2client.service_account import ServiceAccountCredentials
from genFunc import *

worksheetName=dateNow()
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('home/ec2-user/onscoinbot/Current\ rotation/auth.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_key(fetchKey("sheetKey"))
wks.add_worksheet(worksheetName, 500, 20)
cs=wks.worksheet(worksheetName)
cs.update_acell('A1', 'Twitch Username')
cs.update_acell('B1', 'Coins Won')
cs.update_acell('C1', 'SteamID64')
cs.update_acell('D1', 'Sent')
cs.update_acell('E1', 'Reason')
cs.update_acell('F1', 'Date+Time (UTC)')
cs.update_acell('G1', 'Command For Double')
cs.update_acell('H1', 'Subbed?')
cs.update_acell('L2', 'Total Today:')
cs.update_acell('M2', '=SUM(B:B)')
cs.update_acell('L3', 'Average Today:')
cs.update_acell('M3', '=M2/M4')
cs.update_acell('L4', 'Subs Today:')
cs.update_acell('M4', '=count(B2:B)')
with open('home/ec2-user/onscoinbot/Current\ rotation/line.txt','w') as lineNum:
        lineNum.write('2')
