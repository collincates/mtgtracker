from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from collection.models import Collection
from db.models import Card


class collectionUrlsTest(TestCase):

    def test_collection_add_url(self):
        card = Card.objects.create(
            name='Card 1',
            set_name='a test set',
            id=1,
            sdk_id='123'
        )
        response = self.client.get('/collection/add/1/')
        self.assertEqual(response.status_code, 302)

    def test_collection_remove_url(self):
        card = Card.objects.create(
            name='Card 1',
            set_name='a test set',
            id=1,
            sdk_id='123'
        )
        response = self.client.get('/collection/remove/1/')
        self.assertEqual(response.status_code, 302)

    def test_collection_create_url(self):
        self.assertTrue(False)

    def test_collection_detail_url(self):
        user = User.objects.create_user(
            username='testuser',
            password='12345678'
        )

        login = self.client.login(
            username='testuser',
            password='12345678'
        )

        collection = Collection.objects.create(
            name='testcollection',
            owner=user
            )

        response = self.client.get(reverse(
            'collection:collection_detail',
            kwargs={
                'collection_slug': collection.slug,
                'user_name': user.username
            }
        ))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('collection' in response.context)
        self.assertEqual(collection, response.context['collection'])
