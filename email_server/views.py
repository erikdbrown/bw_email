from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.http import HttpResponse


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


def handle_email_request(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)

    try:
        email = validate_email(request.POST)
        return HttpResponse()
    except ValidationError as error:
        return HttpResponse(error.message, status=HTTP_400_BAD_REQUEST)
