from django.urls import include, path

app_name = "oauth"

urlpatterns = [
    path("", include("m_task.oauth.api.v1.urls", namespace="v1")),
]
