# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Set Views Module
=======================


"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Local Modules
from ..models import CookieModel

# Import | Libraries
from django.http import HttpRequest, HttpResponse
from django.views import View

# =============================================================================
# Functions
# =============================================================================


def log_cookie_consent_view(request: HttpRequest) -> HttpResponse:
    """
    Log Cookie Consent View Function
    ================================

    Logs the user"s cookie consent status and sets a cookie to indicate that
    consent was given.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the consent has been logged.
    """
    response = HttpResponse(content="Consent Logged")
    # Example of consent being passed as a GET parameter
    consent_status: str = request.GET.get("consent", "false")
    response.set_cookie(
        key="cookie_consent",
        value=consent_status,
    )
    return response


# =============================================================================
# Classes
# =============================================================================


class LogCookieConsentView(View):
    """
    Log Cookie Consent View Class
    =============================

    A class-based view that logs the user"s cookie consent status and sets a
    cookie to indicate that consent was given.

    Methods:
    --------
    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        Handles GET requests and updates the cookie value.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        """
        Handles GET requests to log the user"s cookie consent status and set a
        corresponding cookie.

        Parameters:
        -----------
        request : HttpRequest
            The request object.

        Returns:
        --------
        HttpResponse
            The response object indicating that the consent has been logged.
        """
        response = HttpResponse(content="Consent Logged")
        consent_status: str = request.GET.get("consent", "false")
        response.set_cookie(
            key="cookie_consent",
            value=consent_status,
        )
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "log_cookie_consent_view",
    "LogCookieConsentView",
]
