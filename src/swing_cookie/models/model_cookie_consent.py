from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserCookieConsent(models.Model):
    """
    User Cookie Consent Model
    =========================

    Tracks the consent status of users for different types of cookies.

    Attributes:
    -----------
    user : User
        The user who provided the consent.
    necessary : bool
        Whether the user consented to necessary cookies.
    analytics : bool
        Whether the user consented to analytics cookies.
    marketing : bool
        Whether the user consented to marketing cookies.
    created_at : datetime
        The timestamp when the consent was recorded.
    updated_at : datetime
        The timestamp when the consent was last updated.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cookie_consent')
    necessary = models.BooleanField(default=True, help_text=_("Consent for necessary cookies."))
    analytics = models.BooleanField(default=False, help_text=_("Consent for analytics cookies."))
    marketing = models.BooleanField(default=False, help_text=_("Consent for marketing cookies."))

    created_at = models.DateTimeField(auto_now_add=True, help_text=_("The timestamp when the consent was recorded."))
    updated_at = models.DateTimeField(auto_now=True, help_text=_("The timestamp when the consent was last updated."))

    class Meta:
        """
        Meta Class
        ----------

        Provides metadata for the UserCookieConsent model.
        """
        verbose_name = _("User Cookie Consent")
        verbose_name_plural = _("User Cookie Consents")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        String Representation
        ---------------------

        Returns a string representation of the user's consent status.

        Returns:
        --------
        str
            The user's username and their consent status.
        """
        return f"{self.user.username}'s Cookie Consent"
    
    
    
    
    
    from django.db import models

class CookieConsent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    consent_date = models.DateTimeField(auto_now_add=True)
    consent_given = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user} - Consent given: {self.consent_given}"