"""
Swing Cookie - A reusable Django app for GDPR-compliant cookie consent management.

This package provides:
- Class-based views for cookie consent management
- Django templates for cookie banners and preferences
- Template tags for easy integration
- Middleware for cookie cleanup
- Models for consent tracking and audit

Usage:
------
1. Add 'swing.cookie' to INSTALLED_APPS
2. Include URLs: path('cookies/', include('swing.cookie.urls'))
3. Add template tag to base template: {% cookie_banner %}

"""

__version__ = "0.7.0"

# Lazy imports to avoid Django configuration issues
__all__ = [
    "__version__",
    "ConsentExportView",
    "ConsentUpdateView",
    "CookieBannerView",
    "CookieConsentWithdrawView",
    "CookieGroupAcceptView",
    "CookieGroupDeclineView",
    "CookieGroupListView",
    "CookiePolicyView",
    "CookiePreferencesView",
    "CookieStatusView",
]


def __getattr__(name: str):
    """Lazy import views to avoid Django configuration issues."""
    if name in __all__ and name != "__version__":
        from . import views
        return getattr(views, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
