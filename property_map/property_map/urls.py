"""property_map URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# The Controller - MVC
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    # Saving search url
    path('save_search/', views.save_search),
    # Google OIDC authentication URLs
    path('oidc/', include('mozilla_django_oidc.urls')),
    # Grappelli URLs
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    # System admin
    path('admin/', admin.site.urls),
]
