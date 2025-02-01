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
from typing import Optional

# Import | Libraries
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import | Local
from .models import CookieGroup
from .utils import clear_cache_after  # Assuming a decorator for cache clearing

# from .managers import CookieManager  # Assuming you have a custom manager


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
    description : Optional[str]
        A brief description of the cookie's purpose.
    domain : Optional[str]
        The domain for which the cookie is valid.
    path : str
        The path for which the cookie is valid.
    value : str
        The value of the cookie.
    expires : Optional[datetime]
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

    # Manager for the CookieModel (optional)
    # objects = CookieManager()

    cookiegroup = models.ForeignKey(
        CookieGroup,
        verbose_name=_(message="Cookie Group"),
        on_delete=models.CASCADE,
        related_name="cookies",
        help_text=_(message="The group to which this cookie belongs."),
    )

    name = models.CharField(
        _(message="Name"),
        max_length=255,
        help_text=_(message="The name of the cookie."),
    )

    description = models.TextField(
        _(message="Description"),
        blank=True,
    )

    domain = models.CharField(
        _(message="Domain"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The domain for which the cookie is valid."),
    )

    path = models.CharField(
        _(message="Path"),
        blank=True,
        max_length=255,
        default="/",
        help_text=_(message="The path for which the cookie is valid."),
    )

    value = models.TextField(
        help_text=_(message="The value of the cookie."),
    )

    expires = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(message="The expiration date and time of the cookie."),
    )

    secure = models.BooleanField(
        default=False,
        help_text=_(
            message="Indicates whether the cookie is secure (sent only over HTTPS)."
        ),
    )

    httponly = models.BooleanField(
        default=False,
        help_text=_(
            message="Indicates whether the cookie is HTTPOnly (not accessible via JavaScript)."
        ),
    )

    created_at = models.DateTimeField(
        _(message="Created"),
        auto_now_add=True,
        blank=True,
        help_text=_(message="The timestamp when the cookie was created."),
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_(message="The timestamp when the cookie was last updated."),
    )

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the CookieModel class, such as verbose names and
        constraints.
        """

        verbose_name: str = _(message="Cookie")
        verbose_name_plural: str = _(message="Cookies")
        constraints = [
            models.UniqueConstraint(
                fields=("name", "domain", "path"),
                name="unique_cookie_constraint",
                # fields=("cookiegroup", "name", "domain"),
                # name="natural_key",
            ),
        ]
        ordering: list[str] = ["-created_at"]

    def __str__(self) -> str:
        """
        String Representation
        ---------------------

        Returns the string representation of the cookie, typically its name.

        Returns:
        --------
        str
            The name of the cookie.
        """
        name = str(object=self.name)
        return name
        # return "%s %s%s" % (self.name, self.domain, self.path)

    @clear_cache_after
    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        super().save(*args, **kwargs)

    @clear_cache_after
    def delete(
        self,
        *args,
        **kwargs,
    ) -> tuple[int, dict[str, int]]:
        return super().delete(*args, **kwargs)

    def natural_key(self):  # -> Any:
        return (self.name, self.domain) + self.cookiegroup.natural_key()

    natural_key.dependencies = ["cookie_consent.cookiegroup"]

    @property
    def varname(self) -> str:
        return "%s=%s:%s" % (self.cookiegroup.varname, self.name, self.domain)

    def get_version(self):  # -> Any:
        return self.created.isoformat()


# =============================================================================
# Module Exports
# =============================================================================

__all__: list[str] = [
    "CookieModel",
]
