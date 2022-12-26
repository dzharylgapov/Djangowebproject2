"""
Definition of urls for DjangoWebProject2.
"""

from django.conf import settings
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
#from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from django.conf.urls.static import static


urlpatterns = [
    path(r'mailing_app/', include('mailing_app.urls')),
    path('admin/', admin.site.urls),
]
