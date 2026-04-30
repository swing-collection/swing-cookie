# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Utilities
========================

This module provides utility functions for managing cookie consent,
including parsing, accepting, declining, and withdrawing consent.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
import datetime
from typing import Any, Optional

# Import | Local
from ..conf import settings
from .cache import all_cookie_groups, get_cookie, get_cookie_group

# Constants imported lazily to avoid circular imports
ACTION_ACCEPTED = "accepted"
ACTION_DECLINED = "declined"


# =============================================================================
# Functions
# =============================================================================


def parse_cookie_str(cookie: Optional[str]) -> dict[str, str]:
    """
    Parses a cookie consent string into a dictionary.

    Parameters:
    -----------
    cookie : str | None
        The cookie string in format "key1=value1|key2=value2".

    Returns:
    --------
    dict[str, str]
        A dictionary mapping cookie group varnames to their consent versions.
    """
    dic: dict[str, str] = {}
    if not cookie:
        return dic
    for c in cookie.split("|"):
        if "=" in c:
            key, value = c.split("=", 1)
            dic[key] = value
    return dic


def dict_to_cookie_str(dic):
    """ """
    return "|".join(["%s=%s" % (k, v) for k, v in dic.items() if v])


def get_cookie_dict_from_request(request):
    """ """
    cookie_str = request.COOKIES.get(settings.COOKIE_CONSENT_NAME)
    return parse_cookie_str(cookie_str)


def set_cookie_dict_to_response(response, dic) -> None:
    """ """
    response.set_cookie(
        settings.COOKIE_CONSENT_NAME,
        dict_to_cookie_str(dic),
        max_age=settings.COOKIE_CONSENT_MAX_AGE,
        domain=settings.COOKIE_CONSENT_DOMAIN,
        secure=settings.COOKIE_CONSENT_SECURE or None,
        httponly=settings.COOKIE_CONSENT_HTTPONLY or None,
        samesite=settings.COOKIE_CONSENT_SAMESITE,
    )


def get_cookie_value_from_request(
    request,
    varname,
    cookie=None,
) -> None | bool:
    """
    Returns if cookie group or its specific cookie has been accepted.

    Returns True or False when cookie is accepted or declined or None
    if cookie is not set.
    """
    cookie_dic = get_cookie_dict_from_request(request)
    if not cookie_dic:
        return None

    cookie_group = get_cookie_group(varname=varname)
    if not cookie_group:
        return None
    if cookie:
        name, domain = cookie.split(":")
        cookie = get_cookie(
            cookie_group=cookie_group,
            name=name,
            domain=domain,
        )
    else:
        cookie = None

    version = cookie_dic.get(varname, None)

    if version == settings.COOKIE_CONSENT_DECLINE:
        return False
    if version is None:
        return None
    if not cookie:
        v = cookie_group.get_version()
    else:
        v = cookie.get_version()
    if version >= v:
        return True
    return None


def get_cookie_groups(varname=None):
    """ """
    cookie_groups = all_cookie_groups()
    if cookie_groups is None:
        return []
    if not varname:
        return cookie_groups.values()
    keys = varname.split(",")
    return [g for k, g in cookie_groups.items() if k in keys]


def accept_cookies(
    request,
    response,
    varname=None,
) -> None:
    """
    Accept cookies in Cookie Group specified by ``varname``.
    """
    cookie_dic = get_cookie_dict_from_request(request=request)
    for cookie_group in get_cookie_groups(varname):
        cookie_dic[cookie_group.varname] = cookie_group.get_version()
        if settings.COOKIE_CONSENT_LOG_ENABLED:
            # Import | Local
            from ..models import LogItem

            LogItem.objects.create(
                action=ACTION_ACCEPTED,
                cookiegroup=cookie_group,
                version=cookie_group.get_version(),
            )
    set_cookie_dict_to_response(response=response, dic=cookie_dic)


def delete_cookies(response, cookie_group) -> None:
    """ """
    if cookie_group.is_deletable:
        for cookie in cookie_group.cookie_set.all():
            response.delete_cookie(cookie.name, cookie.path, cookie.domain)


