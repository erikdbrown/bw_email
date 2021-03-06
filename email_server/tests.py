from django.test import (
    Client,
    TestCase,
)


HTTP_200_OK = 200
HTTP_400_BAD_REQUEST = 400
HTTP_405_NOT_ALLOWED = 405


class PostEmailAPITestCase(TestCase):

    def setUp(self):
        super(PostEmailAPITestCase, self).setUp()
        self.client = Client()
        self.emails_endpoint = '/emails'

    def tearDown(self):
        super(PostEmailAPITestCase, self).tearDown()

    def create_email(self, **kwargs):
        email = {
            'to': 'susan@abcpreschool.org',
            'to_name': 'Miss Susan',
            'from': 'noreply@mybrightwheel.com',
            'from_name': 'brightwheel',
            'subject': 'Your Weekly Report',
            'body': '<h1>Weekly Report</h1><p>You saved 10 hours</p>',
        }

        email.update(kwargs)
        return email

    def test_does_not_accept_get_delete_put(self):
        get_response = self.client.get(self.emails_endpoint)
        self.assertEqual(get_response.status_code, HTTP_405_NOT_ALLOWED)

        put_response = self.client.put(self.emails_endpoint)
        self.assertEqual(put_response.status_code, HTTP_405_NOT_ALLOWED)

        delete_response = self.client.delete(self.emails_endpoint)
        self.assertEqual(delete_response.status_code, HTTP_405_NOT_ALLOWED)

    def test_returns_200_ok_when_email_post_validates(self):
        response = self.client.post(
            self.emails_endpoint,
            data=self.create_email()
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_returns_400_with_invalid_email(self):
        email = self.create_email(to='not-an-email-address')

        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Invalid "to" email address'
        )

        email = self.create_email(**{'from': 'not-an-email-address'})

        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Invalid "from" email address'
        )

    def test_returns_400_with_missing_parameters(self):
        email = self.create_email()
        del email['to']

        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Missing required: to'
        )

        del email['from_name']
        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Missing required: from_name, to'
        )
