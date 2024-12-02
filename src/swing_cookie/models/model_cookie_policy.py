# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Cookie Policy Model Module
===================


"""


# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library

# Import | Libraries
from django.db import models
from django.utils.translation import gettext_lazy as _

# Import | Local


# =============================================================================
# Class
# =============================================================================

class CookiePolicy(models.Model):
    """
    Cookie Policy Model
    ===================

    Defines the cookie policy for the website, including the version and text 
    of the policy.

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

    version = models.CharField(max_length=50, unique=True, help_text=_("The version of the cookie policy."))
    content = models.TextField(help_text=_("The content of the cookie policy."))

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("The timestamp when the policy was created."))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("The timestamp when the policy was last updated."))

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the CookiePolicy model.
        """
        verbose_name = _("Cookie Policy")
        verbose_name_plural = _("Cookie Policies")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        String Representation
        ---------------------

        Returns the string representation of the cookie policy, typically the 
        version.

        Returns:
        --------
        str
            The version of the cookie policy.
        """
        return f"Cookie Policy v{self.version}"
