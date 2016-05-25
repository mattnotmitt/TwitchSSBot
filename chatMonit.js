var irc = require("tmi.js");
var fs = require("fs");
var PythonShell = require('python-shell');
var logins = JSON.parse(fs.readFileSync('data/login.json', 'utf8'));
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
today = dd + '-' + mm + '-' + yyyy;
// Options for connection
var options = {
    options: {
        debug: true
    },
    connection: {
        cluster: "aws",
        reconnect: true
    },
    identity: {
        username: logins.altTwitchUser,
        password: logins.altTwitchOAuth
    },
    channels: logins.twitchChannel
};

var client = new irc.client(options);
// Connect the client to the server..
client.connect();

//===================================== SUB NOTIFICATIONS ======================================

client.on("subanniversary", function(channel, username, months) {
    console.log(username);
    fs.appendFile('data/subs.txt', username.toLowerCase() + "\n", function(err) {});
    fs.appendFile('sub-logs/' + today + '.txt', username + " " + months + "\n", function(err) {});
});
client.on("subscription", function(channel, username) {
    console.log(username);
    fs.appendFile('data/subs.txt', username.toLowerCase() + "\n", function(err) {});
    fs.appendFile('sub-logs/' + today + ".txt", username + "\n", function(err) {});
});

//===================================== CHAT COMMANDS ==========================================

client.on("chat", function(channel, user, message, self) {
    console.log(user);
    var username = user.username;
    if (user['user-type'] == "mod" || user.subscriber === true || user['user-id'] == user['room-id']) {
        mesArray = message.split(" ");
        console.log(mesArray.length);
        console.log(mesArray);
        if (mesArray.length > 1) {
            username = mesArray[1];
        }
        if (mesArray[0] == "!append") {
            if (user['user-type'] == "mod" || user['user-id'] == user['room-id']) {
                fs.appendFile('data/subs.txt', username + "\n", function(err) {});
            } else {
              outputSend(channel, user, "Subs can't add themselves to the list. onsFacepalm");
            }
        } else if (mesArray[0] == "!checksteam") {
            if (mesArray.length == 1) {
                username = user.username;
            }
            pythonCon(username, 'getSteam', function(pythData) {
                console.log(pythData);
                if (mesArray.length > 1) {
                    if (user['user-type'] == 'mod' || user['user-id'] == user['room-id']) {
                      outputSend(channel, user, user['display-name'] + ", " + username + "'s Steam ID 64 is " + pythData + ".");
                    }
                    else {
                      outputSend(channel, user, "You can't call other people's IDs!");
                    }
                } else {
                  outputSend(channel, user, user['display-name'] + ", your Steam ID 64 is " + pythData + ".");                    
                }
            });
        } else if (mesArray[0] == "!coinwins") {
            if (mesArray.length == 1) {
                username = user.username;
            }
            pythonCon(username, 'coinWins', function(pythData) {
                console.log(pythData);
                if (mesArray.length > 1) {
                    if (user['user-type'] == "mod" || user['user-id'] == user['room-id']) {
                        if (pythData == "None") {
                            outputSend(channel, user, user['display-name'] + ", " + username + " has been rolled for no CSGODouble coins.");
                        } else {
                            outputSend(channel, user, user['display-name'] + ", " + username + " has won " + pythData + " CSGODouble coins.");
                        }
                    } else {
                      outputSend(channel, user, "You can't call other people's coins!");
                    }
                } else {
                    if (pythData == "None") {
                        outputSend(channel, user, user['display-name'] + ", you have been rolled for no CSGODouble coins.");
                    } else {
                        outputSend(channel, user, user['display-name'] + ", you have won " + pythData + " CSGODouble coins.");
                    }
                }
            });
        } else if (mesArray[0] == "!rulecheck") {
            if (mesArray.length == 1) {
                username = user.username;
            }
            pythonCon(username, 'rulecheck', function(pythData) {
                console.log(pythData);
                if (mesArray.length > 1) {
                    if (user['user-type'] == "mod" || user['user-id'] == user['room-id']) {
                        if (pythData == "Eligible for Roll.") {
                            outputSend(channel, user, user['display-name'] + ", " + username + " is valid for CSGODouble coins.");
                        } else {
                            outputSend(channel, user, user['display-name'] + ", " + username + " is not valid for CSGODouble coins. Reason: " + pythData);
                        }
                    } else {
                      outputSend(channel, user, "You can't call other people's coins!");
                    }
                } else {
                    if (pythData == "Eligible for Roll.") {
                        outputSend(channel, user, user['display-name'] + ", you are valid for CSGODouble coins.");
                    } else {
                        outputSend(channel, user, user['display-name'] + ", you are not valid for CSGODouble coins. Reason: " + pythData);
                    }
                }
            });
        } else if (mesArray[0]=="!artemishelp") {
            outputSend(channel, user, user['display-name'] + ", find commands for artemisbot at http://pastebin.com/Pgfz5Ht0");
        } else if (mesArray[0]=="!bot") {
            client.action(options.channels[0], "I'm always up onsW - Elmo can't break me.");
        }
    }
});

//=============================== REQUIRED FUNCTIONS =========================================
// Sends outputs to commands
function outputSend(channel, user, msg) {
    if (user['user-type'] == 'mod' || user['user-id'] == user['room-id']) {
        client.action(channel, msg);
    } else if (user.subscriber === true) {
        client.whisper(user['display-name'], msg);
    }
}

// For calling functions from Python
function pythonCon(user, func, cb) {
    var pyshell = new PythonShell('nodeFunc.py');
    pyshell.send(func);
    pyshell.send(user);
    pyshell.on('message', function(message) {
        var pythData = message;
        console.log(pythData);
        cb(pythData);
    });
}
