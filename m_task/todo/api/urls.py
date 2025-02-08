from django.urls import include, path

app_name = 'todo_api'

urlpatterns = [
    path('', include('todo.api.v1.urls', namespace='v1')),
]
