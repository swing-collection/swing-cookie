# -*- coding: utf-8 -*-


# Import | Libraries
from appconf import AppConf

from django.conf import settings  # NOQA


class CookieConsentConf(AppConf):
    """
    Configuration settings for django-cookie-consent.

    All settings are prefixed with COOKIE_CONSENT_ when used in Django settings.
    """

    # Cookie settings for the consent cookie itself
    NAME = "cookie_consent"
    MAX_AGE = 60 * 60 * 24 * 365 * 1  # 1 year
    DOMAIN = None
    SECURE = False
    HTTPONLY = True
    SAMESITE = "Lax"

    # Value used to indicate declined consent
    DECLINE = "-1"

    # Enable/disable the entire consent system
    ENABLED = True

    # If True, cookies are allowed by default (opt-out mode)
    # If False, cookies are blocked until consent is given (opt-in mode, GDPR default)
    OPT_OUT = False

    # Cache backend for cookie groups
    CACHE_BACKEND = "default"

    # Enable logging of consent actions for audit trail
    LOG_ENABLED = True

    # === GDPR Compliance Settings ===

    # Number of days after which consent expires and user must re-consent
    # Set to None or 0 to disable expiry
    EXPIRY_DAYS = 365

    # Re-prompt user when a new policy version is published
    REPROMPT_ON_POLICY_CHANGE = True

    # Include user's IP address in consent logs (for proof of consent)
    # Note: May have privacy implications
    LOG_IP_ADDRESS = True

    # Include user agent in consent logs
    LOG_USER_AGENT = True


__all__: list[str] = ["settings"]
