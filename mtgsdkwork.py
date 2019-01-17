import requests
from mtgsdk import Card

# 44057

grab = 44357    pages 1-444
grab2 = 44357   pages 1-449
grab3 = Card.all()

# function/lcass to get all of the cards within the sdk
class CardGrabber(object):
    def __init__(self):
        self.cards = []
        self.get_cards()
    def get_cards(self):
        for i in range(1, 450):
            self.cards.extend(Card.where(page=i).all())
            print(f'got page {i}')

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
    artist = models.CharField(max_length=100)
    border = models.CharField(max_length=10)
    cmc = models.FloatField()
    color_identity = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    colors = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    flavor = models.TextField(max_length=1000)
    foreign_names = models. """list of dictionaries""" # arraylist postgres? serialize/deserialize json string?
    hand = models. # Nonetype?
    id = models.CharField(max_length=64)
    image_url = models.URLField(max_length=200)
    layout = models.CharField(max_length=15)
    legalities = models. """list of dictionaries""" # arraylist postgres? serialize/deserialize json string?
    life = models. # Nonetype?
    loyalty = models.CharField(max_length=10)
    mana_cost = models.CharField(max_length=100)
    multiverse_id = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    names = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    number = models.CharField(max_length=10)
    original_text = models.TextField(max_length=1000)
    original_type = models.CharField(max_length=255)
    power = models.CharField(max_length=10)
    printings = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    rarity = models.CharField(max_length=50)
    release_date = models.DateField()
    rulings = models. """list of dictionaries""" # arraylist postgres? serialize/deserialize json string?
    set = models.CharField(max_length=10)
    set_name = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    starter = models.BooleanField()
    subtypes = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    supertypes = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    text = models.TextField(max_length=1000)
    timeshifted = models.BooleanField()
    toughness = models.CharField(max_length=10)
    type = models.CharField(max_length=255)
    types = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    variations = models. """list of strings""" # arraylist postgres? serialize/deserialize json string?
    watermark = models.CharField(max_length=50)


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
