# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Consent Export View
===================

Export consent records for GDPR compliance (Article 7.1).

"""

# Import | Standard Library
from datetime import datetime
from typing import Any

from django.http import HttpRequest, JsonResponse
from django.views.generic import View

# Import | Local
from ..models import CookieConsentModel, LogItem


class ConsentExportView(View):
    """
    Export consent records for GDPR compliance (Article 7.1).

    GET /cookie-consent/export/

    Returns JSON with all consent records for the current user/session.
    This provides proof of consent as required by GDPR.

    For authenticated users: Returns consent history for the user.
    For anonymous users: Returns consent for the current session.
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        """Export consent records."""
        records: list[dict[str, Any]] = []

        # Get consent records
        if request.user.is_authenticated:
            consents = (
                CookieConsentModel.objects.filter(user=request.user)
                .select_related("policy_version")
                .order_by("-created_at")
            )
        else:
            session_key = request.session.session_key
            if session_key:
                consents = (
                    CookieConsentModel.objects.filter(session_key=session_key)
                    .select_related("policy_version")
                    .order_by("-created_at")
                )
            else:
                consents = CookieConsentModel.objects.none()

        for consent in consents:
            records.append(
                {
                    "necessary": consent.necessary,
                    "analytics": consent.analytics,
                    "marketing": consent.marketing,
                    "consent_given": consent.consent_given,
                    "consent_date": consent.consent_date.isoformat(),
                    "created": consent.created_at.isoformat(),
                    "policy_version": (
                        consent.policy_version.version
                        if consent.policy_version
                        else None
                    ),
                    "ip_address": consent.ip_address,
                }
            )

        # Get audit log entries
        log_entries: list[dict[str, Any]] = []
        if request.user.is_authenticated:
            logs = (
                LogItem.objects.filter(user=request.user)
                .select_related("cookiegroup")
                .order_by("-timestamp")[:100]
            )
        else:
            session_key = request.session.session_key
            if session_key:
                logs = (
                    LogItem.objects.filter(session_key=session_key)
                    .select_related("cookiegroup")
                    .order_by("-timestamp")[:100]
                )
            else:
                logs = LogItem.objects.none()

        for log in logs:
            log_entries.append(
                {
                    "action": log.action,
                    "cookie_group": (
                        log.cookiegroup.varname if log.cookiegroup else None
                    ),
                    "timestamp": log.timestamp.isoformat(),
                    "version": log.version,
                }
            )

        return JsonResponse(
            {
                "export_date": datetime.now().isoformat(),
                "user": (
                    request.user.username
                    if request.user.is_authenticated
                    else None
                ),
                "session_key": request.session.session_key,
                "consent_records": records,
                "audit_log": log_entries,
            }
        )


__all__: list[str] = ["ConsentExportView"]
