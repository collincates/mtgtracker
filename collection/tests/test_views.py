from django.test import TestCase
from db.models import Collection


class CollectionDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345678')

        self.login = self.client.login(
            username=self.user.username,
            password=self.user.password
        )

        collection = Collection.objects.create(
            name='testcollection',
            owner=self.user
            )

    def test_collection_detail_view_url_exists_at_desired_location(self):
        collection = Collection.objects.get(name='testcollection')
        response = self.client.get(collection.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_collection_detail_view_url_accessible_by_collection_name_and_user_name(self):
        collection = Collection.objects.get(name='testcollection')
        url = f'/db/testuser/testcollection/'
        response = self.client.get(reverse(
            'collection_detail',
            kwargs={
                'collection_name': collection.name,
                'user_name': self.user.username
                }
            ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['request'].path, url)

    # def test_collection_detail_view_contains_collection_name_and_user_name(self):
    #     collection = Collection.objects.get(name='testcollection')
    #     response = self.client.get(reverse(
    #         'collection_detail',
    #         kwargs={
    #             'collection_name': collection.name,
    #             'user_name': self.user.username
    #             }
    #         ))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.context[-1]['view'].context['collection_name'], 'collection_name')
    #     # self.assertEqual(response.context[-1]['view'].collection_name, 'slug')

    def test_collection_detail_view_collection_name_on_detail_page(self):
        collection = Collection.objects.get(name='testcollection')
        response = self.client.get(collection.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, collection.name)
        self.assertEqual(response.context['collection'].name, 'testcollection')

    def test_collection_detail_view_collection_owner_on_detail_page(self):
        collection = Collection.objects.get(name='testcollection')
        response = self.client.get(collection.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, collection.owner)
        self.assertEqual(response.context['collection'].owner, self.user)


class AddCardToCollectionViewTest(TestCase):
    pass
    # self.testuser = User.objects.create_user(username='testuser', password='12345678')
    # self.login = self.client.login(username='testuser', password='12345678')

    # card2 = Card.objects.create(name='Card 2', set_name='a test set', id=2, sdk_id='456')

    # collectioncard_2 = CollectionCard.objects.create(
    #     collection=collection,
    #     card=card2
    # )

    # def test_collectioncard_add_card_to_collection(self):
    #     test_collection = Collection.objects.get(name='testcollection')
    #     card1 = Card.objects.get(name='Card 1')
    #     test_collection.cards.add(card1)
    #     print(test_collection.cards)
    # test add duplicate card


class RemoveCardFromCollectionViewTest(TestCase):
    pass
    # test remove card
    # test remove card to zero qty, what happens?
