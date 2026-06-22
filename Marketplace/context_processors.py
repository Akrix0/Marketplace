from django.middleware.csrf import get_token


def csrf_token(request):
    return {'csrf_token_value': get_token(request)}
