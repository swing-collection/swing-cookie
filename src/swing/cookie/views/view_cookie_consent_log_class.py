# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Log Cookie Consent View Class
=============================
"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views import View

# Import | Local
from .view_cookie_consent_log_func import log_cookie_consent_view


class LogCookieConsentView(View):
    """A class-based view that logs the user's cookie consent status."""

    def get(
        self,
        request: HttpRequest,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> HttpResponse:
        return log_cookie_consent_view(request)


__all__: list[str] = ["LogCookieConsentView"]
