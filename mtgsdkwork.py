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
