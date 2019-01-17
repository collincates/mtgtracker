import copy
import json
import requests


"""
class CardModelFactory(object):
    def __init__(self, data):
        if type(data) is str:
            data = json.loads(data)
        self.from_dict(data)
    def from_dict(self, data):
        for key, value in data.items():
            if value == 'true':
                value = 'True'
            if type(value) is dict:
                value = self.from_dict(value)
            self.__dict__[key] = value

    def create_model(self, model):


for card, attrs in data.items():
    # put these objects in a list of CardModelFactory(attrs)
"""
"""
{
    "\"Ach! Hans, Run!\"": {
        "colorIdentity": [
            "G",
            "R"
        ],
        "colors": [
            "G",
            "R"
        ],
        "convertedManaCost": 6.0,
        "foreignData": [],
        "layout": "normal",
        "legalities": {},
        "manaCost": "{2}{R}{R}{G}{G}",
        "name": "\"Ach! Hans, Run!\"",
        "printings": [
            "UNH"
        ],
        "rulings": [],
        "scryfallId": "84f2c8f5-8e11-4639-b7de-00e4a2cbabee",
        "subtypes": [],
        "supertypes": [],
        "tcgplayerProductId": 37816,
        "tcgplayerPurchaseUrl": "https://mtgjson.com/links/85b366724beadefd",
        "text": "At the beginning of your upkeep, you may say \"Ach Hans, run It's the . . .\" and the name of a creature card. If you do, search your library for a card with that name, put it onto the battlefield, then shuffle your library. That creature gains haste. Exile it at the beginning of the next end step.",
        "type": "Enchantment",
        "types": [
            "Enchantment"
        ],
        "uuid": "d4492969-dc3a-5617-bc14-4f15afc12b2b"
    },
    "\"Rumors of My Death . . .\"": {
        "colorIdentity": [
            "B"
        ],
        "colors": [
            "B"
        ],
        "convertedManaCost": 3.0,
        "foreignData": [],
        "layout": "normal",
        "legalities": {},
        "manaCost": "{2}{B}",
        "name": "\"Rumors of My Death . . .\"",
        "printings": [
            "UST"
        ],
        "rulings": [],
        "scryfallId": "cb3587b9-e727-4f37-b4d6-1baa7316262f",
        "subtypes": [],
        "supertypes": [],
        "text": "{3}{B}, Exile a permanent you control with a League of Dastardly Doom watermark: Return a permanent card with a League of Dastardly Doom watermark from your graveyard to the battlefield.",
        "type": "Enchantment",
        "types": [
            "Enchantment"
        ],
        "uuid": "e063f191-1995-5495-962c-3154775cf674"
    },
    "1996 World Champion": {
        "colorIdentity": [
            "B",
            "G",
            "R",
            "U",
            "W"
        ],
        "colors": [
            "B",
            "G",
            "R",
            "U",
            "W"
        ],
        "convertedManaCost": 5.0,
        "foreignData": [],
        "layout": "normal",
        "legalities": {},
        "manaCost": "{W}{U}{B}{R}{G}",
        "name": "1996 World Champion",
        "printings": [
            "PCEL"
        ],
        "rulings": [],
        "scryfallId": "d3f10f07-7cfe-4a6f-8de6-373e367a731b",
        "starter": true,
        "subtypes": [
            "Legend"
        ],
        "supertypes": [],
        "text": "Cannot be the targets of spells or effects. World Champion has power and toughness equal to the life total of target opponent.\n{0}: Discard your hand to search your library for 1996 World Champion and reveal it to all players. Shuffle your library and put 1996 World Champion on top of it. Use this ability only at the beginning of your upkeep, and only if 1996 World Champion is in your library.",
        "type": "Summon — Legend",
        "types": [
            "Summon"
        ],
        "uuid": "40a3a446-daa8-5cc9-8d52-8b0bfd6fd673"
    },
    "A Display of My Dark Power": {
        "colorIdentity": [],
        "colors": [],
        "convertedManaCost": 0.0,
        "foreignData": [],
        "layout": "scheme",
        "legalities": {},
        "name": "A Display of My Dark Power",
        "printings": [
            "OARC"
        ],
        "rulings": [
            {
                "date": "2010-06-15",
                "text": "The ability affects all players, not just you."
            },
            {
                "date": "2010-06-15",
                "text": "The effect doesn’t wear off until just before your next untap step (even if an effect will cause that untap step to be skipped)."
            },
            {
                "date": "2010-06-15",
                "text": "The types of mana are white, blue, black, red, green, and colorless."
            },
            {
                "date": "2010-06-15",
                "text": "If a land produces more than one type of mana at a single time (as Boros Garrison does, for example), the land’s controller chooses which one of those types of mana is produced by the delayed triggered ability."
            },
            {
                "date": "2010-06-15",
                "text": "If a land is tapped for mana but doesn’t produce any (for example, if you tap Gaea’s Cradle for mana while you control no creatures), the delayed triggered ability won’t trigger."
            }
        ],
        "scryfallId": "c5287e77-890d-41bd-acc6-7a8f1866426d",
        "starter": true,
        "subtypes": [],
        "supertypes": [],
        "text": "When you set this scheme in motion, until your next turn, whenever a player taps a land for mana, that player adds one mana of any type that land produced.",
        "type": "Scheme",
        "types": [
            "Scheme"
        ],
        "uuid": "750e7658-efd4-5173-9385-058345893faa"
    },
}
"""

# Create dictionary object for all card data
def get_data():
    all_cards_data = requests.get('https://mtgjson.com/json/AllCards.json').json()
    # Create dictionary object for all set data
    all_sets_data = requests.get('https://mtgjson.com/json/AllSets.json').json()

def deserialize_data(data):
    for obj in serialize.deserialize('json', data):
        print(obj)


def get_card_data_in_set(set_code, foreign=True):
    """
    Return a dictionary of each card in a set, given a set_code (str).

    set_code (str): A three character set code representing a set name.
    foreign (bool): Can be set to False to remove foreign language data
        from the output. Defaults to True.
    """
    dict_copy = copy.deepcopy(all_cards_data)
    set_data = {name: attrs for name, attrs in dict_copy.items() if set_code in attrs['printings']}
    if foreign == False:
        for card in set_data:
            del set_data[card]['foreignData']
    return set_data




if __name__=="__main__":
    get_data()
    deserialize_data(all_cards_data)
