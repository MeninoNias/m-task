from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import CustomTokenRefreshView, LoginView, LogoutView

app_name = "v1"

urlpatterns = [
    path("login/", csrf_exempt(LoginView.as_view()), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]

