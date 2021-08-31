"""
Copyright (c) 2020 AlexFlipnote

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

import traceback
import json
import ast
from collections import namedtuple

import discord
import i18n

i18n.set('skip_locale_root_data', True)
i18n.translations.container.clear()
i18n.set('file_format', 'yaml')
i18n.set('filename_format', '{locale}.{format}')
i18n.load_path.append('./lang/')

def get(file):
    """ Helper function to open files. """
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")

def responsible(prosecutor, reason):
    """ Surround text with preset text. """
    usr = f"[{prosecutor}]"
    if reason is None:
        return f"{usr} no reason provided."
    return f"{usr} {reason}"

def translate(key, **kwargs):
    return i18n.t(key, **kwargs)

def branded_embed(title: str = None, description: str = None, fields: list = None, color=None,
                 image: str = None, thumbnail: str = None, footer_text: str = None, footer_icon: str = None,
                 author_text: str = None, author_image: str = None, author_url: str = None, title_url: str = None):

    f = open("config.json")
    config = json.load(f)
    accent_color = config.get("accent_color")
    if color is not None:
        if color == "green":
            color = 0x57f287
        elif color == "red":
            color = 0xed4245
    else:
        color = int(accent_color, 16) or discord.Embed.Empty

    if title is None:
        embed = discord.Embed(description=description, color=color)
    else:
        if description is None:
            if title_url is None:
                embed = discord.Embed(title=title, color=color)
            else:
                embed = discord.Embed(title=title, color=color, url=title_url)
        else:
            if title_url is None:
                embed = discord.Embed(title=title, description=description, color=color)
            else:
                embed = discord.Embed(title=title, description=description, color=color, url=title_url)
    if fields is not None:
        for x in range(len(fields)):
            if True in fields[x]:
                inline = True
            else:
                inline = False
            embed.add_field(name=fields[x][0], value=fields[x][1], inline=inline)

    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    if image is not None:
        embed.set_image(url=image)

    if footer_text is not None:
        if footer_icon is not None:
            embed.set_footer(text=footer_text, icon_url=footer_icon)
        else:
            embed.set_footer(text=footer_text)

    if author_text is not None:
        if author_image is not None:
            if author_url is not None:
                embed.set_author(name=author_text, url=author_url, icon_url=author_image)
            else:
                embed.set_author(name=author_text, icon_url=author_image)
        else:
            if author_url is not None:
                embed.set_author(name=author_text, url=author_url)
            else:
                embed.set_author(name=author_text)
    return embed

def traceback_maker(err, advance: bool = True):
    """ Properly render a traceback error. Useful for sending errors. """
    _traceback = ''.join(traceback.format_tb(err.__traceback__))
    error = ('```py\n{1}{0}: {2}\n```').format(type(err).__name__, _traceback, err)
    return error if advance else f"{type(err).__name__}: {err}"

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)
