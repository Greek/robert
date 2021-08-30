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
5. Run `python bot.py`

## config settings
Please make sure you have all these fields in, the bot might break if you don't!

1. `prefix` - the prefix used for running commands
2. `token` - login token
3. `owners` - an array for user IDs, used to represent the owners of the bot.
4. `playing` - playing status shown when bot is online
5. `playing_type [listening|watching]` - represents what playing state the bot
   is in.
6. `status [online|dnd|idle]` - represents the status of the user.
7. `accent_color` - an accent color, primarily used in embeds.

## credits

I cheated and ~~plagiarized~~ borrowed code from Alex's "discord_bot.py" discord
bot, mainly utilities and helper functions. the whole structure of the bot is
inspired from Alex's bot.

[python]: https://www.python.org/

[values]: #config-settings


