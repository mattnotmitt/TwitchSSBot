var irc = require("tmi.js");
var fs = require("fs")
var options = {
    options: {
        debug: true
    },
    connection: {
        cluster: "aws",
        reconnect: true
    },
    identity: {
        username: "xxxxxxxxx",
        password: "oauth:xxxxxxxxxxxx"
    },
    channels: ["#onscreenlol"]
};

var client = new irc.client(options);

// Connect the client to the server..
client.connect();
client.on("subanniversary", function (channel, username, months) {
    console.log(username);
		fs.appendFile('subs.txt', username + "\n", function (err) {
		});
});
client.on("subscription", function (channel, username) {
    console.log(username);
		fs.appendFile('subs.txt', username + "\n", function (err) {
		});
});
