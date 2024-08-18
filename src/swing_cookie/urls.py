# -*- coding: utf-8 -*-

from django.urls import path
from .views import set_cookie_view, get_cookie_view, delete_cookie_view

urlpatterns = [
    path('set-cookie/', set_cookie_view, name='set_cookie_view'),
    path('get-cookie/', get_cookie_view, name='get_cookie_view'),
    path('delete-cookie/', delete_cookie_view, name='delete_cookie_view'),
]




from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt

from .views import (
    CookieGroupAcceptView,
    CookieGroupDeclineView,
    CookieGroupListView,
    CookieStatusView,
)

urlpatterns = [
    path(
        "accept/",
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept_all",
    ),
    # TODO: use form or query string params for this instead?
    re_path(
        r"^accept/(?P<varname>.*)/$",
        csrf_exempt(CookieGroupAcceptView.as_view()),
        name="cookie_consent_accept",
    ),
    # TODO: use form or query string params for this instead?
    re_path(
        r"^decline/(?P<varname>.*)/$",
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline",
    ),
    path(
        "decline/",
        csrf_exempt(CookieGroupDeclineView.as_view()),
        name="cookie_consent_decline_all",
    ),
    path("status/", CookieStatusView.as_view(), name="cookie_consent_status"),
    path("", CookieGroupListView.as_view(), name="cookie_consent_cookie_group_list"),
]
