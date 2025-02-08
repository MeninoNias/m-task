from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from m_task.todo.models import Task
from .schemas import (complete_schema, task_schema)
from .serializers import TaskSerializer


@task_schema
class TaskViewSet(ModelViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.all().only(
            'id', 'titulo', 'descricao', 'data_criacao',
            'data_conclusao', 'status'
        )

    @complete_schema
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Marca uma tarefa como concluída/pendente"""
        task = self.get_object()
        task.handler_complete()
        return Response({
            'status': 'Tarefa atualizada com sucesso',
            'concluida': task.status == 'concluida'
        })
