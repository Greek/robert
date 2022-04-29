"""
Copyright (c) 2021-present flower and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import nextcord
import datetime
import os
import pymongo

from nextcord.ext import commands

from utils import default
from utils.default import translate as _

class Events(commands.Cog):
    """General listeners"""

    def __init__(self, bot):
        self.bot = bot
        self.last_timeStamp = datetime.datetime.utcfromtimestamp(0)
        self.config = default.get("config.json")
        self.db = pymongo.MongoClient(os.environ.get("MONGO_DB"))


    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"[Bot] Logged on as {self.bot.user} on {len(self.bot.guilds)} guild(s)\n"
        )

        if self.config.status == "idle":
            status = nextcord.Status.idle
        elif self.config.status == "dnd":
            status = nextcord.Status.dnd
        else:
            status = nextcord.Status.online

        if self.config.playing_type == "listening":
            playing_type = 2
        elif self.config.playing_type == "watching":
            playing_type = 3
        else:
            playing_type = 0

        await self.bot.change_presence(
            activity=nextcord.Activity(type=playing_type, name=self.config.playing),
            status=status,
        )

def setup(bot):
    bot.add_cog(Events(bot))
