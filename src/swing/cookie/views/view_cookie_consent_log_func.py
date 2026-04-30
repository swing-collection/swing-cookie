# -*- coding: utf-8 -*-

"""
Log Cookie Consent View Function
================================
"""

from django.http import HttpRequest, HttpResponse


def log_cookie_consent_view(request: HttpRequest) -> HttpResponse:
    """
    Logs the user's cookie consent status and sets a cookie to indicate that
    consent was given.
    """
    response = HttpResponse(content="Consent Logged")
    # Example of consent being passed as a GET parameter
    consent_status: str = request.GET.get("consent", "false")
    response.set_cookie(
        key="cookie_consent",
        value=consent_status,
    )
    return response


__all__: list[str] = ["log_cookie_consent_view"]
