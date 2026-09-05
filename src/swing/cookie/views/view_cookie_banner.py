# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Banner View
==================

Renders the cookie banner template for displaying consent options.

"""

# Import | Standard Library
from typing import Any

from django.views.generic import TemplateView

# Import | Local
from ..conf import settings
from ..utils.cache import all_cookie_groups
from ..utils.util import get_cookie_dict_from_request


class CookieBannerView(TemplateView):
    """
    Cookie Banner View
    ==================

    Renders the cookie consent banner template.

    The banner displays:
    - A message about cookie usage
    - Accept all cookies button
    - Decline optional cookies button
    - Link to cookie preferences/settings

    Templates:
    ----------
    - swing_cookie/banner.html - Main banner template
    - swing_cookie/banner_modal.html - Modal variant

    Context:
    --------
    - cookie_groups: List of available cookie groups
    - consent_status: Current consent status for each group
    - accept_all_url: URL to accept all cookies
    - decline_all_url: URL to decline optional cookies
    - preferences_url: URL to cookie preferences page
    - show_banner: Whether to show the banner

    """

    template_name = "swing_cookie/banner.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add cookie banner context."""
        context = super().get_context_data(**kwargs)

        cookie_dict = get_cookie_dict_from_request(self.request)
        cookie_groups = all_cookie_groups()

        # Determine if banner should be shown
        # Show if user hasn't given any consent yet
        show_banner = True
        consent_status: dict[str, dict[str, Any]] = {}

        if cookie_groups:
            for varname, group in cookie_groups.items():
                version = cookie_dict.get(varname)
                is_accepted = False
                is_declined = False

                if version == settings.COOKIE_CONSENT_DECLINE:
                    is_declined = True
                    show_banner = False  # User has made a choice
                elif version is not None:
                    current_version = group.get_version()
                    if version >= current_version:
                        is_accepted = True
                        show_banner = False  # User has made a choice

                consent_status[varname] = {
                    "name": group.name,
                    "description": getattr(group, "description", ""),
                    "accepted": is_accepted,
                    "declined": is_declined,
                    "is_required": group.is_required,
                }

        context.update(
            {
                "cookie_groups": cookie_groups,
                "consent_status": consent_status,
                "show_banner": show_banner,
                "cookie_banner_position": getattr(
                    settings, "COOKIE_BANNER_POSITION", "bottom"
                ),
                "cookie_banner_style": getattr(
                    settings, "COOKIE_BANNER_STYLE", "bar"
                ),
            }
        )
        return context


__all__: list[str] = ["CookieBannerView"]
