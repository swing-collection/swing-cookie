from django.shortcuts import render
from django.http import HttpResponse
from .models import Cookie

def set_cookie_view(request):
    response = HttpResponse("Cookie Set")
    cookie = Cookie(
        name='example_cookie',
        value='example_value',
        domain=request.get_host(),
        path='/',
        expires=None,
        secure=False,
        httponly=True
    )
    cookie.save()
    response.set_cookie(
        key=cookie.name,
        value=cookie.value,
        domain=cookie.domain,
        path=cookie.path,
        expires=cookie.expires,
        secure=cookie.secure,
        httponly=cookie.httponly
    )
    return response