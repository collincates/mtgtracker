from django.test import TestCase

class dbTests(TestCase):

    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_card_list(self):
        response = self.client.get('/db/cards/')
        self.assertEqual(response.status_code, 200)
