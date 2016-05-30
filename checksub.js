var TwitchAPI = require('twitch-api');
var fs = require('fs');
var logins = JSON.parse(fs.readFileSync('data/login.json', 'utf8'));
var twitch = new TwitchAPI({
	clientId: logins.twitchAPIClient,
	clientSecret: logins.twitchAPISecret,
	redirectUri: logins.redirectUri,
	scopes: ['channel_check_subscription', 'channel_subscriptions']
});
var checkUser = process.argv.slice(2);
isSubbed(checkUser)

function isSubbed(currUser) {
	twitch.getUserSubscriptionToChannel(currUser, "onscreenlol", logins.oAuth_Key, function(err, user) {
		if (err) {
			//console.log(err);
			console.log("No");
		} else {
			//console.log(user);
			if (user.hasOwnProperty('created_at')) {
				console.log("Yes");
			}
		}
	});
}