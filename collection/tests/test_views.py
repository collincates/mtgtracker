from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from collection.models import Collection, CollectionCard
from db.models import Card


class CollectionCreateViewTest(TestCase):
    def test_set_this_up(self):
        self.assertTrue(False)


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
        card1 = Card.objects.create(
            name='Card 1',
            set_name='a test set',
            id=1,
            sdk_id='123'
        )
        card2 = Card.objects.create(
            name='Card 2',
            set_name='a test set',
            id=2,
            sdk_id='456'
        )

        collectioncard_3_count = CollectionCard.objects.create(
            collection=collection,
            card=card2,
            count=3
        )

    def test_add_card_to_collection_view_redirects_to_collection_detail(self):
        collection = Collection.objects.get(name='testcollection')
        card1 = Card.objects.get(name='Card 1')
        response = self.client.get(reverse(
            'collection:collection_add',
            kwargs={
                'card_id': card1.id
            }
        ))
        self.assertRedirects(
            response,
            '/collection/testuser/testcollection/'
        )

    def test_add_card_to_collection_view_add_new_card(self):
        collection = Collection.objects.get(name='testcollection')
        card1 = Card.objects.get(name='Card 1')
        response = self.client.get(reverse(
            'collection:collection_add',
            kwargs={
                'card_id': card1.id
            }
        ))
        self.assertEqual(response.status_code, 302)
        card_count = CollectionCard.objects.get(
            collection=collection,
            card=card1
        ).count
        self.assertEqual(card_count, 1)

    def test_add_card_to_collection_view_add_existing_card(self):
        collection = Collection.objects.get(name='testcollection')
        card2 = Card.objects.get(name='Card 2')
        response = self.client.get(reverse(
            'collection:collection_add',
            kwargs={
                'card_id': card2.id
            }
        ))
        self.assertEqual(response.status_code, 302)
        card_count = CollectionCard.objects.get(
            collection=collection,
            card=card2
        ).count
        self.assertEqual(card_count, 4)


class RemoveCardFromCollectionViewTest(TestCase):

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
        card1 = Card.objects.create(
            name='Card 1',
            set_name='a test set',
            id=1,
            sdk_id='123'
        )
        card2 = Card.objects.create(
            name='Card 2',
            set_name='a test set',
            id=2,
            sdk_id='456'
        )
        collectioncard_1_count = CollectionCard.objects.create(
            collection=collection,
            card=card1,
            count=1
        )
        collectioncard_4_count = CollectionCard.objects.create(
            collection=collection,
            card=card2,
            count=4
        )

    def test_remove_card_from_collection_view_redirects_to_collection_detail(self):
        collection = Collection.objects.get(name='testcollection')
        card1 = Card.objects.get(name='Card 1')
        response = self.client.get(reverse(
            'collection:collection_remove',
            kwargs={
                'card_id': card1.id
            }
        ))
        self.assertRedirects(
            response,
            '/collection/testuser/testcollection/'
        )

    def test_remove_card_from_collection_view_remove_one_card_with_some_remaining(self):
        collection = Collection.objects.get(name='testcollection')
        card2 = Card.objects.get(name='Card 2')
        response = self.client.get(reverse(
            'collection:collection_remove',
            kwargs={
                'card_id': card2.id
            }
        ))
        self.assertEqual(response.status_code, 302)
        card_count = CollectionCard.objects.get(
            collection=collection,
            card=card2
        ).count
        self.assertEqual(card_count, 3)

    def test_remove_card_from_collection_view_remove_one_card_with_none_remaining(self):
        """When card count is reduced to zero, the CollectionCard is deleted."""
        collection = Collection.objects.get(name='testcollection')
        card1 = Card.objects.get(name='Card 1')
        response = self.client.get(reverse(
            'collection:collection_remove',
            kwargs={
                'card_id': card1.id
            }
        ))
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(CollectionCard.DoesNotExist):
            card_count = CollectionCard.objects.get(
                collection=collection,
                card=card1
            ).count
