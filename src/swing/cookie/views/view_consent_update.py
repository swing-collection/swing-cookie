# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Consent Update View
===================

AJAX endpoint for updating cookie consent preferences.

"""

# Import | Standard Library
import json
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.utils import timezone
from django.views import View

# Import | Local
from ..conf import settings
from ..models import CookieConsentModel
from ..utils.cache import all_cookie_groups
from ..utils.util import accept_cookies, decline_cookies


class ConsentUpdateView(View):
    """
    Consent Update View
    ===================

    AJAX endpoint for updating cookie consent.

    POST /cookie-consent/update/

    Accepts JSON or form data:
    {
        "analytics": true,
        "marketing": false,
        "preferences": true
    }

    Or simplified:
    {
        "consent": "all" | "essential" | "custom"
    }

    Returns JSON with updated status.

    """

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        """Update consent preferences."""
        # Parse request body
        preferences = self._parse_request(request)

        if "error" in preferences:
            return JsonResponse(preferences, status=400)

        cookie_groups = all_cookie_groups()
        if not cookie_groups:
            return JsonResponse(
                {"error": "No cookie groups configured"},
                status=400,
            )

        response = JsonResponse({
            "success": True,
            "updated": [],
            "consent_given": True,
        })

        updated: list[str] = []

        # Handle simplified consent values
        consent_value = preferences.get("consent")
        if consent_value:
            if consent_value == "all":
                # Accept all cookies
                for varname in cookie_groups:
                    accept_cookies(request, response, varname)
                    updated.append(varname)
            elif consent_value == "essential":
                # Only essential (required) cookies
                for varname, group in cookie_groups.items():
                    if group.is_required:
                        accept_cookies(request, response, varname)
                        updated.append(varname)
                    else:
                        decline_cookies(request, response, varname)
            # custom is handled by individual preferences below
        else:
            # Handle individual preferences
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

        # Persist consent to database if configured
        if getattr(settings, "COOKIE_CONSENT_LOG_ENABLED", True):
            self._log_consent(request, preferences, updated)

        # Update the JSON body in place (rather than returning a brand-new
        # JsonResponse) so the Set-Cookie header written by
        # accept_cookies()/decline_cookies() above is preserved on the
        # response actually sent to the client.
        response_data = json.loads(response.content)
        response_data["updated"] = updated
        response.content = json.dumps(response_data)
        return response

    def _parse_request(self, request: HttpRequest) -> dict[str, Any]:
        """Parse JSON or form data from request."""
        try:
            if request.content_type == "application/json":
                return dict(json.loads(request.body.decode("utf-8")))
            # Form data - QueryDict.dict() collapses multi-value keys to
            # their last value, matching the single-value fields this
            # endpoint expects (varname -> accepted/consent).
            return dict(request.POST.dict())
        except (json.JSONDecodeError, ValueError) as e:
            return {"error": f"Invalid request body: {e}"}

    def _log_consent(
        self,
        request: HttpRequest,
        preferences: dict[str, Any],
        updated: list[str],
    ) -> None:
        """Log consent to database."""
        try:
            # Get user or session identifier
            user = request.user if request.user.is_authenticated else None
            session_key = request.session.session_key if hasattr(
                request, "session"
            ) else None

            # Determine consent values
            analytics = preferences.get(
                "analytics",
                preferences.get("consent") == "all",
            )
            marketing = preferences.get(
                "marketing",
                preferences.get("consent") == "all",
            )

            # Create or update consent record
            if user:
                CookieConsentModel.objects.update_or_create(
                    user=user,
                    defaults={
                        "necessary": True,
                        "analytics": bool(analytics),
                        "marketing": bool(marketing),
                        "consent_given": True,
                        "consent_date": timezone.now(),
                        "ip_address": self._get_client_ip(request),
                    },
                )
            elif session_key:
                CookieConsentModel.objects.update_or_create(
                    session_key=session_key,
                    user__isnull=True,
                    defaults={
                        "necessary": True,
                        "analytics": bool(analytics),
                        "marketing": bool(marketing),
                        "consent_given": True,
                        "consent_date": timezone.now(),
                        "ip_address": self._get_client_ip(request),
                    },
                )
        except Exception:
            # Don't fail the request if logging fails
            pass  # pylint: disable=unnecessary-pass

    def _get_client_ip(self, request: HttpRequest) -> str | None:
        """Extract client IP from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")


__all__: list[str] = ["ConsentUpdateView"]
