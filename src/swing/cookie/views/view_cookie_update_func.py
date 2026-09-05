# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Update Cookie View Function
===========================

Updates cookie values.

"""

from django.http import HttpRequest, HttpResponse


def update_cookie_view(request: HttpRequest) -> HttpResponse:
    """
    Update Cookie View Function
    ===========================

    Updates the value of a specific cookie.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    HttpResponse
        The response object indicating that the cookie has been updated.
    """
    response = HttpResponse(content="Cookie Updated")
    # This value can be dynamic or retrieved from request data
    new_value = "updated_value"
    response.set_cookie(key="example_cookie", value=new_value)
    return response


__all__: list[str] = ["update_cookie_view"]
