# bot

A repository holding all the code responsible for the Robert bot, API and dash.

# database setup

Before setting up the bot, you need to set up a database so Robert knows how to
store and get data.

1. Copy `.env.example` to `.env`
2. Add your database URL to the appropriate field
4. Run the following commands:
```sh
$ python -m pip install prisma # Install Prisma
$ prisma generate
$ prisma db push # Push the DB schema to your database
```

This will make sure that the bot is able to access the database through Prisma.

# how to run (docker)

1. Create a working directory for the bot to hold the `.env` and `config.json` files.
2. Copy `config.json.example` to `config.json`
   and change [appropriate values][values].
3. Copy `.env.example` to `.env` and change the values.
4. Run this docker command (REPLACE THE SOURCE IN THE MOUNT WITH THE PATH TO THE CONFIG JSON FILE!):
```sh
$ docker run -it -d --env-file ./.env --mount type=bind,source=<your relative config path>,target=/usr/src/app/config.json --name robert ghcr.io/greek/robert:master
```

## how to run (bot)

Python 3.9+ is needed to run the bot, as well as some other dependencies on
Linux based systems.

Steps:

1. (Windows only) Install [Python][python] (any version above 3.9 should do)
2. (Unix only) Run `sudo apt install gcc python3-dev`
3. Install requirements: `python -m pip install -r requirements.txt`
4. In the `discord` directory, copy `config.json.example` to `config.json`
   and change [appropriate values][values].
5. In the `discord` directory, copy `.env.example` to `.env` and change the values.
6. If you have Docker installed, run `cd docker && docker-compose up -d`
7. Run `python bot.py`

## config settings

Please make sure you have all these fields in, the bot might break if you don't!

1. `owners` - an array for user IDs, used to represent the owners of the bot.
2. `playing` - playing status shown when bot is online
3. `playing_type [listening|watching]` - represents what playing state the bot
   is in.
4. `status [online|dnd|idle]` - represents the status of the user.
5. `accent_color` - an accent color, primarily used in embeds.
6. `error_reporting` - channel ID to report any runtime errors in your code
7. `guild_log` - channel ID to log any new guilds the bot joins/leaves

[python]: https://www.python.org/
[values]: #config-settings
