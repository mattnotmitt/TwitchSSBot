from genFunc import *


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
        if response == "Eligible for Roll.":
            steamList = steamBefore(check_userID(user))
            if steamList == True:
                print("Steam account used before.")
            elif steamList == False:
                print(response)
        else:
            print(response)


callFunc()
