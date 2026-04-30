# -*- coding: utf-8 -*-

"""
Demo Views
==========

Views for testing swing-cookie functionality.

"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Home page with cookie consent demo.
    """
    return render(request, "demo/home.html")


def analytics_page(request: HttpRequest) -> HttpResponse:
    """
    Page demonstrating analytics scripts that depend on consent.
    """
    return render(request, "demo/analytics.html")


def preferences_page(request: HttpRequest) -> HttpResponse:
    """
    Page for managing cookie preferences.
    """
    return render(request, "demo/preferences.html")
