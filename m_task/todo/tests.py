from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task

User = get_user_model()

class TaskAPITestCase(APITestCase):
    """Testes para API de Tarefas"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Cria uma tarefa para testes
        self.task = Task.objects.create(
            titulo='Tarefa Teste',
            descricao='Descrição da tarefa teste',
            status='pendente'
        )

    def get_task_url(self, action='list', pk=None):
        """Helper para gerar URLs da API"""
        if action == 'list':
            return '/api/tasks/'
        elif action == 'detail':
            return f'/api/tasks/{pk}/'
        elif action == 'complete':
            return f'/api/tasks/{pk}/complete/'
        return None

    def test_list_tasks(self):
        """Testa listagem de tarefas"""
        url = self.get_task_url('list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        """Testa criação de tarefa"""
        url = self.get_task_url('list')
        data = {
            'titulo': 'Nova Tarefa',
            'descricao': 'Descrição da nova tarefa',
            'status': 'pendente'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
        self.assertEqual(response.data['titulo'], 'Nova Tarefa')

    def test_retrieve_task(self):
        """Testa recuperação de tarefa específica"""
        url = self.get_task_url('detail', self.task.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titulo'], 'Tarefa Teste')

    def test_update_task(self):
        """Testa atualização de tarefa"""
        url = self.get_task_url('detail', self.task.id)
        data = {
            'titulo': 'Tarefa Atualizada',
            'descricao': 'Nova descrição',
            'status': 'concluida'
        }
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.titulo, 'Tarefa Atualizada')
        self.assertEqual(self.task.status, 'concluida')

    def test_delete_task(self):
        """Testa exclusão de tarefa"""
        url = self.get_task_url('detail', self.task.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_complete_task(self):
        """Testa ação de completar tarefa"""
        url = self.get_task_url('complete', self.task.id)
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, 'concluida')
        self.assertIsNotNone(self.task.data_conclusao)

    def test_unauthorized_access(self):
        """Testa acesso não autorizado"""
        self.client.credentials()  # Remove credenciais
        url = self.get_task_url('list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
