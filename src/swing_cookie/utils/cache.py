# -*- coding: utf-8 -*-
from django.core.cache import caches

from .conf import settings
from .models import CookieGroup

CACHE_KEY = "cookie_consent_cache"
CACHE_TIMEOUT = 60 * 60  # 60 minutes


def _get_cache():
    """
    Lazily wrap around django.core.cache.

    This prevents the cache object to be resolved at import-time, which breaks the
    `django.test.override_settings` functionality for projects adding tests for this
    package, see https://github.com/bmihelac/django-cookie-consent/issues/41.
    """
    return caches[settings.COOKIE_CONSENT_CACHE_BACKEND]


def delete_cache():
    cache = _get_cache()
    cache.delete(CACHE_KEY)


def _get_cookie_groups_from_db():
    qs = CookieGroup.objects.filter(is_required=False).prefetch_related("cookie_set")
    return qs.in_bulk(field_name="varname")


def all_cookie_groups():
    """
    Get all cookie groups that are optional.

    Reads from the cache where possible, sets the value in the cache if there's a
    cache miss.
    """
    cache = _get_cache()
    return cache.get_or_set(
        CACHE_KEY, _get_cookie_groups_from_db, timeout=CACHE_TIMEOUT
    )


def get_cookie_group(varname):
    return all_cookie_groups().get(varname)


def get_cookie(cookie_group, name, domain):
    for cookie in cookie_group.cookie_set.all():
        if cookie.name == name and cookie.domain == domain:
            return cookie
    return None
