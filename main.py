import json
import os
import string

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

def search_data(info_token, data_type):
    with open('json' + os.sep + data_type + '.json','r') as json_data:
        json_data_tmp = json.loads(json_data.read())
        for data_dict in json_data_tmp:
            key, val = next(iter(data_dict.items()))
            if key.casefold() == info_token.casefold():
                return val
        return None

@bot.command()
async def item(ctx, *args):
    info_token = string.capwords(' '.join(args))
    data = search_data(info_token, 'items')
    if data:
        embed = discord.Embed(title=info_token, color=discord.Color.red(), description=data['type'])
        embed.set_thumbnail(url=os.environ.get('ASSETS_URL') + data['image'][2:])
        embed.add_field(name="Aligments", value=data['alignments'], inline=True)
        embed.add_field(name="Cursed", value=data['cursed'], inline=True)
        embed.add_field(name="A / D", value=data['ad'], inline=True)
        if(data['type'] in ['Hands', 'Dagger', 'Cross', 'Sword', 'Staff', 'Mace', 'Axe', 'Hammer']):
            embed.add_field(name="Damage modifier", value=data['dmgmod'], inline=True)
            embed.add_field(name="Hands", value=data['handsrequired'], inline=True)
            embed.add_field(name="Swings", value=data['swings'], inline=True)
        embed.add_field(name="Stats", value='STR\nINT\nWIS\nCON\nCHA\nDEX', inline=True)
        embed.add_field(name="Required", value=('\n').join(data['req']), inline=True)
        embed.add_field(name="Modified", value=('\n').join(data['mod']), inline=True)
        embed.add_field(name="Guilds", value=('\n').join(data['guilds']), inline=False)
        embed.add_field(name="First seen on level", value=data['firstlvlseen'], inline=True)
        embed.add_field(name="Rarity", value=data['rarity'], inline=True)
        embed.add_field(name="Class restricted", value=data['classrestrict'], inline=True)
        if data['effects'] : embed.add_field(name="Special effects", value=('\n').join(data['effects']), inline=False)
        if data['droppers'] : embed.set_footer(text='\nDropped by : ' + (', ').join(data['droppers']))
        await ctx.send(embed=embed)
    else:
        await ctx.send('No data found')

@bot.command()
async def monster(ctx, *args):
    info_token = string.capwords(' '.join(args))
    data = search_data(info_token, 'monsters')
    if data:
        embed = discord.Embed(title=info_token, color=discord.Color.red(), description=data['size'] + ' ' + data['alignment'] + ' ' + data['type'])
        embed.set_thumbnail(url=os.environ.get('ASSETS_URL') + data['image'][2:])
        embed.add_field(name="Stats", value=('\n').join(data['stats']), inline=True)
        embed.add_field(name="Resistances", value=('\n').join(data['resistances']), inline=True)
        if not data['special'] : data['special'] = ['None']
        embed.add_field(name="Abilities", value=('\n').join(data['special']), inline=True)
        embed.add_field(name="Encounter chance", value=data['rarity'], inline=True)
        embed.add_field(name="Level", value=data['firstlvlseen'], inline=True)
        if not data['drops'] : data['drops'] = ['None']
        embed.add_field(name="Drops", value=('\n').join(data['drops']), inline=True)
        embed.set_footer(text=data['group'])
        await ctx.send(embed=embed)
    else:
        await ctx.send('No data found')
bot.run(os.environ.get('BOT_TOKEN'))