def decline_cookies(
    request,
    response,
    varname=None,
) -> None:
    """
    Decline and delete cookies in CookieGroup specified by ``varname``.
    """
    cookie_dic = get_cookie_dict_from_request(request)
    for cookie_group in get_cookie_groups(varname):
        cookie_dic[cookie_group.varname] = settings.COOKIE_CONSENT_DECLINE
        delete_cookies(response, cookie_group)
        if settings.COOKIE_CONSENT_LOG_ENABLED:
            # Import | Local
            from ..models import LogItem

            LogItem.objects.create(
                action=ACTION_DECLINED,
                cookiegroup=cookie_group,
                version=cookie_group.get_version(),
            )
    set_cookie_dict_to_response(response, cookie_dic)


def are_all_cookies_accepted(request) -> bool:
    """
    Returns if all cookies are accepted.
    """
    return all(
        [
            get_cookie_value_from_request(request, cookie_group.varname)
            for cookie_group in get_cookie_groups()
        ]
    )


def _get_cookie_groups_by_state(
    request,
    state: bool | None,
) -> list[Any]:
    """ """
    return [
        cookie_group
        for cookie_group in get_cookie_groups()
        if get_cookie_value_from_request(
            request=request,
            varname=cookie_group.varname,
        )
        is state
    ]


def get_not_accepted_or_declined_cookie_groups(request) -> list[Any]:
    """
    Returns all cookie groups that are neither accepted or declined.
    """
    return _get_cookie_groups_by_state(request, state=None)


def get_accepted_cookie_groups(request) -> list[Any]:
    """
    Returns all cookie groups that are accepted.
    """
    return _get_cookie_groups_by_state(
        request=request,
        state=True,
    )


def get_declined_cookie_groups(request) -> list[Any]:
    """
    Returns all cookie groups that are declined.
    """
    return _get_cookie_groups_by_state(
        request=request,
        state=False,
    )


def is_cookie_consent_enabled(request):
    """
    Returns if django-cookie-consent is enabled for given request.
    """
    enabled = settings.COOKIE_CONSENT_ENABLED
    if callable(enabled):
        return enabled(request)
    else:
        return enabled


def get_cookie_string(cookie_dic) -> str:
    """
    Returns cookie in format suitable for use in javascript.
    """
    expires = datetime.datetime.now() + datetime.timedelta(
        seconds=settings.COOKIE_CONSENT_MAX_AGE
    )
    cookie_str = "%s=%s; expires=%s; path=/" % (
        settings.COOKIE_CONSENT_NAME,
        dict_to_cookie_str(cookie_dic),
        expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    )
    return cookie_str


def get_accepted_cookies(request):
    """
    Returns all accepted cookies.
    """
    cookie_dic = get_cookie_dict_from_request(request)
    accepted_cookies = []
    cookie_groups = all_cookie_groups()
    if cookie_groups is None:
        return accepted_cookies
    for cookie_group in cookie_groups.values():
        version = cookie_dic.get(cookie_group.varname, None)
        if not version or version == settings.COOKIE_CONSENT_DECLINE:
            continue
        for cookie in cookie_group.cookie_set.all():
            if version >= cookie.get_version():
                accepted_cookies.append(cookie)
    return accepted_cookies


def withdraw_all_consent(request, response) -> None:
    """
    Withdraw all cookie consent.

    This declines all cookie groups, deletes their cookies, and clears
    the consent cookie entirely.

    Parameters:
    -----------
    request : HttpRequest
        The current HTTP request.
    response : HttpResponse
        The HTTP response to modify.

    Returns:
    --------
    None
    """
    # Decline all cookie groups
    for cookie_group in get_cookie_groups():
        delete_cookies(response, cookie_group)
        if settings.COOKIE_CONSENT_LOG_ENABLED:
            # Import | Local
            from ..models import LogItem

            LogItem.log_consent(
                action=ACTION_DECLINED,
                cookiegroup=cookie_group,
                request=request,
            )

    # Clear the consent cookie entirely
    response.delete_cookie(
        settings.COOKIE_CONSENT_NAME,
        path="/",
        domain=settings.COOKIE_CONSENT_DOMAIN,
    )


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "accept_cookies",
    "are_all_cookies_accepted",
    "decline_cookies",
    "delete_cookies",
    "dict_to_cookie_str",
    "get_accepted_cookie_groups",
    "get_accepted_cookies",
    "get_cookie_dict_from_request",
    "get_cookie_groups",
    "get_cookie_string",
    "get_cookie_value_from_request",
    "get_declined_cookie_groups",
    "get_not_accepted_or_declined_cookie_groups",
    "is_cookie_consent_enabled",
    "parse_cookie_str",
    "set_cookie_dict_to_response",
    "withdraw_all_consent",
]
