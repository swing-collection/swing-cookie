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
    name : str
        The name of the cookie.
    value : str
        The value of the cookie.
    domain : Optional[str]
        The domain for which the cookie is valid.
    path : str
        The path for which the cookie is valid.
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
        verbose_name=CookieGroup._meta.verbose_name,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        _("Name"),
        max_length=255,
        help_text=_("The name of the cookie.")
    )

    description = models.TextField(
        _("Description"),
        blank=True,
    )

    domain = models.CharField(
        _("Domain"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The domain for which the cookie is valid.")
    )

    path = models.CharField(
        _("Path"),
        blank=True,
        max_length=255,
        default='/',
        help_text=_("The path for which the cookie is valid.")
    )

    value = models.TextField(
        help_text = _("The value of the cookie.")
    )

    expires = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("The expiration date and time of the cookie.")
    )

    secure = models.BooleanField(
        default=False,
        help_text=_("Indicates whether the cookie is secure (sent only over HTTPS).")
    )
    
    httponly = models.BooleanField(
        default=False,
        help_text=_("Indicates whether the cookie is HTTPOnly (not accessible via JavaScript).")
    )

    created_at = models.DateTimeField(
        _("Created"),
        auto_now_add=True,
        blank=True,
        help_text=_("The timestamp when the cookie was created.")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("The timestamp when the cookie was last updated.")
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
                fields=("name", "domain", "path"),
                name="unique_cookie_constraint",
                # fields=("cookiegroup", "name", "domain"),
                # name="natural_key",
            ),
        ]
        ordering = ["-created_at"]


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
        name = str(self.name)
        return name
        # return "%s %s%s" % (self.name, self.domain, self.path)

    @clear_cache_after
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @clear_cache_after
    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)

    def natural_key(self):
        return (self.name, self.domain) + self.cookiegroup.natural_key()

    natural_key.dependencies = ["cookie_consent.cookiegroup"]

    @property
    def varname(self):
        return "%s=%s:%s" % (self.cookiegroup.varname, self.name, self.domain)

    def get_version(self):
        return self.created.isoformat()

# =============================================================================
# Module Exports
# =============================================================================

__all__ = [
    "CookieModel",
]
