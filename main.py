import json
import os
import string

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def item(ctx, *args):
    info_token = string.capwords(' '.join(args))
    data = search_data(info_token, 'items')
    if data:
        await ctx.send(embed=getitem(data))
    else:
        await ctx.send('Item not found')


@bot.command()
async def itemdrop(ctx, *args):
    info_token = string.capwords(' '.join(args))
    data = search_data(info_token, 'itemdrops')
    if data:
        await ctx.send(embed=getitemdrops(data))
    else:
        await ctx.send('Item not found')


@bot.command()
async def monster(ctx, *args):
    info_token = string.capwords(' '.join(args))
    data = search_data(info_token, 'monsters')
    if data:
        await ctx.send(embed=getmonster(data))
    else:
        await ctx.send('Monster not found')


@bot.command()
async def monsterloot(ctx, *args):
    info_token = string.capwords(' '.join(args))
    data = search_data(info_token, 'monsterloot')
    if data:
        await ctx.send(embed=getmonsterloot(data))
    else:
        await ctx.send('Monster not found')


def search_data(info_token, data_type):
    with open('json' + os.sep + data_type + '.json', 'r') as json_data:
        read_json = json_data.read()
        json_data_tmp = json.loads(read_json)
        for record in json_data_tmp:
            if record.get('name', '').casefold() == info_token.casefold():
                return record
        return None


def getitem(data):
    embed = discord.Embed(title=data['name'], color=discord.Color.red(), description=data['type'])
    embed.set_thumbnail(url=os.environ.get('ASSETS_URL') + data['image'][2:])
    embed.add_field(name='Alignments', value=data['alignments'], inline=True)
    embed.add_field(name='Cursed', value=data['cursed'], inline=True)
    embed.add_field(name='A / D', value=data['atk'] + ' / ' + data['def'], inline=True)
    if data['type'] in ['Hands', 'Dagger', 'Cross', 'Sword', 'Staff', 'Mace', 'Axe', 'Hammer']:
        embed.add_field(name='Damage modifier', value=data['dmgmod'], inline=True)
        embed.add_field(name='Hands', value=data['handsrequired'], inline=True)
        embed.add_field(name='Swings', value=data['swings'], inline=True)
    embed.add_field(name='\u2000', value='\u2000', inline=False) # fake line break
    embed.add_field(name="Stats", value='STR\nINT\nWIS\nCON\nCHA\nDEX', inline=True)
    embed.add_field(name="Required", value='\n'.join(data['req']), inline=True)
    embed.add_field(name="Modified", value='\n'.join(data['mod']), inline=True)
    embed.add_field(name='Guilds', value='\n'.join(data['guilds']), inline=False)
    embed.add_field(name='Floor', value=data['firstseen'], inline=True)
    embed.add_field(name='Rarity', value=data['rarity'], inline=True)
    embed.add_field(name='Class restricted', value=data['classrestricted'], inline=True)
    if data['special']: embed.add_field(name='Special effects', value='\n'.join(data['special']), inline=False)
    if data['dropsfrom']: embed.add_field(name='Dropped by',value='```' + '\n'.join(data['dropsfrom']) + '```', inline=False)
    return embed


def getmonster(data):
    embed = discord.Embed(title=data['name'], color=discord.Color.red(),
                          description=data['size'] + ' ' + data['alignment'] + ' ' + data['type'])
    embed.set_thumbnail(url=os.environ.get('ASSETS_URL') + data['image'][2:])
    embed.add_field(name='Stats', value='\n'.join(data['stats']), inline=True)
    embed.add_field(name='Resistances', value='\n'.join(data['resistances']), inline=True)
    embed.add_field(name='\u2000', value='\u2000', inline=False) # fake line break
    if not data['special']: data['special'] = ['None']
    embed.add_field(name='Abilities', value='\n'.join(data['special']), inline=True)
    if data['spells']:
        embed.add_field(name='Can Cast Spells', value='\n'.join(data['spells']), inline=True)
    if data['drops']:
        embed.add_field(name='Drops', value='```' + '\n'.join(data['drops']) + '```', inline=False)
    else:
        embed.add_field(name='Drops', value='None', inline=False)
    embed.set_footer(text=data['group'])
    return embed


def getmonsterloot(data):
    embed = discord.Embed(title=data['name'], color=discord.Color.red(), description='')
    embed.set_thumbnail(url=os.environ.get('ASSETS_URL') + data['image'][2:])
    if not data['drops']: data['drops'] = ['None']
    for idx, chunk in enumerate(chunk_array(data['drops'], 25)):
        title = 'Drops'
        if idx > 0: title = '\u2000'
        embed.add_field(name=title, value='```' + '\n'.join(chunk) + '```', inline=False)
    return embed


def getitemdrops(data):
    embed = discord.Embed(title=data['name'], color=discord.Color.red(),description='')
    embed.set_thumbnail(url=os.environ.get('ASSETS_URL') + data['image'][2:])
    if data['dropsfrom']:
        for idx, chunk in enumerate(chunk_array(data['dropsfrom'], 30)):
            title = 'Drops from'
            if idx > 0: title = '\u2000'
            embed.add_field(name=title, value='```' + '\n'.join(chunk) + '```', inline=False)
    else:
        embed.add_field(name='Source', value=data['rarity'], inline=False)
    return embed


def chunk_array(array, chunk_size):
    """Splits an array into chunks"""
    for i in range(0, len(array), chunk_size):
        yield array[i:i + chunk_size]


bot.run(os.environ.get('BOT_TOKEN'))
