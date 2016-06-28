# Coins for Subs Code
This is a project I created for [ONSCREENlol][craig] on twitch.tv.

It automatically uploads subs for a specified channel to a specified Google Sheet. Feel free to use this on your own stream, as long as you credit me.

You must get your own keys for Google Docs, and place them in a file named `auth.json` located in the repo's `/data/` directory. Instructions for this can be found [here][docs] in the gspread docs.
The email address in your `auth.json` file must be permitted to edit your spreadsheet.

Each day, the current sheet will update - line 31 of `spreadsheet.py` shows an example if you want to use a custom sheet name.

Written for Python 3.4 & Node.JS 4

I would recommend running spreadsheet.py and chatMonit.js (for basic functionality) under [pm2][PM2] so if they crash, which may occur, they will automatically restart.
## Requirements

``` sh
$ pip install gspread
$ pip install oauth2
$ pip install oauth2client
$ npm install twitch_irc
```
The two below are for extra functions in `chatMonit.js` and `convert.py`:
``` sh
$ npm install python-shell
$ npm install twitch-api
```
### Files which must be added
Add these in a folder named `/data/` in the repo's root directory
```
subs.txt
auth.json
line.txt
login.json
```

### User files

More info on login.json can be found [here][wiki].

The first line of line.txt should state the numerical value of the row of the sheet you want to start on.

[craig]: <twitch.tv/onscreenlol>
[docs]:<http://gspread.readthedocs.io/en/latest/oauth2.html>
[wiki]:<https://github.com/artemisbot/TwitchDoubleBot/wiki/login.json>
[pm2]:<https://github.com/Unitech/pm2>
