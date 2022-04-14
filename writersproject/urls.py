"""writersproject URL Configuration

The `urlpatterns` list routes URLs to cviews. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function cviews
    1. Add an import:  from my_app import cviews
    2. Add a URL to urlpatterns:  path('', cviews.home, name='home')
Class-based cviews
    1. Add an import:  from other_app.cviews import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from writersapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashbooard, name='dashboard'),
    path('writersapp/', include('writersapp.urls')),
]
