# Import | Standard Library
# -*- coding: utf-8 -*-
# Import | Standard Library
from typing import Any

from django.contrib.auth.views import RedirectURLMixin
from django.core.exceptions import SuspiciousOperation
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.middleware.csrf import get_token as get_csrf_token
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import ListView, View

# Import | Local
from ..models import CookieGroup
from ..utils.cache import all_cookie_groups
from ..utils.util import (
    accept_cookies,
    decline_cookies,
    get_accepted_cookie_groups,
    get_cookie_dict_from_request,
    get_declined_cookie_groups,
    get_not_accepted_or_declined_cookie_groups,
    withdraw_all_consent,
)


def is_ajax_like(request: HttpRequest) -> bool:
    # legacy ajax, removed in Django 4.0 (used to be request.is_ajax())
    ajax_header = request.headers.get("X-Requested-With")
    if ajax_header == "XMLHttpRequest":
        return True

    # module-js uses fetch and a custom header
    return bool(request.headers.get("X-Cookie-Consent-Fetch"))


class CookieGroupListView(ListView):
    """
    Display all cookies.
    """

    model = CookieGroup


class CookieGroupBaseProcessView(RedirectURLMixin, View):
    def get_success_url(self):
        """
        If user adds a 'next' as URL parameter or hidden input,
        redirect to the value of 'next'. Otherwise, redirect to
        cookie consent group list
        """
        redirect_to = self.request.POST.get(
            "next", self.request.GET.get("next")
        )
        if redirect_to and not url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        ):
            raise SuspiciousOperation("Unsafe open redirect suspected.")
        return redirect_to or reverse("cookie_consent_cookie_group_list")

    def process(self, request, response, varname):  # pragma: no cover
        raise NotImplementedError()

    def post(self, request, *args, **kwargs):
        varname = kwargs.get("varname", None)
        if is_ajax_like(request):
            response = HttpResponse()
        else:
            response = HttpResponseRedirect(self.get_success_url())
        self.process(request, response, varname)
        return response


class CookieGroupAcceptView(CookieGroupBaseProcessView):
    """
    View to accept CookieGroup.
    """

    def process(self, request, response, varname):
        accept_cookies(request, response, varname)


class CookieGroupDeclineView(CookieGroupBaseProcessView):
    """
    View to decline CookieGroup.
    """

    def process(self, request, response, varname):
        decline_cookies(request, response, varname)

    def delete(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class CookieStatusView(View):
    """
    Returns the current consent status for all cookie groups.

    GET /cookie-consent/status/

    Returns JSON:
    {
        "consent_given": true,
        "groups": {
            "analytics": {
                "name": "Analytics",
                "accepted": true,
                "declined": false,
                "pending": false,
                "is_required": false
            },
            ...
        }
    }
    """

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> JsonResponse:
        """
        Returns the current consent status for all cookie groups.
        """
        cookie_dic = get_cookie_dict_from_request(request)
        cookie_groups = all_cookie_groups()

        groups_status: dict[str, dict[str, Any]] = {}
        any_consent_given = False

        if cookie_groups:
            # Import | Local
            from ..conf import settings

            for varname, group in cookie_groups.items():
                version = cookie_dic.get(varname)
                is_accepted = False
                is_declined = False
                is_pending = True

                if version == settings.COOKIE_CONSENT_DECLINE:
                    is_declined = True
                    is_pending = False
                elif version is not None:
                    # Check if version is current
                    current_version = group.get_version()
                    if version >= current_version:
                        is_accepted = True
                        is_pending = False
                        any_consent_given = True

                groups_status[varname] = {
                    "name": group.name,
                    "accepted": is_accepted,
                    "declined": is_declined,
                    "pending": is_pending,
                    "is_required": group.is_required,
                }

        return JsonResponse(
            {
                "consent_given": any_consent_given,
                "groups": groups_status,
                "csrf_token": get_csrf_token(request),
            }
        )


class CookieConsentWithdrawView(CookieGroupBaseProcessView):
    """
    Withdraw all cookie consent.

    POST /cookie-consent/withdraw/

    Declines all cookie groups and clears consent cookies.
    """

    def process(self, request, response, varname):
        withdraw_all_consent(request, response)
