# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Group Model Module
=========================

This module provides the `CookieGroupModel` class, which organizes cookies
into different categories such as "necessary," "analytics," and "marketing."

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


class CookieGroupModel(models.Model):
    """
    Cookie Group Model
    ==================

    Groups cookies into different categories, such as "necessary,"
    "analytics," and "marketing."

    Attributes:
    -----------
    name : str
        The name of the cookie group (e.g., "Necessary", "Analytics").
    description : str
        A brief description of the cookie group.
    created_at : datetime
        The timestamp when the group was created.
    updated_at : datetime
        The timestamp when the group was last updated.
    """

    name = models.CharField(
        _("Name"),
        max_length=255,
        unique=True,
        help_text=_(
            "The name of the cookie group (e.g., 'Necessary', 'Analytics')."
        ),
    )

    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("A brief description of the cookie group."),
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
        help_text=_("The timestamp when the group was created."),
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
        help_text=_("The timestamp when the group was last updated."),
    )

    class Meta:
        """
        Meta Class
        ----------

        Defines metadata for the `CookieGroupModel` class, such as verbose
        names and ordering.
        """

        verbose_name: str = _("Cookie Group")
        verbose_name_plural: str = _("Cookie Groups")
        ordering: list[str] = ["name"]

    def __str__(self) -> str:
        """
        Returns a string representation of the cookie group.

        Returns:
        --------
        str
            The name of the cookie group.
        """
        return self.name

    def natural_key(self) -> tuple[str]:
        """
        Returns a natural key for serialization and uniqueness.

        Returns:
        --------
        tuple[str]
            A tuple containing the name of the cookie group.
        """
        return (self.name,)

    def save(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Saves the cookie group instance.

        This method ensures that cookie group names are stored in a consistent
        format (e.g., title case) before saving.

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
        self.name: str = self.name.title()  # Ensures name consistency
        super().save(*args, **kwargs)


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "CookieGroupModel",
]
