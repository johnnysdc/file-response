"""fileresponse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from sendfile.views import send_image, send_pdf, send_scaler, send_modelo, UploadAnalisadoresViewset

router = DefaultRouter(trailing_slash=False)
router.register(r'arquivos', UploadAnalisadoresViewset)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('image', send_image, name='send_image'),
    path('pdf', send_pdf, name='send_pdf'),
    path('scaler', send_scaler, name='send_scaler'),
    path('modelo', send_modelo, name='send_modelo'),
    url(r'^', include(router.urls)),
]
