import json

import requests
from django.apps import apps
from django.conf import settings


HTTP_200_OK = 200


class SpendgridProvider():

    @staticmethod
    def send_request(email_id):
        if settings.SPENDGRID_KEY is None:
            raise Exception('SPENDGRID_KEY is not configured.')

        try:
            Email = apps.get_model('email_server', 'Email')
            email = Email.objects.get(pk=email_id)
        except Email.DoesNotExist:
            return

        payload = {
            'sender': '{} <{}>'.format(email.from_name, email.from_email),
            'recipient': '{} <{}>'.format(email.to_name, email.to_email),
            'subject': email.subject,
            'body': email.body,
        }

        return requests.post(
            url='https://bw-interviews.herokuapp.com/spendgrid/send_email',
            data=json.dumps(payload),
            headers={
                'Content-Type': 'application/json',
                'X-Api-Key': settings.SPENDGRID_KEY,
            }
        )


class SnailgunProvider():

    @staticmethod
    def send_request(email_id):
        if settings.SNAILGUN_KEY is None:
            raise Exception('SNAILGUN_KEY is not configured.')

        try:
            Email = apps.get_model('email_server', 'Email')
            email = Email.objects.get(pk=email_id)
        except Email.DoesNotExist:
            return

        payload = {
            'from_email': email.from_email,
            'from_name': email.from_name,
            'to_email': email.to_email,
            'to_name': email.to_name,
            'subject': email.subject,
            'body': email.body,
        }

        response = requests.post(
            url='https://bw-interviews.herokuapp.com/snailgun/emails',
            data=json.dumps(payload),
            headers={
                'Content-Type': 'application/json',
                'X-Api-Key': settings.SNAILGUN_KEY,
            }
        )

        if response.status_code != HTTP_200_OK:
            # TODO: This needs better handling
            raise Exception('Something is wrong')

        response_body = json.loads(response.content)

        email.external_id = response_body.get('id')
        email.status = response_body.get('status')
        email.save()
