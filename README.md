# Twitch Shuffle

The purpose of the website is to allow you to find low viewership streams at random.

## How to run
* Install Docker and Docker-Compose.  
* Create a `vars.env` file in the root directory and populate it with your Twitch ClientID and other variables as shown in `vars_example.env`.
* Run `docker-compose build` and `docker-compose up`.  It will take a few minutes for the stream_retriever to populate the database with initial data.
* Run `docker-compose stop` or `Ctrl-c` to stop. Run `docker-compose down` to destroy and start from scratch as needed, such as to rerun `init.sql`.

## License
MIT
