# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Preferences View
=======================

Manage granular cookie preferences.

"""

# Import | Standard Library
import json
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

# Import | Local
from ..utils.cache import all_cookie_groups
from ..utils.util import accept_cookies, decline_cookies
from .view_cookie_status import CookieStatusView


class CookiePreferencesView(View):
    """
    Manage granular cookie preferences.

    GET: Returns current preferences for all cookie groups.
    POST: Updates preferences for specific cookie groups.

    POST /cookie-consent/preferences/

    Body (JSON or form data):
    {
        "analytics": true,
        "marketing": false,
        "preferences": true
    }

    Returns JSON with updated consent status.
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        """Returns current preferences."""
        # Reuse CookieStatusView logic
        status_view = CookieStatusView()
        return status_view.get(request, *args, **kwargs)

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        """Updates preferences for specific cookie groups."""
        cookie_groups = all_cookie_groups()

        # Parse JSON body or form data
        try:
            if request.content_type == "application/json":
                preferences = json.loads(request.body)
            else:
                preferences = dict(request.POST)
                # Convert single values from lists
                preferences = {
                    k: v[0] if isinstance(v, list) and len(v) == 1 else v
                    for k, v in preferences.items()
                }
        except (json.JSONDecodeError, ValueError):
            return JsonResponse(
                {"error": "Invalid JSON body"},
                status=400,
            )

        if not cookie_groups:
            return JsonResponse(
                {"error": "No cookie groups configured"},
                status=400,
            )

        response = JsonResponse({"success": True, "updated": []})
        updated: list[str] = []

        for varname, accepted in preferences.items():
            if varname not in cookie_groups:
                continue

            group = cookie_groups[varname]

            # Skip required cookies - they can't be declined
            if group.is_required and not accepted:
                continue

            # Convert string to bool if needed
            if isinstance(accepted, str):
                accepted = accepted.lower() in ("true", "1", "yes", "on")

            if accepted:
                accept_cookies(request, response, varname)
            else:
                decline_cookies(request, response, varname)

            updated.append(varname)

        response_data = {
            "success": True,
            "updated": updated,
        }

        # Return as new response with cookies set
        final_response = JsonResponse(response_data)
        # Copy cookies from temp response
        for cookie in response.cookies.values():
            final_response.cookies[cookie.key] = cookie

        return final_response


__all__: list[str] = ["CookiePreferencesView"]
