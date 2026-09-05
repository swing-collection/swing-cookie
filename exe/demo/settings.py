# -*- coding: utf-8 -*-


# =============================================================================
# Docstring
# =============================================================================

"""
Demo Settings
=============

This is a basic settings configuration used to run the app in isolation. It
includes minimal setup for a SQLite database, templates, and installed apps.

It includes:

- A simple SQLite database setup.
- Default Django apps for admin and authentication.
- Template and static file configuration.
- Internationalization settings.

IMPORTANT: Not intended for production use. Update `SECRET_KEY`, `DEBUG`,
and `ALLOWED_HOSTS` appropriately for deployment.

"""

# =============================================================================
# Imports
# =============================================================================

# Import | Standard Library
from pathlib import Path

# Import | Local Modules


# =============================================================================
# Basic Configuration
# =============================================================================

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security: Use a strong secret key in production
SECRET_KEY = "django-insecure-change-this-in-production"

# Debug mode: Set to False in production
DEBUG = True

# Hosts allowed to access the application
# Define allowed hosts in production, e.g., ["example.com"]
ALLOWED_HOSTS = []


# =============================================================================
# Installed Applications
# =============================================================================

INSTALLED_APPS: list[str] = [
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Local apps
    "demo",  # Demo app
    "swing.cookie",  # Cookie consent app
]


# =============================================================================
# Middleware
# =============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Cookie consent middleware - cleans cookies that were declined
    "swing.cookie.middleware.CleanCookiesMiddleware",
]


# =============================================================================
# URL Configuration
# =============================================================================

ROOT_URLCONF = "demo.urls"


# =============================================================================
# Templates
# =============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Add paths to custom templates if needed
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# =============================================================================
# WSGI Application
# =============================================================================

WSGI_APPLICATION = "demo.wsgi.application"


# =============================================================================
# Database
# =============================================================================

# SQLite database for development/testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# =============================================================================
# Password Validation
# =============================================================================

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# =============================================================================
# Internationalization
# =============================================================================

LANGUAGE_CODE = "en-us"  # Default language
TIME_ZONE = "UTC"  # Default timezone
USE_I18N = True  # Enable translations
USE_TZ = True  # Use timezone-aware datetimes


# =============================================================================
# Static Files
# =============================================================================

STATIC_URL = "/static/"  # URL to serve static files
STATICFILES_DIRS: list[Path] = [BASE_DIR / "static"]  # Additional static files


# =============================================================================
# Default Primary Key Field Type
# =============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# =============================================================================
# Cache Configuration
# =============================================================================

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}


# =============================================================================
# Cookie Consent Settings
# =============================================================================

COOKIE_CONSENT_ENABLED = True
COOKIE_CONSENT_CACHE_BACKEND = "default"
COOKIE_CONSENT_NAME = "cookie_consent"
COOKIE_CONSENT_MAX_AGE = 60 * 60 * 24 * 365  # 1 year
COOKIE_CONSENT_DOMAIN = None  # Cookie domain (None = current domain)
COOKIE_CONSENT_SECURE = False
COOKIE_CONSENT_HTTPONLY = True
COOKIE_CONSENT_SAMESITE = "Lax"
COOKIE_CONSENT_OPT_OUT = False  # GDPR default: require opt-in
COOKIE_CONSENT_DECLINE = "-1"  # Value indicating declined consent
COOKIE_CONSENT_LOG_ENABLED = True  # Enable consent logging
COOKIE_CONSENT_LOG_IP_ADDRESS = True  # Log IP for GDPR proof
COOKIE_CONSENT_LOG_USER_AGENT = True  # Log user agent
COOKIE_CONSENT_EXPIRY_DAYS = 365  # Consent expires after 1 year
COOKIE_CONSENT_REPROMPT_ON_POLICY_CHANGE = True
