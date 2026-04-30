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
- `CookieModel` / `Cookie`: Represents an individual cookie stored in the system.
- `CookieGroupModel` / `CookieGroup`: Groups cookies into categories such as
  Necessary, Analytics, and Marketing.
- `CookieConsentModel`: Tracks user consent for different cookie types.
- `CookiePolicyModel`: Stores versioned cookie policy documents.
- `LogItem`: Tracks consent actions for audit trail.

These models facilitate efficient cookie management and compliance with
privacy regulations.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Local
# Import | Local Modules
from .model_cookie import Cookie, CookieModel
from .model_cookie_consent import CookieConsentModel
from .model_cookie_group import CookieGroup, CookieGroupModel
from .model_cookie_policy import CookiePolicyModel
from .model_log_item import (
    ACTION_ACCEPTED,
    ACTION_CHOICES,
    ACTION_DECLINED,
    LogItem,
)

# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    # Models
    "Cookie",
    "CookieModel",
    "CookieConsentModel",
    "CookieGroup",
    "CookieGroupModel",
    "CookiePolicyModel",
    "LogItem",
    # Constants
    "ACTION_ACCEPTED",
    "ACTION_DECLINED",
    "ACTION_CHOICES",
]
