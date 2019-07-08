"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from network import views

urlpatterns = [
    url(r'^test/', views.test),
    url(r'^ip_conf/', views.ip_conf),
    url(r'^group_conf/', views.group_conf),
    url(r'^index/', views.index),
    url (r'^index1/', views.index1),
    url (r'^index2/', views.index2),
    # url(r'^', views.index),
    # url(r'^test/', network.test),
]
