from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from collection.models import Collection, CollectionCard
from db.models import Card


class CollectionDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345678'
        )

        self.login = self.client.login(
            username='testuser',
            password='12345678'
        )

        collection = Collection.objects.create(
            name='testcollection',
            owner=self.user
            )

    def test_collection_detail_view_redirect_if_not_logged_in(self):
        # Log out user for this test
        self.logout = self.client.logout()
        collection = Collection.objects.get(name='testcollection')
        response = self.client.get(reverse(
            'collection:collection_detail',
            kwargs={
                'collection_slug': collection.slug,
                'user_name': self.user.username
            }
        ))
        self.assertRedirects(
            response,
            '/accounts/login/?next=/collection/testuser/testcollection/'
        )

    def test_collection_detail_view_logged_in_uses_correct_template(self):
        collection = Collection.objects.get(name='testcollection')
        response = self.client.get(reverse(
            'collection:collection_detail',
            kwargs={
                'collection_slug': collection.slug,
                'user_name': self.user.username
            }
        ))
        # Check that user is logged in
        self.assertEqual(str(response.context['user']), 'testuser')
        # Check that we get a successful response
        self.assertEqual(response.status_code, 200)
        # Check that the correct template is being used
        self.assertTemplateUsed(response, 'collection/collection_detail.html')

    def test_collection_detail_view_url_exists_at_desired_location(self):
        collection = Collection.objects.get(name='testcollection')
        response = self.client.get(collection.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.wsgi_request.path,
            '/collection/testuser/testcollection/'
        )

    def test_collection_detail_view_url_accessible_by_collection_slug_and_user_name(self):
        collection = Collection.objects.get(name='testcollection')
        url = '/collection/testuser/testcollection/'
        response = self.client.get(reverse(
            'collection:collection_detail',
            kwargs={
                'collection_slug': collection.slug,
                'user_name': self.user.username
                }
            ))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['request'].path, url)

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
