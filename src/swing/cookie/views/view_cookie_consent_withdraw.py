# -*- coding: utf-8 -*-

"""
Cookie Consent Withdraw View
============================

Withdraw all cookie consent.

"""

from ..utils.util import withdraw_all_consent
from .view_cookie_group_base import CookieGroupBaseProcessView


class CookieConsentWithdrawView(CookieGroupBaseProcessView):
    """
    Withdraw all cookie consent.

    POST /cookie-consent/withdraw/

    Declines all cookie groups and clears consent cookies.
    """

    def process(self, request, response, varname):
        withdraw_all_consent(request, response)


__all__: list[str] = ["CookieConsentWithdrawView"]
