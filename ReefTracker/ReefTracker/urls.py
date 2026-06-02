"""
URL configuration for ReefTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as account_views
urlpatterns = [
    # 1. Admin must always be first
    path("admin/", admin.site.urls),
    
    # Landing page at the root
    path("", account_views.landing, name="landing"),
    # 2. Specific apps defined by prefixes
    path("accounts/", include("accounts.urls")),
    path("calculators/", include("calculator.urls")),
    
    # 3. Built-in Auth (Move this after your custom accounts app to avoid conflicts)
 #   path("", include('django.contrib.auth.urls')), 
    
    # 4. The "Catch-all" (Aquariums) goes LAST
    path("aquariums/", include("aquariums.urls")),
    
    
    # This gives allauth control over login/signup/reset routing
    path('accounts/', include('allauth.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)