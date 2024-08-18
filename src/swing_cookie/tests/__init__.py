from django.test import TestCase
from django.urls import reverse

class CookieConsentViewTests(TestCase):
    def test_cookie_consent_view(self):
        response = self.client.get(reverse('cookie_consent'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'swing_cookie/consent_form.html')