import copy
import json
import requests

# Create dictionary object for all card data
all_cards_data = requests.get('https://mtgjson.com/json/AllCards.json').json()
# Create dictionary object for all set data
all_sets_data = requests.get('https://mtgjson.com/json/AllSets.json').json()

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
