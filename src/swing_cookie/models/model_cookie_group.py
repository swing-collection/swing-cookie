from django.db import models
from django.utils.translation import gettext_lazy as _

class CookieGroup(models.Model):
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

    name = models.CharField(max_length=255, unique=True, help_text=_("The name of the cookie group (e.g., 'Necessary', 'Analytics')."))
    description = models.TextField(blank=True, null=True, help_text=_("A brief description of the cookie group."))

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("The timestamp when the group was created."))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("The timestamp when the group was last updated."))

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the CookieGroup model.
        """
        verbose_name = _("Cookie Group")
        verbose_name_plural = _("Cookie Groups")
        ordering = ["name"]

    def __str__(self) -> str:
        """
        String Representation
        ---------------------

        Returns the string representation of the cookie group.

        Returns:
        --------
        str
            The name of the cookie group.
        """
        return self.name