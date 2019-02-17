from django.test import TestCase

from db.models import Card
from db.admin import CardAdmin

class CardAdminTest(TestCase):

    def setUp(self):
        self.card = Card.objects.create(
            name=f'Test Card',
            set_name='a test set',
            id=1,
            sdk_id='test sdk_id',
        )

    def test_card_admin_get_readonly_fields(self):
        response = self.client.get('/tome-administration/db/card/1/change/')
        request = response.wsgi_request
        card_admin_fields = CardAdmin(model=self.card, admin_site='/tome-administration/').get_readonly_fields(self, request)
        self.assertEqual(
            card_admin_fields,
            list(self.card.__dict__.keys())[1:]
        )
