# Twitch Shuffle

Source for [twitchshuffle.com](twitchshuffle.com)

## How to run
* Install Docker and Docker-Compose.  
* Create a vars.env file in the root directory and populate it with your Twitch ClientID and other variables as shown in vars_example.env.
* Run `docker-compose build` and `docker-compose up`.  It will take a few minutes for the database to be populated initially.
* Run `docker-compose down` to destroy and start from scratch.  