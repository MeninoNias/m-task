from django.db import models
from django.utils import timezone


class Task(models.Model):
    """
    Representa uma tarefa a ser realizada
    """
    titulo = models.CharField(
        max_length=255,
        verbose_name="Título"
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição"
    )
    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    data_conclusao = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Data de Conclusão"
    )
    status = models.CharField(
        max_length=10,
        choices=[
            ('pendente', 'Pendente'),
            ('concluida', 'Concluída')
        ],
        default='pendente',
        verbose_name="Status"
    )

    class Meta:
        verbose_name = "Tarefa"
        verbose_name_plural = "Tarefas"

    def __str__(self):
        return self.titulo

    def handler_complete(self):
        if self.data_conclusao:
            self.data_conclusao = None
            self.status = 'pendente'
        else:
            self.data_conclusao = timezone.now()
            self.status = 'concluida'
        self.save()
