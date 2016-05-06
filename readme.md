# CSGODouble Coins for Subs Code
This is a project I created for [ONSCREENlol][craig] on twitch.tv.

You must get your own keys for Google Docs, and place them in a file named 'auth.json' located in the repo's root directory. Instructions for this can be found [here][docs] in the gspread docs.

Written for Python 3.4

## Requirements

``` sh
$ pip install gspread
$ pip install oauth2
$ pip install oauth2client
```
### Files which must be added

```
subs.txt
pastSteamIDs.txt
auth.json
line.txt
login.json
```
More info on login.json can be found [here][wiki].

The first line of line.txt should state the numerical value of the row of the sheet you want to start on.

[craig]: <twitch.tv/onscreenlol>
[docs]:<http://gspread.readthedocs.io/en/latest/oauth2.html>
[wiki]:<https://github.com/artemisbot/TwitchDoubleBot/wiki/login.json>