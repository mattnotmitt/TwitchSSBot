var irc = require("tmi.js");
var fs = require("fs")

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth() + 1; //January is 0!
var yyyy = today.getFullYear();
today = dd + '-' + mm + '-' + yyyy;
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
        username: logins.twitchUser,
        password: logins.twitchOAuth
    },
    channels: [logins.twitchChannel]
};

var client = new irc.client(options);
// Connect the client to the server..
client.connect();
client.on("subanniversary", function(channel, username, months) {
    console.log(username);
    fs.appendFile('sub-logs/' + today + '.txt', username + "\n", function(err) {});
});
client.on("subscription", function(channel, username) {
    console.log(username);
    fs.appendFile('sub-logs/' + today + ".txt", username + "\n", function(err) {});
});