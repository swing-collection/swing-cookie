# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Utilities Module
=======================

This module provides utility functions and decorators for the cookie
consent management system.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from functools import wraps
from typing import Any, Callable, TypeVar

# =============================================================================
# Types
# =============================================================================

F = TypeVar("F", bound=Callable[..., Any])


# =============================================================================
# Constants
# =============================================================================

# Consent action constants
ACTION_ACCEPTED = "accepted"
ACTION_DECLINED = "declined"


# =============================================================================
# Decorators
# =============================================================================


def clear_cache_after(func: F) -> F:
    """
    Decorator that clears the cookie groups cache after the wrapped
    function executes.

    This is typically used on model save/delete methods to ensure
    the cache stays in sync with the database.

    Parameters:
    -----------
    func : Callable
        The function to wrap.

    Returns:
    --------
    Callable
        The wrapped function that clears cache after execution.

    Example:
    --------
    >>> @clear_cache_after
    ... def save(self, *args, **kwargs):
    ...     return super().save(*args, **kwargs)
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        result = func(*args, **kwargs)
        # Import here to avoid circular imports
        # Import | Local
        from .cache import delete_cache

        delete_cache()
        return result

    return wrapper  # type: ignore[return-value]


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "ACTION_ACCEPTED",
    "ACTION_DECLINED",
    "clear_cache_after",
]
