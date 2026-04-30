# -*- coding: utf-8 -*-

"""
Cookie Delete View Function
===========================

Deletes a cookie dynamically based on query parameters.

"""

from django.http import HttpRequest, HttpResponse, JsonResponse

# Import | Local
from ..models import CookieModel


def cookie_delete_view(request: HttpRequest) -> HttpResponse:
    """
    Cookie Delete View Function
    ===========================

    Deletes a cookie dynamically based on query parameters.

    Query Parameters (GET) or Form Data (POST/DELETE):
    ---------------------------------------------------
    name : str (required)
        The name of the cookie to delete.
    from_database : bool (optional, default: False)
        If True, also removes the cookie record from the database.

    Parameters:
    -----------
    request : HttpRequest
        The request object.

    Returns:
    --------
    JsonResponse
        JSON response indicating success or failure.
    """
    params = (
        request.POST if request.method in ("POST", "DELETE") else request.GET
    )
    name = params.get("name")

    if not name:
        return JsonResponse(
            {"error": "Cookie name is required", "param": "name"},
            status=400,
        )

    from_database = params.get("from_database", "").lower() in (
        "true",
        "1",
        "yes",
    )
    deleted_from_db = False

    # Delete from database if requested
    if from_database:
        deleted_count, _ = CookieModel.objects.filter(name=name).delete()
        deleted_from_db = deleted_count > 0

    # Create response and delete browser cookie
    response = JsonResponse(
        {
            "success": True,
            "name": name,
            "deleted_from_browser": True,
            "deleted_from_database": deleted_from_db,
        }
    )
    response.delete_cookie(key=name)
    return response


__all__: list[str] = ["cookie_delete_view"]
