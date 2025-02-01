# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Model Module
===================

This module provides the models for managing cookies, including their
attributes, storage, and tracking user consent.

It includes:
------------
- `CookieModel`: Represents an individual cookie stored in the system.
- `CookieGroupModel`: Groups cookies into categories such as Necessary,
  Analytics, and Marketing.
- `CookieConsentModel`: Tracks user consent for different cookie types.

These models facilitate efficient cookie management and compliance with
privacy regulations.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Local Modules
from .model_cookie import CookieModel
from .model_cookie_consent import CookieConsentModel
from .model_cookie_group import CookieGroupModel
from .model_cookie_policy import CookiePolicyModel

# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "CookieModel",
    "CookieGroupModel",
    "CookieConsentModel",
    "CookiePolicyModel",
]
