from django.shortcuts import render
from django.http import HttpResponse

def get_cookie_view(request):
    cookie_value = request.COOKIES.get('example_cookie')
    return HttpResponse(f"Cookie Value: {cookie_value}")