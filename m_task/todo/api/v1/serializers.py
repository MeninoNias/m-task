from rest_framework import serializers

from m_task.todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Task.
    Realiza validações dos campos ao criar ou editar tarefas.
    """
    class Meta:
        model = Task
        fields = [
            'id',
            'titulo',
            'descricao',
            'data_criacao',
            'data_conclusao',
            'status'
        ]
        read_only_fields = ['data_criacao', 'data_conclusao']
        extra_kwargs = {
            'titulo': {'required': True, 'allow_blank': False},
            'descricao': {'required': False, 'allow_blank': True}
        }

    def validate_titulo(self, value):
        """Valida se o título não está vazio"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("O título é obrigatório.")
        return value.strip()

    def validate(self, attrs):
        """Validação adicional dos dados"""
        if attrs.get('descricao'):
            attrs['descricao'] = attrs['descricao'].strip()
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
