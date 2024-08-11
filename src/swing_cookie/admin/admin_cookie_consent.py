from django.contrib import admin
from .models import CookieConsent

@admin.register(CookieConsent)
class CookieConsentAdmin(admin.ModelAdmin):
    list_display = ['user', 'consent_given', 'consent_date']
    search_fields = ['user__username', 'consent_given']