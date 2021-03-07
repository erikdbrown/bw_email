from django.test import (
    Client,
    TestCase,
    override_settings,
)

from email_server.models import (
    Email,
    EmailProviders,
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
        valid_email = self.create_email()

        response = self.client.post(self.emails_endpoint, data=valid_email)
        self.assertEqual(response.status_code, HTTP_200_OK)

        self.assertEqual(Email.objects.count(), 1)

        email = Email.objects.get(to_email=valid_email['to'])
        self.assertEqual(email.to_name, valid_email['to_name'])
        self.assertEqual(email.from_email, valid_email['from'])
        self.assertEqual(email.from_name, valid_email['from_name'])
        self.assertEqual(email.subject, valid_email['subject'])
        self.assertEqual(email.body, valid_email['body'])

    def test_returns_400_with_invalid_email(self):
        email = self.create_email(to='not-an-email-address')

        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Invalid "to" email address'
        )
        self.assertEqual(Email.objects.count(), 0)

        email = self.create_email(**{'from': 'not-an-email-address'})

        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Invalid "from" email address'
        )
        self.assertEqual(Email.objects.count(), 0)

    def test_returns_400_with_missing_parameters(self):
        email = self.create_email()
        del email['to']

        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Missing required: to'
        )
        self.assertEqual(Email.objects.count(), 0)

        del email['from_name']
        response = self.client.post(self.emails_endpoint, data=email)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.content.decode('utf-8'),
            'Missing required: from_name, to'
        )
        self.assertEqual(Email.objects.count(), 0)


class EmailModelTestCase(TestCase):

    @override_settings(EMAIL_PROVIDER=EmailProviders.SPENDGRID)
    def test_uses_setting_to_set_spendgrid_provider(self):
        email = Email.objects.create(
            to_email='foo@email.com',
            to_name='Foo Bar',
            from_email='noreply@email.com',
            from_name='Baz Qux',
            subject='Important Email',
            body='<p>Foo Bar Content</p>'
        )
        self.assertEqual(email.provider, EmailProviders.SPENDGRID)

    @override_settings(EMAIL_PROVIDER=EmailProviders.SNAILGUN)
    def test_uses_setting_to_set_snailgun_provider(self):
        email = Email.objects.create(
            to_email='foo@email.com',
            to_name='Foo Bar',
            from_email='noreply@email.com',
            from_name='Baz Qux',
            subject='Important Email',
            body='<p>Foo Bar Content</p>'
        )
        self.assertEqual(email.provider, EmailProviders.SNAILGUN)

    @override_settings(EMAIL_PROVIDER=EmailProviders.SNAILGUN)
    def test_does_not_set_provider_if_already_set(self):
        email = Email.objects.create(
            provider=EmailProviders.SPENDGRID,
            to_email='foo@email.com',
            to_name='Foo Bar',
            from_email='noreply@email.com',
            from_name='Baz Qux',
            subject='Important Email',
            body='<p>Foo Bar Content</p>'
        )
        self.assertEqual(email.provider, EmailProviders.SPENDGRID)
