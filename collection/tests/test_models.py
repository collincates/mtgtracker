from django.db.utils import IntegrityError
from django.test import TestCase

from accounts.models import User
from collection.models import Collection, CollectionCard
from db.models import Card
from deck.models import Deck


class CollectionModelTest(TestCase):

    def setUp(self):
        """Create test user, log in test user, create collection for test user."""
        self.user1 = User.objects.create_user(username='testuser1', password='12345678')
        self.user2 = User.objects.create_user(username='testuser2', password='12345678')

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

    def test_collection_override_save_with_slug(self):
        # Collection class comes with a blank slug upon instantiation.
        new_collection = Collection(
            name='Test\'s collection',
            id=3,
            owner=User.objects.create_user(
                username='testuser3',
                password='987654321'
            )
        )
        # Assert SlugField contains default blank value.
        self.assertEqual(new_collection.slug, '')
        # .save() is overriden to call slugify(f'{new_collection.name}')
        new_collection.save()
        self.assertEqual(new_collection.slug, 'tests-collection')

    def test_collection_get_absolute_url(self):
        user = User.objects.get(username='testuser1')
        collection = Collection.objects.get(name='testcollection1')
        collection_abs_url = collection.get_absolute_url()
        self.assertEqual(collection_abs_url, '/collection/testuser1/testcollection1/')


class CollectionCardModelTest(TestCase):

    def setUp(self):
        """
        Create Collection and Card to be used in creation of CollectionCard
        model instance.

        CollectionCard is a ManyToManyField 'through-model'.
        It requires both a Collection and a Card object in order to create
        a row on the CollectionCard table. The 'count' field defaults to 0 (int).

        A Collection object requires a value in the 'owner' field, so we create
        a test user for this set of tests and assign the collection to test user.
        """
        testuser = User.objects.create_user(username='testuser', password='12345678')

        collection = Collection.objects.create(name='testcollection', owner=testuser)

        card1 = Card.objects.create(name='Card 1', set_name='a test set', id=1, sdk_id='123')

    def test_collectioncard_count_field_default_is_zero(self):
        collection = Collection.objects.get(name='testcollection')
        card1 = Card.objects.get(name='Card 1')
        collectioncard_1 = CollectionCard.objects.create(
            collection=collection,
            card=card1
        )
        self.assertEqual(collectioncard_1.count, 0)

    def test_collectioncard_meta_unique_together(self):
        """
        A CollectionCard can only relate to a given Card model once.
        Multiple copies of a Card will instead be indicated in the 'count' field.
        This test confirms that an IntegrityError is raised when an attempt
        is made to form a second relationship with an already related card model.
        """

        collection = Collection.objects.get(name='testcollection')
        card1 = Card.objects.get(name='Card 1')
        collectioncard_1 = CollectionCard.objects.create(
            collection=collection,
            card=card1
        )
        # Attempt to relate the same card model a second time
        with self.assertRaises(IntegrityError):
            collectioncard_1_duplicate = CollectionCard.objects.create(
                collection=collection,
                card=card1
            )

    def test_collectioncard_str_method(self):
        collection = Collection.objects.get(name='testcollection')
        card1 = Card.objects.get(name='Card 1')
        collectioncard_1 = CollectionCard.objects.create(
            collection=collection,
            card=card1
        )
        self.assertEqual(collectioncard_1.__str__(), 'Card 1')
