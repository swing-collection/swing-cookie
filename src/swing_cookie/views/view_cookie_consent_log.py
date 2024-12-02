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
from typing import Any, Dict

# Import | Libraries
from django.http import HttpResponse, HttpRequest
from django.views import View

# Import | Local Modules
from swing_cookie.models.model_cookie import CookieModel


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
    response = HttpResponse("Consent Logged")
    # Example of consent being passed as a GET parameter
    consent_status = request.GET.get("consent", "false")
    response.set_cookie("cookie_consent", consent_status)
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
        **kwargs: Dict[str, Any],
    ) -> HttpResponse:
        Handles GET requests and updates the cookie value.
    """

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: Dict[str, Any],
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
        response = HttpResponse("Consent Logged")
        consent_status = request.GET.get("consent", "false")
        response.set_cookie("cookie_consent", consent_status)
        return response


# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "log_cookie_consent_view",
    "LogCookieConsentView",
]
