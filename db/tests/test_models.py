# from django.conf import settings
from django.test import TestCase

from accounts.models import User
from db.models import Card, Collection, Deck


class CardModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        card1 = Card.objects.create(name='Card 1', set_name='a test set', id=1, sdk_id='123')
        card2 = Card.objects.create(name='Card 2', set_name='a test set', id=2, sdk_id='456')
        card3 = Card.objects.create(
            name='Card 3',
            set_name='a test set',
            id=3,
            sdk_id='789',
            variations=[card1.sdk_id, card2.sdk_id]
        )

    def test_card_meta_verbose_name(self):
        self.assertEqual(Card._meta.verbose_name, 'card')

    def test_card_meta_verbose_name_plural(self):
        self.assertEqual(Card._meta.verbose_name_plural, 'cards')

    def test_card_meta_ordering_by_id(self):
        results = Card.objects.all()
        self.assertEqual(results[0].name, 'Card 1')
        self.assertEqual(results[1].name, 'Card 2')

    def test_card_string_representation(self):
        card = Card.objects.get(id=1)
        self.assertEqual(card.__str__(), card.name)

    def test_card_override_save_with_slug(self):
        # Card class comes with a blank slug upon instantiation by default.
        card = Card(name='MY test Card', id=234)
        # Assert SlugField contains default blank value.
        self.assertEqual(card.slug, '')
        # .save() is overriden to call slugify(f'{card.id}-{card.name}')
        card.save()
        self.assertEqual(card.slug, '234-my-test-card')

    def test_card_get_absolute_url(self):
        card = Card.objects.get(id=1)
        card_abs_url = card.get_absolute_url()
        self.assertEqual(card_abs_url, '/db/card/1-card-1')

    def test_card_art_variations(self):
        card3 = Card.objects.get(id=3)
        art_var = card3.art_variations()
        self.assertQuerysetEqual(
            art_var,
            map(repr, ['1-card-1', '2-card-2', '3-card-3'])
        )

class CollectionModelTest(TestCase):

    def setUp(self):
        """Create test user, log in test user, create collection for test user."""
        self.user1 = User.objects.create_user(username='testuser1', password='12345678')
        self.user2 = User.objects.create_user(username='testuser2', password='12345678')

        self.login = self.client.login(username='testuser1', password='12345678')
        self.login = self.client.login(username='testuser2', password='12345678')

        test_collection1 = Collection.objects.create(name='testcollection1', owner=self.user1)
        test_collection2 = Collection.objects.create(name='testcollection2', owner=self.user2)

        card1 = Card.objects.create(name='Card 1', set_name='a test set', id=1, sdk_id='123')
        card2 = Card.objects.create(name='Card 2', set_name='a test set', id=2, sdk_id='456')

        deck1 = Deck.objects.create(name='testdeck1')#, cards=[card1, card2,])
        deck2 = Deck.objects.create(name='testdeck2')#, cards=[card1, card2,])

        cards = [card1, card2,]


    def test_collection_meta_verbose_name(self):
        self.assertEqual(Collection._meta.verbose_name, 'collection')

    def test_collection_meta_verbose_name_plural(self):
        self.assertEqual(Collection._meta.verbose_name_plural, 'collections')

    def test_collection_meta_ordering_by_id(self):
        results = Collection.objects.all()
        self.assertEqual(results[0].name, 'testcollection1')
        self.assertEqual(results[1].name, 'testcollection2')

    def test_collection_string_representation(self):
        collection = Collection.objects.get(name='testcollection1')
        self.assertEqual(collection.__str__(), collection.name)

    def test_collection_get_absolute_url(self):
        user = User.objects.get(username='testuser1')
        collection = Collection.objects.get(name='testcollection1')
        collection_abs_url = collection.get_absolute_url()
        self.assertEqual(collection_abs_url, '/db/testuser1/testcollection1/')
