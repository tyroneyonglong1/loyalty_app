from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("customer/<int:customer_id>/", views.customer_detail, name="customer_detail"),
    path("customer/<int:customer_id>/redeem/", views.redeem, name="redeem"),
]