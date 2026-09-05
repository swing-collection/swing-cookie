# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Policy View
==================

Renders the cookie policy page with detailed information about cookies used.

"""

# Import | Standard Library
from typing import Any

from django.views.generic import TemplateView

# Import | Local
from ..conf import settings
from ..models import CookieModel
from ..utils.cache import all_cookie_groups


class CookiePolicyView(TemplateView):
    """
    Cookie Policy View
    ==================

    Renders a comprehensive cookie policy page.

    The page displays:
    - Overview of cookie usage
    - List of all cookie categories/groups
    - Detailed list of individual cookies
    - Information about each cookie (name, purpose, duration, etc.)
    - Links to update preferences

    Templates:
    ----------
    - swing_cookie/policy.html - Main policy page

    Context:
    --------
    - cookie_groups: All cookie groups with their cookies
    - site_name: Name of the site
    - contact_email: Contact email for privacy inquiries

    """

    template_name = "swing_cookie/policy.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add cookie policy context."""
        context = super().get_context_data(**kwargs)

        # Get all cookie groups with their cookies
        cookie_groups = all_cookie_groups()
        groups_with_cookies: list[dict[str, Any]] = []

        if cookie_groups:
            for varname, group in cookie_groups.items():
                group_data = {
                    "varname": varname,
                    "name": group.name,
                    "description": getattr(group, "description", ""),
                    "is_required": group.is_required,
                    "cookies": [],
                }

                # Get all cookies in this group
                if hasattr(group, "cookie_set"):
                    for cookie in group.cookie_set.all():
                        cookie_data = {
                            "name": cookie.name,
                            "path": getattr(cookie, "path", "/"),
                            "domain": getattr(cookie, "domain", ""),
                            "description": getattr(cookie, "description", ""),
                            "duration": self._format_duration(cookie),
                        }
                        group_data["cookies"].append(cookie_data)

                groups_with_cookies.append(group_data)

        context.update(
            {
                "cookie_groups": groups_with_cookies,
                "site_name": getattr(settings, "COOKIE_SITE_NAME", ""),
                "contact_email": getattr(settings, "COOKIE_CONTACT_EMAIL", ""),
                "last_updated": getattr(settings, "COOKIE_POLICY_DATE", ""),
            }
        )
        return context

    def _format_duration(self, cookie: CookieModel) -> str:
        """Format cookie duration for display."""
        if hasattr(cookie, "max_age") and cookie.max_age:
            days = cookie.max_age // 86400
            if days >= 365:
                years = days // 365
                return f"{years} year{'s' if years > 1 else ''}"
            if days >= 30:
                months = days // 30
                return f"{months} month{'s' if months > 1 else ''}"
            if days > 0:
                return f"{days} day{'s' if days > 1 else ''}"
            hours = cookie.max_age // 3600
            if hours > 0:
                return f"{hours} hour{'s' if hours > 1 else ''}"
            return "Session"
        return "Session"


__all__: list[str] = ["CookiePolicyView"]
