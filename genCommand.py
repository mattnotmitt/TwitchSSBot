from genFunc import *
# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"# Hostname of the IRC-Server in this case twitch's
PORT = 6667 # Default IRC-Port
CHAN = fetchKey("twitchChannel")
NICK = fetchKey("twitchUser")
PASS = fetchKey("twitchOAuth")
# --------------------------------------------- End Settings -------------------------------------------------------
con = socket.socket()
con.connect((HOST, PORT))
send_pass(PASS,con)
send_nick(NICK,con)
join_channel(CHAN,con)
data = ""
mods = ['artemisbot','deelmo','artemisbot','zashgamer','onscreenlol']
while True:
    try:
        
        data = data+con.recv(1024).decode('UTF-8')
        data_split = re.split(r"[~\r\n]+", data)
        data = data_split.pop()
        for line in data_split:
            line = str.rstrip(line)
            line = str.split(line)
            if line[0] == 'PING':
                send_pong(line[1],con)
            if line[1] == 'PRIVMSG':
                message = get_message(line)
                sender = get_sender(line[0])
                print(message)
                print(sender)
                print(line)
                if sender in mods:
                    if line[3]==':!append':
                        twitchUser=line[4]
                        with open('subs.txt', 'a') as subs:
                            subs.write(twitchUser+"\n")
                        send_message(CHAN,"/w artemisbot User added to spreadsheet.",con)
                    elif line[3]==':!querysay':
                        send_message(CHAN,message[10:],con)            

    except socket.error:
        print("Socket died")

    except socket.timeout:
        print("Socket timeout")