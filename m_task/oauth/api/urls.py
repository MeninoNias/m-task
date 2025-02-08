from django.urls import include, path

app_name = "oauth"

urlpatterns = [
    path("v1/", include("m_task.oauth.api.v1.urls", namespace="v1")),
]
