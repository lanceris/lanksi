"""lanksi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from accounts import views as bank_views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', bank_views.register, name='register'),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^account/logout/$', auth_views.logout, name='logout'),
    url(r'^', include('accounts.urls', namespace='accounts')),
    url(r'^categories/', include('categories.urls', namespace='categories')),
    url(r'^goals/', include('goals.urls', namespace='goals')),
    url(r'^patterns/', include('patterns.urls', namespace='patterns')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()