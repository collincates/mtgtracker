from django.test import TestCase

from db.models import Card


class CardAdminTest(TestCase):
    pass
    # @classmethod
    # def setUpTestData(cls):
    #     # user = get_user_model.objects.create(username='test_user')
    #     card = Card.objects.create(
    #         name=f'Test Card',
    #         set_name='a test set',
    #         id=1,
    #         sdk_id='test sdk_id',
    #     )
    #
    # def test_card_admin_get_readonly_fields(self):
    #     responsecard = Card.objects.get(id=1)
    #     print(card.get_readonly_fields())
