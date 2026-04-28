from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("lookup/", views.customer_lookup, name="customer_lookup"),

    path("customer/<int:customer_id>/", views.customer_detail, name="customer_detail"),

    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/customer/<int:customer_id>/", views.staff_panel, name="staff_panel"),
    path("customer/<int:customer_id>/redeem/", views.redeem, name="redeem"),

    path("login/", auth_views.LoginView.as_view(template_name="loyalty/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
]