from src.urls import scriptUrl
import urllib.parse

ALIGNMENT_DICT = {
    "townsfolk": "good",
    "outsider": "good",
    "minion": "evil",
    "demon": "evil",
    "fabled": "storyteller",
    "traveller": "good/evil"
}


class Character:
    def __init__(self, title, id, ctype, edition, ability, iconPath):
        self.title = title
        self.id = id
        self.type = ctype
        self.alignment = getCharacterAlignment(self.type)
        self.edition = edition
        self.ability = ability
        self.iconPath = iconPath

    def __str__(self):
        return f"{self.title} ({self.id}):\n\t{self.type} - {self.alignment}\n\t\"{self.ability}\"\n\tEdition: {self.edition}\n\tIcon Path: {self.iconPath}"
    

def getCharacter(json, page):
    return Character(
        getCharacterTitle(page),
        getCharacterID(json),
        getCharacterType(json),
        getCharacterEdition(page),
        getCharacterAbility(page),
        getCharacterIconPath(json)
    )


def getCharacterTitle(page):
    return page['title']

def getCharacterID(json):
    return json['id']

def getCharacterType(json):
    ctype = json['roleType']
    if ctype == "travellers":
        return "traveller"
    return ctype

def getCharacterEdition(page):
    content = getPageContent(page)
    edition = content.split("Appears in")[1]\
                    .split("<br>")[0]\
                    .strip("</h4> \n\t")\
                    .split('|')[-1]\
                    .strip(']')\
                    .split('=')[1]
    if "experimental" in edition.lower():
        edition = "Experimental"
    if "fabled" in edition.lower():
        edition = "All Editions"
    return edition

def getCharacterAbility(page):
    content = getPageContent(page)
    ability = content.split("Character Text")[1]\
                    .split("<br>")[0]\
                    .strip('= \n\t\"')
    return ability

def getCharacterAlignment(type):
    return ALIGNMENT_DICT[type]

def getCharacterIconPath(json):
    parsed = urllib.parse.urlparse(json['icon'].lstrip('./'))
    subpath = urllib.parse.quote(parsed.path)
    url = urllib.parse.urljoin(scriptUrl, subpath, parsed.query)
    return url

def getPageContent(page):
    return page['revisions'][0]['*']