# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================


"""
Cookie Policy Model Module
==========================

This module provides the `CookiePolicy` model, which defines the cookie
policy for the website, including its version, content, and timestamps.

"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any

# Import | Libraries
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import | Local


# =============================================================================
# Class
# =============================================================================


class CookiePolicyModel(models.Model):
    """
    Cookie Policy Model
    ===================

    Defines the cookie policy for the website, including the version and
    content of the policy.

    Attributes:
    -----------
    version : str
        The version of the cookie policy.
    content : str
        The content of the cookie policy.
    created_at : datetime
        The timestamp when the policy was created.
    updated_at : datetime
        The timestamp when the policy was last updated.
    """

    version = models.CharField(
        _("Version"),
        max_length=50,
        unique=True,
        help_text=_("The version of the cookie policy."),
    )

    content = models.TextField(
        _("Content"),
        help_text=_("The content of the cookie policy."),
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
        help_text=_("The timestamp when the policy was created."),
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
        help_text=_("The timestamp when the policy was last updated."),
    )

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the `CookiePolicy` model.
        """

        verbose_name = _("Cookie Policy")
        verbose_name_plural = _("Cookie Policies")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Returns a string representation of the cookie policy, typically its
        version.

        Returns:
        --------
        str
            The version of the cookie policy.
        """
        return f"Cookie Policy v{self.version}"

    def save(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Overrides the save method to enforce consistent formatting
        for the version field.

        Parameters:
        -----------
        *args : Any
            Variable-length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns:
        --------
        None
        """
        self.version = self.version.strip().upper()  # Ensures consistency
        super().save(*args, **kwargs)


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "CookiePolicyModel",
]
