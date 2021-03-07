from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import HttpResponse

from email_server.models import Email


HTTP_400_BAD_REQUEST = 400
HTTP_405_METHOD_NOT_ALLOWED = 405


def validate_email(data):
    required_fields = {'to', 'to_name', 'from', 'from_name', 'subject', 'body'}
    validators = {
        'to': EmailValidator('Invalid "to" email address'),
        'from': EmailValidator('Invalid "from" email address'),
    }

    missing_fields = required_fields - set(data.keys())

    if missing_fields:
        msg = 'Missing required: {}'.format(', '.join(sorted(missing_fields)))
        raise ValidationError(msg)

    for field, validator in validators.items():
        validator(data.get(field))

    return data


def deserialize_email(data):
    email_data = validate_email(data)

    return {
        'to_email': email_data.get('to'),
        'to_name': email_data.get('to_name'),
        'from_email': email_data.get('from'),
        'from_name': email_data.get('from_name'),
        'subject': email_data.get('subject'),
        'body': email_data.get('body'),
    }


def handle_email_request(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)

    try:
        email_data = deserialize_email(request.POST)
        email = Email.objects.create(**email_data)
        return HttpResponse()
    except ValidationError as error:
        return HttpResponse(error.message, status=HTTP_400_BAD_REQUEST)
