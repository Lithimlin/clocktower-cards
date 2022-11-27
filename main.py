from src.crawler import getRoles, getRolePage
from src.character import getCharacter

import requests
import urllib.parse, urllib.request, urllib.error
import os

EDITION_DICT = {
    "Trouble Brewing": "img/trouble_brewing",
    "Bad Moon Rising": "img/bad_moon_rising",
    "Sects & Violets": "img/sects_and_violets",
    "Experimental": "img/experimental",
    "All Editions": "img/all_editions",
}

# \card{Librarian}
#     {img/character_icons/Librarian_icon}
#     {\color{goodcolor}Townsfolk - Good}
#     {You start knowing that 1 of 2 players is a particular Outsider. (Or that zero are in play.)}
#     {ID: 1234}
#     {Trouble Brewing}
#     {img/trouble_brewing}

def downloadImage(character):
    urlPath = urllib.parse.urlparse(character.iconPath).path
    urlPath = urllib.parse.unquote(urlPath).replace(' ', '_')
    imgName = urlPath.split('/')[-1]
    fsPath = os.path.join('img', 'character_icons', imgName)

    urllib.request.urlretrieve(character.iconPath, os.path.join('tex', fsPath))
    return fsPath


roles = getRoles()
for i, role in enumerate(roles):
    role['id'] = i

content = ""

for role in roles:
    page = getRolePage(role['name'])
    char = getCharacter(role, page)

    iconPath = downloadImage(char)
    char.iconPath = iconPath

    midbanner = ""
    if char.alignment == "good":
        midbanner = f"\\color{{goodcolor}}{char.type.title()} - {char.alignment.title()}"
    elif char.alignment == "evil":
        midbanner = f"\\color{{evilcolor}}{char.type.title()} - {char.alignment.title()}"
    elif char.alignment == "good/evil":
        midbanner = f"\\color{{goodcolor}}{char.type.title()} \\color{{evilcolor}}- {char.alignment.title()}"
    elif char.alignment == "storyteller":
        midbanner = f"\\color{{storytellercolor}}{char.type.title()} - {char.alignment.title()}"

    content += f"\\card{{{char.title}}}\n\t{{{char.iconPath}}}\n\t{{{midbanner}}}\n\t{{{char.ability}}}\
        \n\t{{ID: {char.id}}}\n\t{{{char.edition.title().replace('/', ' or ')}}}\n\t{{{EDITION_DICT[char.edition]}}}\n"
    
    print(char.title)


with open(os.path.join('tex', "cardsGen.tex"), 'w') as file:
    file.write(content.replace("%", "\\%").replace("&", "\\&"))

with open(os.path.join('tex', "cardBacksGen.tex"), 'w') as file:
    backs = "\\backside\n" * len(roles)
    file.write(backs)