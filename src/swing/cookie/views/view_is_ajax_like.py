# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Ajax-like Request Detection
===========================

Utility function to detect AJAX-like requests.

"""

from django.http import HttpRequest


def is_ajax_like(request: HttpRequest) -> bool:
    """
    Check if request is AJAX-like.

    Detects legacy XMLHttpRequest or modern fetch with custom header.
    """
    # legacy ajax, removed in Django 4.0 (used to be request.is_ajax())
    ajax_header = request.headers.get("X-Requested-With")
    if ajax_header == "XMLHttpRequest":
        return True

    # module-js uses fetch and a custom header
    return bool(request.headers.get("X-Cookie-Consent-Fetch"))


__all__: list[str] = ["is_ajax_like"]
