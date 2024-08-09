from django.shortcuts import render
from django.http import HttpResponse

def delete_cookie_view(request):
    response = HttpResponse("Cookie Deleted")
    response.delete_cookie('example_cookie')
    return response