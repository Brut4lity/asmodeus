import io
import json
import os

import pandas as pd
from bs4 import BeautifulSoup

# Datasource from Mordor The Hendersons website
path = 'datasource'
directory = os.listdir(path)
item_data_tmp = []
monster_data_tmp = []
for f in directory:
    with open(path + os.sep + f, 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')
        dfs = pd.read_html(str(soup))
        name = soup.h2.string
        image = soup.img['src']
        if f.startswith('item'):
            guildparse = [ guildlvl.split(" ")[1:] for guildlvl in dfs[7][0][0].split("Level")[1:]]
            lvlrarity = [additionalinfos.string for additionalinfos in soup.select("table~p")[:-1] if additionalinfos.string not in [None, ' ', '', '\xa0']][0].split('level ')[1]
            firstlvlseen = lvlrarity[:2].strip()
            droppers = [monster.string[1:] if monster.string else monster.text.strip() for monster in soup.select("br~a")]
            if droppers:
                rarity = 'Only dropped by ' + (' ').join(droppers) if 'ONLY' in lvlrarity else lvlrarity.split('"')[1]
            else:
                rarity = 'Found in General Store' 
            effects = [value.strip() for indice,value in enumerate([effect for effect in soup.findAll("td", {"valign" : "top", "width" : "33%"})][0].contents) if indice > 1 and indice % 2 == 0 and value not in [None, ' ', '', '\xa0', '\n'] ]

            data = {
                name: {
                    "image": image,
                    "type": dfs[2][0][0][6:],
                    "alignments": dfs[2][1][0][12:],
                    "cursed": dfs[2][2][0][8:],
                    "ad": dfs[3][0][1],
                    "dmgmod": dfs[3][1][1],
                    "handsrequired": dfs[3][2][1],
                    "swings": dfs[3][3][1],
                    "req": [dfs[4][1][1],dfs[4][2][1],dfs[4][3][1],dfs[4][4][1],dfs[4][5][1],dfs[4][6][1]],
                    "mod": [dfs[4][1][2],dfs[4][2][2],dfs[4][3][2],dfs[4][4][2],dfs[4][5][2],dfs[4][6][2]],
                    "guilds": [guildname[1] + ' ' + guildname[0] for guildname in guildparse],
                    "droppers": droppers,
                    "rarity": rarity,
                    "firstlvlseen": firstlvlseen,
                    "effects": effects,
                    "classrestrict": 'N' if 'not' in dfs[7][0][0].split("Level")[0] else 'Y'
                }
            }
            item_data_tmp.append(data)
        elif f.startswith('monster'):
            abilities = soup.find(lambda tag:tag.name=="p" and "Abilities" in tag.text).find_next_siblings('p')
            special = []
            i = 0
            while abilities[i].string not in [None, ' ', '', '\xa0']:
               special.append(abilities[i].string)
               i = i+1
            dfsi = 5
            if 'travel' in dfs[5][0][0]:
                dfsi = 6
            data = {
                name: {
                    "image": image,
                    "size": dfs[2][1][0][6:],
                    "type": dfs[2][0][0][6:],
                    "alignment": dfs[2][2][0][11:],
                    "stats": ['Hits : ' + dfs[3][0][1], 'A / D : ' + dfs[3][1][1], 'STR : ' + dfs[3][2][1], 'CON : ' + dfs[3][3][1], 'DEX : ' + dfs[3][4][1]],
                    "resistances": ['Fire : ' + dfs[dfsi+1][0][1], 'Cold : ' + dfs[dfsi+1][1][1], 'Electric : ' + dfs[dfsi+1][2][1], 'Mind : ' + dfs[dfsi+1][3][1], 'Disease : ' + dfs[dfsi+1][4][1], 'Poison : ' + dfs[dfsi+1][5][1],
                     'Magic : ' + dfs[dfsi+2][0][1], 'Stone : ' + dfs[dfsi+2][1][1], 'Paralysis : ' + dfs[dfsi+2][2][1], 'Drain : ' + dfs[dfsi+2][3][1], 'Acid : ' + dfs[dfsi+2][4][1]],
                    "rarity": 'Laired monster' if 'Lair' in dfs[dfsi][0][0] else dfs[dfsi][0][0].split('"')[1].strip(),
                    "firstlvlseen": dfs[1][1][0].split("level ")[1],
                    "special": special,
                    "drops": [drop for drop in dfs[dfsi+3][0] if drop not in 'None'],
                    "group": dfs[4][0][0]
                }
            }
            monster_data_tmp.append(data)

# Typo fixing in datasource
def replace_func(target_string):
    target_string = target_string.replace('Wizzards', 'Wizards')
    target_string = target_string.replace('Villians', 'Villains')
    target_string = target_string.replace('Invisiblity', 'Invisibility')
    target_string = target_string.replace('Can See Invisibles', 'Can See Invisible')
    target_string = target_string.replace('Invisibile', 'Invisible')
    target_string = target_string.replace('Can Electricute', 'Can Electrocute')
    return target_string

item_data_tmp = json.loads(replace_func(json.dumps(item_data_tmp)))
monster_data_tmp = json.loads(replace_func(json.dumps(monster_data_tmp)))

with open('json'+ os.sep + 'items.json','w') as json_data:
    json.dump(item_data_tmp, json_data)

with open('json/monsters.json','w') as json_data:
    json.dump(monster_data_tmp, json_data)
