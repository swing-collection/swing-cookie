<p align="center">
    <img src="https://github.com/scape-agency/swing.dj/blob/85830584264bca52c02e1f0dcfa3648f84783805/res/swing-logo.png" width="20%" height="20%" alt="Django Swing Logo">
</p>
<h1 align='center' style='border-bottom: none;'>Swing Cookie</h1>
<h3 align='center'>Django Swing Collection</h3>
<br/>

## Overview

Swing Cookie ...

## Usage in a Django Project

After installing the package, you can add swing_cookie to your INSTALLED_APPS and include the views in your project’s URLs.

``` python
# settings.py
INSTALLED_APPS = [
    ...
    'swing_cookie',
    ...
]   
```

``` python
# urls.py
from django.urls import path
from swing_cookie.views import cookie_consent_view

urlpatterns = [
    path('cookie-consent/', cookie_consent_view, name='cookie_consent'),
]
```
