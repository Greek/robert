# bot

A Discord bot made in Python. It uses a slightly modified version of Discord.py, which 

## how to run

Python 3.x is needed to run the bot, as well as some other dependencies on
Linux based systems.

Steps:

1. (Windows only) Install [Python][python] (any version above 2.x should do)
2. (Unix only) Run `sudo apt install gcc python3-dev`
3. Install requirements: `python -m pip install -r requirements.txt`
4. Copy `config.json.example` to `config.json` and change [appropriate values][values].
5. Copy `.env.example` to `.env` and change the values.
6. Run `python bot.py`

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

## credits

I cheated and ~~plagiarized~~ borrowed code from Alex's "discord_bot.py" discord
bot, mainly utilities and helper functions. the whole structure of the bot is
inspired from Alex's bot.

[python]: https://www.python.org/

[values]: #config-settings


