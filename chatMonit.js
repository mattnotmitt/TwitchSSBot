var irc = require("tmi.js");
var fs = require("fs");
var RegEx = require("regex");
var PythonShell = require('python-shell');
var logins = JSON.parse(fs.readFileSync('data/login.json', 'utf8'));
var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
today = dd + '-' + mm + '-' + yyyy;
console.log(logins.twitchChannel);
// Options for connection
var options = {
    options: {
        debug: false
    },
    connection: {
        cluster: "aws",
        reconnect: true
    },
    identity: {
        username: logins.twitchUser,
        password: logins.twitchOAuth
    },
    channels: logins.twitchChannel
};

var client = new irc.client(options);
// Connect the client to the server..
client.connect();

//===================================== SUB NOTIFICATIONS ======================================

client.on("subanniversary", function(channel, username, months) {
    console.log(username);
    console.log(channel.substring(1));
    fs.appendFile('data/'+channel.substring(1)+'subs.txt', username.toLowerCase() + "\n", function(err) {});
});
client.on("subscription", function(channel, username) {
    console.log(username);
    console.log(channel.substring(1));
    fs.appendFile('data/'+channel.substring(1)+'subs.txt', username.toLowerCase() + "\n", function(err) {});
});

//===================================== CHAT COMMANDS ==========================================

client.on("chat", function(channel, user, message, self) {
  mesArray = message.split(" ");
    if (channel=="#onscreenlol" || channel=="#artemisbot"){
      var username = user.username;
      if (message == (new RegEx(/((pls)|(plz)|(please)){0,1} (send ){0,1}[0-9]{0,} (coins ){0,1}[0-9]{17}/g))) {
        console.log("Regex tripped.");
        if (user.subscriber === false) {
          client.timeout(channel, user.username, 600);
          client.action(channel, user['display-name'] + " don't beg for coins. 10 minute timeout.");
        } else {
          client.timeout(channel, user.username, 1);
          client.action(channel, user['display-name'] + " don't beg for coins. You've been purged.");
        }
      }
      if (user['user-type'] == "mod" || user.subscriber === true || user['user-id'] == user['room-id'] || channel=="#artemisbot") {
          if (mesArray.length > 1) {
              username = mesArray[1];
          }
          if (mesArray[0] == "!append") {
              if (user['user-type'] == "mod" || user['user-id'] == user['room-id']) {
                  fs.appendFile('data/onscreenlolsubs.txt', username + "\n", function(err) {});
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
    }
  else if (channel=="#hotted89") {
    if (user['user-type'] == 'mod' || user['user-id'] == user['room-id']) {
      if (mesArray[0]=='!refreshID') {
        var update = new PythonShell('hottedConvert.py');
        update.send(mesArray[1]);
        update.send(mesArray[2]);
        update.send(mesArray[3]);
        update.send('true');
        update.on('message', function(message) {
          client.action('#hotted89', message);
        })
      }
      else if (mesArray[0]=='!append') {
        fs.appendFile('data/hotted89subs.txt', mesArray[1] + "\n", function(err) {});
      }
    }
  } 
  /*
  else if (channel=="#joaquimblaze") {
    console.log(user);
    if (user['user-type'] == 'mod' || user['user-id'] == user['room-id']) {
      if (mesArray[0]=='!append') {
        fs.appendFile('data/joaquimblazesubs.txt', mesArray[1] + "\n", function(err) {});
      }
    }
  } */
});

//=============================== REQUIRED FUNCTIONS =========================================
// Sends outputs to commands
function outputSend(channel, user, msg) {
    console.log("Message sending...");
    console.log(user);
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
