from django.test import TestCase


class coreUrlsTest(TestCase):

    def test_core_urls_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)
