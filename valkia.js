var irc = require("tmi.js");
var fs = require("fs");
var logins = JSON.parse(fs.readFileSync('data/login.json', 'utf8'));
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
    channels: ['#valkia']
};
var entryList = [];
var subGiveaway = false;
var keyWord = "";
var index = 0
var winner = ""
var client = new irc.client(options);
// Connect the client to the server..
client.connect();
client.on("chat", function(channel, user, message, self) {
  mesArray = message.split(" ");
	//console.log(user['display-name']);
	//console.log(subGiveaway);
	if (user['user-type'] == "mod" || user['user-id'] == user['room-id'] || user['display-name'] == 'artemisbot') {
  		if (mesArray[0] == "!startSubGame") {
				entryList = [];
				subGiveaway = true;
				keyWord = mesArray[1];
				client.action(options.channels[0], "Sub game entry open with keyword '"+keyWord+"'!");
			}
			else if (mesArray[0] == "!rollSubGame") {
				winner = entryList[Math.floor(Math.random() * entryList.length)];
				client.action(options.channels[0], "The winner of the sub game entry is "+winner+"!");
				index = entryList.indexOf(winner);
				entryList.splice(index, 1);
			}
			else if (subGiveaway === true) {
				if (mesArray[0] == "!closeSubGame") {
					subGiveaway = false;
					client.action(options.channels[0], "Sub game entry closed!");
				}
				else if (mesArray[0] == "!subGameEntries") {
					client.action(options.channels[0], entryList.length + " subs want to play a sub game - they are: " + entryList.join(","));
				}
			}
  }
	if (subGiveaway === true) {
		//console.log(user['user-type']);
		if (user.subscriber === true || user['user-type'] == "mod") {
			if (mesArray[0] ==  keyWord) {
				entryList.push(user['display-name']);
			}
		}
	}
});