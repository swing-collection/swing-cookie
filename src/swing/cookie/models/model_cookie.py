# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Model Module
===================

This module provides the `CookieModel` class, which represents a model for
storing and managing cookies in the database.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from typing import Any, Optional

from django.db import models
from django.utils.translation import gettext_lazy as _

# Import | Local
from ..utils import clear_cache_after
from .model_cookie_group import CookieGroupModel

# =============================================================================
# Class
# =============================================================================


class CookieModel(models.Model):
    """
    Cookie Model Class
    ==================

    Represents a cookie stored in the database, including its name, value,
    domain, path, and other relevant properties.

    Attributes:
    -----------
    cookiegroup : CookieGroup
        The group to which the cookie belongs (e.g., necessary, analytics, etc.).
    name : str
        The name of the cookie.
    description : str | None
        A brief description of the cookie's purpose.
    domain : str | None
        The domain for which the cookie is valid.
    path : str
        The path for which the cookie is valid.
    value : str
        The value of the cookie.
    expires : datetime | None
        The expiration date and time of the cookie.
    secure : bool
        Whether the cookie is secure (sent only over HTTPS).
    httponly : bool
        Whether the cookie is HTTPOnly (not accessible via JavaScript).
    created_at : datetime
        The timestamp when the cookie was created.
    updated_at : datetime
        The timestamp when the cookie was last updated.
    """

    cookiegroup = models.ForeignKey(
        CookieGroupModel,
        verbose_name=_("Cookie Group"),
        on_delete=models.CASCADE,
        related_name="cookie_set",
        help_text=_("The group to which this cookie belongs."),
    )

    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("The name of the cookie."),
    )

    description = models.TextField(
        _("Description"),
        blank=True,
        null=True,
        help_text=_("A brief description of the cookie's purpose."),
    )

    domain = models.CharField(
        _("Domain"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The domain for which the cookie is valid."),
    )

    path = models.CharField(
        _("Path"),
        max_length=255,
        default="/",
        help_text=_("The path for which the cookie is valid."),
    )

    value = models.TextField(
        _("Value"),
        help_text=_("The value stored in the cookie."),
    )

    expires = models.DateTimeField(
        _("Expiration Date"),
        blank=True,
        null=True,
        help_text=_("The expiration date and time of the cookie."),
    )

    secure = models.BooleanField(
        _("Secure"),
        default=False,
        help_text=_(
            "Indicates whether the cookie is secure (sent only over HTTPS)."
        ),
    )

    httponly = models.BooleanField(
        _("HTTPOnly"),
        default=False,
        help_text=_(
            "Indicates whether the cookie is HTTPOnly (not accessible via JavaScript)."
        ),
    )

    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True,
        help_text=_("The timestamp when the cookie was created."),
    )

    updated_at = models.DateTimeField(
        _("Updated At"),
        auto_now=True,
        help_text=_("The timestamp when the cookie was last updated."),
    )

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the CookieModel class, such as verbose names and
        constraints.
        """

        verbose_name = _("Cookie")
        verbose_name_plural = _("Cookies")
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "cookiegroup",
                    "name",
                    "domain",
                ),
                name="unique_cookie_constraint",
            ),
        ]
        ordering: list[str] = [
            "-created_at",
        ]

    def __str__(self) -> str:
        """
        Returns a string representation of the cookie.

        Returns:
        --------
        str
            A human-readable name of the cookie.
        """
        return f"{self.name} ({self.domain or 'No Domain'})"

    @clear_cache_after
    def save(self, *args: Any, **kwargs: Any) -> None:
        """
        Overrides the save method to clear the cache after saving.

        Parameters:
        -----------
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns:
        --------
        None
        """
        super().save(*args, **kwargs)

    @clear_cache_after
    def delete(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> tuple[int, dict[str, int]]:
        """
        Overrides the delete method to clear the cache after deleting.

        Parameters:
        -----------
        *args : Any
            Variable length argument list.
        **kwargs : Any
            Arbitrary keyword arguments.

        Returns:
        --------
        tuple[int, dict[str, int]]
            The number of rows deleted and a dictionary with details.
        """
        return super().delete(*args, **kwargs)

    def natural_key(self) -> tuple[str, str | None, str]:
        """
        Returns a natural key that uniquely identifies the cookie.

        Returns:
        --------
        tuple[str, str | None, str]
            A tuple containing the cookie name, domain, and group varname.
        """
        return (self.name, self.domain) + self.cookiegroup.natural_key()

    natural_key.dependencies = ["swing_cookie.cookiegroupmodel"]

    @property
    def varname(self) -> str:
        """
        Returns a variable name representation of the cookie.

        Returns:
        --------
        str
            A formatted variable name including group and domain.
        """
        return f"{self.cookiegroup.varname}={self.name}:{self.domain or 'No Domain'}"

    def get_version(self) -> str:
        """
        Returns the creation timestamp as a version identifier.

        Returns:
        --------
        str
            The ISO formatted timestamp.
        """
        return self.created_at.isoformat()


# =============================================================================
# Aliases
# =============================================================================

# Alias for compatibility with existing code
Cookie = CookieModel


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "Cookie",
    "CookieModel",
]
