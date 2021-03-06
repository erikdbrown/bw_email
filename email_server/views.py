from django.http import HttpResponse


HTTP_405_METHOD_NOT_ALLOWED = 405


def handle_email_request(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTP_405_METHOD_NOT_ALLOWED)

    return HttpResponse()
