import requests
from mtgsdk import Card


class CardModelFactory(object):
    def __init__(self, mtgsdk_card):
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



class Card(models.Model):
    artist = models.
    border = models.
    cmc = models.
    color_identity = models.
    colors = models.
    flavor = models.
    foreign_names = models.
    hand = models.
    id = models.
    image_url = models.    f'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid={multiverse_id}&type=card'
    layout = models.
    legalities = models.
    life = models.
    loyalty = models.
    mana_cost = models.
    multiverse_id = models.
    name = models.
    names = models.
    number = models.
    original_text = models.
    original_type = models.
    power = models.
    printings = models.
    rarity = models.
    release_date = models.
    rulings = models.
    set = models.
    set_name = models.
    source = models.
    starter = models.
    subtypes = models.
    supertypes = models.
    text = models.
    timeshifted = models.
    toughness = models.
    type = models.
    types = models.
    variations = models.
    watermark = models.Model


class CardPrice(models.Model):
    card = models.ForeignKey(Card, related_name='prices')
    price_cfb = models.DecimalField(max_digits=12, decimal_places=4)
    price_csi = models.DecimalField(max_digits=12, decimal_places=4)
    price_scg = models.DecimalField(max_digits=12, decimal_places=4)
    price_tcg = models.DecimalField(max_digits=12, decimal_places=4)
    datetime = models.DateTimeField(auto_now_add=True)


class Deck(models.Model):
    name = models.CharField(max_length=255)


class Collection(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )


classattrs = ['artist', 'border', 'cmc', 'color_identity', 'colors', 'flavor', 'foreign_names', 'hand', 'id', 'image_url', 'layout', 'legalities', 'life', 'loyalty', 'mana_cost', 'multiverse_id', 'name', 'names', 'number', 'original_text', 'original_type', 'power', 'printings', 'rarity', 'release_date', 'rulings', 'set', 'set_name', 'source', 'starter', 'subtypes', 'supertypes', 'text', 'timeshifted', 'toughness', 'type', 'types', 'variations', 'watermark']

# attr = [ 'artist', 'border', 'cmc', 'colorIdentity', 'colors', 'contains', 'flavor', 'foreignNames', 'gameFormat', 'hand', 'id', 'imageUrl', 'language', 'layout', 'legalities', 'legality', 'life', 'loyalty', 'manaCost', 'multiverseid', 'name', 'names', 'number', 'orderBy', 'originalText', 'originalType', 'page', 'pageSize', 'power', 'printings', 'random', 'rarity', 'releaseDate', 'reserved', 'rulings', 'set', 'setName', 'source', 'starter', 'subtypes', 'supertypes', 'text', 'timeshifted', 'toughness', 'type', 'types', 'variations', 'watermark', ]
#
#
