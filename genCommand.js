var irc = require("tmi.js");
var fs = require("fs");
var PythonShell = require('python-shell');
var logins = JSON.parse(fs.readFileSync('login.json', 'utf8'));
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
    channels: [logins.twitchChannel]
};

function pythonCon(user, func, cb){
	var pyshell = new PythonShell('nodeFunc.py');
	pyshell.send(func);
	pyshell.send(user);
	pyshell.on('message', function (message) {
  	var pythData = message;
		console.log(pythData);
		cb(pythData);
	});
}

var client = new irc.client(options);
// Connect the client to the server..
client.connect();
client.on("chat", function (channel, user, message, self) {
		if (user['user-type'] == "mod"){
			mesArray=message.split(" ");
			var username=mesArray[1]
			if (mesArray[0]=="!append") {
				fs.appendFile('subs.txt', username + "\n", function (err) {
				});
			}
			else if (mesArray[0]=="!checksteam") {
			 if (mesArray.length == 1){
					username = user['display-name'];
				}
				pythonCon(username, 'getSteam', function(pythData){
					console.log(pythData);
					if (mesArray.length == 1){
					 client.action(options.channels[0], user['display-name']+", your Steam ID 64 is "+pythData+".");
				 }
				 else {
				  client.action(options.channels[0], user['display-name']+", "+username+"'s Steam ID 64 is "+pythData+".");
					}
				});
			}
			else if (mesArray[0]=="!coinwins") {
				if (mesArray.length == 1){
					username = user['display-name'];
				}
				pythonCon(username, 'coinWins', function(pythData){
					console.log(pythData);
					if (mesArray.length > 1){
						client.action(options.channels[0], user['display-name']+", "+username+" has won "+pythData+" CSGODouble coins.");
					}
					else {
						client.action(options.channels[0], user['display-name']+", you have won "+pythData+" CSGODouble coins.");
					}
				});
			}
		}
});
