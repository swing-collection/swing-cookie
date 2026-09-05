# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Consent Middleware
=========================

Re-exports middleware classes.

"""

# Import | Local
from .middleware import CleanCookiesMiddleware

__all__: list[str] = ["CleanCookiesMiddleware"]
