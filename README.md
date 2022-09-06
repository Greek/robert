# bot

A monorepository holding all the code responsible for the Toilet bot, API and dash.

## monorepo setup

To begin coding in the monorepo, ensure you have your IDE opened in the root
directory of the repository. Do NOT open your IDE in the place you wish to edit.

Follow these installation steps:

1. Begin with installing the **recommended** version of [NodeJS](https://nodejs.org/en/)
2. Install [Yarn v1](https://classic.yarnpkg.com/en/docs/install)

# how to run (docker)

1. Create a working directory for the bot to hold the `.env` and `config.json` files.
2. Copy `config.json.example` to `config.json`
   and change [appropriate values][values].
3. Copy `.env.example` to `.env` and change the values.
4. Run this docker command:
```sh
$ docker run -it -d --env-file ./.env --name toilet ghcr.io/greek/toilet-bot:master
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
6. Run `python discord/bot.py`

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
