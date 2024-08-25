
class CookieStatusView(View):
    """
    Check the current accept/decline status for cookies.

    The returned accept and decline URLs are specific to this user and include the
    cookie groups that weren't accepted or declined yet.

    Note that this endpoint also returns a CSRF Token to be used by the frontend,
    as baking a CSRFToken into a cached page will not reliably work.
    """

    def get(self, request: HttpRequest) -> JsonResponse:
        accepted = get_accepted_cookie_groups(request)
        declined = get_declined_cookie_groups(request)
        not_accepted_or_declined = get_not_accepted_or_declined_cookie_groups(request)
        # TODO: change this csv URL param into proper POST params
        varnames = ",".join([group.varname for group in not_accepted_or_declined])
        data = {
            "csrftoken": get_csrf_token(request),
            "acceptUrl": reverse("cookie_consent_accept", kwargs={"varname": varnames}),
            "declineUrl": reverse(
                "cookie_consent_decline", kwargs={"varname": varnames}
            ),
            "acceptedCookieGroups": [group.varname for group in accepted],
            "declinedCookieGroups": [group.varname for group in declined],
            "notAcceptedOrDeclinedCookieGroups": [
                group.varname for group in not_accepted_or_declined
            ],
        }
        return JsonResponse(data)
