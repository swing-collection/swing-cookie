# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Status View
==================

Returns the current consent status for all cookie groups.

"""

# Import | Standard Library
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token as get_csrf_token
from django.views.generic import View

# Import | Local
from ..utils.cache import all_cookie_groups
from ..utils.util import get_cookie_dict_from_request


class CookieStatusView(View):
    """
    Returns the current consent status for all cookie groups.

    GET /cookie-consent/status/

    Returns JSON:
    {
        "consent_given": true,
        "groups": {
            "analytics": {
                "name": "Analytics",
                "accepted": true,
                "declined": false,
                "pending": false,
                "is_required": false
            },
            ...
        }
    }
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        """
        Returns the current consent status for all cookie groups.
        """
        cookie_dic = get_cookie_dict_from_request(request)
        cookie_groups = all_cookie_groups()

        groups_status: dict[str, dict[str, Any]] = {}
        any_consent_given = False

        if cookie_groups:
            # Import | Local
            from ..conf import settings

            for varname, group in cookie_groups.items():
                version = cookie_dic.get(varname)
                is_accepted = False
                is_declined = False
                is_pending = True

                if version == settings.COOKIE_CONSENT_DECLINE:
                    is_declined = True
                    is_pending = False
                elif version is not None:
                    # Check if version is current
                    current_version = group.get_version()
                    if version >= current_version:
                        is_accepted = True
                        is_pending = False
                        any_consent_given = True

                groups_status[varname] = {
                    "name": group.name,
                    "accepted": is_accepted,
                    "declined": is_declined,
                    "pending": is_pending,
                    "is_required": group.is_required,
                }

        return JsonResponse(
            {
                "consent_given": any_consent_given,
                "groups": groups_status,
                "csrf_token": get_csrf_token(request),
            }
        )


__all__: list[str] = ["CookieStatusView"]
