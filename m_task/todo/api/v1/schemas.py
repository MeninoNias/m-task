from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)

from .serializers import TaskSerializer

task_schema = extend_schema(
    tags=["Tarefas 📝"],
    description="Gerenciamento de tarefas do usuário",
    responses={
        200: TaskSerializer,
        400: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            'Exemplo de criação de tarefa',
            value={
                'titulo': 'Minha tarefa',
                'descricao': 'Descrição da tarefa',
                'status': 'pendente'
            },
            request_only=True,
        )
    ]
)

complete_schema = extend_schema(
    operation_id="complete_task",
    description="Alterna o status da tarefa entre concluída e pendente",
    responses={
        200: OpenApiResponse(
            description="Status da tarefa atualizado",
            response={
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'concluida': {'type': 'boolean'}
                }
            }
        ),
        404: OpenApiResponse(description="Tarefa não encontrada"),
    },
)
