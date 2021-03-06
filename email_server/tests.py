from django.test import (
    Client,
    TestCase,
)


HTTP_200_OK = 200
HTTP_405_NOT_ALLOWED = 405


class PostEmailAPITestCase(TestCase):

    def setUp(self):
        super(PostEmailAPITestCase, self).setUp()
        self.client = Client()
        self.emails_endpoint = '/emails'

    def tearDown(self):
        super(PostEmailAPITestCase, self).tearDown()

    def test_does_not_accept_get_delete_put(self):
        get_response = self.client.get(self.emails_endpoint)
        self.assertEqual(get_response.status_code, HTTP_405_NOT_ALLOWED)

        put_response = self.client.put(self.emails_endpoint)
        self.assertEqual(put_response.status_code, HTTP_405_NOT_ALLOWED)

        delete_response = self.client.delete(self.emails_endpoint)
        self.assertEqual(delete_response.status_code, HTTP_405_NOT_ALLOWED)
