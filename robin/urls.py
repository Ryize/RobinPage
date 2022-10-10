from django.urls import path

from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("check_hash/", check_site_hash, name="check_site_hash"),
]
