# -*- coding: utf-8 -*-


from appconf import AppConf
from django.conf import settings  # NOQA


class CookieConsentConf(AppConf):
    """ """

    # django-cookie-consent cookie settings that store the configuration
    NAME = "cookie_consent"
    # TODO: rename to AGE for parity with django settings
    MAX_AGE = 60 * 60 * 24 * 365 * 1  # 1 year,
    DOMAIN = None
    SECURE = False
    HTTPONLY = True
    SAMESITE = "Lax"

    DECLINE = "-1"

    ENABLED = True

    OPT_OUT = False

    CACHE_BACKEND = "default"

    LOG_ENABLED = True


__all__: list[str] = ["settings"]
