from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import User
from db.models import Card, Collection, Deck


class SetListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_cards = 302

        for card_id in range(number_of_cards):
            Card.objects.create(
                name=f'Card {card_id}',
                set_name='Test Set Name',
                id=f'{card_id}',
                sdk_id=f'{card_id}',
            )
    #
    # def test_set_list_view_url_exists_at_desired_location(self):
    #     response = self.client.get('/db/Test Set Name/')
    #     self.assertEqual(response.status_code, 200)


    def test_set_list_view_url_accessible_by_name(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('set_list', args=[card.set_name]))
        self.assertEqual(response.status_code, 200)

    def test_set_list_view_uses_correct_template(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('set_list', args=[card.set_name]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'db/set_list.html')

    def test_set_list_view_empty_database(self):
        Card.objects.all().delete()
        with self.assertRaises(NameError):
            response = self.client.get(reverse('set_list', args=[card.set_name]))

    def test_set_list_view_with_empty_queryset(self):
        queryset = None
        with self.assertRaises(NameError):
            response = self.client.get(reverse('set_list', args=[card.set_name]))

    def test_set_list_view_pagination_is_one_hundred(self):
        card = Card.objects.all()
        response = self.client.get(reverse('set_list', args=[card[0].set_name]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 100)

    def test_set_list_view_pagination_lists_all_cards(self):
        card = Card.objects.all()
        response = self.client.get(reverse('set_list', args=[card[0].set_name]))

        response = self.client.get(reverse('set_list', args=[card[0].set_name]) + '?page=4')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 2)


class CardListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create 203 cards for pagination tests
        number_of_cards = 203

        for card_id in range(number_of_cards):
            Card.objects.create(
                name=f'Card {card_id}',
                id=f'{card_id}',
                sdk_id=f'{card_id}',
            )

    def test_card_list_view_url_exists_at_desired_location(self):
        response = self.client.get('/db/cards/')
        self.assertEqual(response.status_code, 200)

    def test_card_list_view_url_accessible_by_name(self):
        response = self.client.get(reverse('card_list'))
        self.assertEqual(response.status_code, 200)

    def test_card_list_view_uses_correct_template(self):
        response = self.client.get(reverse('card_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'db/card_list.html')

    def test_card_list_view_has_no_cards(self):
        Card.objects.all().delete()
        response = self.client.get(reverse('card_list'))
        self.assertContains(
            response,
            'No cards are available with these options.'
        )

    def test_card_list_view_pagination_is_one_hundred(self):
        response = self.client.get(reverse('card_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 100)

    def test_card_list_view_pagination_lists_all_cards(self):
        response = self.client.get(reverse('card_list') + '?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['card_list']) == 3)


class CardDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # user = get_user_model.objects.create(username='test_user')
        card = Card.objects.create(
            name=f'Test Card',
            set_name='a test set',
            id=1,
            sdk_id='test sdk_id',
        )

    def test_card_detail_view_url_exists_at_desired_location(self):
        card = Card.objects.get(id=1)
        response = self.client.get(card.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_card_detail_view_url_accessible_by_name_with_slug_argument(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)

    def test_card_detail_view_contains_custom_slug_field(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse(
            'card_detail',
            kwargs={
                # 'set_slug': slugify(card.set_name),
                'card_slug': card.slug,
            }
        ))
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.context[-1]['view'].slug_field, 'slug')

    def test_card_detail_view_contains_custom_slug_url_kwarg(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[-1]['view'].slug_url_kwarg, 'slug')

    def test_card_detail_view_card_name_on_detail_page(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, card.name)
        self.assertEqual(response.context['card'].name, 'Test Card')

    def test_card_detail_view_card_sdk_id_on_detail_page(self):
        card = Card.objects.get(id=1)
        response = self.client.get(reverse('card_detail', args=[card.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, card.name)
        self.assertEqual(response.context['card'].sdk_id, 'test sdk_id')


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
