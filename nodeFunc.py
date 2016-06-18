from genFunc import *
import datetime
mydate = datetime.datetime.now()
def callFunc():
    func = input()
    user = input()
    if func == "getSteam":
        print(check_userID(user))
    elif func == "coinWins":
        wonCoins = coinCheck(user)
        if wonCoins == "False":
            print("None")
        else:
            print((', '.join(map(str, wonCoins))))
    elif func == "rulecheck":
        response = checkCSGO(check_userID(user))
        print(response)


callFunc()
