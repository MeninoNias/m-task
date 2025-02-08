from django.urls import include, path

app_name = 'todo_api'

urlpatterns = [
    path('v1/', include('todo.api.v1.urls', namespace='v1')),
]
