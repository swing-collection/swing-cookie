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
import re
from typing import Any

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# Import | Local
from ..utils import clear_cache_after

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
    varname : str
        A URL-safe identifier for the cookie group.
    description : str
        A brief description of the cookie group.
    is_required : bool
        Whether the cookie group is required (cannot be declined).
    is_deletable : bool
        Whether cookies in this group should be deleted when declined.
    ordering : int
        The display order of the cookie group.
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

    varname = models.SlugField(
        _("Variable Name"),
        max_length=255,
        unique=True,
        help_text=_(
            "A URL-safe identifier for this cookie group "
            "(auto-generated from name if not provided)."
        ),
    )

    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("A brief description of the cookie group."),
    )

    is_required = models.BooleanField(
        _("Required"),
        default=False,
        help_text=_(
            "If checked, this cookie group is required and users cannot "
            "decline it. Use for essential cookies like session or CSRF."
        ),
    )

    is_deletable = models.BooleanField(
        _("Deletable"),
        default=True,
        help_text=_(
            "If checked, cookies in this group will be automatically "
            "deleted when the user declines or withdraws consent."
        ),
    )

    ordering = models.PositiveIntegerField(
        _("Display Order"),
        default=0,
        help_text=_(
            "The order in which this group appears in the consent dialog. "
            "Lower numbers appear first."
        ),
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
        ordering: list[str] = ["ordering", "name"]

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
            A tuple containing the varname of the cookie group.
        """
        return (self.varname,)

    def get_version(self) -> str:
        """
        Returns the latest version timestamp for this cookie group.

        The version is determined by the most recently updated cookie
        in this group. This is used to detect when users need to
        re-consent due to cookie changes.

        Returns:
        --------
        str
            The ISO formatted timestamp of the latest cookie update,
            or the group's own updated_at if no cookies exist.
        """
        latest_cookie = self.cookie_set.order_by("-updated_at").first()
        if latest_cookie:
            return latest_cookie.updated_at.isoformat()
        return self.updated_at.isoformat()

    def for_json(self) -> dict[str, Any]:
        """
        Returns a JSON-serializable representation of the cookie group.

        Returns:
        --------
        dict[str, Any]
            A dictionary containing the cookie group's data.
        """
        return {
            "name": self.name,
            "varname": self.varname,
            "description": self.description or "",
            "is_required": self.is_required,
            "cookies": [
                {
                    "name": cookie.name,
                    "description": cookie.description or "",
                    "domain": cookie.domain or "",
                }
                for cookie in self.cookie_set.all()
            ],
        }

    @clear_cache_after
    def save(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Saves the cookie group instance.

        This method ensures that cookie group names are stored in a consistent
        format (e.g., title case) and generates a varname if not provided.

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
        self.name = self.name.title()  # Ensures name consistency

        # Auto-generate varname from name if not provided
        if not self.varname:
            base_varname = slugify(self.name).replace("-", "_")
            # Ensure it's a valid Python identifier
            base_varname = re.sub(r"^[^a-zA-Z_]+", "", base_varname)
            self.varname = base_varname or "cookie_group"

        super().save(*args, **kwargs)

    @clear_cache_after
    def delete(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[int, dict[str, int]]:
        """
        Deletes the cookie group and clears the cache.

        Parameters:
        -----------
        *args : Any
            Variable-length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns:
        --------
        tuple[int, dict[str, int]]
            The number of rows deleted and a dictionary with details.
        """
        return super().delete(*args, **kwargs)


# =============================================================================
# Aliases
# =============================================================================

# Alias for compatibility with existing code
CookieGroup = CookieGroupModel


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "CookieGroup",
    "CookieGroupModel",
]
